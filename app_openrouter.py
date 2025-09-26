#!/usr/bin/env python3
"""
Pharmaceutical Compliance RAG System with OpenRouter
Real-time drug ban detection and regulatory monitoring
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

class PharmaComplianceApp:
    def __init__(self, config_path="app_openrouter.yaml"):
        """Initialize the pharmaceutical compliance RAG application"""
        # Load environment variables
        load_dotenv()
        
        self.config_path = config_path
        self.validate_environment()
        
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
        os.environ.setdefault("PATHWAY_REGULATORY_FOCUS", "drug_bans,scheduling,compliance")
        
    def run(self):
        """Run the pharmaceutical compliance RAG system with upload capabilities"""
        try:
            logger.info("🧬 Starting Pharmaceutical Compliance RAG System...")
            logger.info("📊 Configuration: OpenRouter LLM with local embeddings + File Upload")
            
            # Setup pharmaceutical context
            self.setup_pharmaceutical_context()
            
            # Load and run the Pathway configuration
            logger.info(f"📋 Loading configuration from {self.config_path}")
            
            with open(self.config_path) as f:
                config = pw.load_yaml(f)
            
            # Create enhanced server with upload capabilities
            logger.info("🚀 Starting document processing pipeline...")
            logger.info("📡 REST API server starting on http://0.0.0.0:8000")
            logger.info("🔍 Ready to process pharmaceutical regulatory documents")
            
            # Standard API endpoints info
            logger.info("💡 API Endpoints:")
            logger.info("   POST /v1/pw_ai_answer           - LLM-powered queries")
            logger.info("   POST /v1/pw_list_documents      - List indexed documents")
            logger.info("   POST /v1/retrieve               - Vector search") 
            
            # Create and start the standard Pathway server
            from pathway.xpacks.llm.servers import QASummaryRestServer
            
            server = QASummaryRestServer(
                host=config.get("host", "0.0.0.0"),
                port=config.get("port", 8000),
                rag_question_answerer=config["question_answerer"]
            )
            
            # Run the main server
            server.run(
                with_cache=True,
                terminate_on_error=False,
                cache_backend=pw.persistence.Backend.filesystem("Cache"),
            )
            
        except FileNotFoundError:
            logger.error(f"❌ Configuration file not found: {self.config_path}")
            logger.info("💡 Available configurations:")
            logger.info("   - app_openrouter.yaml (OpenRouter LLM)")
            logger.info("   - app_no_llm.yaml (Document processing only)")
            
        except Exception as e:
            logger.error(f"❌ Error starting application: {e}")
            
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

def main():
    """Main entry point"""
    print("🧬 Pharmaceutical Compliance RAG System")
    print("🔗 Powered by OpenRouter + Pathway AI")
    print("="*50)
    
    app = PharmaComplianceApp()
    app.run()

if __name__ == "__main__":
    main()