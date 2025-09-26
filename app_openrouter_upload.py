#!/usr/bin/env python3
"""
Enhanced Pharmaceutical Compliance RAG System with File Upload
Real-time drug ban detection and regulatory monitoring
"""

import os
import pathway as pw
from dotenv import load_dotenv
import logging
from pathlib import Path
import shutil
from aiohttp import web
import aiofiles
import threading
import time

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
        self.data_dir = Path("./data")
        self.data_dir.mkdir(exist_ok=True)
        self.validate_environment()
        
    def validate_environment(self):
        """Validate required environment variables"""
        required_vars = ["OPENROUTER_API_KEY", "OPENROUTER_API_BASE"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"❌ Missing environment variables: {missing_vars}")
            logger.info("📝 Please set these variables in your .env file:")
            for var in missing_vars:
                logger.info(f"   {var}=your_value_here")
            raise EnvironmentError(f"Missing required environment variables: {missing_vars}")
        
        logger.info("✅ OpenRouter configuration validated")

    def setup_pharmaceutical_context(self):
        """Setup pharmaceutical domain-specific context"""
        pharma_context = """
        🧬 PHARMACEUTICAL COMPLIANCE SYSTEM INITIALIZED
        
        Domain Focus Areas:
        • Drug ban notifications and regulatory changes
        • CDSCO guidelines and compliance requirements  
        • Pharmaceutical manufacturing standards
        • Clinical trial regulations
        • Import/export restrictions
        • Quality control and safety protocols
        • Penalty structures for violations
        • Licensing and registration processes
        
        Document Processing Optimized For:
        📋 Gazette notifications
        📋 CDSCO circulars
        📋 Drug ban lists
        📋 Manufacturing guidelines
        📋 Safety alerts
        📋 Regulatory updates
        """
        logger.info("🔬 Pharmaceutical domain context activated")

    async def upload_handler(self, request):
        """Handle file upload requests"""
        try:
            reader = await request.multipart()
            
            while True:
                part = await reader.next()
                if part is None:
                    break
                    
                if part.name == 'file':
                    filename = part.filename
                    if not filename:
                        return web.json_response(
                            {"error": "No filename provided"}, 
                            status=400
                        )
                    
                    # Validate file type
                    allowed_extensions = {'.pdf', '.txt', '.doc', '.docx'}
                    file_ext = Path(filename).suffix.lower()
                    if file_ext not in allowed_extensions:
                        return web.json_response(
                            {"error": f"File type {file_ext} not supported. Allowed: {list(allowed_extensions)}"}, 
                            status=400
                        )
                    
                    # Save file to data directory
                    file_path = self.data_dir / filename
                    
                    async with aiofiles.open(file_path, 'wb') as f:
                        while True:
                            chunk = await part.read_chunk(8192)
                            if not chunk:
                                break
                            await f.write(chunk)
                    
                    file_size = file_path.stat().st_size
                    logger.info(f"📄 File uploaded successfully: {filename} ({file_size} bytes)")
                    
                    return web.json_response({
                        "message": "File uploaded and queued for RAG indexing",
                        "filename": filename,
                        "size": file_size,
                        "path": str(file_path),
                        "status": "Processing - will be available for queries in ~30 seconds"
                    })
            
            return web.json_response({"error": "No file found in request"}, status=400)
            
        except Exception as e:
            logger.error(f"❌ Upload error: {e}")
            return web.json_response({"error": str(e)}, status=500)

    async def health_handler(self, request):
        """Enhanced health check endpoint"""
        try:
            file_count = len(list(self.data_dir.glob("*")))
            return web.json_response({
                "status": "healthy",
                "service": "Pharmaceutical RAG System with Upload",
                "data_directory": str(self.data_dir),
                "indexed_files": file_count,
                "upload_endpoint": "/v1/upload",
                "query_endpoint": "/v1/pw_ai_answer",
                "supported_formats": [".pdf", ".txt", ".doc", ".docx"]
            })
        except Exception as e:
            return web.json_response({
                "status": "error",
                "error": str(e)
            }, status=500)

    def create_upload_server(self):
        """Create aiohttp server with upload and health endpoints"""
        app = web.Application()
        app.router.add_post('/v1/upload', self.upload_handler)
        app.router.add_get('/v1/health', self.health_handler)
        return app

    def run_upload_server(self):
        """Run upload server on port 8001"""
        upload_app = self.create_upload_server()
        logger.info("🎯 Upload server starting on http://0.0.0.0:8001")
        web.run_app(upload_app, host="0.0.0.0", port=8001)

    def run(self):
        """Run the pharmaceutical compliance RAG system"""
        try:
            logger.info("🧬 Starting Pharmaceutical Compliance RAG System...")
            logger.info("📊 Configuration: OpenRouter LLM + File Upload + Local Embeddings")
            
            # Setup pharmaceutical context
            self.setup_pharmaceutical_context()
            
            # Load Pathway configuration
            logger.info(f"📋 Loading configuration from {self.config_path}")
            
            with open(self.config_path) as f:
                config = pw.load_yaml(f)
            
            # Start upload server in background thread
            upload_thread = threading.Thread(target=self.run_upload_server, daemon=True)
            upload_thread.start()
            
            logger.info("🚀 Starting document processing pipeline...")
            logger.info("📡 Main RAG server starting on http://0.0.0.0:8000")
            logger.info("🎯 Upload server running on http://0.0.0.0:8001")
            logger.info("🔍 Ready to process pharmaceutical regulatory documents")
            
            # Enhanced API endpoints info
            logger.info("💡 API Endpoints:")
            logger.info("   GET  http://localhost:8001/v1/health    - System health & file stats")
            logger.info("   POST http://localhost:8001/v1/upload    - Upload PDF/TXT files")
            logger.info("   POST http://localhost:8000/v1/pw_ai_answer - LLM-powered queries")
            logger.info("   POST http://localhost:8000/v1/pw_list_documents - List documents")
            
            # Create and start the main Pathway server
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
            return False
        except Exception as e:
            logger.error(f"❌ Error starting application: {e}")
            raise

def main():
    """Main entry point"""
    print("🧬 Pharmaceutical Compliance RAG System")
    print("🔗 Powered by OpenRouter + Pathway AI + File Upload")
    print("="*60)
    
    app = PharmaComplianceApp()
    app.run()

if __name__ == "__main__":
    main()