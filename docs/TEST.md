# Comprehensive Testing Guide

## Overview

This guide provides detailed instructions for testing the Government Pharmaceutical Compliance System. The testing suite is organized into multiple layers to ensure complete system validation from configuration to production deployment.

## Test Organization

### Test Categories

1. **Configuration Tests** - Validate YAML and system configuration
2. **Unit Tests** - Test individual components and functions
3. **Integration Tests** - Test system component interactions
4. **API Tests** - Validate HTTP endpoints and responses
5. **Performance Tests** - Benchmark system performance and scalability
6. **Compliance Tests** - Verify pharmaceutical regulatory accuracy

### Test File Structure

```
tests/
├── test_api.py                 # HTTP API endpoint validation
├── test_custom_prompt.py       # YAML configuration testing
├── test_government_system.py    # Government compliance workflow
├── test_live_server.py         # Live server integration testing
├── test_llm_query.py           # Direct LLM query validation
├── test_openrouter.py          # OpenRouter API integration
├── test_prompt_replacement.py  # Custom prompt functionality
├── test_query.py               # Basic query processing
└── test_server.py              # Server infrastructure testing
```

## Testing Prerequisites

### Environment Setup

1. **Virtual Environment**
   ```bash
   cd /root/code/python-host/pharma-rag-query
   source venv/bin/activate
   ```

2. **Dependencies Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration Validation**
   ```bash
   # Verify YAML configuration files exist
   ls -la *.yaml
   
   # Verify system prompt exists
   cat system_prompt.txt
   ```

4. **API Credentials**
   - Ensure OpenRouter API key is configured
   - Verify network connectivity to OpenRouter services
   - Check anthropic/claude-sonnet-4 model availability

### Data Preparation

1. **CDSCO Documents**
   ```bash
   # Verify regulatory documents are available
   ls -la data/cdsco_*.pdf
   ```

2. **Test Data**
   ```bash
   # Ensure test pharmaceutical data exists
   ls -la data/test_pharma_document.txt
   ```

## Test Execution Guide

### 1. Configuration Testing

**Purpose**: Validate YAML configurations and prompt templates

```bash
# Test YAML configuration validity
python tests/test_custom_prompt.py

# Expected Output:
# ✓ YAML files load successfully
# ✓ Government prompt template present
# ✓ S1-S6 categories validated
# ✓ P1-P8 workflow steps confirmed
```

**Key Validations**:
- YAML syntax correctness
- Government prompt integration
- Configuration parameter completeness
- Pharmaceutical compliance terminology

### 2. Server Infrastructure Testing

**Purpose**: Validate server startup and basic functionality

```bash
# Test server infrastructure
python tests/test_server.py

# Expected Output:
# ✓ Server binds to port successfully
# ✓ HTTP endpoints respond correctly
# ✓ Error handling functions properly
# ✓ Security measures active
```

**Key Validations**:
- Port binding and network configuration
- HTTP method support
- Error response generation
- Security header implementation

### 3. API Endpoint Testing

**Purpose**: Validate HTTP API functionality and responses

```bash
# Test API endpoints
python tests/test_api.py

# Expected Output:
# ✓ Health check endpoint responds
# ✓ Query endpoint accepts requests
# ✓ JSON response format correct
# ✓ Authentication mechanisms active
```

**Key Validations**:
- Endpoint availability
- Request/response formats
- Authentication and authorization
- Error code accuracy

### 4. Direct LLM Query Testing

**Purpose**: Test LLM integration without server overhead

```bash
# Test direct LLM queries
python tests/test_llm_query.py

# Expected Output:
# ✓ OpenRouter API connectivity established
# ✓ Claude-sonnet-4 model responds
# ✓ Pharmaceutical queries processed
# ✓ JSON output format validated
```

**Key Validations**:
- OpenRouter API integration
- Model response accuracy
- Pharmaceutical analysis quality
- JSON structure compliance

### 5. Prompt Replacement Testing

**Purpose**: Verify custom prompt functionality

```bash
# Test custom prompt replacement
python tests/test_prompt_replacement.py

# Expected Output:
# ✓ Default prompts successfully replaced
# ✓ Government system prompt active
# ✓ Custom responses generated
# ✓ Pharmaceutical context maintained
```

