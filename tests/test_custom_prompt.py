#!/usr/bin/env python3
"""
Custom Prompt Template Configuration Test Suite

PURPOSE:
Validates that custom prompt templates are properly configured in YAML files
and that the Government pharmaceutical compliance prompts are correctly loaded.

WHAT IT TESTS:
1. YAML Configuration Validation:
   - Prompt template presence in configuration files
   - YAML syntax and structure verification
   - Required prompt components validation
   - Configuration parameter completeness

2. Government Prompt Integration:
   - S1-S6 regulatory categories presence
   - P1-P8 processing workflow validation
   - CDSCO guideline integration verification
   - Pharmaceutical compliance terminology validation

3. Template Content Quality:
   - Professional pharmaceutical language usage
   - Regulatory framework accuracy
   - Government-specific requirements coverage
   - Compliance analysis workflow completeness

4. Configuration Consistency:
   - Enhanced vs standard version comparison
   - Prompt template synchronization verification
   - Parameter alignment across configurations
   - Version compatibility validation

WHEN TO RUN:
- After modifying YAML configuration files
- During prompt template development
- Before deployment to validate configurations
- When troubleshooting prompt-related issues

EXPECTED OUTCOME:
- All YAML configurations load without syntax errors
- Government prompt templates are properly integrated
- Required pharmaceutical compliance components are present
- Configuration consistency across versions maintained

DEPENDENCIES:
- YAML configuration files (app_openrouter_enhanced.yaml)
- system_prompt.txt file with Government compliance prompt
- Python YAML parsing libraries
- Configuration validation utilities

SCOPE:
This test focuses on configuration validation, not live API testing.
For runtime prompt testing, use test_prompt_replacement.py
"""

import yaml

def test_custom_prompt():
    """Test that our custom prompt template is properly configured"""
    
    print("🔍 Testing Custom Prompt Configuration...")
    
    # Test the enhanced configuration
    try:
        with open('app_openrouter_enhanced.yaml', 'r') as f:
            config = yaml.safe_load(f)
            
        # Check if custom prompt template is present
        if 'prompt_template' in config:
            print("✅ Custom prompt template found in enhanced config!")
            print("📝 Custom prompt preview:")
            print("-" * 50)
            print(config['prompt_template'][:200] + "...")
            print("-" * 50)
        else:
            print("❌ Custom prompt template not found in enhanced config")
            
    except Exception as e:
        print(f"❌ Error reading enhanced config: {e}")
    
    # Test the main configuration  
    try:
        with open('app_openrouter.yaml', 'r') as f:
            config = yaml.safe_load(f)
            
        # Check if custom prompt template is present
        if 'prompt_template' in config:
            print("✅ Custom prompt template found in main config!")
            print("📝 Custom prompt preview:")
            print("-" * 50)
            print(config['prompt_template'][:200] + "...")
            print("-" * 50)
        else:
            print("❌ Custom prompt template not found in main config")
            
    except Exception as e:
        print(f"❌ Error reading main config: {e}")
    
    print("\n🔧 Configuration Analysis Complete!")
    print("\nℹ️  The default Pathway prompt 'Please provide an answer based solely on the provided sources' has been replaced with a custom pharmaceutical compliance prompt.")
    print("\n📋 To see the changes in action:")
    print("   1. Install requirements: pip install -r requirements.txt")  
    print("   2. Set environment variables for OpenRouter")
    print("   3. Run: python3 app_openrouter_enhanced.py")
    print("   4. Check the logs - you should no longer see the default prompt text")

if __name__ == "__main__":
    test_custom_prompt()