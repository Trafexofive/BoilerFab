# {{PROJECT_NAME}}

A comprehensive microservices platform with your proven architecture patterns, universal Makefile, and production-ready tooling.

## 🏗️ Architecture

This platform follows your established patterns from DeepS, Cortex-Prime-MK1, and DB-Forge-MK1:

```
{{PROJECT_NAME}}/
├── services/              # Microservices (your pattern)
│   ├── api-gateway/      # Main API routing and orchestration
│   ├── auth-service/     # Authentication and authorization
│   └── web-client/       # Frontend application
├── infra/                # Infrastructure configuration
│   ├── config/           # Service configurations
│   └── docker/           # Docker-related files
├── scripts/              # Utility scripts
├── docs/                 # Documentation
├── testing/              # Comprehensive testing
├── Makefile             # Your universal Docker Compose Makefile
└── docker-compose.yml   # Multi-service orchestration
```

## 🚀 Quick Start

### 1. Start the Platform

```bash
# Start all services
make up

# Or start services individually
make api-gateway    # Start API gateway only
make auth-service   # Start auth service only  
make web-client     # Start web client only
```

### 2. Verify Services

```bash
# Check all services status
make status

# Check health of specific service
make health service=api-gateway

# Follow logs
make logs                    # All services
make logs service=api-gateway # Specific service
```

### 3. Development Workflow

```bash
# Interactive shell into service
make ssh service=api-gateway

# Execute commands in service
make exec service=auth-service args="python manage.py migrate"

# Rebuild and restart
make re                     # Rebuild all
make rere                   # Rebuild without cache
```

## 🛠️ Universal Makefile Commands

Your comprehensive Makefile provides these capabilities:

### Core Stack Management
- `make up/down/restart` - Basic lifecycle management
- `make re/rere` - Rebuild patterns (42 School style)
- `make pull` - Update all images

### Service-Specific Operations
- `make logs service=<name>` - Service-specific logs
- `make ssh service=<name>` - Interactive shell
- `make exec service=<name> args="<command>"` - Execute commands
- `make inspect service=<name>` - Container inspection

### Development Tools
- `make test` - Run all tests
- `make format` - Format all code
- `make lint` - Run linting

### Monitoring & Debugging
- `make health` - Check service health
- `make status` - Service status overview
- `make project-volumes` - List project volumes
- `make project-networks` - List project networks

### Cleanup Operations
- `make clean` - Basic cleanup
- `make fclean` - Deep cleanup (with confirmation)
- `make prune` - System-wide cleanup (dangerous)

## 📊 Services Overview

| Service | Port | Purpose | Technology |
|---------|------|---------|------------|
| **api-gateway** | {{main_service_port}} | Main API routing and orchestration | FastAPI/Python |
| **auth-service** | 8001 | Authentication and user management | FastAPI/Python |
| **web-client** | 3000 | Frontend application | React/TypeScript |
| **postgres** | 5432 | Primary database | PostgreSQL 15 |
| **redis** | 6379 | Caching and sessions | Redis 7 |
| **prometheus** | 9090 | Metrics collection | Prometheus |
| **grafana** | 3001 | Monitoring dashboards | Grafana |

## 🔧 Configuration

### Environment Variables

Each service supports environment-based configuration:

```bash
# API Gateway
SERVICE_NAME={{PROJECT_NAME}}-api-gateway
AUTH_SERVICE_URL=http://auth-service:8001

# Auth Service  
DATABASE_URL=postgresql://postgres:password@postgres:5432/{{PROJECT_NAME}}_auth
JWT_SECRET=your-jwt-secret-change-in-production

# Web Client
REACT_APP_API_URL=http://localhost:{{main_service_port}}
```

### Development vs Production

```bash
# Development with hot reloading
make up file=docker-compose.dev.yml

# Production deployment
make up file=docker-compose.prod.yml
```

## 🧪 Testing

Comprehensive testing following your patterns:

```bash
# Run all tests
make test

# Test specific service
make exec service=api-gateway args="python -m pytest tests/ -v"

# Integration tests
make exec service=api-gateway args="python -m pytest tests/integration/ -v"
```

## 📈 Monitoring

Built-in observability stack:

- **Prometheus**: Metrics collection at http://localhost:9090
- **Grafana**: Dashboards at http://localhost:3001 (admin/admin)
- **Health Checks**: Built into each service
- **Logging**: Centralized via Docker Compose

## 🔐 Security

Production-ready security features:

- **JWT Authentication** with secure token handling
- **Database isolation** with dedicated auth database
- **Redis password protection** for cache security
- **Health check endpoints** for monitoring
- **Container isolation** with dedicated networks

## 🚀 Deployment

### Local Development

```bash
make up                    # Standard development
make up file=docker-compose.dev.yml  # Development mode
```

### Production

```bash
# Production with optimized settings
make up file=docker-compose.prod.yml

# Or using environment overrides
COMPOSE_FILE=docker-compose.prod.yml make up
```

### Cloud Deployment

The platform is ready for:
- **Kubernetes** deployment with Helm charts
- **Docker Swarm** orchestration
- **Cloud providers** (AWS, GCP, Azure)
- **CI/CD pipelines** with automated testing

## 📚 Your Architecture Patterns Implemented

This template incorporates patterns from your projects:

✅ **DeepS Pattern**: Microservices with `services/` directory  
✅ **Cortex-Prime Pattern**: Infrastructure separation and agent architecture  
✅ **DB-Forge Pattern**: Gateway-based API access  
✅ **Universal Makefile**: Your comprehensive Docker Compose management  
✅ **Testing Strategy**: Comprehensive test coverage  
✅ **Documentation**: Clear README and architecture docs  

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the established patterns
4. Test your changes (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

**Built with your proven architecture patterns and universal tooling!** 🚀