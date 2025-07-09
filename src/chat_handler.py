import openai
from typing import List, Dict, Optional, Any
import os
import json
from datetime import datetime
from templates import TemplateRegistry

class ChatHandler:
    """Handles OpenAI API interactions for the structured business chat assistant"""
    
    def __init__(self, api_key: str, template_type: str = "business_decision"):
        """Initialize the chat handler with OpenAI API key and template type"""
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.template_type = template_type
        self.template_config = self._load_template_config()
        
        # Initialize conversation state before system prompt
        self.conversation_state = {
            "current_stage": 0,
            "completed_stages": [],
            "json_config": {},
            "template_type": template_type,
            "created_date": datetime.now().isoformat(),
            "use_case_name": "",
            "last_updated": datetime.now().isoformat(),
            "auto_save_enabled": True
        }
        
        self.system_prompt = self._get_system_prompt()
    
    def _load_template_config(self) -> Dict[str, Any]:
        """Load template configuration based on template type"""
        return TemplateRegistry.get_template_config(self.template_type)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt based on template type"""
        base_prompt = f"""You are an expert business consultant using the {self.template_config['name']} framework. Your role is to guide users through a structured decision-making process.

IMPORTANT INSTRUCTIONS:
1. Follow the template stages in order: {', '.join([stage['title'] for stage in self.template_config['stages']])}
2. For each stage, present the main question and offer relevant examples
3. Collect user responses and build a structured JSON configuration
4. Reference previous decisions when relevant (e.g., "Given your budget from earlier...")
5. Be conversational but structured
6. Ask follow-up questions to get specific details
7. Track progress through the framework

Current conversation state: Stage {self.conversation_state['current_stage'] + 1} of {len(self.template_config['stages'])}

