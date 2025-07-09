"""
Template loader for reading and parsing conversation templates from markdown files.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

class TemplateLoader:
    """Loads and parses conversation templates from markdown files"""
    
    def __init__(self, templates_dir: str = "docs/templates"):
        self.templates_dir = Path(templates_dir)
        self._template_cache = {}
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get metadata for all available templates"""
        templates = {}
        
        if not self.templates_dir.exists():
            return templates
        
        for template_file in self.templates_dir.glob("*.md"):
            if template_file.name == "README.md":
                continue
                
            try:
                metadata = self._parse_template_metadata(template_file)
                if metadata:
                    template_id = metadata.get("template_id", template_file.stem)
                    templates[template_id] = metadata
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")
        
        return templates
    
    def get_template_config(self, template_id: str) -> Dict[str, Any]:
        """Get full configuration for a specific template"""
        if template_id in self._template_cache:
            return self._template_cache[template_id]
        
        template_file = self.templates_dir / f"{template_id}.md"
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        try:
            config = self._parse_template_file(template_file)
            self._template_cache[template_id] = config
            return config
        except Exception as e:
            raise ValueError(f"Error parsing template {template_id}: {e}")
    
    def _parse_template_metadata(self, template_file: Path) -> Optional[Dict[str, Any]]:
        """Parse just the metadata section of a template file"""
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find metadata JSON block
        metadata_match = re.search(r'## Template Metadata\s*```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if not metadata_match:
            return None
        
        try:
            metadata = json.loads(metadata_match.group(1))
            return metadata
        except json.JSONDecodeError:
            return None
    
    def _parse_template_file(self, template_file: Path) -> Dict[str, Any]:
        """Parse a complete template file"""
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse metadata
        metadata = self._parse_template_metadata(template_file)
        if not metadata:
            raise ValueError("Template metadata not found or invalid")
        
        # Parse stages
        stages = self._parse_stages(content)
        
        return {
            "name": metadata.get("name", "Unknown Template"),
            "description": metadata.get("description", ""),
            "category": metadata.get("category", "General"),
            "version": metadata.get("version", "1.0"),
            "stages": stages
        }
    
    def _parse_stages(self, content: str) -> List[Dict[str, Any]]:
        """Parse stage configurations from template content"""
        stages = []
        
        # Find all stage sections
        stage_pattern = r'### Stage \d+: (.+?)\n\*\*Key\*\*: `([^`]+)`\n\*\*Title\*\*: (.+?)\n\*\*Prompt\*\*: (.+?)\n\n\*\*Examples\*\*:\n(.*?)\n\n\*\*Follow-up Questions\*\*:\n(.*?)\n\n\*\*JSON Structure\*\*:\n```json\s*(\{.*?\})\s*```'
        
        matches = re.finditer(stage_pattern, content, re.DOTALL)
        
        for match in matches:
            stage_title = match.group(1).strip()
            stage_key = match.group(2).strip()
            stage_title_repeat = match.group(3).strip()
            stage_prompt = match.group(4).strip()
            examples_text = match.group(5).strip()
            followup_text = match.group(6).strip()
            json_structure_text = match.group(7).strip()
            
            # Parse examples
            examples = []
            for line in examples_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    examples.append(line[2:].strip())
            
            # Parse follow-up questions
            follow_up = []
            for line in followup_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    follow_up.append(line[2:].strip())
            
            # Parse JSON structure
            try:
                json_structure = json.loads(json_structure_text)
            except json.JSONDecodeError:
                json_structure = {}
            
            stage = {
                "key": stage_key,
                "title": stage_title,
                "prompt": stage_prompt,
                "examples": examples,
                "follow_up": follow_up,
                "json_structure": json_structure
            }
            
            stages.append(stage)
        
        return stages
    
    def validate_template(self, template_id: str) -> Dict[str, Any]:
        """Validate a template and return validation results"""
        try:
            config = self.get_template_config(template_id)
            
            validation = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "stage_count": len(config.get("stages", [])),
                "total_examples": sum(len(stage.get("examples", [])) for stage in config.get("stages", [])),
                "total_followups": sum(len(stage.get("follow_up", [])) for stage in config.get("stages", []))
            }
            
            # Check for required fields
            if not config.get("name"):
                validation["errors"].append("Template name is missing")
            
            if not config.get("stages"):
                validation["errors"].append("No stages found in template")
            
            # Validate stages
            for i, stage in enumerate(config.get("stages", [])):
                stage_num = i + 1
                
                if not stage.get("key"):
                    validation["errors"].append(f"Stage {stage_num}: Missing key")
                
                if not stage.get("title"):
                    validation["errors"].append(f"Stage {stage_num}: Missing title")
                
                if not stage.get("prompt"):
                    validation["errors"].append(f"Stage {stage_num}: Missing prompt")
                
                if len(stage.get("examples", [])) < 3:
                    validation["warnings"].append(f"Stage {stage_num}: Less than 3 examples")
                
                if len(stage.get("follow_up", [])) < 2:
                    validation["warnings"].append(f"Stage {stage_num}: Less than 2 follow-up questions")
            
            if validation["errors"]:
                validation["valid"] = False
            
            return validation
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Template parsing error: {str(e)}"],
                "warnings": [],
                "stage_count": 0,
                "total_examples": 0,
                "total_followups": 0
            }
    
    def list_template_files(self) -> List[str]:
        """List all template files in the templates directory"""
        if not self.templates_dir.exists():
            return []
        
        return [f.name for f in self.templates_dir.glob("*.md") if f.name != "README.md"]
    
    def refresh_cache(self):
        """Clear the template cache to force reload"""
        self._template_cache.clear()
