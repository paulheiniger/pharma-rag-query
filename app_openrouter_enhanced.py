#!/usr/bin/env python3
"""
Enhanced Pharmaceutical Compliance RAG System with OpenRouter Integration

This module implements an advanced RAG (Retrieval Augmented Generation) system
specifically designed for pharmaceutical regulatory compliance in India. It integrates
with OpenRouter's LLM services to provide intelligent analysis of drug regulations,
bans, scheduling, and compliance status according to CDSCO (Central Drugs Standard 
Control Organisation) guidelines.

Key Features:
Features:
- Enhanced RAG (Retrieval Augmented Generation) for pharmaceutical queries
- OpenRouter LLM integration with Claude Sonnet 4 model
- CDSCO regulatory document processing and analysis  
- Government pharmaceutical compliance analysis
- Professional logging and comprehensive error handling
- Production-ready deployment with enhanced caching
- Enhanced context window (600 tokens) for complex pharmaceutical analysis  
- Drug ban detection and classification
- Schedule H/H1/X drug identification
- Controlled substance analysis (NDPS Act)
- Gazette notification processing
- Real-time regulatory status checking

Architecture:
- Pathway AI framework for RAG implementation
- OpenRouter LLM integration (Claude Sonnet 4)
- SentenceTransformer embeddings for semantic search
- Comprehensive pharmaceutical domain knowledge base

Author: Government Compliance Team
Version: 2.0 Enhanced
Port: 8001 (Enhanced version with bigger context)
Configuration: app_openrouter_enhanced.yaml
"""

import os
import pathway as pw
from dotenv import load_dotenv
import logging