Guidelines:
- Be professional yet approachable
- Use the provided examples when presenting options
- Ask clarifying questions when more context is needed
- Reference the user's previous answers to maintain context
- Provide actionable insights based on their responses
- Maintain a supportive and encouraging tone"""

        return base_prompt
    
    def get_current_stage_info(self) -> Dict[str, Any]:
        """Get information about the current stage"""
        if self.conversation_state["current_stage"] < len(self.template_config["stages"]):
            stage = self.template_config["stages"][self.conversation_state["current_stage"]]
            return {
                "stage_number": self.conversation_state["current_stage"] + 1,
                "total_stages": len(self.template_config["stages"]),
                "stage_title": stage["title"],
                "stage_key": stage["key"],
                "prompt": stage["prompt"],
                "examples": stage["examples"],
                "follow_up": stage["follow_up"]
            }
        return {"completed": True}
    
    def update_json_config(self, stage_key: str, data: Dict[str, Any]) -> None:
        """Update the JSON configuration with stage data"""
        self.conversation_state["json_config"][stage_key] = data
        self.conversation_state["last_updated"] = datetime.now().isoformat()
        
        if stage_key not in self.conversation_state["completed_stages"]:
            self.conversation_state["completed_stages"].append(stage_key)
        
        # Extract use case name from first stage if available
        if stage_key == "problem_definition" and "primary_problem" in data:
            self._extract_use_case_name(data["primary_problem"])
        elif stage_key == "project_scope" and "main_goal" in data:
            self._extract_use_case_name(data["main_goal"])
        elif stage_key == "market_overview" and "industry" in data:
            self._extract_use_case_name(data["industry"])
    
    def set_project_name(self, project_name: str) -> None:
        """Set the project name for this decision analysis (used temporarily, not saved until finalization)"""
        # Clean and format the project name
        import re
        clean_name = re.sub(r'[^\w\s-]', '', project_name)
        clean_name = re.sub(r'\s+', ' ', clean_name.strip())
        
        # Store temporarily but don't save to JSON or auto-save until finalization
        self.conversation_state["pending_project_name"] = clean_name
        self.conversation_state["last_updated"] = datetime.now().isoformat()
    
    def get_project_name(self) -> str:
        """Get the current project name (pending or finalized)"""
        return self.conversation_state.get("pending_project_name", self.conversation_state.get("project_name", ""))
    
    def get_pending_project_name(self) -> str:
        """Get the pending project name (before finalization)"""
        return self.conversation_state.get("pending_project_name", "")
    
    def get_finalized_project_name(self) -> str:
        """Get the finalized project name (after confirmation)"""
        return self.conversation_state.get("project_name", "")
    
    def is_project_completed(self) -> bool:
        """Check if all stages are completed and project is ready for finalization"""
        return len(self.conversation_state["completed_stages"]) >= len(self.template_config["stages"]) - 1
    
    def finalize_project(self, project_name: str = "") -> Dict[str, Any]:
        """Finalize the project with a proper name and generate final configuration"""
        # Use provided project name or pending project name
        if project_name:
            final_name = project_name.strip()
        else:
            final_name = self.conversation_state.get("pending_project_name", "")
        
        if final_name:
            # Clean and format the final project name
            import re
            clean_name = re.sub(r'[^\w\s-]', '', final_name)
            clean_name = re.sub(r'\s+', ' ', clean_name.strip())
            
            # NOW officially set the project name in the JSON
            self.conversation_state["project_name"] = clean_name
            # Remove pending name since it's now finalized
            self.conversation_state.pop("pending_project_name", None)
        
        # Mark all remaining stages as completed if we're at the end
        for stage in self.template_config["stages"]:
            stage_key = stage["key"]
            if stage_key not in self.conversation_state["completed_stages"]:
                # Add minimal completion data for missing stages
                self.conversation_state["json_config"][stage_key] = {
                    "status": "not_completed",
                    "note": "Stage skipped or not fully completed"
                }
                self.conversation_state["completed_stages"].append(stage_key)
        
        # Generate final configuration
        final_config = self.get_final_json_config()
        
        # Auto-save the final version (now with the finalized project name)
        self.auto_save_progress()
        
        return final_config
    
    def _extract_use_case_name(self, description: str) -> None:
        """Extract a meaningful use case name from description"""
        # Clean and truncate description for filename
        import re
        clean_description = re.sub(r'[^\w\s-]', '', description)
        clean_description = re.sub(r'\s+', '_', clean_description.strip())
        self.conversation_state["use_case_name"] = clean_description[:50]  # Limit length
    
    def generate_temp_filename(self) -> str:
        """Generate a temporary filename for auto-save before finalization"""
        created_date = datetime.fromisoformat(self.conversation_state["created_date"])
        date_str = created_date.strftime("%Y%m%d_%H%M%S")
        
        # Use use_case_name for temporary files (not pending_project_name)
        use_case_name = self.conversation_state.get("use_case_name", "")
        
        if use_case_name:
            # Clean use_case_name for filename
            import re
            clean_name = re.sub(r'[^\w\s-]', '', use_case_name)
            clean_name = re.sub(r'\s+', '_', clean_name.strip())
            return f"{clean_name}_{date_str}_temp.json"
        else:
            return f"business_decision_{date_str}_temp.json"

    def generate_filename(self) -> str:
        """Generate a meaningful filename for saving progress"""
        created_date = datetime.fromisoformat(self.conversation_state["created_date"])
        date_str = created_date.strftime("%Y%m%d_%H%M%S")
        
        # Use finalized project_name if available, otherwise fall back to use_case_name
        project_name = self.conversation_state.get("project_name", "")
        if not project_name:
            project_name = self.conversation_state.get("use_case_name", "")
        
        if project_name:
            # Clean project name for filename
            import re
            clean_name = re.sub(r'[^\w\s-]', '', project_name)
            clean_name = re.sub(r'\s+', '_', clean_name.strip())
            return f"{clean_name}_{date_str}.json"
        else:
            return f"business_decision_{date_str}.json"
    
    def auto_save_progress(self) -> Optional[str]:
        """Auto-save progress to file with meaningful filename"""
        if not self.conversation_state.get("auto_save_enabled", True):
            return None
        
        try:
            os.makedirs("saved_configs", exist_ok=True)
            
            # Use temporary filename if not finalized, otherwise use final filename
            if self.conversation_state.get("project_name"):
                # Project is finalized, use final filename
                filename = self.generate_filename()
            else:
                # Project not finalized, use temporary filename
                filename = self.generate_temp_filename()
            
            filepath = f"saved_configs/{filename}"
            
            save_data = self.save_conversation_state()
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return filepath
        except Exception as e:
            print(f"Auto-save error: {e}")
            return None
    
    def advance_stage(self) -> None:
        """Move to the next stage"""
        if self.conversation_state["current_stage"] < len(self.template_config["stages"]) - 1:
            self.conversation_state["current_stage"] += 1
            self.conversation_state["last_updated"] = datetime.now().isoformat()
            
            # Auto-save progress after advancing stage
            self.auto_save_progress()
    
    def get_progress_percentage(self) -> float:
        """Get completion percentage"""
        total_stages = len(self.template_config["stages"])
        completed = len(self.conversation_state["completed_stages"])
        return (completed / total_stages) * 100
    
    def get_stage_progress_details(self) -> Dict[str, Any]:
        """Get detailed progress information including substages"""
        stages_detail = []
        
        for i, stage in enumerate(self.template_config["stages"]):
            stage_key = stage["key"]
            is_completed = stage_key in self.conversation_state["completed_stages"]
            is_current = i == self.conversation_state["current_stage"]
            
            stage_detail = {
                "stage_number": i + 1,
                "title": stage["title"],
                "key": stage_key,
                "completed": is_completed,
                "current": is_current,
                "data": self.conversation_state["json_config"].get(stage_key, {})
            }
            stages_detail.append(stage_detail)
        
        return {
            "total_stages": len(self.template_config["stages"]),
            "completed_count": len(self.conversation_state["completed_stages"]),
            "current_stage": self.conversation_state["current_stage"] + 1,
            "progress_percentage": self.get_progress_percentage(),
            "stages": stages_detail,
            "template_name": self.template_config["name"],
            "use_case_name": self.conversation_state.get("use_case_name", ""),
            "created_date": self.conversation_state.get("created_date", ""),
            "last_updated": self.conversation_state.get("last_updated", "")
        }
    
    def get_final_json_config(self) -> Dict[str, Any]:
        """Get the final complete JSON configuration"""
        # Only include project_name if it's been finalized
        config = {
            "template_type": self.template_type,
            "template_name": self.template_config.get("name", ""),
            "created_date": self.conversation_state.get("created_date", datetime.now().isoformat()),
            "last_updated": self.conversation_state.get("last_updated", datetime.now().isoformat()),
            "completion_status": f"{len(self.conversation_state['completed_stages'])}/{len(self.template_config['stages'])} stages completed",
            "completion_percentage": f"{self.get_progress_percentage():.1f}%",
            **self.conversation_state["json_config"],
            "next_steps": self._generate_next_steps(),
            "recommendations": self._generate_recommendations(),
            "metadata": {
                "use_case_name": self.conversation_state.get("use_case_name", ""),
                "auto_save_enabled": self.conversation_state.get("auto_save_enabled", True),
                "filename": self.generate_filename() if self.get_finalized_project_name() else self.generate_temp_filename()
            }
        }
        
        # Only add project_name if it's been finalized
        finalized_name = self.get_finalized_project_name()
        if finalized_name:
            config["project_name"] = finalized_name
        
        return config
    
    def _generate_next_steps(self) -> List[str]:
        """Generate next steps based on the collected information"""
        # This could be enhanced with AI-generated suggestions
        return [
            "Review and validate the collected requirements",
            "Create detailed project timeline",
            "Assign roles and responsibilities",
            "Set up regular progress check-ins"
        ]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on the analysis"""
        # This could be enhanced with AI-generated suggestions
        return [
            "Consider starting with a pilot program to reduce risk",
            "Establish clear success metrics before beginning",
            "Ensure stakeholder buy-in at each phase",
            "Plan for regular reviews and adjustments"
        ]
    
    def load_conversation_state(self, state_data: Dict[str, Any]) -> None:
        """Load a saved conversation state"""
        self.conversation_state.update(state_data)
        # Update system prompt with current state
        self.system_prompt = self._get_system_prompt()
    
    def save_conversation_state(self) -> Dict[str, Any]:
        """Save current conversation state"""
        return {
            **self.conversation_state,
            "saved_date": datetime.now().isoformat(),
            "filename": self.generate_filename(),
            "template_config": {
                "name": self.template_config["name"],
                "description": self.template_config.get("description", ""),
                "category": self.template_config.get("category", ""),
                "stages_count": len(self.template_config["stages"])
            },
            # Include the final project config structure in the saved state
            "final_config_preview": self.get_final_json_config()
        }
        """Get the system prompt for business assistant context"""
        return """You are an expert business consultant and decision-making assistant. Your role is to help users make informed business decisions by providing:

1. Strategic Analysis: Break down complex business problems into manageable components
2. Data-Driven Insights: Provide evidence-based recommendations when possible
3. Multiple Perspectives: Consider various angles and potential outcomes
4. Actionable Advice: Give specific, implementable suggestions
5. Risk Assessment: Highlight potential risks and mitigation strategies

Guidelines for your responses:
- Be professional yet approachable
- Use structured formats (bullet points, numbered lists) when helpful
- Ask clarifying questions when more context is needed
- Provide examples and case studies when relevant
- Consider both short-term and long-term implications
- Be honest about limitations and suggest when professional consultation might be needed

Focus areas include:
- Market analysis and competitive intelligence
- Financial planning and budgeting
- Marketing and customer acquisition strategies
- Operations and process optimization
- Team management and organizational development
- Growth strategies and scaling
- Risk management and contingency planning

Always maintain a supportive and encouraging tone while being realistic about challenges and opportunities."""
    
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenAI API with structured conversation awareness"""
        try:
            # Prepare messages with system prompt
            api_messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation context about current stage
            stage_info = self.get_current_stage_info()
            if not stage_info.get("completed"):
                context_msg = f"""
