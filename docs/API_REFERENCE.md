# 🔌 API Reference - Pharmaceutical Compliance RAG System

This document provides comprehensive API documentation for the Government Pharmaceutical Compliance RAG System.

## 🌐 Server Information

### Enhanced Version (Recommended)
- **Base URL**: `http://localhost:8001`
- **Features**: Government compliance analysis, enhanced context windows
- **Configuration**: `app_openrouter_enhanced.yaml`
- **Cache**: `Cache_Enhanced/` directory

### Standard Version  
- **Base URL**: `http://localhost:8000`
- **Features**: Basic pharmaceutical queries
- **Configuration**: `app_openrouter.yaml`  
- **Cache**: `Cache/` directory

## 🔑 Authentication

### Environment Variables Required
```bash
# Set in .env file
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
```

### API Key Validation
```bash
# Test API key validity
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models
```

## 📡 API Endpoints

### 1. POST /v1/pw_ai_answer
**Primary endpoint for pharmaceutical compliance analysis**

#### Description
Provides comprehensive pharmaceutical regulatory compliance analysis using Government-specific prompts and CDSCO regulatory knowledge.

#### Request Format
```http
POST /v1/pw_ai_answer
Content-Type: application/json

{
  "prompt": "Your pharmaceutical compliance query here"
}
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Pharmaceutical compliance query or drug name for analysis |

#### Example Requests

##### Drug Ban Analysis
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Is Tramadol banned in India according to CDSCO regulations?"
  }'
```

##### Schedule Classification Query
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the schedule classification of Alprazolam in India?"
  }'
```

##### Government Compliance Analysis
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze Paracetamol for Government listing compliance"
  }'
```

##### Controlled Substance Check
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Is Morphine a controlled substance under NDPS Act?"
  }'
```

##### Fixed Dose Combination Analysis
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Check if Nimesulide + Paracetamol combination is banned in India"
  }'
```

#### Response Format
```json
{
  "response": "Concise 1-2 line pharmaceutical compliance summary focusing on regulatory status, ban status, scheduling information, and Government listing recommendations."
}
```

#### Example Responses

##### Open Drug (Not Banned)
```json
{
  "response": "paracetamol is an open drug that is widely available and not subject to any regulatory restrictions, making it compliant for listing on government as a safe and commonly used analgesic."
}
```

##### Banned Drug  
```json
{
  "response": "tramadol hydrochloride is banned under cdsco notification gsr 456(e) dated january 15, 2024 and should not be listed on government for retail sale."
}
```

##### Scheduled Drug
```json
{
  "response": "alprazolam is classified as schedule h1 drug requiring prescription and special regulatory compliance, suitable for government listing with prescription requirements clearly mentioned."
}
```

#### Response Time
- **Typical**: 3-8 seconds
- **Enhanced Version**: 5-10 seconds (due to bigger context analysis)
- **Factors**: Document retrieval, LLM processing, regulatory complexity

#### Error Responses

##### Invalid Request Format
```json
{
  "error": "prompt is required",
  "status": 400
}
```

##### API Key Issues  
```json
{
  "error": "Invalid API key",
  "status": 401
}
```

##### Server Error
```json
{
  "error": "Internal server error",
  "status": 500,
  "message": "LLM service unavailable"
}
```

### 2. POST /v1/pw_list_documents
**List indexed regulatory documents**

#### Description
Returns a list of all CDSCO regulatory documents currently indexed in the system.

#### Request Format
```http
POST /v1/pw_list_documents  
Content-Type: application/json

{}
```

#### Example Request
```bash
curl -X POST "http://localhost:8001/v1/pw_list_documents" \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Response Format
```json
{
  "documents": [
    {
      "id": "doc_001",
      "filename": "cdsco_banned_02Aug2024.pdf",
      "path": "./data/cdsco_banned_02Aug2024.pdf",
      "size": 1234567,
      "modified": "2024-08-02T10:30:00Z",
      "indexed": "2024-09-25T15:45:30Z"
    }
  ],
  "total_documents": 12,
  "total_size": 15234567
}
```

### 3. POST /v1/retrieve
**Enhanced semantic search for regulatory documents**

#### Description
Performs semantic search across CDSCO regulatory documents using advanced embeddings.

#### Request Format
```http
POST /v1/retrieve
Content-Type: application/json

