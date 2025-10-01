# Contributing to BoilerFab

We welcome contributions to BoilerFab! This project follows proven architectural patterns and maintains high standards for code quality and developer experience.

## 🚀 Quick Start for Contributors

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/BoilerFab.git
cd BoilerFab

# 2. Set up development environment
./scripts/dev/setup.sh

# 3. Start development stack
make up file=docker-compose.dev.yml

# 4. Verify everything works
make health
./boilerfab-client list
```

## 🏗️ Architecture Overview

BoilerFab follows microservices patterns with:
- **Universal Makefile**: Comprehensive Docker Compose management
- **Settings-driven configuration**: YAML-based customization
- **Standalone client**: Works from anywhere with intelligent config discovery
- **Production-ready**: Multi-environment deployment support

## 🛠️ Development Workflow

### Making Changes

```bash
# Create feature branch
git checkout -b feature/awesome-improvement

# Make your changes following our patterns
# ... edit code ...

# Test your changes
make test                          # Run all tests
make lint                          # Code quality checks
make health                        # Service health

# Test client functionality
./boilerfab-client generate test-project --template fastapi-minimal
```

### Universal Makefile Commands

Our comprehensive Makefile provides 40+ commands:

```bash
# Development workflow
make up                           # Start services
make down                         # Stop services
make re                           # Rebuild and restart (42 School style)
make rere                         # Rebuild without cache

# Service-specific operations
make logs service=boilerfab-service    # Service logs
make ssh service=boilerfab-service     # Interactive shell
make exec service=boilerfab-service args="ls -la"  # Execute command

# Debugging and monitoring
make health                       # Check service health
make status                       # Service status
make project-volumes              # List project volumes
make project-networks             # List project networks
```

## 📝 Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use type hints for better code clarity
- Add docstrings for public functions and classes
- Format with Black: `make format`

### Configuration Files
- Use YAML for configuration (settings.yaml)
- Environment variables for runtime overrides
- Document all configuration options

### Docker & Infrastructure
- Multi-stage Dockerfiles for optimization
- Health checks for all services
- Resource limits in production
- Proper labeling following our patterns

## 🧪 Testing

### Test Categories
```bash
make unit-test                    # Unit tests only
make e2e-test                     # End-to-end tests
make compose-test                 # Container integration tests
make test                         # Full test suite
```

### Adding Tests
- Unit tests in `testing/`
- Integration tests for new templates
- Client functionality tests
- Docker deployment tests

## 📦 Adding New Templates

### Template Structure
```
templates/my-template/
├── metadata.json                 # Template configuration
├── README.md                     # Template documentation
├── requirements.txt              # Dependencies
├── Dockerfile                    # Container setup
└── src/                          # Template files with {{PROJECT_NAME}}
```

### Template Metadata
```json
{
  "name": "my-template",
  "description": "Description of what this template creates",
  "version": "1.0.0",
  "author": "Your Name",
  "license": "MIT",
  "tags": ["category", "technology", "type"],
  "parameters": [
    {
      "name": "project_name",
      "type": "string",
      "description": "Name of the project",
      "required": true
    }
  ]
}
```

### Testing Templates
```bash
# Test template generation
./boilerfab-client generate test-project --template my-template

# Verify generated project structure
cd test-project
# ... test the generated project ...
```

## 🔧 Configuration Management

### Settings System
- Primary: `settings.yaml` (main configuration)
- Override: Environment variables
- Examples: `configs/settings.example.yaml`

### Multi-Environment Support
```bash
make up file=docker-compose.dev.yml     # Development
make up file=docker-compose.prod.yml    # Production
```

## 🚀 Deployment

### Local Development
```bash
./scripts/dev/setup.sh           # Initial setup
make up file=docker-compose.dev.yml    # Start dev stack
```

### Production
```bash
cp .env.example .env              # Configure environment
make up file=docker-compose.prod.yml   # Start production stack
```

## 📊 Monitoring & Observability

### Lightweight Monitoring
```bash
# CLI-based monitoring
./scripts/monitoring/simple-monitor.sh          # Quick health check
./scripts/monitoring/simple-monitor.sh -d      # Detailed with resources

# Web-based monitoring (optional)
make up --profile monitoring

# Access dashboards  
open http://localhost:9999        # Dozzle (real-time logs)
open http://localhost:3001        # Uptime Kuma (status page)
```

### Health Checks
```bash
make health                       # Service health overview
curl http://localhost:8000/health # Direct health endpoint
```

### Why Lightweight?
Instead of heavy monitoring stacks (Prometheus/Grafana), we use:
- **Dozzle**: Simple log viewer (~10MB vs ~200MB for ELK stack)
- **Uptime Kuma**: Status monitoring (~50MB vs ~500MB+ for Grafana)
- **CLI Scripts**: Zero overhead monitoring tools

## 🔐 Security Guidelines

### API Security
- All endpoints require API key authentication
- CORS configuration for web clients
- Input validation on all parameters

### Container Security
- Non-root user in all containers
- Resource limits in production
- Network isolation between services
- Read-only mounts where possible

## 📋 Pull Request Guidelines

### Before Submitting
1. **Test thoroughly**: All tests must pass
2. **Follow conventions**: Use established patterns
3. **Update docs**: Keep documentation current
4. **Validate config**: Ensure settings work correctly

### PR Template
- **Description**: Clear explanation of changes
- **Testing**: How you tested the changes
- **Breaking changes**: Any compatibility impacts
- **Configuration**: New settings or environment variables

### Review Process
1. Automated tests must pass
2. Code review by maintainer
3. Manual testing of key functionality
4. Documentation review

## 🤝 Community

### Getting Help
- **Documentation**: Check `docs/` directory
- **Issues**: Search existing GitHub issues
- **Architecture**: Review `docs/ARCHITECTURE.md`

### Reporting Issues
- **Bug reports**: Include reproduction steps
- **Feature requests**: Explain use case and benefits
- **Template issues**: Provide template name and parameters used

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Maintain professional communication

## 📚 Resources

- **Architecture**: `docs/ARCHITECTURE.md`
- **Universal Makefile**: `docs/UNIVERSAL_MAKEFILE.md`
- **API Documentation**: `http://localhost:8000/docs`
- **Settings Reference**: `settings.yaml` with inline comments

Thank you for contributing to BoilerFab! 🚀