**Key Validations**:
- Prompt template replacement
- Government-specific responses
- Pharmaceutical compliance accuracy
- Response quality improvement

### 6. Government System Testing

**Purpose**: Comprehensive Government workflow validation

```bash
# Test Government compliance system
python tests/test_government_system.py

# Expected Output:
# ✓ S1-S6 regulatory categories processed
# ✓ P1-P8 workflow steps executed
# ✓ 21-column output generated
# ✓ CDSCO compliance validated
```

**Key Validations**:
- Regulatory category assignment
- Processing workflow execution
- Structured output generation
- Compliance accuracy verification

### 7. Basic Query Testing

**Purpose**: Validate fundamental query processing

```bash
# Test basic query functionality
python tests/test_query.py

# Expected Output:
# ✓ Query preprocessing successful
# ✓ Document retrieval functional
# ✓ Response generation accurate
# ✓ Edge cases handled gracefully
```

**Key Validations**:
- Input validation and sanitization
- Context retrieval accuracy
- Response quality consistency
- Error handling robustness

### 8. OpenRouter Integration Testing

**Purpose**: Validate OpenRouter API integration

```bash
# Test OpenRouter integration
python tests/test_openrouter.py

# Expected Output:
# ✓ API authentication successful
# ✓ Model selection validated
# ✓ Request/response cycle functional
# ✓ Error handling operational
```

**Key Validations**:
- API credential validation
- Model availability confirmation
- Response format compliance
- Network error handling

### 9. Live Server Integration Testing

**Purpose**: End-to-end system validation with running server

```bash
# Start the enhanced server first
python app_openrouter_enhanced.py &

# Wait for server startup
sleep 5

# Run live server tests
python tests/test_live_server.py

# Expected Output:
# ✓ Server responds to health checks
# ✓ Query processing functional
# ✓ Government compliance active
# ✓ JSON output format correct
```

**Key Validations**:
- Complete system integration
- Real-time query processing
- Government workflow execution
- Production-ready functionality

## Test Execution Order

### Recommended Testing Sequence

1. **Pre-flight Checks**
   ```bash
   # Verify environment and dependencies
   python -c "import yaml, requests, openai; print('Dependencies OK')"
   ```

2. **Configuration Validation**
   ```bash
   python tests/test_custom_prompt.py
   ```

3. **Server Infrastructure**
   ```bash
   python tests/test_server.py
   ```

4. **API Layer Testing**
   ```bash
   python tests/test_api.py
   ```

5. **Core Functionality**
   ```bash
   python tests/test_llm_query.py
   python tests/test_query.py
   ```

6. **Prompt System Validation**
   ```bash
   python tests/test_prompt_replacement.py
   ```

7. **OpenRouter Integration**
   ```bash
   python tests/test_openrouter.py
   ```

8. **Government System Validation**
   ```bash
   python tests/test_government_system.py
   ```

9. **Live System Testing**
   ```bash
   # Start server
   python app_openrouter_enhanced.py &
   
   # Run live tests
   python tests/test_live_server.py
   
   # Stop server
   pkill -f app_openrouter_enhanced.py
   ```

## Expected Test Results

### Success Criteria

Each test should demonstrate:

1. **Functionality Validation**
   - All core features operate as designed
   - Pharmaceutical compliance analysis accuracy
   - Government workflow execution completeness

2. **Performance Standards**
   - Query response time < 30 seconds
   - Server startup time < 60 seconds
   - Memory usage within acceptable limits

3. **Error Handling**
   - Graceful degradation under failure conditions
   - Informative error messages
   - System recovery capabilities

4. **Compliance Standards**
   - CDSCO regulatory accuracy
   - Government specification adherence
   - Professional pharmaceutical analysis quality

### Failure Investigation

If tests fail, investigate in this order:

1. **Configuration Issues**
   - Verify YAML file syntax
   - Check system_prompt.txt content
   - Validate API credentials

2. **Network Connectivity**
   - Test internet connection
   - Verify OpenRouter API accessibility
   - Check firewall and proxy settings

