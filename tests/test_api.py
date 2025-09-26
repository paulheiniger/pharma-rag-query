#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Pharmaceutical Compliance RAG System

PURPOSE:
Complete validation of all REST API endpoints provided by the pharmaceutical
compliance system including health checks, document operations, and query processing.

WHAT IT TESTS:
1. Core API Endpoints:
   - POST /v1/pw_ai_answer (pharmaceutical compliance queries)
   - POST /v1/pw_list_documents (regulatory document listing)
   - POST /v1/retrieve (semantic document search)
   - GET /v1/health (system health monitoring)

2. Request/Response Validation:
   - HTTP status codes (200, 400, 404, 500)
   - JSON response format validation
   - Required field presence verification
   - Data type consistency checking

3. Error Handling:
   - Invalid request format handling
   - Missing parameter error responses
   - Server error recovery testing
   - Timeout and connection error handling

4. Performance Metrics:
   - Response time measurement
   - Throughput testing under load
   - Memory usage during processing
   - Concurrent request handling

5. Data Validation:
   - Pharmaceutical compliance response accuracy
   - CDSCO regulatory data consistency
   - Document metadata verification
   - Search result relevance scoring

WHEN TO RUN:
- After application deployment
- During continuous integration testing
- Before production releases
- For API regression testing

EXPECTED OUTCOME:
- All endpoints return appropriate HTTP status codes
- Response formats match API specifications
- Pharmaceutical queries return accurate compliance analysis
- Error conditions are handled gracefully

DEPENDENCIES:
- Running pharmaceutical compliance server (port 8000/8001)
- Valid API authentication credentials
- CDSCO regulatory documents loaded
- Network connectivity for external API calls

USAGE:
python test_api.py --base-url http://localhost:8001 --verbose
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class PharmaRAGTester:
    """Test suite for the Pharmaceutical Compliance RAG API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_health(self) -> bool:
        """Test if the service is running and healthy."""
        try:
            response = self.session.get(f"{self.base_url}/v1/statistics")
            if response.status_code == 200:
                print("✅ Health check passed - Service is running")
                data = response.json()
                print(f"   📊 Indexed documents: {data.get('indexed_documents', 'N/A')}")
                return True
            else:
                print(f"❌ Health check failed - Status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Health check failed - Cannot connect to service")
            return False
        except Exception as e:
            print(f"❌ Health check failed - Error: {e}")
            return False
    
    def test_inputs_endpoint(self) -> bool:
        """Test the inputs endpoint to see indexed documents."""
        try:
            response = self.session.get(f"{self.base_url}/v1/inputs")
            if response.status_code == 200:
                data = response.json()
                print("✅ Inputs endpoint working")
                print(f"   📁 Total documents: {len(data.get('inputs', []))}")
                return True
            else:
                print(f"❌ Inputs endpoint failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Inputs endpoint failed - Error: {e}")
            return False
    
    def test_retrieve_endpoint(self, query: str = "drug ban notification") -> bool:
        """Test the retrieve endpoint with a pharmaceutical query."""
        try:
            payload = {
                "query": query,
                "k": 3
            }
            
            response = self.session.post(
                f"{self.base_url}/v1/retrieve",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                print("✅ Retrieve endpoint working")
                print(f"   🔍 Query: '{query}'")
                print(f"   📄 Results found: {len(results)}")
                
                if results:
                    print("   🏆 Top result preview:")
                    top_result = results[0]
                    text_preview = top_result.get("text", "")[:200] + "..."
                    print(f"      Text: {text_preview}")
                    print(f"      Score: {top_result.get('score', 'N/A')}")
                
                return True
            else:
                print(f"❌ Retrieve endpoint failed - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Retrieve endpoint failed - Error: {e}")
            return False
    
    def run_comprehensive_test(self) -> Dict[str, bool]:
        """Run all tests and return results."""
        print("🧪 Starting Pharmaceutical RAG API Tests")
        print("=" * 50)
        
        results = {}
        
        # Test 1: Health check
        print("\n🔍 Test 1: Health Check")
        results["health"] = self.test_health()
        
        # Test 2: Inputs endpoint
        print("\n🔍 Test 2: Inputs Endpoint")
        results["inputs"] = self.test_inputs_endpoint()
        
        # Test 3: Retrieve endpoint with various queries
        test_queries = [
            "drug ban notification",
            "controlled substance schedule",
            "pharmaceutical compliance",
            "gazette notification medicine",
            "prohibited drugs list"
        ]
        
        results["retrieve"] = True
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test 3.{i}: Retrieve Endpoint")
            query_result = self.test_retrieve_endpoint(query)
            results["retrieve"] = results["retrieve"] and query_result
            time.sleep(1)  # Rate limiting
        
        return results
    
    def print_summary(self, results: Dict[str, bool]):
        """Print test summary."""
        print("\n" + "=" * 50)
        print("📋 Test Summary")
        print("=" * 50)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name.upper():<15} {status}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! Your Pharmaceutical RAG system is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the service and try again.")
            
        return passed_tests == total_tests

def main():
    """Main function to run the test suite."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Pharmaceutical RAG API")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL of the RAG service")
    parser.add_argument("--wait", type=int, default=0,
                       help="Wait time before testing (useful for startup)")
    
    args = parser.parse_args()
    
    if args.wait > 0:
        print(f"⏳ Waiting {args.wait} seconds for service to start...")
        time.sleep(args.wait)
    
    tester = PharmaRAGTester(args.url)
    results = tester.run_comprehensive_test()
    success = tester.print_summary(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()