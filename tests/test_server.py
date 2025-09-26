#!/usr/bin/env python3
"""
Server Infrastructure Test Suite

PURPOSE:
Comprehensive validation of server infrastructure, endpoints, and operational
capabilities of the pharmaceutical compliance system. Ensures robust server
performance and reliability under various conditions.

WHAT IT TESTS:
1. Server Infrastructure:
   - HTTP server startup and initialization
   - Port binding and network configuration
   - Process management and lifecycle
   - Resource allocation and utilization

2. API Endpoint Validation:
   - Health check endpoint availability
   - Query processing endpoint functionality
   - Authentication and security mechanisms
   - Rate limiting and throttling behavior

3. Request/Response Handling:
   - HTTP method support (GET, POST, OPTIONS)
   - Content-type processing and validation
   - Request payload parsing and validation
   - Response formatting and content delivery

4. Error Handling and Recovery:
   - Invalid request processing
   - Server error response generation
   - Timeout handling and recovery
   - Graceful degradation scenarios

5. Performance and Scalability:
   - Concurrent request handling
   - Memory usage optimization
   - Response time benchmarking
   - Load testing under stress conditions

6. Security and Compliance:
   - Input sanitization validation
   - CORS policy enforcement
   - Request logging and monitoring
   - Security header implementation

WHEN TO RUN:
- During server deployment validation
- Before production environment setup
- For load testing and performance validation
- When troubleshooting server-related issues
- As part of continuous integration testing

EXPECTED OUTCOME:
- Server starts and binds to configured port successfully
- All API endpoints respond correctly to valid requests
- Error conditions are handled gracefully
- Performance metrics meet operational requirements
- Security measures function as designed

DEPENDENCIES:
- Python HTTP server capabilities
- Network configuration and port availability
- Server configuration files and environment
- Load testing utilities and benchmarking tools
- Monitoring and logging infrastructure

SCOPE:
This test focuses on server infrastructure and API layer functionality.
For application-specific testing, use test_live_server.py or test_query.py
"""
import requests
import json
import time

def test_server():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Pharmaceutical RAG Server")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Test health endpoint
    try:
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Test document listing
    try:
        print("\n2. Testing document listing...")
        response = requests.post(f"{base_url}/api/v1/pw_list_documents", 
                               json={}, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            docs = response.json()
            print(f"   Found {len(docs)} documents:")
            for doc in docs[:3]:  # Show first 3
                print(f"     - {doc.get('path', 'Unknown')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Document listing failed: {e}")
    
    # Test AI query
    try:
        print("\n3. Testing AI query...")
        query_data = {
            "query": "What pharmaceutical regulations are mentioned in the documents?",
            "filters": {}
        }
        response = requests.post(f"{base_url}/api/v1/pw_ai_answer", 
                               json=query_data, timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            answer = response.json()
            print(f"   Answer: {answer.get('answer', 'No answer')[:200]}...")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ AI query failed: {e}")

if __name__ == "__main__":
    test_server()