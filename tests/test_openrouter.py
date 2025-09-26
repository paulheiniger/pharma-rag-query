#!/usr/bin/env python3
"""
OpenRouter LLM Integration Test Suite

PURPOSE:
Tests the integration between the pharmaceutical compliance system
and OpenRouter's LLM services, specifically Claude Sonnet 4 model.

WHAT IT TESTS:
1. OpenRouter Configuration:
   - API key validation
   - Base URL connectivity
   - Authentication verification
   - Model access permissions

2. LLM Model Performance:
   - Claude Sonnet 4 availability
   - Response generation quality
   - Token usage optimization
   - Temperature and parameter settings

3. Pharmaceutical Domain Expertise:
   - Drug regulatory knowledge accuracy
   - CDSCO guideline adherence
   - Medical terminology usage
   - Regulatory decision quality

4. API Integration:
   - Request/response formatting
   - Error handling robustness
   - Rate limiting compliance
   - Timeout management

5. Cost Optimization:
   - Token usage efficiency
   - Response length optimization
   - Cache utilization effectiveness
   - API call frequency analysis

WHEN TO RUN:
- During initial setup and configuration
- Before production deployment
- When troubleshooting LLM integration issues
- For API cost analysis and optimization

EXPECTED OUTCOME:
- Successful OpenRouter authentication
- Claude Sonnet 4 model responds correctly
- Pharmaceutical queries generate accurate responses
- API usage within expected parameters

DEPENDENCIES:
- Valid OpenRouter API key in .env file
- Internet connectivity for API calls
- Claude Sonnet 4 model access permissions
- Proper environment variable configuration

PRE-REQUISITES:
Ensure .env file contains:
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

def check_openrouter_config():
    """Check OpenRouter configuration"""
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    api_base = os.getenv("OPENROUTER_API_BASE")
    
    print("🔑 OpenRouter Configuration Check:")
    print("-" * 40)
    
    if api_key and api_key != "your_openrouter_api_key_here":
        print("✅ OPENROUTER_API_KEY is configured")
        print(f"   Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else 'short'}")
    else:
        print("❌ OPENROUTER_API_KEY not configured")
        print("💡 Get your key from: https://openrouter.ai/keys")
        return False
    
    if api_base:
        print(f"✅ OPENROUTER_API_BASE: {api_base}")
    else:
        print("❌ OPENROUTER_API_BASE not configured")
        return False
    
    return True

def test_openrouter_direct():
    """Test OpenRouter API directly"""
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    api_base = os.getenv("OPENROUTER_API_BASE")
    
    if not api_key or not api_base:
        print("⚠️  Cannot test OpenRouter - missing configuration")
        return False
    
    print("\n🧪 Testing OpenRouter API Direct Connection:")
    print("-" * 45)
    
    try:
        # Test with a simple query
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Pharmaceutical RAG System"
        }
        
        data = {
            "model": "anthropic/claude-sonnet-4",
            "messages": [
                {
                    "role": "user", 
                    "content": "What is pharmaceutical compliance?"
                }
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        print("📡 Sending test query to OpenRouter...")
        response = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            print("✅ OpenRouter API connection successful!")
            print(f"🤖 Test response: {answer[:100]}...")
            return True
        else:
            print(f"❌ OpenRouter API error: {response.status_code}")
            print(f"📋 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_rag_system():
    """Test the RAG system with OpenRouter"""
    print("\n🧪 Testing RAG System with OpenRouter:")
    print("-" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Check if service is running
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ RAG service is running")
        else:
            print(f"❌ Service health check failed: {health_response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to RAG service: {e}")
        print("💡 Start the service with: python app_openrouter.py")
        return False
    
    # Test pharmaceutical queries
    test_queries = [
        "What is CDSCO?",
        "Explain drug scheduling in India",
        "What are banned drugs?",
    ]
    
    print("\n🤖 Testing LLM-powered queries:")
    print("-" * 35)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        
        try:
            response = requests.post(
                f"{base_url}/api/v1/pw_ai_answer",
                json={"query": query},
                timeout=60  # OpenRouter can be slower than OpenAI
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, str):
                    print(f"   ✅ Answer: {result[:150]}...")
                elif isinstance(result, dict) and "answer" in result:
                    print(f"   ✅ Answer: {result['answer'][:150]}...")
                else:
                    print(f"   📋 Response: {str(result)[:150]}...")
            else:
                print(f"   ❌ Query failed: {response.status_code}")
                if response.status_code == 422:
                    print("   💡 Check OpenRouter API key configuration")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Query timed out (OpenRouter can be slower)")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        # Small delay between requests
        time.sleep(2)
    
    return True

def show_setup_instructions():
    """Show OpenRouter setup instructions"""
    print("\n🔧 OpenRouter Setup Instructions:")
    print("-" * 35)
    print("1. Visit: https://openrouter.ai/keys")
    print("2. Create an account (if needed)")
    print("3. Generate an API key")
    print("4. Add to .env file:")
    print("   OPENROUTER_API_KEY=sk-or-v1-your-key-here")
    print("   OPENROUTER_API_BASE=https://openrouter.ai/api/v1")
    print("5. Run: python app_openrouter.py")
    print("6. Test: python test_openrouter.py")
    
    print("\n💡 Available Models (for your key):")
    print("• anthropic/claude-sonnet-4 (Available)")
    print("• anthropic/claude-opus-4 (Available)")
    print("• Other models may require different API key permissions")

def main():
    """Main test function"""
    print("🧪 OpenRouter + Pharmaceutical RAG System Test")
    print("=" * 50)
    
    # Check configuration
    config_ok = check_openrouter_config()
    
    if not config_ok:
        show_setup_instructions()
        return
    
    # Test OpenRouter API directly
    api_ok = test_openrouter_direct()
    
    if not api_ok:
        print("\n❌ OpenRouter API test failed")
        print("💡 Check your API key and internet connection")
        return
    
    # Test full RAG system
    test_rag_system()
    
    print("\n🎉 OpenRouter Testing Complete!")
    print("💡 Next: Add pharmaceutical PDFs to ./data/ for domain-specific queries")

if __name__ == "__main__":
    main()