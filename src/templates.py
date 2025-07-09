"""
Template configurations for different business decision frameworks.
This module uses the TemplateLoader to read templates from markdown files.
"""

from typing import Dict, Any, List
import sys
from pathlib import Path

# Add src directory to path for imports
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from template_loader import TemplateLoader

class TemplateRegistry:
    """Registry for managing different conversation templates"""
    
    def __init__(self):
        self.loader = TemplateLoader()
    
    @staticmethod
    def get_available_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available templates from markdown files"""
        loader = TemplateLoader()
        return loader.get_available_templates()
    
    @staticmethod
    def get_template_config(template_type: str) -> Dict[str, Any]:
        """Get detailed configuration for a specific template"""
        loader = TemplateLoader()
        try:
            return loader.get_template_config(template_type)
        except (FileNotFoundError, ValueError) as e:
            raise ValueError(f"Template '{template_type}' not found or invalid: {e}")
    
    @staticmethod
    def validate_template(template_id: str) -> Dict[str, Any]:
        """Validate a template configuration"""
        loader = TemplateLoader()
        return loader.validate_template(template_id)
    
    @staticmethod
    def list_available_templates() -> List[str]:
        """List all available template IDs"""
        loader = TemplateLoader()
        return list(loader.get_available_templates().keys())