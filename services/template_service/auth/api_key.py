"""
Authentication module for API key management
"""
import os
import secrets
import json
from pathlib import Path
from typing import Optional


class APIKeyManager:
    def __init__(self, config_file: str = "api_config.json"):
        self.config_file = Path(config_file)
        self.api_key = self._load_or_create_api_key()
    
    def _load_or_create_api_key(self) -> str:
        """Load existing API key or create a new one"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return config.get('api_key', self._generate_api_key())
        else:
            new_key = self._generate_api_key()
            self._save_api_key(new_key)
            print(f"🚀 New API Key generated: {new_key}")
            print("⚠️  Save this key - it will not be shown again!")
            return new_key
    
    def _generate_api_key(self) -> str:
        """Generate a secure API key"""
        return f"ftk_{secrets.token_urlsafe(32)}"
    
    def _save_api_key(self, api_key: str):
        """Save API key to config file"""
        config = {
            'api_key': api_key,
            'created_at': str(self.config_file.stat().st_mtime if self.config_file.exists() else __import__('datetime').datetime.now())
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def get_api_key(self) -> str:
        """Get the current API key"""
        return self.api_key
    
    def validate_api_key(self, provided_key: str) -> bool:
        """Validate the provided API key"""
        return secrets.compare_digest(provided_key, self.api_key)


# Global instance
api_key_manager = APIKeyManager()