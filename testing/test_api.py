import unittest
import requests
import subprocess
import time
import os
from pathlib import Path
import json
import sys
import threading


def get_api_key():
    """Get API key from config file"""
    config_path = Path("api_config.json")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    return None
import sys
import threading


class TestFastAPITemplateService(unittest.TestCase):
    """Test cases for FastAPI Template Service"""

    BASE_URL = "http://localhost:8000"
    
    @classmethod
    def setUpClass(cls):
        """Start the service before running tests"""
        # Start the service in background using the new location
        cls.service_process = subprocess.Popen(
            ["python", "-c", "from services.template_service import main; import uvicorn; uvicorn.run('services.template_service.main:app', host='127.0.0.1', port=8000, log_level='info')"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Wait for service to start (with API key generation time)
        time.sleep(8)
        
        # Get the API key for tests
        cls.api_key = get_api_key()
        if not cls.api_key:
            cls.service_process.terminate()
            cls.service_process.wait()
            raise Exception("Could not retrieve API key from config file")
    
    @classmethod
    def tearDownClass(cls):
        """Stop the service after tests finish"""
        cls.service_process.terminate()
        cls.service_process.wait()
    
    def get_headers(self):
        """Get headers with API key"""
        return {"X-API-Key": self.api_key}
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.BASE_URL}/health", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = requests.get(f"{self.BASE_URL}/", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("status", data)
    
    def test_templates_endpoint(self):
        """Test templates listing endpoint"""
        response = requests.get(f"{self.BASE_URL}/api/v1/templates", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        templates = response.json()
        # Should have at least the fastapi-minimal template
        self.assertGreaterEqual(len(templates), 1)
        
        # Check that template has required fields
        template = templates[0]
        self.assertIn("name", template)
        self.assertIn("description", template)
        self.assertIn("version", template)
    
    def test_generate_endpoint_with_invalid_template(self):
        """Test generate endpoint with non-existent template (should return 404)"""
        payload = {
            "template_name": "nonexistent-template",
            "project_name": "test-project",
            "parameters": {}
        }
        response = requests.post(f"{self.BASE_URL}/api/v1/generate", json=payload, headers=self.get_headers())
        self.assertEqual(response.status_code, 404)
    
    def test_generate_endpoint_with_valid_template(self):
        """Test generate endpoint with valid template"""
        payload = {
            "template_name": "fastapi-minimal",
            "project_name": "test-project",
            "parameters": {}
        }
        response = requests.post(f"{self.BASE_URL}/api/v1/generate", json=payload, headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        # Should return a zip file
        self.assertEqual(response.headers.get('content-type'), 'application/zip')
        
        # Verify that we can read the zip file
        import zipfile
        import io
        zip_buffer = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
            file_list = zip_file.namelist()
            # Should contain files from the template
            self.assertGreater(len(file_list), 0)


if __name__ == "__main__":
    unittest.main()