{
  "query": "search query",
  "k": 5
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query for regulatory documents |
| `k` | integer | No | 3 | Number of top results to return |

#### Example Request
```bash
curl -X POST "http://localhost:8001/v1/retrieve" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "CDSCO banned drug notifications 2024",
    "k": 5
  }'
```

#### Response Format
```json
{
  "results": [
    {
      "id": "chunk_001",
      "text": "Ministry of Health and Family Welfare notification...",
      "metadata": {
        "filename": "cdsco_banned_02Aug2024.pdf",
        "page": 2,
        "chunk_id": "001"
      },
      "similarity_score": 0.892
    }
  ],
  "query": "CDSCO banned drug notifications 2024",
  "total_results": 5
}
```

## 🧬 Pharmaceutical Query Patterns

### Drug Ban Queries
```bash
# Check specific drug ban status
"Is [DRUG_NAME] banned in India?"
"Check CDSCO ban status for [DRUG_NAME]"
"Analyze [DRUG_NAME] regulatory compliance"

# Fixed Dose Combination queries
"Is [DRUG_A] + [DRUG_B] combination banned?"
"Check FDC status for [DRUG_COMBINATION]"
```

### Schedule Classification Queries
```bash
# Schedule determination
"What schedule is [DRUG_NAME] classified under?"
"Is [DRUG_NAME] a Schedule H/H1/X drug?"
"Check prescription requirements for [DRUG_NAME]"
```

### Government Compliance Queries  
```bash
# Platform-specific compliance
"Analyze [DRUG_NAME] for Government listing compliance"
"Can [DRUG_NAME] be listed on Government?"
"Government compliance check for [DRUG_NAME]"
```

### Controlled Substance Queries
```bash
# NDPS Act compliance
"Is [DRUG_NAME] controlled under NDPS Act?"
"Check controlled substance status for [DRUG_NAME]"
"NDPS Act compliance for [DRUG_NAME]"
```

## 📊 Response Analysis Framework

### S1-S6 Regulatory Categories

The system analyzes drugs according to six regulatory categories:

#### S1: New Banned Drugs
- **Sources**: CDSCO gazette notifications, Ministry of Health publications
- **Keywords**: "prohibition", "prohibited", "FDC", "restricted"

#### S2: Previously Banned, Now Approved
- **Sources**: Gazette subsection (i) notifications for prohibition withdrawals  
- **Keywords**: "drugs", "revised", "withdraw"

#### S3: Scheduled Drugs  
- **Sources**: Updated Drugs Rules 1945, CDSCO scheduled drug lists
- **Keywords**: "Schedule H", "Schedule H1", "Schedule X"

#### S4: Import Banned Drugs
- **Sources**: Delhi drug department, court judgments
- **Keywords**: "court", "judgement", "import"

#### S5: Controlled Substances
- **Sources**: Department of Revenue gazette notifications
- **Keywords**: NDPS Act, controlled substances

#### S6: Substandard Quality (NSQ)
- **Sources**: Monthly CDSCO NSQ alerts  
- **Keywords**: "NSQ", "not of standard quality"

### P1-P8 Processing Workflow

Each query follows an 8-step analysis process:

1. **P1-P2**: Input processing and drug identification
2. **P3**: Image-name consistency verification
3. **P4**: Ban status analysis (S1, S4)
4. **P5**: Approval status verification (S2)  
5. **P6**: Schedule classification (S3)
6. **P7**: Controlled substance checking (S5)
7. **P8**: Quality and miscellaneous factors (S6)

## 🔧 Error Handling

### Common HTTP Status Codes

| Status Code | Description | Common Causes |
|-------------|-------------|---------------|
| **200** | Success | Request processed successfully |
| **400** | Bad Request | Missing `prompt` parameter, invalid JSON |
| **401** | Unauthorized | Invalid or missing OpenRouter API key |  
| **404** | Not Found | Endpoint not available |
| **429** | Rate Limited | Too many requests to OpenRouter API |
| **500** | Internal Error | Server error, LLM service unavailable |
| **503** | Service Unavailable | Server starting up or maintenance |

### Error Response Format
```json
{
  "error": "Error description",
  "status": 400,
  "message": "Detailed error message",
  "timestamp": "2024-09-25T20:15:30Z"
}
```

### Retry Logic Recommendations

#### For Rate Limiting (429)
```bash
# Exponential backoff strategy
sleep_time = 2^attempt_number
max_retries = 3
```

#### For Server Errors (5xx)  
```bash
# Linear backoff for server issues
sleep_time = attempt_number * 5
max_retries = 5
```

## 🧪 Testing and Validation

### Health Check Script
```python
#!/usr/bin/env python3
import requests
import json

def health_check():
    """Perform comprehensive API health check"""
    base_url = "http://localhost:8001"
    
    # Test basic connectivity
    try:
        response = requests.post(
            f"{base_url}/v1/pw_ai_answer",
            json={"prompt": "Test server status"},
            timeout=10
        )
        print(f"✅ Server responding: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    health_check()
```

### Performance Testing
```python
#!/usr/bin/env python3
import requests
import time
import statistics

def performance_test():
    """Test API response times for pharmaceutical queries"""
    queries = [
        "Is Paracetamol banned in India?",
        "Check Tramadol regulatory status",
        "Analyze Alprazolam schedule classification",
        "Government compliance for Morphine",
        "Is Aspirin controlled under NDPS Act?"
    ]
    
    response_times = []
    
    for query in queries:
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8001/v1/pw_ai_answer",
            json={"prompt": query},
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)
        
        print(f"Query: {query[:30]}... | Time: {response_time:.2f}s")
    
    print(f"\n📊 Performance Statistics:")
    print(f"Average: {statistics.mean(response_times):.2f}s")
    print(f"Median: {statistics.median(response_times):.2f}s")
    print(f"Min: {min(response_times):.2f}s")
    print(f"Max: {max(response_times):.2f}s")

if __name__ == "__main__":
    performance_test()
```

## 📈 Rate Limits and Usage

### OpenRouter Rate Limits
- **Requests per minute**: Varies by subscription plan
- **Tokens per request**: 1000 max (configured)
- **Concurrent requests**: Limited by plan

### Recommended Usage Patterns

#### Batch Processing
```python
# Process multiple drugs efficiently
drugs = ["Paracetamol", "Aspirin", "Tramadol", "Alprazolam"]

for drug in drugs:
    response = requests.post(
        "http://localhost:8001/v1/pw_ai_answer",
        json={"prompt": f"Analyze {drug} for Government compliance"},
        timeout=30
    )
    
    # Add delay between requests to respect rate limits
    time.sleep(2)
```

#### Caching Recommendations
```python
# Cache responses for repeated queries
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def cached_compliance_check(drug_name):
    """Check compliance with caching"""
    cache_key = f"compliance:{drug_name.lower()}"
    cached_result = cache.get(cache_key)
    
    if cached_result:
        return json.loads(cached_result)
    
    # Make API request
    response = requests.post(
        "http://localhost:8001/v1/pw_ai_answer",
        json={"prompt": f"Analyze {drug_name} for Government compliance"}
    )
    
    result = response.json()
    
    # Cache for 24 hours (regulatory data changes infrequently)
    cache.setex(cache_key, 86400, json.dumps(result))
    
    return result
```

---

## 📞 API Support

### Troubleshooting Checklist

1. **Server Status**: Verify server is running on correct port
2. **API Keys**: Check OpenRouter credentials in `.env` file  
3. **Network**: Ensure no firewall blocking port 8001
4. **Dependencies**: Verify all Python packages installed
5. **Documents**: Check CDSCO regulatory files in `./data` directory

### Debug Mode
```bash
# Enable detailed API logging
export PATHWAY_LOG_LEVEL=DEBUG
python app_openrouter_enhanced.py

# Monitor API logs
tail -f server.log
```

### Contact and Support

- **Technical Issues**: Check server logs and error responses
- **Regulatory Questions**: Consult CDSCO official documentation
- **Performance Issues**: Review rate limits and caching strategies

---

**⚠️ Important**: This API provides pharmaceutical compliance assistance based on available regulatory documents. Always verify critical regulatory decisions with official CDSCO sources and qualified professionals.