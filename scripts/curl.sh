#!/bin/bash

# Government Pharmaceutical Compliance System - API Testing Script
# 
# PURPOSE:
# Comprehensive curl-based testing script for validating all API endpoints
# of the government pharmaceutical compliance system. Provides real-world
# examples of API usage with expected responses and error handling.
#
# USAGE:
# 1. Start the server: python app_openrouter_enhanced.py
# 2. Run this script: bash curl.sh
# 3. Review outputs and response codes
#
# REQUIREMENTS:
# - Server running on localhost:8001
# - curl command available
# - jq for JSON formatting (optional but recommended)

set -e  # Exit on any error

# Configuration
SERVER_URL="http://localhost:8001"
TIMEOUT=60
VERBOSE=false

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Utility functions
print_header() {
    echo -e "\n${BLUE}=================================================================================${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${BLUE}=================================================================================${NC}\n"
}

print_test() {
    echo -e "${CYAN}TEST: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ SUCCESS: $1${NC}"
}

print_error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
}

# Check if server is running
check_server() {
    print_header "SERVER CONNECTIVITY CHECK"
    
    print_test "Checking if server is accessible at $SERVER_URL"
    
    if curl -s --connect-timeout 5 "$SERVER_URL" > /dev/null 2>&1; then
        print_success "Server is accessible"
        return 0
    else
        print_error "Server is not accessible at $SERVER_URL"
        echo "Please start the server with: python app_openrouter_enhanced.py"
        exit 1
    fi
}

