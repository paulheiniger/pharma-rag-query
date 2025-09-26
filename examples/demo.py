#!/usr/bin/env python3
"""
Pharmaceutical Compliance RAG System - Demo Script
Shows both document ingestion and retrieval capabilities
"""

import os
import sys
import time
from pathlib import Path
import pathway as pw
from dotenv import load_dotenv

# Load environment
load_dotenv()

class PharmaRAGDemo:
    def __init__(self):
        self.config_path = "app_no_llm.yaml"
        
    def run_ingestion_demo(self):
        """Run the document ingestion pipeline"""
        print("🧬 Pharmaceutical Compliance RAG System")
        print("="*50)
        print("📊 Starting document ingestion pipeline...")
        
        # Check for documents
        data_dir = Path("./data")
        pdf_files = list(data_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("❌ No PDF files found in ./data/ directory")
            print("📋 Add pharmaceutical regulatory documents to test the system")
            return False
            
        print(f"📚 Found {len(pdf_files)} PDF document(s):")
        for pdf in pdf_files:
            print(f"   • {pdf.name} ({pdf.stat().st_size/1024:.1f} KB)")
        
        try:
            # Run the ingestion pipeline
            print("\n🔄 Processing documents...")
            
            # Load YAML configuration
            with open(self.config_path) as f:
                config = pw.load_yaml(f)
            
            # Run the computation
            pw.run()
            
            print("✅ Document processing complete!")
            print("🔍 Documents are now indexed and searchable")
            return True
            
        except Exception as e:
            print(f"❌ Error during processing: {e}")
            return False
    
    def demonstrate_features(self):
        """Show what the system can do"""
        print("\n🎯 System Capabilities:")
        print("-" * 30)
        print("✓ PDF document ingestion from Gazette of India")
        print("✓ Intelligent text chunking and parsing")  
        print("✓ Vector embeddings for semantic search")
        print("✓ REST API endpoints for integration")
        print("✓ Real-time document updates")
        
        print("\n📡 Available API Endpoints:")
        print("-" * 30)
        print("GET  /health                    - Health check")
        print("POST /api/v1/pw_list_documents  - List indexed documents")  
        print("POST /api/v1/pw_ai_answer       - Query with LLM (requires OpenAI key)")
        print("POST /api/v1/retrieve           - Semantic document retrieval")
        
        print("\n🔑 To Enable LLM Queries:")
        print("-" * 30)
        print("1. Get OpenAI API key: https://platform.openai.com/api-keys")
        print("2. Set OPENAI_API_KEY in .env file")
        print("3. Use app.yaml (full configuration) instead of app_no_llm.yaml")
        print("4. Query: 'What drugs were banned by CDSCO?'")
        
        print("\n🧪 Example Use Cases:")
        print("-" * 30)
        print("• Track drug ban notifications from CDSCO")
        print("• Monitor pharmaceutical scheduling changes")
        print("• Search regulatory compliance documents")
        print("• Alert on new drug safety warnings")
        print("• Analyze regulatory policy changes")

def main():
    demo = PharmaRAGDemo()
    
    # Run document ingestion
    success = demo.run_ingestion_demo()
    
    # Show system capabilities
    demo.demonstrate_features()
    
    if success:
        print("\n🚀 Next Steps:")
        print("1. Test API endpoints with curl or test_api.py")
        print("2. Add more regulatory documents to ./data/")
        print("3. Configure OpenAI API key for LLM queries")
    else:
        print("\n📝 Setup Instructions:")
        print("1. Add PDF documents to ./data/ directory")
        print("2. Run: python demo.py")
        print("3. Check API endpoints at http://localhost:8000")

if __name__ == "__main__":
    main()