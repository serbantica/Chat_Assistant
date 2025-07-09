import streamlit as st
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from chat_handler import ChatHandler
from utils import setup_page_config, display_chat_history, get_user_input
from templates import TemplateRegistry

# Load environment variables
load_dotenv()

def get_available_templates():
    """Get list of available templates"""
    return TemplateRegistry.get_available_templates()

def save_config_to_file(config_data, filename):
    """Save configuration to JSON file"""
    try:
        os.makedirs("saved_configs", exist_ok=True)
        filepath = f"saved_configs/{filename}"
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)
        return filepath
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def load_config_from_file(filepath):
    """Load configuration from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def display_progress_sidebar(chat_handler):
    """Display enhanced progress information in sidebar"""
    with st.sidebar:
        st.markdown("### 📊 Progress Tracker")
        
        progress_details = chat_handler.get_stage_progress_details()
        
        # Progress bar and percentage
        progress = progress_details["progress_percentage"]
        st.progress(progress / 100)
        st.write(f"**{progress:.1f}% Complete**")
        
        # Current stage info
        if progress_details["completed_count"] < progress_details["total_stages"]:
            current_stage = progress_details["stages"][chat_handler.conversation_state["current_stage"]]
            st.write(f"**Current Stage:** {current_stage['title']}")
            st.write(f"**Step:** {progress_details['current_stage']} of {progress_details['total_stages']}")
        else:
            st.write("✅ **All stages completed!**")
        
        # Use case info - only show if project is finalized
        finalized_name = chat_handler.get_finalized_project_name()
        if finalized_name:
            st.write(f"**Project:** {finalized_name}")
        elif progress_details["use_case_name"]:
            st.write(f"**Working on:** {progress_details['use_case_name']} *(temporary)*")
        
        # Show all stages with status
        st.markdown("#### 📋 Stages Overview")
        for stage in progress_details["stages"]:
            if stage["completed"]:
                status_icon = "✅"
            elif stage["current"]:
                status_icon = "🔄"
            else:
                status_icon = "⏳"
            
            st.write(f"{status_icon} **{stage['stage_number']}.** {stage['title']}")
            
        # Auto-save status
        if progress_details["last_updated"]:
            last_update = datetime.fromisoformat(progress_details["last_updated"])
            st.markdown("---")
            st.write(f"💾 **Auto-saved:** {last_update.strftime('%H:%M:%S')}")
        
        # Show filename that would be used for saving
        finalized_name = chat_handler.get_finalized_project_name()
        if finalized_name:
            filename = chat_handler.generate_filename()
            st.write(f"📝 **Save as:** `{filename}`")
        else:
            temp_filename = chat_handler.generate_temp_filename()
            st.write(f"📝 **Auto-save as:** `{temp_filename}` *(temporary)*")

def display_template_selector():
    """Display template selection interface"""
    st.markdown("### 🎯 Choose Your Framework")
    
    templates = get_available_templates()
    
    if len(templates) == 1:
        # If only one template, auto-select it
        return list(templates.keys())[0]
    
    # Multiple templates - show selection
    template_options = []
    for key, template in templates.items():
        stages_count = template.get('stages_count', len(template.get('stages', [])))
        template_options.append(f"{template['name']} - {template['description']} ({stages_count} stages)")
    
    selected_idx = st.selectbox(
        "Select a framework to guide your decision-making process:",
        range(len(template_options)),
        format_func=lambda x: template_options[x],
        key="template_selector"
    )
    
    return list(templates.keys())[selected_idx]

def display_save_load_controls(chat_handler):
    """Display save/load controls"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💾 Save/Load Configuration")
        
        # Auto-save toggle
        auto_save = st.checkbox(
            "� Auto-save progress", 
            value=chat_handler.conversation_state.get("auto_save_enabled", True),
            help="Automatically save progress after each stage completion"
        )
        chat_handler.conversation_state["auto_save_enabled"] = auto_save
        
        # Manual save with suggested filename
        finalized_name = chat_handler.get_finalized_project_name()
        if finalized_name:
            suggested_filename = chat_handler.generate_filename()
            save_label = f"💾 Save as {suggested_filename}"
        else:
            suggested_filename = chat_handler.generate_temp_filename()
            save_label = f"💾 Auto-save as {suggested_filename}"
        
        if st.button(save_label, use_container_width=True):
            config_data = chat_handler.save_conversation_state()
            
            filepath = save_config_to_file(config_data, suggested_filename)
            if filepath:
                st.success(f"✅ Saved to {suggested_filename}")
                
                # Offer download
                with open(filepath, 'r') as f:
                    st.download_button(
                        label="⬇️ Download Config File",
                        data=f.read(),
                        file_name=suggested_filename,
                        mime="application/json",
                        use_container_width=True
                    )
        
        # Load from file
        uploaded_file = st.file_uploader(
            "📁 Load Configuration", 
            type=['json'],
            help="Upload a previously saved configuration file"
        )
        
        if uploaded_file is not None:
            try:
                config_data = json.load(uploaded_file)
                if st.button("🔄 Load This Configuration"):
                    chat_handler.load_conversation_state(config_data)
                    st.success("✅ Configuration loaded successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
        
        # Quick load from saved files
        saved_files_dir = "saved_configs"
        if os.path.exists(saved_files_dir):
            saved_files = [f for f in os.listdir(saved_files_dir) if f.endswith('.json')]
            if saved_files:
                st.markdown("#### 📂 Previously Saved")
                selected_file = st.selectbox(
                    "Quick load:",
                    [""] + saved_files,
                    format_func=lambda x: "Select a file..." if x == "" else x
                )
                
                if selected_file and st.button("� Load Selected"):
                    filepath = os.path.join(saved_files_dir, selected_file)
                    config_data = load_config_from_file(filepath)
                    if config_data:
                        chat_handler.load_conversation_state(config_data)
                        st.success("✅ Configuration loaded!")
                        st.rerun()

def display_project_finalization(chat_handler):
    """Display project finalization controls when near completion"""
    progress = chat_handler.get_progress_percentage()
    
    if progress >= 70:  # Show when 70% or more complete
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🎯 Project Finalization")
            
            # Check if project is already finalized
            finalized_name = chat_handler.get_finalized_project_name()
            pending_name = chat_handler.get_pending_project_name()
            
            if finalized_name:
                st.success(f"✅ **Project Finalized:** {finalized_name}")
                st.info("This project has been finalized with the confirmed name.")
            else:
                st.info("⚠️ **Project name will only be saved after confirmation below**")
                
                if pending_name:
                    st.write(f"**Pending Name:** {pending_name}")
                
                # Project name input
                project_name = st.text_input(
                    "Final Project Name:",
                    value=pending_name,
                    placeholder="Enter a concise project name",
                    help="This will be used in the filename and final JSON configuration ONLY after you confirm finalization"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Preview Name", use_container_width=True):
                        if project_name and project_name.strip():
                            chat_handler.set_project_name(project_name.strip())
                            st.success("✅ Name ready for finalization!")
                            st.rerun()
                
                with col2:
                    if st.button("🏁 Confirm & Finalize", use_container_width=True):
                        if project_name and project_name.strip():
                            final_config = chat_handler.finalize_project(project_name.strip())
                            st.success("🎉 Project finalized with confirmed name!")
                            
                            # Show download button for final config
                            json_str = json.dumps(final_config, indent=2)
                            st.download_button(
                                label="⬇️ Download Final Report",
                                data=json_str,
                                file_name=f"{chat_handler.generate_filename()}",
                                mime="application/json",
                                use_container_width=True
                            )
                            st.rerun()
                        else:
                            st.error("Please enter a project name before finalizing!")
                
                # Show current auto-save status
                if not finalized_name:
                    st.caption("💡 Auto-save uses temporary names until finalization")
            
            # Show completion status
            if chat_handler.is_project_completed():
                st.success("🎉 All stages completed! Ready to finalize.")
            else:
                remaining = len(chat_handler.template_config["stages"]) - len(chat_handler.conversation_state["completed_stages"])
                st.info(f"📋 {remaining} stages remaining before finalization.")

def display_stage_data_input(chat_handler):
    """Allow manual stage data input and validation"""
    stage_info = chat_handler.get_current_stage_info()
    
    if stage_info.get("completed"):
        return
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📝 Stage Data Capture")
        
        stage_key = stage_info["stage_key"]
        stage_title = stage_info["stage_title"]
        
        st.write(f"**Current:** {stage_title}")
        
        # Show current stage data if any
        current_data = chat_handler.conversation_state["json_config"].get(stage_key, {})
        if current_data:
            st.write("**Captured Data:**")
            st.json(current_data)
        
        # Manual data input based on stage
        if st.button("🔧 Update Stage Data", use_container_width=True):
            st.session_state.show_manual_input = True
        
        if st.session_state.get("show_manual_input", False):
            st.markdown("#### Manual Data Entry")
            
            # Generic text input for key information
            key_info = st.text_area(
                "Key Information:",
                value=json.dumps(current_data, indent=2) if current_data else "",
                height=100,
                help="Enter structured data for this stage"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Data"):
                    try:
                        if key_info.strip():
                            # Try to parse as JSON first
                            try:
                                parsed_data = json.loads(key_info)
                                chat_handler.update_json_config(stage_key, parsed_data)
                                st.success("✅ Data saved!")
                            except json.JSONDecodeError:
                                # If not JSON, create a simple structure
                                simple_data = {
                                    "raw_input": key_info,
                                    "stage": stage_title,
                                    "timestamp": datetime.now().isoformat()
                                }
                                chat_handler.update_json_config(stage_key, simple_data)
                                st.success("✅ Data saved as raw input!")
                        
                        st.session_state.show_manual_input = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error saving data: {e}")
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_manual_input = False
                    st.rerun()
            
            # Stage advancement controls
            st.markdown("#### Stage Control")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Next Stage", use_container_width=True):
                    if stage_key not in chat_handler.conversation_state["completed_stages"]:
                        # Mark current stage as completed with minimal data
                        if not current_data:
                            chat_handler.update_json_config(stage_key, {
                                "status": "completed_manually",
                                "timestamp": datetime.now().isoformat()
                            })
                    chat_handler.advance_stage()
                    st.rerun()
            
            with col2:
                if st.button("⬅️ Previous Stage", use_container_width=True):
                    if chat_handler.conversation_state["current_stage"] > 0:
                        chat_handler.conversation_state["current_stage"] -= 1
                        st.rerun()
    """Allow manual stage data input and validation"""
    stage_info = chat_handler.get_current_stage_info()
    
    if stage_info.get("completed"):
        return
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### � Stage Data Capture")
        
        stage_key = stage_info["stage_key"]
        stage_title = stage_info["stage_title"]
        
        st.write(f"**Current:** {stage_title}")
        
        # Show current stage data if any
        current_data = chat_handler.conversation_state["json_config"].get(stage_key, {})
        if current_data:
            st.write("**Captured Data:**")
            st.json(current_data)
        
        # Manual data input based on stage
        if st.button("� Update Stage Data", use_container_width=True):
            st.session_state.show_manual_input = True
        
        if st.session_state.get("show_manual_input", False):
            st.markdown("#### Manual Data Entry")
            
            # Generic text input for key information
            key_info = st.text_area(
                "Key Information:",
                value=json.dumps(current_data, indent=2) if current_data else "",
                height=100,
                help="Enter structured data for this stage"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Data"):
                    try:
                        if key_info.strip():
                            # Try to parse as JSON first
                            try:
                                parsed_data = json.loads(key_info)
                                chat_handler.update_json_config(stage_key, parsed_data)
                                st.success("✅ Data saved!")
                            except json.JSONDecodeError:
                                # If not JSON, create a simple structure
                                simple_data = {
                                    "raw_input": key_info,
                                    "stage": stage_title,
                                    "timestamp": datetime.now().isoformat()
                                }
                                chat_handler.update_json_config(stage_key, simple_data)
                                st.success("✅ Data saved as raw input!")
                        
                        st.session_state.show_manual_input = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error saving data: {e}")
            
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_manual_input = False
                    st.rerun()
            
            # Stage advancement controls
            st.markdown("#### Stage Control")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Next Stage", use_container_width=True):
                    if stage_key not in chat_handler.conversation_state["completed_stages"]:
                        # Mark current stage as completed with minimal data
                        if not current_data:
                            chat_handler.update_json_config(stage_key, {
                                "status": "completed_manually",
                                "timestamp": datetime.now().isoformat()
                            })
                    chat_handler.advance_stage()
                    st.rerun()
            
            with col2:
                if st.button("⬅️ Previous Stage", use_container_width=True):
                    if chat_handler.conversation_state["current_stage"] > 0:
                        chat_handler.conversation_state["current_stage"] -= 1
                        st.rerun()

def display_json_preview(chat_handler):
    """Display current JSON configuration"""
    if chat_handler.conversation_state["json_config"]:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 📋 Current Configuration")
            
            if st.button("👁️ Preview JSON", use_container_width=True):
                st.session_state.show_json = not st.session_state.get("show_json", False)
            
            if st.session_state.get("show_json", False):
                current_config = chat_handler.get_final_json_config()
                st.json(current_config)
                
                # Export option
                json_str = json.dumps(current_config, indent=2)
                
                # Use appropriate filename based on finalization status
                finalized_name = chat_handler.get_finalized_project_name()
                if finalized_name:
                    export_filename = chat_handler.generate_filename()
                else:
                    export_filename = chat_handler.generate_temp_filename()
                
                st.download_button(
                    label="⬇️ Export JSON",
                    data=json_str,
                    file_name=export_filename,
                    mime="application/json"
                )

def main():
    """Main application function"""
    # Set up page configuration
    setup_page_config()
    
    # Initialize session state
    if "template_selected" not in st.session_state:
        st.session_state.template_selected = False
    
    # Template selection
    if not st.session_state.template_selected:
        st.title("🏢 Business Decision Assistant")
        st.markdown("---")
        
        selected_template = display_template_selector()
        
        if st.button("🚀 Start Decision Framework", use_container_width=True):
            st.session_state.selected_template = selected_template
            st.session_state.template_selected = True
            st.rerun()
        
        return
    
    # Initialize chat handler with selected template
    if "chat_handler" not in st.session_state:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("🔑 OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            st.stop()
        st.session_state.chat_handler = ChatHandler(api_key, st.session_state.selected_template)
    
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
        template_name = get_available_templates()[st.session_state.selected_template]["name"]
        welcome_msg = f"""👋 Welcome to the {template_name}!

I'll guide you through a structured approach to analyze your business decision. We'll cover:

{chr(10).join([f"{i+1}. {stage['title']}" for i, stage in enumerate(st.session_state.chat_handler.template_config['stages'])])}

At each stage, I'll provide examples and ask follow-up questions to ensure we capture all the important details. 

Let's start with the first stage. What business challenge or opportunity would you like to analyze?"""
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": welcome_msg
        })
    
    # Display header with template info
    template_info = get_available_templates()[st.session_state.selected_template]
    st.title(f"{template_info['name']}")
    
    # Progress sidebar
    display_progress_sidebar(st.session_state.chat_handler)
    
    # Save/Load controls
    display_save_load_controls(st.session_state.chat_handler)
    
    # Project finalization (when near completion)
    display_project_finalization(st.session_state.chat_handler)
    
    # Stage data input controls
    display_stage_data_input(st.session_state.chat_handler)
    
    # JSON preview
    display_json_preview(st.session_state.chat_handler)
    
    st.markdown("---")
    
    # Display chat history
    display_chat_history(st.session_state.messages)
    
    # Get user input
    user_input = get_user_input()
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your response..."):
                try:
                    response = st.session_state.chat_handler.get_response(
                        st.session_state.messages
                    )
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
                    
                    # Rerun to update progress display
                    st.rerun()
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
    
    # Additional sidebar controls
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🛠️ Chat Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    st.session_state.chat_handler = ChatHandler(
                        api_key, 
                        st.session_state.selected_template
                    )
                st.rerun()
        
        with col2:
            if st.button("� New Template", use_container_width=True):
                # Reset everything
                for key in ["template_selected", "selected_template", "messages", "chat_handler"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    main()