3. **Dependencies**
   - Verify all required packages installed
   - Check Python version compatibility
   - Validate virtual environment activation

4. **Data Availability**
   - Ensure CDSCO documents present
   - Verify test data files exist
   - Check file permissions and accessibility

## Performance Benchmarking

### Key Metrics

1. **Response Time Targets**
   - Simple queries: < 10 seconds
   - Complex pharmaceutical analysis: < 30 seconds
   - Bulk processing: < 60 seconds per document

2. **Throughput Expectations**
   - Concurrent users: 5-10 simultaneous queries
   - Daily query volume: 1000+ pharmaceutical inquiries
   - Peak load handling: 20 queries/minute

3. **Resource Utilization**
   - Memory usage: < 2GB during normal operation
   - CPU utilization: < 80% during peak load
   - Storage requirements: < 10GB for full deployment

### Benchmarking Commands

```bash
# Measure response times
time python tests/test_query.py

# Monitor memory usage
python -c "
import psutil
import subprocess
proc = subprocess.Popen(['python', 'app_openrouter_enhanced.py'])
# Monitor process memory
"

# Network performance testing
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8001/v1/pw_list_documents"
```

## Troubleshooting Common Issues

### Configuration Problems

1. **YAML Parsing Errors**
   ```bash
   # Validate YAML syntax
   python -c "import yaml; yaml.safe_load(open('app_openrouter_enhanced.yaml'))"
   ```

2. **Missing System Prompt**
   ```bash
   # Verify system prompt file
   wc -l system_prompt.txt
   grep -i "government" system_prompt.txt
   ```

### API Integration Issues

1. **OpenRouter Connectivity**
   ```bash
   # Test API connectivity
   curl -H "Authorization: Bearer YOUR_API_KEY" https://openrouter.ai/api/v1/models
   ```

2. **Model Availability**
   ```bash
   # Check model status
   python -c "
   import requests
   response = requests.get('https://openrouter.ai/api/v1/models')
   models = [m['id'] for m in response.json()['data']]
   print('anthropic/claude-3.5-sonnet' in models)
   "
   ```

### Server Issues

1. **Port Binding Problems**
   ```bash
   # Check port availability
   netstat -tlnp | grep :8001
   
   # Kill existing processes
   pkill -f app_openrouter_enhanced.py
   ```

2. **Memory Issues**
   ```bash
   # Monitor memory usage
   ps aux | grep python
   free -h
   ```

## Continuous Integration

### Automated Testing Pipeline

```bash
#!/bin/bash
# CI/CD test pipeline

set -e  # Exit on any error

echo "Starting pharmaceutical compliance system testing..."

# Environment setup
source venv/bin/activate

# Configuration validation
echo "Testing configurations..."
python tests/test_custom_prompt.py

# Core functionality testing
echo "Testing core functionality..."
python tests/test_query.py
python tests/test_llm_query.py

# API integration testing
echo "Testing API integrations..."
python tests/test_openrouter.py
python tests/test_api.py

# System integration testing
echo "Testing system integration..."
python tests/test_government_system.py

# Live system testing
echo "Starting live system tests..."
python app_openrouter_enhanced.py &
SERVER_PID=$!
sleep 10

python tests/test_live_server.py

# Cleanup
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null || true

echo "All tests completed successfully!"
```

## Test Data Management

### Test Datasets

1. **Pharmaceutical Test Cases**
   - Standard drug names and classifications
   - CDSCO banned substance lists
   - Regulatory compliance scenarios
   - Edge cases and ambiguous queries

2. **Expected Outputs**
   - Structured JSON response samples
   - Government 21-column format examples
   - Error response templates
   - Performance benchmark baselines

### Data Privacy and Security

- No real pharmaceutical company data in tests
- Anonymized regulatory document excerpts
- Synthetic query examples for validation
- Secure handling of API credentials

## Conclusion

This comprehensive testing guide ensures the Government Pharmaceutical Compliance System meets all functional, performance, and regulatory requirements. Regular execution of these tests maintains system reliability and compliance accuracy.

For additional support or test customization, refer to the main documentation or contact the development team.