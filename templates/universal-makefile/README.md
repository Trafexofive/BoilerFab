# {{PROJECT_NAME}}

A project with your comprehensive universal Docker Compose Makefile for professional service management.

## 🛠️ Universal Makefile Features

This project includes your battle-tested universal Makefile with comprehensive Docker Compose management:

### 🚀 Core Commands

```bash
# Basic lifecycle
make up                    # Start all services
make down                  # Stop and remove services
make restart               # Restart all services
make re                    # Rebuild and restart (42 School style)
make rere                  # Rebuild without cache and restart

# Development workflow
make logs                  # Follow all logs
make logs service=app      # Service-specific logs
make ssh service=app       # Interactive shell into service
make exec service=app args="ls -la"  # Execute command in service
```

### 📊 Monitoring & Debugging

```bash
# Status and health
make status                # Show service status
make health                # Check service health
make ps                    # List running services

# Resource management
make project-volumes       # List project volumes
make project-networks      # List project networks
make inspect service=app   # Inspect service container
```

### 🔧 Building & Configuration

```bash
# Building
make build                 # Build all images
make build service=app     # Build specific service
make no-cache              # Build without cache
make pull                  # Pull latest images

# Configuration
make config                # Validate and show config
make validate-compose      # Validate compose file syntax
make check-running         # Check which services are running
```

### 🧹 Cleanup Operations

```bash
# Progressive cleanup levels
make clean                 # Basic cleanup (containers + networks)
make fclean                # Deep cleanup (+ volumes + images) [with confirmation]
make prune                 # System-wide cleanup [DANGEROUS - with confirmation]
```

### 🎯 Advanced Features

- **🎨 Color-coded output** with status indicators
- **🔍 Service-specific operations** with `service=<name>` parameter
- **📁 Flexible compose files** with `file=<compose-file>` parameter
- **🛡️ Safety confirmations** for destructive operations
- **📋 Project isolation** - only affects current project resources
- **📚 Comprehensive help** with examples and usage patterns

## 🚀 Quick Start

```bash
# Start your services
make up

# Check status
make status

# Follow logs
make logs

# Get interactive shell
make ssh service=app

# When done, clean up
make down
```

## 🔧 Customization

### Adding Services

Edit `docker-compose.yml` to add more services following the pattern:

```yaml
services:
  your-service:
    build: ./path/to/service
    ports:
      - "3000:3000"
    labels:
      - "com.docker.compose.project={{PROJECT_NAME}}"
```

### Environment Files

Use different compose files for different environments:

```bash
make up file=docker-compose.dev.yml     # Development
make up file=docker-compose.prod.yml    # Production  
make up file=docker-compose.test.yml    # Testing
```

### Custom Commands

The Makefile is easily extensible. Add your own targets:

```makefile
# Add to Makefile
your-command: ## Your custom command description
	@echo "Running your custom command..."
	@$(COMPOSE) exec app your-command
```

## 📖 Your Architecture Patterns

This Makefile supports the patterns from your projects:

✅ **Service isolation** with project-specific networks and volumes  
✅ **Health monitoring** with built-in health check commands  
✅ **Development workflow** with hot reloading and interactive debugging  
✅ **Production readiness** with proper cleanup and resource management  
✅ **42 School conventions** with `re/rere` rebuild patterns  
✅ **Safety measures** with confirmation prompts for destructive operations  

## 💡 Pro Tips

```bash
# Chain commands for common workflows
make down && make build && make up    # Full rebuild workflow
make re                               # Same as above, but shorter

# Use with different compose files
make logs file=docker-compose.dev.yml service=app

# Monitor multiple services
make logs service=app &               # Background logs for app
make logs service=db                  # Foreground logs for db

# Quick debugging session
make ssh service=app                  # Get shell
# Inside container: ps aux, htop, tail logs, etc.
```

## 🔗 Integration

This Makefile works seamlessly with:
- **CI/CD pipelines** - use `make test`, `make build`, etc.
- **Development IDEs** - integrate make commands as tasks
- **Monitoring tools** - use `make health` for health checks
- **Deployment scripts** - standardized interface across projects

---

**Your universal Docker Compose management solution!** 🚀