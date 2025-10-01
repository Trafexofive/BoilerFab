#!/bin/bash

# Script to test the FastAPI Template Service end-to-end
set -e

echo "Starting FastAPI Template Service End-to-End Test..."

# Start the service in the background
echo "Starting service..."
make dev-run > /dev/null 2>&1 &
SERVICE_PID=$!
sleep 8  # Wait for service to start (include time to generate API key)

echo "Service started with PID: $SERVICE_PID"

# Get the API key
API_KEY=$(cat api_config.json | grep -o '"ftk_[^"]*"')
API_KEY=${API_KEY#\"}
API_KEY=${API_KEY%\"}

echo "Using API key: ${API_KEY:0:10}..."

# Test 1: Check if service is running
echo "Test 1: Checking if service is running..."
if curl -f -H "X-API-Key: $API_KEY" http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    kill $SERVICE_PID
    exit 1
fi

# Test 2: List available templates
echo "Test 2: Listing available templates..."
TEMPLATES=$(python services/template_service/client.py list --server http://localhost:8000)
if echo "$TEMPLATES" | grep -q "fastapi-minimal"; then
    echo "✅ Templates listing works"
else
    echo "❌ Templates listing failed"
    kill $SERVICE_PID
    exit 1
fi

# Test 3: Generate a project
echo "Test 3: Generating a project..."
if python services/template_service/client.py generate test-project --template fastapi-minimal --server http://localhost:8000 --output /tmp; then
    echo "✅ Project generation successful"
    # Verify the generated project exists
    if [ -d "/tmp/test-project" ]; then
        echo "✅ Generated project directory exists"
        # Check for required files
        if [ -f "/tmp/test-project/app/main.py" ] && [ -f "/tmp/test-project/requirements.txt" ]; then
            echo "✅ Generated project has expected files"
        else
            echo "❌ Generated project missing expected files"
            kill $SERVICE_PID
            exit 1
        fi
    else
        echo "❌ Generated project directory does not exist"
        kill $SERVICE_PID
        exit 1
    fi
else
    echo "❌ Project generation failed"
    kill $SERVICE_PID
    exit 1
fi

# Test 4: Check that placeholder replacement worked
echo "Test 4: Verifying placeholder replacement..."
if grep -q "test-project" /tmp/test-project/app/main.py; then
    echo "✅ Placeholder replacement worked correctly"
else
    echo "❌ Placeholder replacement failed"
    kill $SERVICE_PID
    exit 1
fi

# Test 5: Test template creation
echo "Test 5: Testing template creation..."
if python services/template_service/client.py create test-template-cli --description "CLI test template" --author "Test Suite" --server http://localhost:8000; then
    echo "✅ Template creation works"
    # Clean up the created template
    rm -rf templates/test-template-cli
else
    echo "❌ Template creation failed"
    kill $SERVICE_PID
    exit 1
fi

# Cleanup
echo "Cleaning up..."
kill $SERVICE_PID 2>/dev/null || true
rm -rf /tmp/test-project

echo "✅ All end-to-end tests passed!"