# FastAPI Template Service

A microservice for generating FastAPI project templates using a server-client architecture with authentication and advanced template management.

## Overview

The FastAPI Template Service provides a centralized solution for generating standardized FastAPI projects from templates. It follows a containerized microservice architecture with secure template management and project generation capabilities.

## Features

- **Template-based Project Generation**: Generate standardized FastAPI projects from configurable templates
- **Server-Client Architecture**: Centralized server with distributed client access
- **Containerized Deployment**: Secure, isolated execution environment
- **RESTful API**: Standard HTTP endpoints for integration
- **Customizable Templates**: Dynamic parameter substitution and customization
- **API Key Authentication**: Secure access control with automatically generated keys
- **Advanced Template Management**: Create, list, and detail templates with metadata support
- **Scalable**: Designed for container orchestration platforms

## Architecture

This service is organized as follows:

```
fastapi-template-service/
├── services/                  # Service implementations
│   └── template_service/      # Main template service
│       ├── main.py            # Application factory
│       ├── api/               # API routes
│       ├── models/            # Data models
│       ├── utils/             # Utility functions
│       ├── config/            # Configuration settings
│       ├── auth/              # Authentication module
│       └── client.py          # CLI client
├── templates/                 # Template definitions
├── docs/                      # Documentation
├── testing/                   # Test files
├── scripts/                   # Utility scripts
├── docker-compose.yml         # Docker orchestration
└── requirements.txt           # Dependencies
```

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Make

### Running the Service

```bash
# Using Docker Compose (recommended)
make compose-up

# Using Makefile (development mode)
make dev-run
```

### Using the Client

```bash
# Install dependencies
make build

# List available templates
python services/template_service/client.py --server http://localhost:8000 list

# Get template details
python services/template_service/client.py --server http://localhost:8000 detail fastapi-minimal

# Generate a project
python services/template_service/client.py --server http://localhost:8000 generate my-service --template fastapi-minimal

# Create a new template
python services/template_service/client.py --server http://localhost:8000 create my-template --description "My custom template" --author "My Name" --tags web api
```

## API Endpoints

- `GET /` - Service status (requires API key)
- `GET /health` - Health check endpoint (requires API key)
- `GET /api/v1/templates` - List available templates (requires API key)
- `GET /api/v1/templates/{name}` - Get template details (requires API key)
- `POST /api/v1/templates` - Create new template (requires API key)
- `POST /api/v1/generate` - Generate project from template (requires API key)
- `POST /api/v1/templates/{name}/validate-parameters` - Validate parameters (requires API key)

## Authentication

The service uses API key authentication:

- API key is automatically generated on first run and stored in `api_config.json`
- Key is displayed only once during generation
- All endpoints require the API key in the `X-API-Key` header
- Client automatically reads and uses the API key from the config file

## Adding New Templates

Templates are stored in the `templates/` directory with the following structure:
```
templates/
└── template-name/
    ├── app/
    ├── requirements.txt
    ├── Dockerfile
    ├── README.md
    └── metadata.json  # Optional template metadata
```

1. Create a directory in `templates/` with your template name
2. Add template files with placeholders like `{{PROJECT_NAME}}`
3. Optionally include `metadata.json` with template information

## Development

To run tests:
```bash
# Unit tests
make unit-test

# Run comprehensive test suite
./scripts/test_suite.sh

# Run end-to-end tests with containers
make compose-test
```

## End-to-End Testing

Run the complete test suite:
```bash
./scripts/test_suite.sh
```

This will:
1. Start the service
2. Test all API endpoints
3. Test client functionality
4. Test Docker build
5. Stop the service

## Configuration

Environment variables:
- `SERVICE_PORT`: Server port (default: 8000)
- `SERVICE_HOST`: Bind address (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: INFO)
- `TEMPLATES_DIR`: Template storage directory (default: ./templates)

## Docker Deployment

```bash
# Build and run with Docker Compose
make compose-up

# Stop the service
make compose-down

# View logs
make compose-logs
```

## Security

- Runs as non-root user in container
- API key authentication required for all endpoints
- Input validation and sanitization
- CORS configured for controlled access
- Secure API key generation and storage