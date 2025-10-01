# CLI Client Documentation

## Overview

The FastAPI Template Service CLI client provides command-line access to the template service. It supports all major operations including template management, project generation, and service interaction.

## Installation

The client is included in the FastAPI Template Service repository and can be executed directly:

```bash
python services/template_service/client.py [options] [command] [args...]
```

## Configuration

The client automatically reads the API key from the `api_config.json` file in the project root directory. The API key is generated when the service is first started.

## Commands

### `list`
Lists all available templates on the service.

```bash
python services/template_service/client.py --server http://localhost:8000 list
```

**Options:**
- `--server`: Service URL (default: http://localhost:8000)

**Example Output:**
```
Available templates:
  - fastapi-minimal: A minimal FastAPI project template with basic structure (v1.0.0)
  - web-api-template: Template for web APIs with custom parameters (v1.0.0) (tags: web, api)
```

### `detail`
Gets detailed information about a specific template.

```bash
python services/template_service/client.py --server http://localhost:8000 detail <template-name>
```

**Options:**
- `--server`: Service URL (default: http://localhost:8000)
- `template-name`: Name of the template to get details for

**Example Output:**
```
Template: fastapi-minimal
Description: A minimal FastAPI project template with basic structure
Version: 1.0.0
Author: None
Tags: 
Created: None
Parameters:
```

### `create`
Creates a new template on the service.

```bash
python services/template_service/client.py --server http://localhost:8000 create <name> --description "<description>" [options]
```

**Options:**
- `--server`: Service URL (default: http://localhost:8000)
- `name`: Name of the template
- `--description, -d`: Description of the template (required)
- `--version, -v`: Version of the template (default: 1.0.0)
- `--author, -a`: Author of the template
- `--license, -l`: License of the template
- `--tags, -t`: Tags for the template (space-separated)

**Example:**
```bash
python services/template_service/client.py --server http://localhost:8000 create my-template --description "My custom template" --author "John Doe" --tags web api
```

### `generate`
Generates a project from a template.

```bash
python services/template_service/client.py --server http://localhost:8000 generate <project-name> [options]
```

**Options:**
- `--server`: Service URL (default: http://localhost:8000)
- `project-name`: Name of the project to generate
- `--template, -t`: Template to use (default: fastapi-minimal)
- `--output, -o`: Output directory (default: current directory)

**Example:**
```bash
python services/template_service/client.py --server http://localhost:8000 generate my-new-service --template fastapi-minimal --output /tmp
```

## Global Options

- `--server`: Service URL (default: http://localhost:8000)
  - Specifies the URL of the FastAPI Template Service
  - Should match the server where the service is running
  - Include port if not using the default (8000)

## Authentication

The client automatically handles API key authentication:
- Reads the API key from `api_config.json`
- Includes the key in the `X-API-Key` header for all requests
- No manual configuration required

## Return Values

- `0`: Success
- `1`: Error (connection, authentication, or service error)

## Examples

### Basic Usage
```bash
# List all templates
python services/template_service/client.py list

# Generate a project with default template
python services/template_service/client.py generate my-project

# Generate a project with specific template
python services/template_service/client.py generate my-project --template fastapi-minimal
```

### Advanced Usage
```bash
# Generate a project to a specific location
python services/template_service/client.py generate my-project --template fastapi-minimal --output /path/to/output

# Create a new template
python services/template_service/client.py create new-template --description "New template" --author "Me" --tags web fastapi

# Get detailed information about a template
python services/template_service/client.py detail fastapi-minimal
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Error: "Error connecting to server" or authentication error
   - Solution: Ensure `api_config.json` exists and is accessible

2. **Connection Refused**
   - Error: Connection error
   - Solution: Verify service URL and ensure service is running

3. **404 Not Found**
   - Error: Template or endpoint not found
   - Solution: Verify template name or endpoint exists

### Debugging Tips

- Check that the service is running: `curl http://localhost:8000/health` (with appropriate API key)
- Verify the API key file exists: `ls -la api_config.json`
- Confirm the server URL is correct and accessible

## Integration Examples

### In Scripts
```bash
#!/bin/bash
# Generate multiple projects
for project in service1 service2 service3; do
    python services/template_service/client.py generate $project --template fastapi-minimal --output ./projects
done
```

### With Environment Variables
```bash
export SERVER_URL="http://my-template-service:8000"
python services/template_service/client.py --server $SERVER_URL list
```