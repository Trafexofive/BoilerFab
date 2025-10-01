# 🏭 BoilerFab - Universal Project Scaffolding Platform

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Traefik](https://img.shields.io/badge/Traefik-Integrated-green.svg)](https://traefik.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-red.svg)](https://fastapi.tiangolo.com/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)

**🎯 Factorio-approved project scaffolding with Universal Docker Compose Makefile**

*Generate production-ready projects in seconds. Deploy anywhere. Scale infinitely.*

</div>

---

## ⚡ **One-Command Deploy**

**The factory starts with a single command:**

```bash
git clone https://github.com/Trafexofive/BoilerFab.git
cd BoilerFab
make up    # 🚀 Everything starts automatically!
```

**That's it! You now have:**
- 🔥 **BoilerFab API** running at `http://localhost:8000`
- 📚 **Interactive docs** at `http://localhost:8000/docs`  
- 🎯 **CLI client** ready to use globally
- 🛠️ **Traefik dashboard** at `http://localhost:8080`
- 📊 **Monitoring stack** (Dozzle + Uptime Kuma)

## ✨ Why BoilerFab?

- **🎯 Consistency**: Standardize project setups across your entire team
- **⚡ Speed**: Generate production-ready projects in seconds
- **🔒 Security**: API-key authentication and secure template management
- **🐳 Cloud-Ready**: Containerized architecture for easy deployment
- **🔧 Extensible**: Support for any framework or technology stack
- **📊 Template Management**: Version control and metadata tracking for templates

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| **🏗️ Multi-Framework Support** | Generate projects for FastAPI, Flask, Django, React, Vue, Express.js, and more |
| **🏛️ Server-Client Architecture** | Centralized server with distributed client access via CLI or API |
| **🐳 Container-Native** | Full Docker support with Docker Compose orchestration |
| **🔐 Secure Authentication** | API key-based authentication with automatic key generation |
| **📝 Template Management** | Create, version, and manage templates with rich metadata |
| **⚙️ Parameter Substitution** | Dynamic customization with type-safe parameter validation |
| **📊 RESTful API** | Complete REST API with interactive documentation |
| **🔍 Template Discovery** | Search and explore available templates with detailed information |

## 🏗️ Architecture

BoilerFab follows a clean, modular architecture designed for extensibility and maintainability:

```
BoilerFab/
├── 🔧 Core Service
│   ├── services/template_service/    # Main service implementation
│   │   ├── main.py                   # FastAPI application
│   │   ├── api/                      # REST API endpoints  
│   │   ├── models/                   # Data models
│   │   ├── auth/                     # Authentication
│   │   └── client.py                 # Python CLI client
│   └── templates/                    # Template definitions
├── 🐳 Deployment
│   ├── Dockerfile                    # Container definition
│   ├── docker-compose.yml           # Orchestration
│   └── Makefile                      # Build automation
├── 📋 Configuration
│   ├── api_config.json              # API keys (auto-generated)
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Environment template
└── 🧪 Testing & Documentation
    ├── scripts/                     # Test and utility scripts
    ├── docs/                        # Documentation
    └── testing/                     # Test files
```

### Component Overview

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Template Service** | Core API and business logic | FastAPI, Python 3.8+ |
| **CLI Client** | Command-line interface | Python, Requests |
| **Authentication** | API key management | Custom middleware |
| **Template Engine** | Project generation | Jinja2, ZIP handling |
| **Container Runtime** | Deployment platform | Docker, Docker Compose |

## 🚀 Quick Start

Get up and running in 3 simple steps:

### 1. Prerequisites
```bash
# Ensure you have these installed:
- Python 3.8+
- Docker & Docker Compose
- Git
```

### 2. Start the Service
```bash
# Clone and start
git clone <repository-url>
cd BoilerFab

# Option A: Docker Compose (Recommended)
make compose-up

# Option B: Development Mode
make dev-run
```

### 3. Generate Your First Project
```bash
# Using the standalone client (works from anywhere)
./boilerfab-client list
./boilerfab-client generate my-awesome-api --template fastapi-minimal

# Or use the Python client directly (from project directory)
python services/template_service/client.py --server http://localhost:8000 generate my-project
```

The service will be available at `http://localhost:8000` with interactive documentation at `/docs`.

> 💡 **Pro Tip**: The `boilerfab-client` is a standalone executable that works from anywhere! It automatically discovers API keys from multiple locations and provides colored output, health checks, and intelligent error handling.

### 🔧 Installing the Standalone Client

The `boilerfab-client` is a completely standalone executable that works from anywhere without dependencies.

#### Quick Installation

```bash
# Run the installer
./install.sh

# Choose your installation method:
# 1. System-wide (/usr/local/bin) - requires sudo  
# 2. User installation (~/.local/bin) - no sudo
# 3. Current directory symlink
# 4. Custom path
```

#### Manual Installation

```bash
# System-wide (requires sudo)
sudo cp boilerfab-client /usr/local/bin/
sudo chmod +x /usr/local/bin/boilerfab-client

# User installation (recommended)
mkdir -p ~/.local/bin
cp boilerfab-client ~/.local/bin/
chmod +x ~/.local/bin/boilerfab-client
export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.bashrc

# Now use from anywhere
boilerfab-client --help
```

#### First-Time Setup

```bash
# Configure API key (interactive)
boilerfab-client setup

# Or set via environment
export BOILERFAB_API_KEY="your_api_key_here"
export BOILERFAB_SERVER="https://your-server.com"  # Optional

# Test connection
boilerfab-client health
```

## 📖 Usage Guide

### Command Line Interface

BoilerFab provides both a standalone client and project-local Python CLI:

```bash
# Standalone client (works from anywhere)
./boilerfab-client <command> [options]

# Project-local Python client
python services/template_service/client.py --server http://localhost:8000 <command> [options]
```

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | Show all available templates | `./boilerfab-client list` |
| `detail <template>` | Get template information | `./boilerfab-client detail fastapi-minimal` |
| `generate <name>` | Create a new project | `./boilerfab-client generate my-app --template web-api` |
| `create <template>` | Register new template | `./boilerfab-client create my-template -d "Description"` |
| `health` | Check service connectivity | `./boilerfab-client health` |
| `setup` | Configure API key | `./boilerfab-client setup` |

#### API Key Configuration

The standalone client automatically finds your API key from:

1. **Environment variable**: `BOILERFAB_API_KEY`
2. **Current directory**: `api_config.json`
3. **User config**: `~/.config/boilerfab/config.json`
4. **User home**: `~/.boilerfab/config.json`

```bash
# Set via environment (recommended for CI/CD)
export BOILERFAB_API_KEY="your_api_key_here"

# Or run interactive setup
./boilerfab-client setup
```

#### Generate Project Examples

```bash
# Basic project generation
./boilerfab-client generate my-service

# With specific template
./boilerfab-client generate my-api --template fastapi-minimal

# To specific directory
./boilerfab-client generate my-project --output ./projects/

# With custom parameters
./boilerfab-client generate my-app --param database postgres --param auth jwt

# Get template details first
./boilerfab-client detail fastapi-minimal

# Use with remote server
./boilerfab-client list --server https://templates.mycompany.com
```

### REST API Usage

Interact directly with the service using HTTP requests:

```bash
# Set your API key
API_KEY=$(cat api_config.json | grep -o '"ftk_[^"]*"' | head -1 | sed 's/"//g')

# List templates
curl -H "X-API-Key: $API_KEY" http://localhost:8000/api/v1/templates

# Generate project (returns ZIP file)
curl -H "X-API-Key: $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"template_name":"fastapi-minimal","project_name":"my-service"}' \
     http://localhost:8000/api/v1/generate \
     --output my-service.zip
```

## 📚 API Reference

BoilerFab provides a comprehensive REST API for programmatic access. All endpoints require API key authentication via the `X-API-Key` header.

### Core Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/` | Service status and information | Required |
| `GET` | `/health` | Health check endpoint | Required |
| `GET` | `/docs` | Interactive API documentation | None |

### Template Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/templates` | List all available templates |
| `GET` | `/api/v1/templates/{name}` | Get detailed template information |
| `POST` | `/api/v1/templates` | Register/create a new template |
| `POST` | `/api/v1/templates/{name}/validate-parameters` | Validate parameters against template |

### Project Generation

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `POST` | `/api/v1/generate` | Generate project from template | ZIP file download |

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Both interfaces provide interactive API testing and comprehensive endpoint documentation.

## 🔐 Authentication & Security

BoilerFab implements robust security measures to protect your template service:

### Security Features

| Feature | Implementation | Benefit |
|---------|---------------|---------|
| **🔑 API Key Authentication** | Automatic generation and secure storage | Controlled access to all endpoints |
| **⏱️ Constant-Time Comparison** | Prevents timing attacks | Enhanced security against exploitation |
| **🛡️ Input Validation** | Parameter validation against schemas | Prevents injection and malformed requests |
| **🚫 Non-Root Execution** | Container runs as non-privileged user | Reduced attack surface |
| **🔒 Secure Key Generation** | Cryptographically secure random keys | Unpredictable API keys |
| **🌐 CORS Configuration** | Configurable cross-origin policies | Controlled browser access |

### API Key Management

```bash
# API key is automatically generated on first run
# View your API key (shown only once during generation)
cat api_config.json

# The CLI client automatically reads from this file
# No manual key management required for local usage
```

### Security Best Practices

- **🔄 Rotate API keys** periodically in production environments
- **🔒 Use HTTPS** in production with proper TLS certificates  
- **📁 Secure config files** with appropriate file permissions (600)
- **🏗️ Use reverse proxy** (Nginx/Traefik) for production deployments
- **📊 Monitor access** and implement rate limiting as needed

## 📝 Creating Custom Templates

BoilerFab's template system is highly flexible and supports any project structure. Templates use a simple directory-based approach with parameter substitution.

### Template Structure

```
templates/
└── my-custom-template/
    ├── 📄 metadata.json          # Template configuration and parameters
    ├── 📁 project-files/         # Your template files with {{placeholders}}
    │   ├── src/
    │   │   └── main.{{extension}}
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   └── README.md
    └── 📁 config/                # Optional configuration files
```

### Step-by-Step Template Creation

#### 1. Create Template Directory
```bash
mkdir -p templates/my-awesome-template
cd templates/my-awesome-template
```

#### 2. Add Template Files
Create your project structure with placeholder variables:

```python
# src/main.py
"""
{{PROJECT_NAME}} - {{description}}
Generated by BoilerFab
"""

def main():
    print("Hello from {{PROJECT_NAME}}!")
    return "{{author}}"

if __name__ == "__main__":
    main()
```

#### 3. Define Template Metadata
```json
{
  "name": "my-awesome-template",
  "description": "My custom project template with advanced features",
  "version": "1.0.0",
  "author": "Your Name",
  "license": "MIT",
  "tags": ["python", "web", "api", "custom"],
  "parameters": [
    {
      "name": "project_name",
      "type": "string", 
      "description": "Name of the project",
      "required": true
    },
    {
      "name": "description",
      "type": "string",
      "description": "Project description",
      "required": false,
      "default": "An awesome project"
    },
    {
      "name": "author",
      "type": "string",
      "description": "Project author",
      "required": false,
      "default": "Developer"
    },
    {
      "name": "extension",
      "type": "string",
      "description": "File extension to use",
      "required": false,
      "default": "py"
    }
  ]
}
```

#### 4. Register Your Template
```bash
# Register with the service
./client.sh create my-awesome-template \
  --description "My custom project template" \
  --author "Your Name" \
  --tags python web custom
```

#### 5. Test Your Template
```bash
# Generate a project using your template
./client.sh generate test-project --template my-awesome-template

# Verify the generated project
ls -la test-project/
```

### Advanced Template Features

| Feature | Usage | Example |
|---------|-------|---------|
| **🔧 Parameter Types** | `string`, `number`, `boolean`, `array` | `"type": "boolean"` |
| **✅ Required Parameters** | Force user input for critical values | `"required": true` |
| **🎯 Default Values** | Provide sensible defaults | `"default": "my-app"` |
| **🏷️ Template Tags** | Organize and categorize templates | `"tags": ["web", "api"]` |
| **📋 Parameter Validation** | Ensure correct parameter formats | Built-in type checking |
| **🔄 Nested Placeholders** | Use parameters within other parameters | `{{BASE_{{type}}_PATH}}` |

### Template Best Practices

- **📁 Use clear directory structures** that match target project conventions
- **📝 Provide comprehensive metadata** with detailed parameter descriptions  
- **🧪 Test templates thoroughly** before deployment to production
- **📖 Document parameter usage** and provide examples
- **🏷️ Use descriptive tags** for template discovery
- **🔄 Version your templates** for tracking and rollback capabilities

## Development & Testing

BoilerFab includes a comprehensive testing framework to ensure reliability:

```bash
# Unit tests only
make unit-test

# End-to-end tests with containers
make compose-test

# Run complete test suite
make test

# Run comprehensive test suite directly
./scripts/test_suite.sh

# Run end-to-end tests only
make e2e-test
```

### Test Suite Components

The comprehensive test suite includes:
1. **API Endpoint Tests**: Validates all REST endpoints
2. **Client Functionality Tests**: Ensures CLI client works properly
3. **Docker Build Tests**: Verifies containerization works correctly
4. **Template Generation Tests**: Confirms project generation functionality
5. **Parameter Validation Tests**: Tests custom parameter handling

### Running in Development Mode

```bash
# Start service with auto-reload for development
make dev-run

# Build and run with Docker
make docker-run

# View logs
make compose-logs
```

## Configuration

BoilerFab is highly configurable through environment variables:

### Environment Variables

- `SERVICE_PORT`: Server port (default: 8000)
- `SERVICE_HOST`: Bind address (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: INFO)
- `TEMPLATES_DIR`: Template storage directory (default: ./templates)
- `SERVICE_NAME`: Service name for identification (default: "FastAPI Template Service")
- `DEBUG_MODE`: Enable debug mode (default: false)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (default: ["*"])

### Configuration File

API keys are automatically managed in `api_config.json`. The first time the service runs, it generates a secure API key and stores it in this file.

### Docker Configuration

Use environment variables in your docker-compose.yml or .env file to customize the service:

```yaml
environment:
  - SERVICE_PORT=8000
  - SERVICE_HOST=0.0.0.0
  - LOG_LEVEL=INFO
  - TEMPLATES_DIR=/app/templates
```

## 🐳 Deployment & Operations

BoilerFab is designed for modern containerized deployments with support for various orchestration platforms.

### Local Development

```bash
# Development with hot reloading
make dev-run

# Build and test locally  
make build
make test
```

### Docker Deployment

```bash
# Single container deployment
make docker-build
make docker-run

# Docker Compose (recommended)
make compose-up

# View logs and monitor
make compose-logs

# Stop and cleanup
make compose-down
```

### Production Deployment

#### Using Docker Compose

1. **Configure Environment**
```bash
cp docs/.env.example .env
# Edit .env with your production settings
```

2. **Secure Configuration**
```yaml
# docker-compose.prod.yml
services:
  template-service:
    environment:
      - SERVICE_HOST=0.0.0.0
      - SERVICE_PORT=8000
      - LOG_LEVEL=WARNING
      - CORS_ORIGINS=https://your-domain.com
    restart: unless-stopped
    volumes:
      - ./api_config.json:/app/api_config.json:ro
      - ./templates:/app/templates:ro
```

3. **Deploy with Reverse Proxy**
```nginx
# nginx configuration
server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: boilerfab
spec:
  replicas: 3
  selector:
    matchLabels:
      app: boilerfab
  template:
    metadata:
      labels:
        app: boilerfab
    spec:
      containers:
      - name: template-service
        image: boilerfab:latest
        ports:
        - containerPort: 8000
        env:
        - name: SERVICE_HOST
          value: "0.0.0.0"
        - name: LOG_LEVEL
          value: "INFO"
        volumeMounts:
        - name: api-config
          mountPath: /app/api_config.json
          subPath: api_config.json
        - name: templates
          mountPath: /app/templates
      volumes:
      - name: api-config
        secret:
          secretName: boilerfab-config
      - name: templates
        configMap:
          name: boilerfab-templates
---
apiVersion: v1
kind: Service
metadata:
  name: boilerfab-service
spec:
  selector:
    app: boilerfab
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### Environment Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVICE_PORT` | `8000` | Server port |
| `SERVICE_HOST` | `0.0.0.0` | Bind address |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `TEMPLATES_DIR` | `./templates` | Template storage directory |
| `SERVICE_NAME` | `BoilerFab Template Service` | Service identification |
| `DEBUG_MODE` | `false` | Enable debug mode |
| `CORS_ORIGINS` | `["*"]` | Allowed origins (comma-separated) |

### Health Monitoring

```bash
# Health check endpoint
curl -H "X-API-Key: $API_KEY" http://localhost:8000/health

# Service status  
curl -H "X-API-Key: $API_KEY" http://localhost:8000/

# Prometheus metrics (if enabled)
curl http://localhost:8000/metrics
```

## 🧪 Development & Testing

BoilerFab includes a comprehensive testing framework to ensure reliability and maintainability.

### Test Suite Overview

| Test Type | Command | Coverage |
|-----------|---------|----------|
| **Unit Tests** | `make unit-test` | Core functionality and API endpoints |
| **Integration Tests** | `make e2e-test` | End-to-end client-server interactions |
| **Container Tests** | `make compose-test` | Docker deployment and orchestration |
| **Full Suite** | `make test` | Complete test coverage |

### Running Tests

```bash
# Quick unit tests
make unit-test

# Full end-to-end testing with containers
make compose-test

# Run comprehensive test suite
./scripts/test_suite.sh

# Custom test runs
python -m pytest testing/ -v
python services/template_service/client.py --server http://localhost:8000 list
```

### Test Components

The test suite validates:

- ✅ **API Endpoint Functionality** - All REST endpoints respond correctly
- ✅ **Client-Server Communication** - CLI client interacts properly with API
- ✅ **Template Generation** - Projects are created with correct structure
- ✅ **Parameter Substitution** - Dynamic values are properly replaced
- ✅ **Authentication Flow** - API keys are validated correctly
- ✅ **Error Handling** - Graceful handling of invalid inputs
- ✅ **Container Deployment** - Docker images build and run successfully

### Development Workflow

```bash
# Start development environment
make dev-run

# Make code changes...

# Run tests to verify changes
make test

# Check logs for any issues
make compose-logs

# Build production image
make docker-build
```

### Debugging

```bash
# Enable debug mode
DEBUG_MODE=true make dev-run

# View detailed logs
LOG_LEVEL=DEBUG make compose-up

# Interactive container debugging
docker exec -it boilerfab-service bash
```

## 📊 Configuration Reference

### Complete Environment Variables

```bash
# Service Configuration
SERVICE_PORT=8000                    # Server port
SERVICE_HOST=0.0.0.0                # Bind address  
SERVICE_NAME="BoilerFab"             # Service name
DEBUG_MODE=false                     # Debug mode

# Logging
LOG_LEVEL=INFO                       # DEBUG|INFO|WARNING|ERROR

# Directories
TEMPLATES_DIR=./templates            # Template storage path

# Security  
CORS_ORIGINS="*"                     # Comma-separated allowed origins

# Performance
MAX_WORKERS=4                        # Uvicorn worker processes
TIMEOUT=30                           # Request timeout seconds
```

### API Key Configuration

The `api_config.json` file is automatically managed:

```json
{
  "api_key": "ftk_secure_generated_key_here",
  "created_at": "2024-01-15T10:30:00Z",
  "service_name": "BoilerFab Template Service"
}
```

**⚠️ Important**: Keep this file secure and never commit it to version control!

## 🤝 Contributing

We welcome contributions to make BoilerFab even better! Here's how to get involved:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/BoilerFab.git
cd BoilerFab

# Create a development branch
git checkout -b feature/awesome-improvement

# Set up development environment
make dev-run

# Run tests to ensure everything works
make test
```

### Contribution Guidelines

- 🐛 **Bug Reports**: Use detailed issue descriptions with reproduction steps
- ✨ **Feature Requests**: Explain the use case and expected behavior  
- 🔧 **Code Contributions**: Follow existing code style and add tests
- 📝 **Documentation**: Help improve guides, examples, and API docs
- 🧪 **Testing**: Expand test coverage for better reliability

### Code Quality Standards

- All code must pass existing tests (`make test`)
- New features require corresponding tests
- Follow Python PEP 8 style guidelines
- Add docstrings for public functions and classes
- Update documentation for user-facing changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

Need help? We've got you covered:

| Resource | Link | Purpose |
|----------|------|---------|
| 📖 **Documentation** | [./docs/](./docs/) | Comprehensive guides and tutorials |
| 🐛 **Issue Tracker** | [GitHub Issues](https://github.com/Trafexofive/BoilerFab/issues) | Bug reports and feature requests |
| 💬 **Discussions** | [GitHub Discussions](https://github.com/Trafexofive/BoilerFab/discussions) | Questions and community support |
| 📧 **Security Issues** | [Security Policy](SECURITY.md) | Private vulnerability reporting |

### Getting Help

1. **Check existing documentation** in the [docs/](./docs/) directory
2. **Search closed issues** - your question might already be answered
3. **Create a detailed issue** with:
   - Your environment (OS, Python version, Docker version)
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Relevant logs or error messages

---

## 🎯 About BoilerFab

**BoilerFab** transforms the way development teams approach project creation. By providing a centralized, secure, and infinitely extensible template service, we help you:

- **🚀 Accelerate Development**: Generate production-ready projects in seconds
- **📏 Maintain Consistency**: Ensure all projects follow your team's standards  
- **🔒 Enhance Security**: Built-in authentication and secure template management
- **📈 Scale Efficiently**: Container-native architecture grows with your needs
- **🛠️ Stay Flexible**: Support for any technology stack or framework

Whether you're building microservices, web applications, or complex distributed systems, BoilerFab provides the foundation for rapid, consistent, and secure project scaffolding.

**Ready to supercharge your development workflow?** [Get started in 5 minutes](#-quick-start) and see the difference! 🚀

**Ready to supercharge your development workflow?** 

```bash
git clone https://github.com/Trafexofive/BoilerFab.git
cd BoilerFab  
make up
```

**The great work starts now!** 🏭🚀

---

## 📊 **Quick Stats**
- **⚡ Deploy Time**: < 30 seconds
- **🔧 Commands Available**: 47+ Makefile targets
- **📦 Templates Ready**: 11+ production frameworks
- **🌐 Services**: Traefik + API + Monitoring
- **🏭 Organization**: Factorio-approved efficiency

**Perfect for Nginx Proxy Manager users - just add subdomains and go!** 🎯