# Test 1: Health Check Endpoint
test_health_check() {
    print_header "1. HEALTH CHECK ENDPOINT TEST"
    
    print_test "GET /v1/pw_list_documents - Health check and document listing"
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X GET \
        -H "Content-Type: application/json" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_list_documents")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "Health check successful (HTTP $code)"
        echo -e "${PURPLE}Response:${NC}"
        echo "$body" | head -20
        if [ ${#body} -gt 1000 ]; then
            echo "... (truncated, full response contains $(echo "$body" | wc -c) characters)"
        fi
    else
        print_error "Health check failed (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 2: Basic Pharmaceutical Query
test_basic_query() {
    print_header "2. BASIC PHARMACEUTICAL QUERY TEST"
    
    print_test "POST /v1/pw_ai_answer - Basic drug information query"
    
    query='{
        "prompt": "Is aspirin banned in India? Please provide CDSCO compliance information.",
        "model": "anthropic/claude-3.5-sonnet"
    }'
    
    echo -e "${PURPLE}Query:${NC}"
    echo "$query" | jq '.' 2>/dev/null || echo "$query"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "Basic query successful (HTTP $code)"
        echo -e "${PURPLE}Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        print_error "Basic query failed (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 3: Complex Government Compliance Query
test_government_compliance() {
    print_header "3. INDIAMART COMPLIANCE ANALYSIS TEST"
    
    print_test "POST /v1/pw_ai_answer - Complex pharmaceutical compliance analysis"
    
    query='{
        "prompt": "Analyze the regulatory status of Paracetamol 500mg tablets for Government marketplace listing. Provide S1-S6 category classification and P1-P8 processing workflow with CDSCO compliance verification.",
        "model": "anthropic/claude-3.5-sonnet"
    }'
    
    echo -e "${PURPLE}Query:${NC}"
    echo "$query" | jq '.' 2>/dev/null || echo "$query"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "Government compliance analysis successful (HTTP $code)"
        echo -e "${PURPLE}Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        print_error "Government compliance analysis failed (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 4: Banned Drug Query
test_banned_drug_query() {
    print_header "4. BANNED DRUG VERIFICATION TEST"
    
    print_test "POST /v1/pw_ai_answer - Banned substance verification"
    
    query='{
        "prompt": "Is Nimesulide banned in India? Check against CDSCO banned drug list and provide regulatory status with dates and reasons.",
        "model": "anthropic/claude-3.5-sonnet"
    }'
    
    echo -e "${PURPLE}Query:${NC}"
    echo "$query" | jq '.' 2>/dev/null || echo "$query"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "Banned drug verification successful (HTTP $code)"
        echo -e "${PURPLE}Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        print_error "Banned drug verification failed (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 5: JSON Format Validation
test_json_format() {
    print_header "5. JSON OUTPUT FORMAT VALIDATION TEST"
    
    print_test "POST /v1/pw_ai_answer - JSON format compliance check"
    
    query='{
        "prompt": "Provide Government pharmaceutical compliance analysis for Metformin 500mg tablets in JSON format with all 21 required columns: Drug_Name, Generic_Name, Brand_Names, Therapeutic_Category, Regulatory_Status, CDSCO_Classification, Manufacturing_License_Required, Import_License_Required, Prescription_Category, Controlled_Substance_Status, FDA_Approval_Status, WHO_Prequalification, Indian_Pharmacopoeia_Compliance, Shelf_Life_Months, Storage_Conditions, Contraindications, Side_Effects, Drug_Interactions, Pediatric_Use, Pregnancy_Category, Government_Listing_Eligibility.",
        "model": "anthropic/claude-3.5-sonnet"
    }'
    
    echo -e "${PURPLE}Query:${NC}"
    echo "$query" | jq '.' 2>/dev/null || echo "$query"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "JSON format validation successful (HTTP $code)"
        echo -e "${PURPLE}Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
        
        # Validate JSON structure
        json_response=$(echo "$body" | jq -r '.choices[0].message.content' 2>/dev/null || echo "$body")
        if echo "$json_response" | jq '.' >/dev/null 2>&1; then
            print_success "Response contains valid JSON structure"
        else
            print_warning "Response may not contain properly formatted JSON"
        fi
    else
        print_error "JSON format validation failed (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 6: Error Handling - Invalid Request
test_invalid_request() {
    print_header "6. ERROR HANDLING - INVALID REQUEST TEST"
    
    print_test "POST /v1/pw_ai_answer - Invalid request format"
    
    query='{
        "invalid_field": "This should cause an error",
        "missing_required_fields": true
    }'
    
    echo -e "${PURPLE}Query:${NC}"
    echo "$query" | jq '.' 2>/dev/null || echo "$query"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "400" ] || [ "$code" = "422" ] || [ "$code" = "500" ]; then
        print_success "Error handling working correctly (HTTP $code)"
        echo -e "${PURPLE}Error Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        print_warning "Unexpected response code for invalid request (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 7: Empty Query Handling
test_empty_query() {
    print_header "7. EMPTY QUERY HANDLING TEST"
    
    print_test "POST /v1/pw_ai_answer - Empty prompt handling"
    
    query='{
        "prompt": "",
        "model": "anthropic/claude-3.5-sonnet"
    }'
    
    echo -e "${PURPLE}Query:${NC}"
    echo "$query" | jq '.' 2>/dev/null || echo "$query"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ] || [ "$code" = "400" ]; then
        print_success "Empty query handled appropriately (HTTP $code)"
        echo -e "${PURPLE}Response:${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        print_error "Unexpected response for empty query (HTTP $code)"
        echo "$body"
    fi
    
    echo ""
}

# Test 8: Large Query Handling
test_large_query() {
    print_header "8. LARGE QUERY HANDLING TEST"
    
    print_test "POST /v1/pw_ai_answer - Large pharmaceutical query processing"
    
    # Create a large query with multiple drug names
    large_prompt="Provide comprehensive Government pharmaceutical compliance analysis for the following medications: "
    drugs=("Paracetamol" "Ibuprofen" "Aspirin" "Amoxicillin" "Metformin" "Atorvastatin" "Omeprazole" "Cetirizine" "Diclofenac" "Ranitidine")
    
    for drug in "${drugs[@]}"; do
        large_prompt="$large_prompt $drug 500mg tablets,"
    done
    
    large_prompt="$large_prompt. For each medication, provide S1-S6 category classification, P1-P8 processing workflow, CDSCO compliance status, and Government listing eligibility in structured JSON format."
    
    query=$(cat <<EOF
{
    "prompt": "$large_prompt",
    "model": "anthropic/claude-3.5-sonnet"
}
EOF
)
    
    echo -e "${PURPLE}Query (truncated):${NC}"
    echo "$query" | head -5
    echo "... (query contains $(echo "$query" | wc -c) characters)"
    echo ""
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "Large query processed successfully (HTTP $code)"
        echo -e "${PURPLE}Response (truncated):${NC}"
        echo "$body" | head -20
        echo "... (response contains $(echo "$body" | wc -c) characters)"
    else
        print_error "Large query processing failed (HTTP $code)"
        echo "$body" | head -10
    fi
    
    echo ""
}

# Test 9: CORS and Options Request
test_cors_options() {
    print_header "9. CORS AND OPTIONS REQUEST TEST"
    
    print_test "OPTIONS /v1/pw_ai_answer - CORS preflight request"
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X OPTIONS \
        -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ] || [ "$code" = "204" ]; then
        print_success "CORS preflight handled correctly (HTTP $code)"
    else
        print_warning "CORS preflight may not be properly configured (HTTP $code)"
    fi
    
    echo ""
}

# Test 10: Performance Timing Test
test_performance() {
    print_header "10. PERFORMANCE TIMING TEST"
    
    print_test "Performance measurement for standard pharmaceutical query"
    
    query='{
        "prompt": "What is the CDSCO regulatory status of Ciprofloxacin 500mg tablets?",
        "model": "anthropic/claude-3.5-sonnet"
    }'
    
    start_time=$(date +%s.%N)
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$query" \
        --connect-timeout $TIMEOUT \
        "$SERVER_URL/v1/pw_ai_answer")
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc -l)
    
    body=$(echo "$response" | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    code=$(echo "$response" | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$code" = "200" ]; then
        print_success "Performance test completed (HTTP $code)"
        printf "Response Time: %.2f seconds\n" "$duration"
        
        if (( $(echo "$duration < 30" | bc -l) )); then
            print_success "Response time within acceptable limits (< 30 seconds)"
        else
            print_warning "Response time exceeded 30 seconds - may need optimization"
        fi
    else
        print_error "Performance test failed (HTTP $code)"
    fi
    
    echo ""
}

# Main execution
main() {
    print_header "INDIAMART PHARMACEUTICAL COMPLIANCE SYSTEM - API TESTING"
    
    echo -e "${WHITE}Testing Server: $SERVER_URL${NC}"
    echo -e "${WHITE}Timeout: $TIMEOUT seconds${NC}"
    echo -e "${WHITE}Timestamp: $(date)${NC}\n"
    
    # Check if jq is available for JSON formatting
    if command -v jq &> /dev/null; then
        echo -e "${GREEN}✓ jq available for JSON formatting${NC}"
    else
        echo -e "${YELLOW}⚠ jq not available - JSON will not be formatted${NC}"
    fi
    
    # Run all tests
    check_server
    test_health_check
    test_basic_query
    test_government_compliance
    test_banned_drug_query
    test_json_format
    test_invalid_request
    test_empty_query
    test_large_query
    test_cors_options
    test_performance
    
    # Final summary
    print_header "API TESTING COMPLETED"
    echo -e "${GREEN}All API tests have been executed.${NC}"
    echo -e "${WHITE}Review the results above for any failures or warnings.${NC}"
    echo -e "${CYAN}For detailed analysis, check server logs at: app_enhanced_simple.log${NC}"
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi