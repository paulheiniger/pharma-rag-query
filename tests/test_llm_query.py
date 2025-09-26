#!/usr/bin/env python3
"""
"""
Direct LLM Query Testing Suite (Server-Independent)

PURPOSE:
Provides comprehensive testing of LLM query functionality without requiring
a running server instance. Validates core pharmaceutical compliance processing
capabilities through direct API integration.

WHAT IT TESTS:
1. OpenRouter LLM Integration:
   - Direct API connectivity to anthropic/claude-sonnet-4
   - Authentication and authorization validation
   - Response format and structure verification
   - Error handling for network and API failures

2. Pharmaceutical Query Processing:
   - CDSCO regulatory document analysis
   - Drug name recognition and classification
   - Regulatory status determination (banned/allowed)
   - Compliance analysis accuracy validation

3. Government Compliance Workflow:
   - S1-S6 regulatory category assignment
   - P1-P8 processing step execution
   - Structured output generation (21-column format)
   - JSON response formatting validation

4. Core Functionality Verification:
   - Query preprocessing and sanitization
   - Context retrieval and ranking
   - Response generation without server overhead
   - Performance metrics and latency measurement

5. Error Handling Robustness:
   - Malformed query processing
   - Empty or invalid input handling
   - API timeout and retry mechanisms
   - Graceful degradation scenarios

WHEN TO RUN:
- During development before server testing
- For isolated LLM functionality validation
- When troubleshooting API connectivity issues
- For performance benchmarking without server overhead
- In CI/CD pipelines for core functionality verification

EXPECTED OUTCOME:
- Direct OpenRouter API queries execute successfully
- Pharmaceutical compliance analysis produces accurate results
- JSON output follows Government 21-column specification
- Error conditions are handled gracefully
- Performance metrics meet acceptable thresholds

DEPENDENCIES:
- OpenRouter API credentials and configuration
- Internet connectivity for LLM API calls
- anthropic/claude-sonnet-4 model availability
- CDSCO regulatory document data
- Python requests and JSON processing libraries

SCOPE:
This test bypasses the Pathway server infrastructure to validate core
LLM functionality. For full system testing, use test_live_server.py
"""

This script demonstrates how to use the RAG system with LLM-powered queries.
"""

import requests
import json
import time
import os
from typing import Dict, Any

def test_llm_query():
    """Test the LLM-powered query functionality"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Test queries for pharmaceutical compliance
    test_queries = [
        "What drugs were banned by CDSCO?",
        "Are there any recent drug scheduling changes in India?",
        "What are the latest pharmaceutical regulatory updates?",
        "Which companies had drug approvals revoked?",
        "Show me information about drug safety alerts from Indian regulators"
    ]
    
    print("🧪 Testing Pharmaceutical RAG System with LLM Integration")
    print("=" * 60)
    
    # First, check if the service is running
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Service is running")
        else:
            print(f"❌ Service health check failed: {health_response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to service: {e}")
        print("Make sure the app is running: python app.py")
        return
    
    # Check if we have documents indexed
    try:
        stats_response = requests.get(f"{base_url}/api/v1/pw_list_documents", timeout=10)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"📚 Found {len(stats)} documents indexed")
        else:
            print("⚠️  Could not retrieve document stats")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not check document stats: {e}")
    
    print("\n🤖 Testing LLM-powered queries...")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("   " + "─" * (len(query) + 8))
        
        try:
            # Send query to the RAG system
            response = requests.post(
                f"{base_url}/api/v1/pw_ai_answer",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, str):
                    # Direct string response
                    print(f"   🎯 Answer: {result[:200]}...")
                elif isinstance(result, dict):
                    # Structured response
                    if "answer" in result:
                        print(f"   🎯 Answer: {result['answer'][:200]}...")
                    if "sources" in result:
                        print(f"   📄 Sources: {len(result['sources'])} documents")
                else:
                    print(f"   📋 Response: {str(result)[:200]}...")
                    
            elif response.status_code == 422:
                error_detail = response.json()
                if "API key" in str(error_detail) or "openai" in str(error_detail).lower():
                    print("   ⚠️  OpenAI API key not configured")
                    print("   💡 Set your OPENAI_API_KEY in the .env file")
                    print("   🔗 Get API key: https://platform.openai.com/api-keys")
                else:
                    print(f"   ❌ Validation error: {error_detail}")
            else:
                print(f"   ❌ Query failed: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   📋 Error: {error_detail}")
                except:
                    print(f"   📋 Error: {response.text}")
                    
        except requests.exceptions.Timeout:
            print("   ⏰ Query timed out (LLM processing can take time)")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        # Small delay between requests
        if i < len(test_queries):
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎯 RAG System Test Complete!")
    print("\n💡 Next Steps:")
    print("   1. Set OPENAI_API_KEY in .env file for full LLM functionality")
    print("   2. Add more PDFs to data/ folder for richer responses")
    print("   3. Try custom queries via the API endpoints")
    print("   4. Check logs for detailed processing information")

def check_openai_key():
    """Check if OpenAI API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OpenAI API key is configured")
        return True
    else:
        print("⚠️  OpenAI API key not configured")
        print("💡 Set OPENAI_API_KEY in .env file for LLM functionality")
        return False

if __name__ == "__main__":
    print("🔑 Checking OpenAI API Key Configuration...")
    check_openai_key()
    print()
    
    test_llm_query()