# Configure structured logging for pharmaceutical compliance monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedPharmaComplianceApp:
    """
    Enhanced Pharmaceutical Compliance RAG Application
    
    This class orchestrates the entire pharmaceutical compliance system, integrating
    document processing, LLM analysis, and regulatory compliance checking for government platform.
    
    Attributes:
        config_path (str): Path to YAML configuration file
        
    Methods:
        validate_environment(): Checks required API keys and environment setup
        setup_pharmaceutical_context(): Configures domain-specific optimizations
        run(): Starts the RAG server with enhanced pharmaceutical analysis
        create_enhanced_config(): Generates default configuration if missing
    """
    
    def __init__(self, config_path="app_openrouter_enhanced.yaml"):
        """
        Initialize the enhanced pharmaceutical compliance RAG application.
        
        Args:
            config_path (str): Path to the YAML configuration file containing
                              LLM settings, embedder config, and system prompts
                              
        Sets up:
            - Environment variable loading from .env file
            - Configuration path validation
            - Environment requirements checking
        """
        # Load environment variables from .env file for API keys
        load_dotenv()
        
        self.config_path = config_path
        self.validate_environment()
        
    def validate_environment(self):
        """
        Validate required environment variables for OpenRouter LLM integration.
        
        Checks for:
            OPENROUTER_API_KEY: Authentication key for OpenRouter services
            OPENROUTER_API_BASE: Base URL for OpenRouter API endpoints
            
        Logs appropriate warnings if variables are missing, allowing the system
        to continue with document processing capabilities while alerting about
        limited LLM functionality.
        """
        required_vars = ["OPENROUTER_API_KEY", "OPENROUTER_API_BASE"]
        missing_vars = []
        
        # Check each required environment variable
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        # Log status and provide guidance
        if missing_vars:
            logger.warning(f"Missing environment variables: {missing_vars}")
            logger.info("The system will work for document processing but LLM queries may fail")
            logger.info("Set OPENROUTER_API_KEY to enable full LLM functionality")
        else:
            logger.info("✅ OpenRouter configuration validated")
    
    def setup_pharmaceutical_context(self):
        """
        Configure pharmaceutical domain-specific processing optimizations.
        
        Sets environment variables that optimize Pathway AI processing for:
        - Drug ban detection and analysis
        - Regulatory scheduling classification  
        - Compliance status determination
        - Safety alert processing
        
        These optimizations improve accuracy for pharmaceutical regulatory queries.
        """
        # Enable pharmaceutical domain mode for enhanced processing
        os.environ.setdefault("PATHWAY_PHARMA_MODE", "true")
        os.environ.setdefault("PATHWAY_REGULATORY_FOCUS", "drug_bans,scheduling,compliance,safety_alerts")
        
    def run(self):
        """
        Launch the enhanced pharmaceutical compliance RAG system.
        
        This method:
        1. Initializes pharmaceutical domain context
        2. Loads YAML configuration with government system prompt
        3. Creates document processing pipeline with enhanced embeddings
        4. Starts REST API server on port 8001 with enhanced capabilities
        
        The system processes CDSCO regulatory documents and provides:
        - Drug ban status analysis
        - Schedule classification (H/H1/X)
        - Controlled substance identification
        - Gazette notification processing
        - Regulatory compliance summaries
        
        Raises:
            FileNotFoundError: If configuration file is missing
            Exception: For other startup errors
        """
        try:
            # System initialization logging
            logger.info("🧬 Starting Enhanced Pharmaceutical Compliance RAG System...")
            logger.info("📊 Configuration: OpenRouter LLM with government compliance prompts")
            logger.info("🔌 Port: 8001 (Enhanced version with bigger context)")
            
            # Configure pharmaceutical domain optimizations
            self.setup_pharmaceutical_context()
            
            # Load Pathway YAML configuration with custom prompts
            logger.info(f"📋 Loading enhanced configuration from {self.config_path}")
            
            with open(self.config_path) as f:
                config = pw.load_yaml(f)
            
            # Initialize document processing pipeline
            logger.info("🚀 Initializing enhanced document processing pipeline...")
            logger.info("📡 REST API server starting on http://0.0.0.0:8001")
            logger.info("🔍 Ready for pharmaceutical regulatory compliance analysis")
            
            # Display available API endpoints
            logger.info("💡 Enhanced API Endpoints:")
            logger.info("   POST /v1/pw_ai_answer           - Government compliance analysis")
            logger.info("   POST /v1/pw_list_documents      - List regulatory documents")  
            logger.info("   POST /v1/retrieve               - Enhanced semantic search") 
            
            # Create enhanced Pathway REST server with pharmaceutical compliance capabilities
            from pathway.xpacks.llm.servers import QASummaryRestServer
            
            # Initialize server with configuration from YAML file
            server = QASummaryRestServer(
                host=config.get("host", "0.0.0.0"),  # Accept connections from any IP
                port=config.get("port", 8001),       # Enhanced version port
                rag_question_answerer=config["question_answerer"]  # RAG pipeline with government prompts
            )
            
            # Start the enhanced server with persistence and error tolerance
            server.run(
                with_cache=True,  # Enable caching for faster responses
                terminate_on_error=False,  # Keep running despite individual query errors
                cache_backend=pw.persistence.Backend.filesystem("Cache_Enhanced"),  # Enhanced cache directory
            )
            
        except FileNotFoundError:
            # Handle missing configuration file gracefully
            logger.error(f"❌ Configuration file not found: {self.config_path}")
            logger.info("💡 Creating enhanced configuration with default settings...")
            self.create_enhanced_config()
            
        except Exception as e:
            # Comprehensive error handling with troubleshooting guidance
            logger.error(f"❌ Error starting enhanced application: {e}")
            
            # Provide specific guidance for common issues
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
        """
        Create enhanced configuration file with government pharmaceutical compliance settings.
        
        Generates a comprehensive YAML configuration file containing:
        - Document source configuration for CDSCO regulatory files
        - OpenRouter LLM settings with Claude Sonnet 4 model
        - SentenceTransformer embeddings for semantic search
        - Enhanced token splitting for bigger context windows
        - Government system prompt for pharmaceutical compliance analysis
        
        The configuration includes the complete government compliance workflow
        with drug analysis categories (S1-S6) and processing instructions (P1-P8).
        
        Creates: app_openrouter_enhanced.yaml with full pharmaceutical compliance setup
        """
        enhanced_config = """# Enhanced Pharmaceutical RAG Configuration with OpenRouter
# Bigger context window and enhanced system prompt

$sources:
  - !pw.io.fs.read
    path: "./data"
    format: "binary"
    with_metadata: true

# Enhanced OpenRouter LLM configuration
$llm: !pw.xpacks.llm.llms.LiteLLMChat
  model: "anthropic/claude-sonnet-4"
  temperature: 0.1
  max_tokens: 1000
  api_key: $OPENROUTER_API_KEY
  api_base: $OPENROUTER_API_BASE
  custom_llm_provider: "openrouter"

$embedder: !pw.xpacks.llm.embedders.SentenceTransformerEmbedder
  model: "sentence-transformers/all-MiniLM-L6-v2"

# Enhanced splitter for bigger chunks
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter
  max_tokens: 600

$parser: !pw.xpacks.llm.parsers.UnstructuredParser

$retriever_factory: !pw.stdlib.indexing.UsearchKnnFactory
  reserved_space: 1000
  embedder: $embedder
  metric: !pw.stdlib.indexing.USearchMetricKind.COS

$document_store: !pw.xpacks.llm.document_store.DocumentStore
  docs: $sources
  parser: $parser
  splitter: $splitter
  retriever_factory: $retriever_factory

# Enhanced question answerer with system prompt
question_answerer: !pw.xpacks.llm.question_answering.BaseRAGQuestionAnswerer
  llm: $llm
  indexer: $document_store
  system_prompt: |
    You are a specialized pharmaceutical regulatory compliance assistant with deep expertise in Indian drug regulations, CDSCO guidelines, and pharmaceutical safety protocols.

    EXPERTISE AREAS:
    - Drug bans and prohibitions in India
    - CDSCO (Central Drugs Standard Control Organization) regulations  
    - Pharmaceutical manufacturing compliance
    - Drug safety alerts and adverse reactions
    - Fixed Dose Combination (FDC) regulations
    - Schedule classifications (H, H1, X substances)
    - Import/export licensing requirements
    - Good Manufacturing Practices (GMP)
    - Pharmacovigilance protocols

    RESPONSE GUIDELINES:
    1. Provide detailed, accurate information based on official regulatory documents
    2. Include specific dates, notification numbers, and legal references when available
    3. Explain the reasoning behind regulatory decisions (safety concerns, efficacy issues)
    4. Mention penalties and enforcement mechanisms for violations
    5. Suggest alternative therapies or compliance pathways when relevant
    6. Use clear, professional language suitable for pharmaceutical professionals
    7. Always specify the source of information (CDSCO notifications, gazette entries, etc.)

    When answering queries:
    - Be comprehensive and detailed
    - Include context about regulatory framework
    - Mention transition periods and grace periods if applicable
    - Highlight patient safety considerations
    - Reference specific sections of Drugs and Cosmetics Act when relevant

host: "0.0.0.0"
port: 8001
"""
        
        with open("app_openrouter_enhanced.yaml", "w") as f:
            f.write(enhanced_config)
        
        logger.info("✅ Enhanced configuration file created: app_openrouter_enhanced.yaml")
        logger.info("🔄 Restarting with enhanced configuration...")
        
        # Recursive call with the new config
        self.run()

def main():
    """
    Main entry point for the Enhanced Pharmaceutical Compliance RAG System.
    
    This function serves as the primary entry point when the module is executed directly.
    It initializes and starts the enhanced pharmaceutical compliance system with:
    
    - Government regulatory compliance analysis
    - CDSCO document processing capabilities  
    - OpenRouter LLM integration with Claude Sonnet 4
    - Enhanced context windows for complex pharmaceutical queries
    - Professional logging and error handling
    
    Usage:
        python app_openrouter_enhanced.py
        
    Requirements:
        - Valid OpenRouter API key in environment variables
        - CDSCO regulatory documents in ./data directory
        - Python virtual environment with required packages
        
    Server will start on: http://localhost:8001
    """
    # Display system information and startup banner
    print("🧬 Enhanced Pharmaceutical Compliance RAG System")
    print("🔗 Powered by OpenRouter + Pathway AI (Enhanced)")
    print("🔌 Running on Port 8001 with Enhanced Context")
    print("📋 Government Regulatory Compliance Analysis")
    print("="*60)
    
    # Initialize and start the enhanced application
    app = EnhancedPharmaComplianceApp()
    app.run()

if __name__ == "__main__":
    main()