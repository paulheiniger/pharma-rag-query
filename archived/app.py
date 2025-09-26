"""
Pharmaceutical Compliance RAG Application

This application provides real-time indexing and querying of pharmaceutical regulatory documents,
specifically designed to monitor drug bans, scheduling changes, and compliance requirements from
the Gazette of India and other regulatory sources.

Features:
- Real-time document ingestion and indexing
- Vector similarity search for regulatory queries
- REST API endpoints for document retrieval
- Specialized parsing for pharmaceutical documents
- Live monitoring of regulatory changes

API Endpoints:
- POST /v1/retrieve: Query documents with similarity search
- GET /v1/statistics: Get indexing statistics
- GET /v1/inputs: List all indexed documents
"""

import logging
import pathway as pw
from dotenv import load_dotenv
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.xpacks.llm.servers import DocumentStoreServer
from pydantic import BaseModel, ConfigDict, InstanceOf

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Set Pathway license key (demo key for testing)
pw.set_license_key("demo-license-key-with-telemetry")

class PharmaComplianceApp(BaseModel):
    """
    Main application class for the Pharmaceutical Compliance RAG system.
    
    This class orchestrates the document indexing pipeline and provides
    REST API endpoints for querying pharmaceutical regulatory documents.
    """
    
    document_store: InstanceOf[DocumentStore]
    host: str = "0.0.0.0"
    port: int = 8000
    with_cache: bool = True
    terminate_on_error: bool = False

    model_config = ConfigDict(extra="forbid")
        
    def run(self):
        """
        Start the pharmaceutical compliance document indexing service.
        
        This method loads the configuration and starts the document store server
        with specialized endpoints for pharmaceutical document queries.
        """
        print("🏥 Starting Pharmaceutical Compliance RAG Application...")
        print(f"📊 Server will be available at http://{self.host}:{self.port}")
        print("🔍 API Endpoints:")
        print("   POST /v1/retrieve - Query pharmaceutical documents")
        print("   GET /v1/statistics - View indexing statistics")
        print("   GET /v1/inputs - List indexed documents")
        print("📁 Monitoring regulatory documents in ./data directory")
        print("=" * 60)
        
        # Start the document store server
        server = DocumentStoreServer(self.host, self.port, self.document_store)
        server.run(
            with_cache=self.with_cache,
            terminate_on_error=self.terminate_on_error,
        )

def main():
    """Main entry point for the pharmaceutical compliance RAG application."""
    with open("app.yaml") as f:
        config = pw.load_yaml(f)
    app = PharmaComplianceApp(**config)
    app.run()

if __name__ == "__main__":
    main()