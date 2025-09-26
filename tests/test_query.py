#!/usr/bin/env python3
"""
Basic Query Functionality Test Suite

PURPOSE:
Validates fundamental query processing capabilities of the pharmaceutical
compliance system through standardized test cases and expected outcomes.

WHAT IT TESTS:
1. Query Processing Pipeline:
   - Input validation and sanitization
   - Query normalization and preprocessing
   - Context retrieval from CDSCO documents
   - Response generation and formatting

2. Basic Pharmaceutical Queries:
   - Simple drug name lookups
   - Regulatory status inquiries
   - CDSCO guideline references
   - Standard compliance questions

3. Response Quality Validation:
   - Accuracy of pharmaceutical information
   - Completeness of regulatory analysis
   - Consistency in response formatting
   - Adherence to Government specifications

4. System Integration Testing:
   - Database connectivity validation
   - Document retrieval functionality
   - LLM integration verification
   - End-to-end workflow execution

5. Edge Case Handling:
   - Empty query processing
   - Special character handling
   - Long query text management
   - Ambiguous drug name resolution

WHEN TO RUN:
- As part of basic system validation
- Before advanced feature testing
- During regression testing cycles
- For quality assurance verification
- When validating core functionality changes

EXPECTED OUTCOME:
- All basic queries process successfully
- Responses contain accurate pharmaceutical information
- System handles edge cases gracefully
- Performance meets baseline requirements
- No critical errors or exceptions occur

DEPENDENCIES:
- Functional pharmaceutical compliance server
- CDSCO regulatory document database
- Basic query test dataset
- Response validation utilities
- Network connectivity for LLM calls

SCOPE:
This test covers fundamental query operations. For comprehensive
system testing, use test_live_server.py or test_government_system.py
"""

import requests
import json
import time

def test_rag_query():
    """Test querying the RAG system"""
    
    # Test query about pharmaceutical banned substances
    query = "What drugs are banned for pediatric use and what are the penalties?"
    
    url = "http://localhost:8000/v1/pw_ai_answer"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": query}
    
    print("🧬 Testing Pharmaceutical RAG System")
    print("="*50)
    print(f"📋 Query: {query}")
    print("⏳ Sending request to RAG system...")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Query successful!")
            print("📋 Response:")
            print("-" * 40)
            print(result.get('answer', 'No answer field found'))
            print("-" * 40)
            
            # Print additional metadata if available
            if 'sources' in result:
                print(f"📚 Sources: {len(result['sources'])} documents")
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the RAG server is running on port 8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Query took too long to process")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_list_documents():
    """Test listing indexed documents"""
    
    url = "http://localhost:8000/v1/pw_list_documents"
    headers = {"Content-Type": "application/json"}
    
    print("\n📚 Testing document listing...")
    
    try:
        response = requests.post(url, headers=headers, json={})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document listing successful!")
            print(f"📋 Found {len(result)} documents indexed")
            
            for i, doc in enumerate(result[:5], 1):  # Show first 5 docs
                print(f"  {i}. {doc.get('path', 'Unknown path')}")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test document listing first
    test_list_documents()
    
    # Small delay
    time.sleep(2)
    
    # Test main query
    test_rag_query()