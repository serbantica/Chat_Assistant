#!/usr/bin/env python3
"""
Template validation script to test all templates in the system.
"""

import sys
import os
sys.path.append('src')

from template_loader import TemplateLoader
from templates import TemplateRegistry

def main():
    print("🔍 Template Validation Report")
    print("=" * 50)
    
    # Test TemplateLoader
    loader = TemplateLoader()
    
    print("\n📁 Available Template Files:")
    files = loader.list_template_files()
    for file in files:
        print(f"  - {file}")
    
    print("\n📋 Template Metadata:")
    templates = loader.get_available_templates()
    for template_id, metadata in templates.items():
        print(f"\n🎯 {template_id}:")
        print(f"    Name: {metadata.get('name', 'N/A')}")
        print(f"    Description: {metadata.get('description', 'N/A')}")
        print(f"    Category: {metadata.get('category', 'N/A')}")
        print(f"    Stages: {metadata.get('stages_count', 'N/A')}")
    
    print("\n✅ Template Validation Results:")
    for template_id in templates.keys():
        try:
            validation = loader.validate_template(template_id)
            status = "✅ VALID" if validation["valid"] else "❌ INVALID"
            print(f"\n{status} {template_id}:")
            print(f"    Stages: {validation['stage_count']}")
            print(f"    Examples: {validation['total_examples']}")
            print(f"    Follow-ups: {validation['total_followups']}")
            
            if validation["errors"]:
                print("    Errors:")
                for error in validation["errors"]:
                    print(f"      - {error}")
            
            if validation["warnings"]:
                print("    Warnings:")
                for warning in validation["warnings"]:
                    print(f"      - {warning}")
                    
        except Exception as e:
            print(f"❌ ERROR {template_id}: {e}")
    
    print("\n🧪 Testing Template Registry Integration:")
    try:
        registry_templates = TemplateRegistry.get_available_templates()
        print(f"Registry found {len(registry_templates)} templates")
        
        for template_id in registry_templates.keys():
            try:
                config = TemplateRegistry.get_template_config(template_id)
                print(f"  ✅ {template_id}: {len(config.get('stages', []))} stages loaded")
            except Exception as e:
                print(f"  ❌ {template_id}: {e}")
                
    except Exception as e:
        print(f"❌ Registry error: {e}")
    
    print("\n🎉 Validation Complete!")

if __name__ == "__main__":
    main()
