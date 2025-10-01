#!/bin/bash

# Comprehensive test suite for FastAPI Template Service
set -e

echo \"Starting FastAPI Template Service Test Suite...\"

# Function to start the service
start_service() {
    echo "Starting service..."
            python -c 'from services.template_service import main; import uvicorn; uvicorn.run("services.template_service.main:app", host="127.0.0.1", port=8000, log_level="error")' > /dev/null 2>&1 || true
    SERVICE_PID=$!
    sleep 3  # Wait for service to start
    echo "Service started with PID: $SERVICE_PID"
}

# Function to stop the service
stop_service() {
    echo \"Stopping service...\"
    kill $SERVICE_PID 2>/dev/null || true
    wait $SERVICE_PID 2>/dev/null || true
    echo \"Service stopped\"
}

# Test the API directly
test_api() {
    echo \"Testing API endpoints...\"
    
    # Test health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo \"✅ Health endpoint: OK\"
    else
        echo \"❌ Health endpoint: FAILED\"
        return 1
    fi
    
    # Test root endpoint
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        echo \"✅ Root endpoint: OK\"
    else
        echo \"❌ Root endpoint: FAILED\"
        return 1
    fi
    
    # Test templates endpoint
    if curl -f http://localhost:8000/api/v1/templates > /dev/null 2>&1; then
        echo \"✅ Templates endpoint: OK\"
    else
        echo \"❌ Templates endpoint: FAILED\"
        return 1
    fi
    
    # Test invalid template generation
    if curl -f -X POST http://localhost:8000/api/v1/generate \\
        -H \"Content-Type: application/json\" \\
        -d '{\"template_name\":\"nonexistent\",\"project_name\":\"test\",\"parameters\":{}}' \\
        -w \"%{http_code}\" -o /dev/null | grep -q \"404\"; then
        echo \"✅ Invalid template test: OK\"
    else
        echo \"❌ Invalid template test: FAILED\"
        return 1
    fi
}

# Test the client
test_client() {
    echo \"Testing client functionality...\"
    
    # Test client list command
    if python services/template_service/client.py list --server http://localhost:8000 | grep -q \"fastapi-minimal\"; then
        echo \"✅ Client list command: OK\"
    else
        echo \"❌ Client list command: FAILED\"
        return 1
    fi
    
    # Test client generate command
    if python services/template_service/client.py generate test-client-project \\
        --template fastapi-minimal --server http://localhost:8000 --output /tmp; then
        echo \"✅ Client generate command: OK\"
        # Check if the project was created properly
        if [ -f \"/tmp/test-client-project/app/main.py\" ]; then
            echo \"✅ Generated project has expected structure: OK\"
            # Check placeholder replacement
            if grep -q \"test-client-project\" /tmp/test-client-project/app/main.py; then
                echo \"✅ Placeholder replacement: OK\"
            else
                echo \"❌ Placeholder replacement: FAILED\"
                return 1
            fi
        else
            echo \"❌ Generated project missing expected structure: FAILED\"
            return 1
        fi
        # Cleanup
        rm -rf /tmp/test-client-project
    else
        echo \"❌ Client generate command: FAILED\"
        return 1
    fi
}

# Test Docker build
test_docker() {
    echo \"Testing Docker build...\"
    
    if docker build -t fastapi-template-test . > /dev/null 2>&1; then
        echo \"✅ Docker build: OK\"
        # Clean up image
        docker rmi fastapi-template-test > /dev/null 2>&1 || true
    else
        echo \"❌ Docker build: FAILED\"
        return 1
    fi
}

# Run all tests
start_service

echo \"\"
echo \"Running API tests...\"
if test_api; then
    echo \"✅ All API tests passed!\"
else
    echo \"❌ API tests failed!\"
    stop_service
    exit 1
fi

echo \"\"
echo \"Running client tests...\"
if test_client; then
    echo \"✅ All client tests passed!\"
else
    echo \"❌ Client tests failed!\"
    stop_service
    exit 1
fi

echo \"\"
echo \"Running Docker tests...\"
if test_docker; then
    echo \"✅ All Docker tests passed!\"
else
    echo \"❌ Docker tests failed!\"
    stop_service
    exit 1
fi

stop_service

echo \"\"
echo \"🎉 All tests passed! FastAPI Template Service is working correctly.\"