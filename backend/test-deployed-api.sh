#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# API Base URL
API_BASE="https://mindease-gigu.onrender.com"

# Track test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
FAILED_ENDPOINTS=()

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to test an endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    local auth_header=$5
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    print_status "Testing $description..."
    
    if [ "$method" = "GET" ]; then
        if [ -n "$auth_header" ]; then
            response=$(curl -s -w "\n%{http_code}" -H "$auth_header" "$API_BASE$endpoint")
        else
            response=$(curl -s -w "\n%{http_code}" "$API_BASE$endpoint")
        fi
    elif [ "$method" = "POST" ]; then
        if [ -n "$data" ]; then
            if [ -n "$auth_header" ]; then
                response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -H "$auth_header" -d "$data" "$API_BASE$endpoint")
            else
                response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$API_BASE$endpoint")
            fi
        else
            if [ -n "$auth_header" ]; then
                response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" -H "$auth_header" "$API_BASE$endpoint")
            else
                response=$(curl -s -w "\n%{http_code}" -X POST -H "Content-Type: application/json" "$API_BASE$endpoint")
            fi
        fi
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n1)
    # Extract response body (all lines except last)
    body=$(echo "$response" | head -n -1)
    
    if [ "$status_code" -ge 200 ] && [ "$status_code" -lt 300 ]; then
        print_success "$description - Status: $status_code"
        echo "Response: $body" | head -c 200
        if [ ${#body} -gt 200 ]; then
            echo "..."
        fi
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_error "$description - Status: $status_code"
        echo "Response: $body"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        FAILED_ENDPOINTS+=("$description (Status: $status_code)")
    fi
    echo ""
}

echo "🧪 Testing MindEase API on Render"
echo "=================================="
echo "API Base URL: $API_BASE"
echo ""

# Test 1: Health Check (No Auth Required)
test_endpoint "GET" "/health" "" "Health Check"

# Test 2: Root Endpoint (No Auth Required)
test_endpoint "GET" "/" "" "Root Endpoint"

# Test 3: API Documentation
print_status "API Documentation available at: $API_BASE/docs"

# Test 4: Get Authentication Token
print_status "Getting authentication token..."
auth_response=$(curl -s -X POST -H "Content-Type: application/json" -d '{}' "$API_BASE/api/v1/auth/anonymous")
token=$(echo "$auth_response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$token" ]; then
    print_success "Authentication token obtained successfully"
    auth_header="Authorization: Bearer $token"
    echo "Token: ${token:0:20}..."
else
    print_error "Failed to get authentication token"
    exit 1
fi

echo ""

# Test 5: Anonymous Authentication (No Auth Required)
test_endpoint "POST" "/api/v1/auth/anonymous" "{}" "Anonymous Authentication"

# Test 6: Daily Topics (Auth Required)
test_endpoint "GET" "/api/v1/topics/daily" "" "Get Daily Topics" "$auth_header"

# Test 7: Topic Categories (Auth Required)
test_endpoint "GET" "/api/v1/topics/categories" "" "Get Topic Categories" "$auth_header"

# Test 8: Wellness Activities (Auth Required)
test_endpoint "GET" "/api/v1/wellness/activity" "" "Get Wellness Activities" "$auth_header"

# Test 9: Analytics Insights (Auth Required)
test_endpoint "GET" "/api/v1/analytics/insights" "" "Get Analytics Insights" "$auth_header"

# Test 10: Mood Entries (Auth Required)
test_endpoint "GET" "/api/v1/wellness/mood" "" "Get Mood Entries" "$auth_header"

# Test 11: Wellness Statistics (Auth Required)
test_endpoint "GET" "/api/v1/wellness/stats" "" "Get Wellness Statistics" "$auth_header"

# Test 12: Mood Trends (Auth Required)
test_endpoint "GET" "/api/v1/analytics/mood/trend" "" "Get Mood Trends" "$auth_header"

# Test 13: Session Activity (Auth Required)
test_endpoint "GET" "/api/v1/analytics/sessions/activity" "" "Get Session Activity" "$auth_header"

# Test 14: Wellness Progress (Auth Required)
test_endpoint "GET" "/api/v1/analytics/wellness/progress" "" "Get Wellness Progress" "$auth_header"

# Test 15: Emotion Summary (Auth Required)
test_endpoint "GET" "/api/v1/analytics/emotions/summary" "" "Get Emotion Summary" "$auth_header"

# Test 16: Create Chat Session (Auth Required)
test_endpoint "POST" "/api/v1/chat/session" '{"session_type": "free_form"}' "Create Chat Session" "$auth_header"

echo "🎉 API Testing Completed!"
echo "========================="

# Show detailed results
echo "📊 Test Results Summary:"
echo "   Total Tests: $TOTAL_TESTS"
echo "   Passed: $PASSED_TESTS"
echo "   Failed: $FAILED_TESTS"

if [ $FAILED_TESTS -eq 0 ]; then
    print_success "All endpoints tested successfully!"
else
    print_warning "Some endpoints failed:"
    for endpoint in "${FAILED_ENDPOINTS[@]}"; do
        echo "   ❌ $endpoint"
    done
    echo ""
    print_status "Consider investigating the failed endpoints before production deployment"
fi

echo ""
print_status "Next steps:"
echo "1. Visit $API_BASE/docs for interactive API documentation"
echo "2. Test the frontend integration"
echo "3. Monitor the API performance"
echo "4. Test with real user data"
echo "" 