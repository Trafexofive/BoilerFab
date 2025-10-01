# BoilerFab Architecture

## Overview

BoilerFab follows proven microservices architecture patterns with clean separation of concerns, comprehensive tooling, and production-ready deployment capabilities.

## Architecture Principles

### 1. **Service-Oriented Design**
- **Core Service**: Template generation and management
- **Standalone Client**: Independent CLI tool for universal access
- **Configuration-Driven**: YAML-based settings for flexibility

### 2. **Universal Tooling**
- **Universal Makefile**: Comprehensive Docker Compose management
- **Multi-Environment**: Dev, staging, production configurations
- **Health Monitoring**: Built-in observability and debugging

### 3. **Template System**
- **Extensible**: Easy addition of new templates
- **Parameterized**: Dynamic project generation
- **Validated**: Type-safe parameter handling

## Directory Structure

```
BoilerFab/
├── 🔧 Core Service
│   ├── services/template_service/    # Main FastAPI service
│   ├── templates/                    # Template definitions
│   └── settings.yaml                 # Configuration management
│
├── 🛠️ Universal Tooling
│   ├── Makefile                     # Universal Docker Compose management
│   ├── boilerfab-client            # Standalone CLI client
│   └── install.sh                   # Installation automation
│
├── 🏗️ Infrastructure
│   ├── infra/                       # Infrastructure configuration
│   │   ├── config/                  # Service configurations
│   │   ├── monitoring/              # Observability setup
│   │   └── backup/                  # Backup configurations
│   └── docker-compose*.yml          # Multi-environment orchestration
│
├── 🧪 Development & Testing
│   ├── scripts/                     # Development utilities
│   ├── testing/                     # Test suites
│   └── docs/                        # Documentation
│
└── 📦 Distribution
    ├── configs/                     # Example configurations
    └── backups/                     # Automated backups
```

## Service Components

### Core Template Service
- **FastAPI Application**: REST API with automatic documentation
- **Template Engine**: Jinja2-based project generation
- **Parameter Validation**: Pydantic schema validation
- **Authentication**: API key-based security

### Standalone Client
- **Cross-Platform**: Python-based CLI tool
- **Configuration Discovery**: Multiple config file locations
- **Rich Output**: Colored, informative user interface
- **Error Handling**: Comprehensive error reporting

### Universal Makefile
- **42 Commands**: Complete Docker Compose lifecycle management
- **Service-Specific**: Individual service operations
- **Safety Features**: Confirmation prompts for destructive operations
- **Project Isolation**: Scoped resource management

## Data Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Client CLI     │───▶│  Template API    │───▶│  Template       │
│                 │    │                  │    │  Generation     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Configuration  │    │  Authentication  │    │  Project ZIP    │
│  Discovery      │    │  & Validation    │    │  Generation     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Configuration Management

### Settings Hierarchy
1. **settings.yaml** - Primary configuration
2. **Environment variables** - Runtime overrides
3. **Docker Compose** - Container configuration
4. **Client config** - User-specific settings

### Environment Support
- **Development**: Hot reloading, debug logging, full observability
- **Production**: Optimized resources, security hardening, monitoring
- **Testing**: Isolated containers, comprehensive validation

## Security Model

### Authentication
- **API Keys**: Automatically generated, securely stored
- **CORS Protection**: Configurable origin restrictions
- **Input Validation**: Parameter sanitization and validation

### Container Security
- **Non-Root User**: All containers run as non-privileged user
- **Resource Limits**: CPU and memory constraints
- **Network Isolation**: Service-specific networks
- **Read-Only Mounts**: Production template protection

## Scalability & Performance

### Horizontal Scaling
- **Stateless Design**: No server-side session storage
- **Container Ready**: Docker Swarm and Kubernetes support
- **Load Balancer Ready**: Health checks and graceful shutdown

### Performance Optimization
- **Template Caching**: In-memory template storage
- **Async Operations**: Non-blocking I/O operations
- **Resource Pooling**: Efficient resource utilization

## Monitoring & Observability

### Built-in Monitoring
- **Health Endpoints**: Service health and dependency checks
- **Simple Monitoring**: Lightweight CLI and web-based tools
- **Structured Logging**: JSON-formatted, searchable logs

### Lightweight Monitoring Stack (Optional)
Instead of heavy tools like Prometheus/Grafana, BoilerFab uses practical alternatives:

- **Dozzle**: Real-time log viewer (9999)
  - Lightweight Docker log viewer (~10MB)
  - Real-time streaming and search
  - No configuration required

- **Uptime Kuma**: Status monitoring (3001)  
  - Self-hosted uptime monitoring (~50MB)
  - HTTP/TCP/Ping monitoring
  - Status pages and notifications

- **Simple Monitor Script**: CLI health checking
  - `./scripts/monitoring/simple-monitor.sh`
  - Resource usage and log summaries
  - No external dependencies

## Deployment Patterns

### Local Development
```bash
make up file=docker-compose.dev.yml    # Full dev stack with hot reload
```

### Production Deployment
```bash
make up file=docker-compose.prod.yml   # Production-optimized configuration
```

### Cloud Deployment
- **Kubernetes**: Helm charts and manifests
- **Docker Swarm**: Stack deployment files
- **Cloud Providers**: AWS, GCP, Azure ready

## Extension Points

### Adding New Templates
1. Create template directory structure
2. Define metadata.json with parameters
3. Service automatically discovers and validates

### Custom Authentication
- Implement custom authentication provider
- Configure in settings.yaml
- Maintain API compatibility

### Monitoring Integration
- Add custom metrics endpoints
- Configure alerting rules
- Integrate with existing observability stack