Current Stage: {stage_info['stage_title']} ({stage_info['stage_number']}/{stage_info['total_stages']})
Progress: {self.get_progress_percentage():.1f}% complete

Stage Prompt: {stage_info['prompt']}

Available Examples:
{chr(10).join(stage_info['examples'])}

Previous Decisions Summary:
{json.dumps(self.conversation_state['json_config'], indent=2) if self.conversation_state['json_config'] else 'None yet'}

IMPORTANT: After the user provides their response, you must:
1. Acknowledge their input
2. Extract the key information and structure it according to the JSON schema
3. Ask follow-up questions if needed
4. When ready to move to the next stage, clearly indicate completion

JSON Schema for this stage:
{json.dumps(stage_info.get('json_structure', {}), indent=2)}
"""
                api_messages.append({"role": "system", "content": context_msg})
            
            # Add conversation history (skip the welcome message)
            for msg in messages:
                if msg["role"] in ["user", "assistant"] and not msg["content"].startswith("👋"):
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                max_tokens=1200,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to extract and update JSON config from the conversation
            self._extract_stage_data_from_messages(messages, ai_response)
            
            return ai_response
            
        except openai.APIConnectionError:
            return "❌ Connection error. Please check your internet connection and try again."
        except openai.RateLimitError:
            return "⏳ Rate limit exceeded. Please wait a moment and try again."
        except openai.APIError as e:
            return f"❌ API error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def _extract_stage_data_from_messages(self, messages: List[Dict[str, str]], ai_response: str) -> None:
        """Extract structured data from conversation messages and update JSON config"""
        if not messages:
            return
        
        stage_info = self.get_current_stage_info()
        if stage_info.get("completed"):
            return
        
        stage_key = stage_info["stage_key"]
        
        # Skip if this stage is already completed
        if stage_key in self.conversation_state["completed_stages"]:
            return
        
        # Look for recent user input and AI response to extract data
        recent_user_input = None
        for msg in reversed(messages):
            if msg["role"] == "user":
                recent_user_input = msg["content"]
                break
        
        if not recent_user_input:
            return
        
        # Try to extract structured data based on stage type
        extracted_data = self._extract_data_for_stage(stage_key, recent_user_input, ai_response)
        
        if extracted_data:
            # Update the JSON config with extracted data
            self.update_json_config(stage_key, extracted_data)
            
            # Check if we should advance to next stage
            if self._should_advance_stage(ai_response):
                self.advance_stage()
    
    def _extract_data_for_stage(self, stage_key: str, user_input: str, ai_response: str) -> Optional[Dict[str, Any]]:
        """Extract structured data for a specific stage"""
        
        # Simple keyword-based extraction based on stage
        if stage_key == "problem_definition":
            return {
                "primary_problem": user_input[:200],  # Truncate for brevity
                "pain_points": self._extract_list_items(user_input + " " + ai_response),
                "urgency_level": self._extract_urgency(user_input + " " + ai_response),
                "cost_of_inaction": self._extract_cost_impact(user_input + " " + ai_response)
            }
        
        elif stage_key == "stakeholders":
            return {
                "decision_makers": self._extract_stakeholders(user_input + " " + ai_response, "decision|authority|manager|ceo|director"),
                "affected_parties": self._extract_stakeholders(user_input + " " + ai_response, "team|staff|employee|customer|user"),
                "influencers": self._extract_stakeholders(user_input + " " + ai_response, "influence|advisor|consultant|expert"),
                "concerns": self._extract_list_items(user_input + " " + ai_response, "concern|worry|issue|challenge")
            }
        
        elif stage_key == "solution_approach":
            return {
                "preferred_type": self._extract_solution_type(user_input),
                "alternatives_considered": self._extract_list_items(user_input + " " + ai_response, "alternative|option|consider|approach"),
                "past_attempts": self._extract_list_items(user_input + " " + ai_response, "previous|past|tried|attempted"),
                "constraints": self._extract_list_items(user_input + " " + ai_response, "constraint|limitation|requirement|must")
            }
        
        elif stage_key == "resources":
            return {
                "budget_range": self._extract_budget(user_input + " " + ai_response),
                "timeline": self._extract_timeline(user_input + " " + ai_response),
                "team_size": self._extract_team_size(user_input + " " + ai_response),
                "technical_expertise": self._extract_expertise_level(user_input + " " + ai_response),
                "data_availability": self._extract_data_availability(user_input + " " + ai_response),
                "constraints": self._extract_list_items(user_input + " " + ai_response, "constraint|limitation|challenge")
            }
        
        elif stage_key == "success_criteria":
            return {
                "primary_metrics": self._extract_list_items(user_input + " " + ai_response, "metric|measure|kpi|indicator"),
                "target_improvements": self._extract_targets(user_input + " " + ai_response),
                "timeline_to_results": self._extract_timeline(user_input + " " + ai_response),
                "success_definition": self._extract_success_definition(user_input + " " + ai_response)
            }
        
        elif stage_key == "implementation":
            return {
                "approach": self._extract_implementation_approach(user_input),
                "phases": self._extract_list_items(user_input + " " + ai_response, "phase|stage|step|milestone"),
                "timeline": self._extract_timeline(user_input + " " + ai_response),
                "leadership": self._extract_leadership(user_input + " " + ai_response),
                "dependencies": self._extract_list_items(user_input + " " + ai_response, "depend|require|need|prerequisite")
            }
        
        elif stage_key == "risk_management":
            return {
                "identified_risks": self._extract_list_items(user_input + " " + ai_response, "risk|threat|challenge|problem"),
                "risk_levels": self._extract_risk_levels(user_input + " " + ai_response),
                "mitigation_strategies": self._extract_list_items(user_input + " " + ai_response, "mitigate|prevent|address|handle"),
                "contingency_plans": self._extract_list_items(user_input + " " + ai_response, "contingency|backup|alternative|fallback")
            }
        
        return None
    
    def _should_advance_stage(self, ai_response: str) -> bool:
        """Determine if we should advance to the next stage based on AI response"""
        advance_indicators = [
            "let's move to the next stage",
            "ready for the next step",
            "moving on to",
            "now let's discuss",
            "great! next we'll",
            "perfect! now let's",
            "excellent! the next stage"
        ]
        
        ai_lower = ai_response.lower()
        return any(indicator in ai_lower for indicator in advance_indicators)
    
    # Helper methods for data extraction
    def _extract_list_items(self, text: str, keywords: str = "") -> List[str]:
        """Extract list items from text"""
        import re
        items = []
        
        # Look for bullet points and numbered lists
        bullet_pattern = r'[•\-\*\+]\s*(.+?)(?=\n|$)'
        numbered_pattern = r'\d+\.\s*(.+?)(?=\n|$)'
        
        items.extend(re.findall(bullet_pattern, text, re.MULTILINE))
        items.extend(re.findall(numbered_pattern, text, re.MULTILINE))
        
        # Clean up items
        cleaned_items = []
        for item in items:
            item = item.strip()
            if item and len(item) > 3:  # Filter out very short items
                cleaned_items.append(item[:100])  # Truncate long items
        
        return cleaned_items[:5]  # Limit to 5 items
    
    def _extract_stakeholders(self, text: str, pattern: str) -> List[str]:
        """Extract stakeholders matching a pattern"""
        import re
        stakeholders = []
        
        # Find sentences containing stakeholder keywords
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            if re.search(pattern, sentence, re.IGNORECASE):
                # Extract potential stakeholder names
                words = sentence.split()
                for i, word in enumerate(words):
                    if re.search(pattern, word, re.IGNORECASE):
                        # Take surrounding words as potential stakeholders
                        context = " ".join(words[max(0, i-2):i+3])
                        if context.strip():
                            stakeholders.append(context.strip()[:50])
        
        return stakeholders[:3]  # Limit to 3 stakeholders
    
    def _extract_urgency(self, text: str) -> str:
        """Extract urgency level from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["critical", "urgent", "immediate", "asap"]):
            return "critical"
        elif any(word in text_lower for word in ["high", "important", "priority", "soon"]):
            return "high"
        elif any(word in text_lower for word in ["medium", "moderate", "normal"]):
            return "medium"
        else:
            return "low"
    
    def _extract_cost_impact(self, text: str) -> str:
        """Extract cost impact from text"""
        import re
        cost_patterns = [
            r'cost.*?(\$[\d,]+|\d+.*?dollar)',
            r'lose.*?(\$[\d,]+|\d+.*?dollar)',
            r'save.*?(\$[\d,]+|\d+.*?dollar)',
            r'impact.*?(\$[\d,]+|\d+.*?dollar)'
        ]
        
        for pattern in cost_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)[:100]
        
        return "Impact not quantified"
    
    def _extract_solution_type(self, text: str) -> str:
        """Extract solution type from text"""
        solution_types = {
            "technology": ["software", "system", "platform", "tool", "automation", "ai", "digital"],
            "process": ["process", "workflow", "procedure", "methodology", "framework"],
            "people": ["hiring", "training", "team", "staff", "personnel", "human"],
            "partnership": ["partner", "vendor", "outsource", "collaborate", "third-party"],
            "financial": ["investment", "funding", "budget", "financial", "money"]
        }
        
        text_lower = text.lower()
        for category, keywords in solution_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return category.title() + " solution"
        
        return "Mixed approach"
    
    def _extract_budget(self, text: str) -> str:
        """Extract budget information from text"""
        import re
        budget_patterns = [
            r'\$[\d,]+(?:\.\d+)?[kmb]?',
            r'€[\d,]+(?:\.\d+)?[kmb]?',
            r'£[\d,]+(?:\.\d+)?[kmb]?',
            r'\d+k?\s*(?:dollar|euro|pound)',
            r'budget.*?(\d+)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return "Not specified"
    
    def _extract_timeline(self, text: str) -> str:
        """Extract timeline from text"""
        import re
        timeline_patterns = [
            r'\d+\s*(?:week|month|year|day)s?',
            r'(?:quarter|q[1-4])',
            r'(?:january|february|march|april|may|june|july|august|september|october|november|december)'
        ]
        
        for pattern in timeline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return "Not specified"
    
    def _extract_team_size(self, text: str) -> str:
        """Extract team size from text"""
        import re
        size_patterns = [
            r'\d+\s*(?:people|person|member|developer|employee)',
            r'team.*?(\d+)',
            r'(?:small|medium|large)\s*team'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return "Not specified"
    
    def _extract_expertise_level(self, text: str) -> str:
        """Extract technical expertise level"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["expert", "advanced", "senior", "experienced"]):
            return "Advanced"
        elif any(word in text_lower for word in ["intermediate", "moderate", "some experience"]):
            return "Intermediate"
        elif any(word in text_lower for word in ["basic", "beginner", "novice", "learning"]):
            return "Basic"
        else:
            return "Not specified"
    
    def _extract_data_availability(self, text: str) -> str:
        """Extract data availability information"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["extensive", "lots", "abundant", "comprehensive"]):
            return "Extensive"
        elif any(word in text_lower for word in ["moderate", "some", "adequate"]):
            return "Moderate"
        elif any(word in text_lower for word in ["limited", "little", "minimal", "lacking"]):
            return "Limited"
        else:
            return "Not specified"
    
    def _extract_targets(self, text: str) -> Dict[str, str]:
        """Extract target improvements"""
        import re
        targets = {}
        
        # Look for percentage improvements
        percent_pattern = r'(\d+)%\s*(?:improvement|increase|reduction|decrease)'
        matches = re.findall(percent_pattern, text, re.IGNORECASE)
        
        for i, match in enumerate(matches):
            targets[f"target_{i+1}"] = f"{match}% improvement"
        
        return targets
    
    def _extract_success_definition(self, text: str) -> str:
        """Extract success definition"""
        success_keywords = ["success", "successful", "achieve", "accomplish", "goal", "objective"]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in success_keywords):
                return sentence.strip()[:200]
        
        return "Success criteria to be defined"
    
    def _extract_implementation_approach(self, text: str) -> str:
        """Extract implementation approach"""
        approaches = {
            "phased": ["phase", "gradual", "step", "incremental"],
            "pilot": ["pilot", "test", "trial", "experiment"],
            "full": ["full", "complete", "all at once", "big bang"],
            "iterative": ["iterative", "agile", "sprint", "iteration"]
        }
        
        text_lower = text.lower()
        for approach, keywords in approaches.items():
            if any(keyword in text_lower for keyword in keywords):
                return approach.title() + " approach"
        
        return "Approach to be determined"
    
    def _extract_leadership(self, text: str) -> str:
        """Extract leadership information"""
        leadership_terms = ["lead", "manage", "oversee", "responsible", "accountable", "owner"]
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(term in sentence.lower() for term in leadership_terms):
                return sentence.strip()[:100]
        
        return "Leadership to be assigned"
    
    def _extract_risk_levels(self, text: str) -> Dict[str, str]:
        """Extract risk levels"""
        risks = {}
        risk_levels = ["high", "medium", "low", "critical"]
        
        sentences = text.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for level in risk_levels:
                if level in sentence_lower and "risk" in sentence_lower:
                    risks[sentence.strip()[:50]] = level
        
        return risks
    
    def validate_api_key(self) -> bool:
        """Validate if the API key is working"""
        try:
            self.client.models.list()
            return True
        except:
            return False
