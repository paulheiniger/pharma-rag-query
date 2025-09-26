#!/usr/bin/env python3
"""
Simple file upload server for pharmaceutical RAG system
Handles PDF uploads and saves to data directory for Pathway to process
"""

import os
from aiohttp import web
import aiofiles
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FileUploadServer:
    def __init__(self, data_dir="./data", port=8001):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.port = port

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
        """Health check endpoint"""
        try:
            file_count = len(list(self.data_dir.glob("*")))
            files = [f.name for f in self.data_dir.glob("*") if f.is_file()]
            
            return web.json_response({
                "status": "healthy",
                "service": "Pharmaceutical RAG Upload Server",
                "data_directory": str(self.data_dir),
                "indexed_files": file_count,
                "files": files,
                "upload_endpoint": f"http://localhost:{self.port}/v1/upload",
                "supported_formats": [".pdf", ".txt", ".doc", ".docx"],
                "instructions": {
                    "upload": f"curl -X POST -F 'file=@your_document.pdf' http://localhost:{self.port}/v1/upload",
                    "health": f"curl http://localhost:{self.port}/v1/health"
                }
            })
        except Exception as e:
            return web.json_response({
                "status": "error",
                "error": str(e)
            }, status=500)

    def create_app(self):
        """Create aiohttp application"""
        app = web.Application()
        app.router.add_post('/v1/upload', self.upload_handler)
        app.router.add_get('/v1/health', self.health_handler)
        return app

    def run(self):
        """Run the upload server"""
        app = self.create_app()
        logger.info(f"🎯 Pharmaceutical RAG Upload Server starting on http://0.0.0.0:{self.port}")
        logger.info("📁 Files uploaded here will be automatically processed by the main RAG system")
        logger.info(f"📂 Data directory: {self.data_dir}")
        logger.info("💡 Usage:")
        logger.info(f"   Upload: curl -X POST -F 'file=@document.pdf' http://localhost:{self.port}/v1/upload")
        logger.info(f"   Health: curl http://localhost:{self.port}/v1/health")
        
        web.run_app(app, host="0.0.0.0", port=self.port)

def main():
    """Main entry point"""
    print("🎯 Pharmaceutical RAG Upload Server")
    print("📁 Upload PDF/TXT files for RAG processing")
    print("="*50)
    
    server = FileUploadServer()
    server.run()

if __name__ == "__main__":
    main()