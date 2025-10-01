#!/usr/bin/env python3
"""
FastAPI Template Service Client
A CLI tool to interact with the FastAPI Template Service
"""

import argparse
import requests
import zipfile
import io
import json
from pathlib import Path
import sys


def get_api_key_from_config():
    """Get the API key from the config file"""
    config_path = Path("api_config.json")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    return None


def get_templates(server_url):
    """Get list of available templates from the server"""
    try:
        api_key = get_api_key_from_config()
        headers = {"X-API-Key": api_key} if api_key else {}
        response = requests.get(f"{server_url}/api/v1/templates", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return None


def get_template_detail(server_url, template_name):
    """Get detailed information about a specific template"""
    try:
        api_key = get_api_key_from_config()
        headers = {"X-API-Key": api_key} if api_key else {}
        response = requests.get(f"{server_url}/api/v1/templates/{template_name}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting template details: {e}")
        return None


def create_template(server_url, template_data):
    """Register a new template"""
    try:
        api_key = get_api_key_from_config()
        headers = {"X-API-Key": api_key} if api_key else {}
        response = requests.post(f"{server_url}/api/v1/templates", json=template_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating template: {e}")
        return None


def generate_project(server_url, template_name, project_name, output_dir, parameters=None):
    """Request project generation from the server and download the result"""
    if parameters is None:
        parameters = {}
    
    try:
        payload = {
            "template_name": template_name,
            "project_name": project_name,
            "parameters": parameters
        }
        
        api_key = get_api_key_from_config()
        headers = {"X-API-Key": api_key} if api_key else {}
        
        response = requests.post(f"{server_url}/api/v1/generate", json=payload, headers=headers)
        response.raise_for_status()
        
        # The server returns a zip file, so always try to handle it as such
        # Download and extract the zip file
        zip_buffer = io.BytesIO(response.content)
        output_path = Path(output_dir) / project_name
        
        with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
            zip_file.extractall(output_path)
        
        print(f"✅ Project '{project_name}' generated and downloaded to {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error generating project: {e}")
        return False
    except zipfile.BadZipFile:
        print("Error: Server did not return a valid zip file")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="FastAPI Template Service Client")
    parser.add_argument("--server", default="http://localhost:8000", 
                        help="Template service URL (default: http://localhost:8000)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available templates")
    
    # Get template details
    detail_parser = subparsers.add_parser("detail", help="Get detailed information about a template")
    detail_parser.add_argument("template_name", help="Name of the template to get details for")
    
    # Create/register a new template
    create_parser = subparsers.add_parser("create", help="Register a new template")
    create_parser.add_argument("name", help="Name of the template")
    create_parser.add_argument("--description", "-d", required=True, help="Description of the template")
    create_parser.add_argument("--version", "-v", default="1.0.0", help="Version of the template")
    create_parser.add_argument("--author", "-a", help="Author of the template")
    create_parser.add_argument("--license", "-l", help="License of the template")
    create_parser.add_argument("--tags", "-t", nargs="*", default=[], help="Tags for the template")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a project from template")
    generate_parser.add_argument("project_name", help="Name of the project to generate")
    generate_parser.add_argument("--template", "-t", default="fastapi-minimal", 
                                 help="Template to use (default: fastapi-minimal)")
    generate_parser.add_argument("--output", "-o", default=".", 
                                 help="Output directory (default: current directory)")
    
    args = parser.parse_args()
    
    if args.command == "list":
        templates = get_templates(args.server)
        if templates is not None:
            print("Available templates:")
            for template in templates:
                tags_str = f" (tags: {', '.join(template.get('tags', []) or [])})" if template.get('tags') else ""
                params_str = f" ({template.get('parameter_count', 0)} params)" if template.get('parameter_count', 0) > 0 else ""
                print(f"  - {template['name']}: {template['description']} (v{template['version']}){tags_str}{params_str}")
    
    elif args.command == "detail":
        template = get_template_detail(args.server, args.template_name)
        if template is not None:
            print(f"Template: {template['name']}")
            print(f"Description: {template['description']}")
            print(f"Version: {template['version']}")
            print(f"Author: {template.get('author', 'Unknown')}")
            print(f"Tags: {', '.join(template.get('tags', []))}")
            print(f"Created: {template.get('created_at', 'N/A')}")
            print("Parameters:")
            for param in template.get('parameters', []):
                required_str = " (required)" if param.get('required', True) else " (optional)"
                print(f"  - {param['name']} ({param['type']}){required_str}: {param['description']}")
                if 'default' in param and param['default'] is not None:
                    print(f"    Default: {param['default']}")
    
    elif args.command == "create":
        template_data = {
            "name": args.name,
            "description": args.description,
            "version": args.version,
            "author": args.author,
            "license": args.license,
            "tags": args.tags,
            "parameters": []  # For now we're not adding parameters via CLI
        }
        result = create_template(args.server, template_data)
        if result:
            print(f"✅ {result['message']}")
    
    elif args.command == "generate":
        success = generate_project(
            server_url=args.server,
            template_name=args.template,
            project_name=args.project_name,
            output_dir=args.output
        )
        if success:
            print(f"Project '{args.project_name}' generated successfully!")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()