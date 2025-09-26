#!/usr/bin/env python3
"""
Enhanced Pharmaceutical Compliance RAG System with System Prompt
Simple approach: prepend system prompt to user queries
"""

import os
import pathway as pw
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedPharmaComplianceApp:
    def __init__(self, config_path="app_openrouter_enhanced.yaml", system_prompt_file="system_prompt.txt"):
        """Initialize the enhanced pharmaceutical compliance RAG application"""
        # Load environment variables
        load_dotenv()
        
        self.config_path = config_path
        self.system_prompt_file = system_prompt_file
        self.system_prompt = self.load_system_prompt()
        self.validate_environment()
        
    def load_system_prompt(self):
        """Load system prompt from file"""
        try:
            with open(self.system_prompt_file, 'r') as f:
                prompt = f.read().strip()
                logger.info(f"✅ System prompt loaded from {self.system_prompt_file}")
                return prompt
        except FileNotFoundError:
            logger.warning(f"⚠️ System prompt file not found: {self.system_prompt_file}")
            return ""
        
    def validate_environment(self):
        """Validate required environment variables"""
        required_vars = ["OPENROUTER_API_KEY", "OPENROUTER_API_BASE"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.warning(f"Missing environment variables: {missing_vars}")
            logger.info("The system will work for document processing but LLM queries may fail")
            logger.info("Set OPENROUTER_API_KEY to enable full LLM functionality")
        else:
            logger.info("✅ OpenRouter configuration validated")
    
    def setup_pharmaceutical_context(self):
        """Set up pharmaceutical-specific processing context"""
        # Set environment variables for pharmaceutical domain optimization
        os.environ.setdefault("PATHWAY_PHARMA_MODE", "true")
        os.environ.setdefault("PATHWAY_REGULATORY_FOCUS", "drug_bans,scheduling,compliance,safety_alerts")
        
    def enhance_prompt(self, user_prompt):
        """Enhance user prompt with system prompt prefix"""
        if self.system_prompt:
            enhanced = f"{self.system_prompt}\n\nUser Question: {user_prompt}"
            logger.info(f"🔍 Enhanced prompt created (length: {len(enhanced)} chars)")
            logger.info(f"📝 System prompt prefix: {self.system_prompt[:200]}...")
            logger.info(f"❓ User query: {user_prompt}")
            return enhanced
        else:
            logger.warning("⚠️ No system prompt - using original query")
            return user_prompt
        
    def run(self):
        """Run the enhanced pharmaceutical compliance RAG system"""
        try:
            logger.info("🧬 Starting Enhanced Pharmaceutical Compliance RAG System...")
            logger.info("📊 Configuration: OpenRouter LLM with enhanced prompts")
            logger.info("🔌 Port: 8001 (Enhanced version)")
            logger.info(f"📋 System prompt: {'✅ Active' if self.system_prompt else '❌ Not loaded'}")
            
            # Setup pharmaceutical context
            self.setup_pharmaceutical_context()
            
            # Load and run the Pathway configuration
            logger.info(f"📋 Loading configuration from {self.config_path}")
            
            with open(self.config_path) as f:
                config = pw.load_yaml(f)
            
            # Create enhanced server
            logger.info("🚀 Starting enhanced document processing pipeline...")
            logger.info("📡 REST API server starting on http://0.0.0.0:8001")
            logger.info("🔍 Ready to process pharmaceutical regulatory documents with enhanced prompts")
            
            # Enhanced API endpoints info
            logger.info("💡 Enhanced API Endpoints:")
            logger.info("   POST /v1/pw_ai_answer           - Enhanced LLM queries with system prompt")
            logger.info("   POST /v1/pw_list_documents      - List indexed documents")
            logger.info("   POST /v1/retrieve               - Vector search") 
            
            # Patch the question answerer to use enhanced prompts
            original_qa = config["question_answerer"]
            
            # Create a wrapper that enhances prompts
            class EnhancedQuestionAnswerer:
                def __init__(self, original_qa, prompt_enhancer):
                    self.original_qa = original_qa
                    self.enhance_prompt = prompt_enhancer
                
                def __call__(self, query, **kwargs):
                    enhanced_query = self.enhance_prompt(query)
                    return self.original_qa(enhanced_query, **kwargs)
                
                def __getattr__(self, name):
                    return getattr(self.original_qa, name)
            
            enhanced_qa = EnhancedQuestionAnswerer(original_qa, self.enhance_prompt)
            
            # Create and start the enhanced Pathway server
            from pathway.xpacks.llm.servers import QASummaryRestServer
            
            server = QASummaryRestServer(
                host=config.get("host", "0.0.0.0"),
                port=8001,  # Force port 8001 for enhanced version
                rag_question_answerer=enhanced_qa
            )
            
            # Run the enhanced server
            server.run(
                with_cache=True,
                terminate_on_error=False,
                cache_backend=pw.persistence.Backend.filesystem("Cache_Enhanced"),
            )
            
        except FileNotFoundError:
            logger.error(f"❌ Configuration file not found: {self.config_path}")
            logger.info("💡 Using original configuration as template...")
            # Copy the original config and modify port
            self.create_enhanced_config()
            
        except Exception as e:
            logger.error(f"❌ Error starting enhanced application: {e}")
            
            # Check for common issues
            if "api_key" in str(e).lower():
                logger.info("🔑 API Key Issue Detected:")
                logger.info("1. Get OpenRouter API key: https://openrouter.ai/keys")
                logger.info("2. Set OPENROUTER_API_KEY in .env file")
                logger.info("3. Verify OPENROUTER_API_BASE is set correctly")
            
            elif "connection" in str(e).lower():
                logger.info("🌐 Connection Issue Detected:")
                logger.info("1. Check internet connection")
                logger.info("2. Verify OpenRouter API base URL")
                logger.info("3. Test with: curl https://openrouter.ai/api/v1/models")
            
            raise

    def create_enhanced_config(self):
        """Create enhanced configuration file based on original"""
        try:
            # Read original config
            with open("app_openrouter.yaml", 'r') as f:
                original_config = f.read()
            
            # Modify port and max_tokens for enhanced version
            enhanced_config = original_config.replace('port: 8000', 'port: 8001')
            enhanced_config = enhanced_config.replace('max_tokens: 500', 'max_tokens: 1000')
            
            # Write enhanced config
            with open(self.config_path, 'w') as f:
                f.write(enhanced_config)
                
            logger.info(f"✅ Enhanced configuration created: {self.config_path}")
            logger.info("🔄 Restarting with enhanced configuration...")
            
            # Recursive call with the new config
            self.run()
            
        except Exception as e:
            logger.error(f"❌ Could not create enhanced config: {e}")
            raise

def main():
    """Main entry point for enhanced version"""
    print("🧬 Enhanced Pharmaceutical Compliance RAG System")
    print("🔗 Powered by OpenRouter + Pathway AI (Enhanced)")
    print("🔌 Running on Port 8001 with System Prompt")
    print("="*60)
    
    app = EnhancedPharmaComplianceApp()
    app.run()

if __name__ == "__main__":
    main()