# ======================================================================================
# BoilerFab - Universal Docker Compose Makefile (Organized Edition)
# ======================================================================================

RED     := \033[0;31m
GREEN   := \033[0;32m
YELLOW  := \033[1;33m
BLUE    := \033[0;34m
NC      := \033[0m

# ======================================================================================
# GENERAL CONFIGURATION
# ======================================================================================

SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

# Organized paths (Factorio-style efficiency!)
COMPOSE_FILE ?= deployment/docker-compose.yml
COMPOSE_DEV_FILE ?= deployment/docker-compose.dev.yml
COMPOSE_PROD_FILE ?= deployment/docker-compose.prod.yml
COMPOSE := docker compose -f $(COMPOSE_FILE)

# Detect project name from directory or allow override
PROJECT_NAME ?= $(shell basename $(CURDIR))

# ======================================================================================
# DEFAULT TARGET & SELF-DOCUMENTATION
# ======================================================================================
.DEFAULT_GOAL := help

# Phony targets - don't represent files
.PHONY: help up down logs ps build no-cache restart re config status clean fclean prune \
        stop start ssh exec inspect list-volumes list-networks rere rebuild it backend \
        format lint health pull push validate-compose check-running project-volumes project-networks \
        dev prod monitoring traefik get-api-key client-setup monitoring-down nginx-config test

# ======================================================================================
# HELP & USAGE - ORGANIZED EDITION
# ======================================================================================

help:
	@echo -e "$(BLUE)========================================================================="
	@echo -e " BoilerFab - Universal Docker Compose Makefile (Traefik Edition)"
	@echo -e " Project: $(PROJECT_NAME)"
	@echo -e " 🏭 Factorio-approved with Traefik integration!"
	@echo -e "=========================================================================$(NC)"
	@echo ""
	@echo -e "$(YELLOW)Usage: make [target] [service=SERVICE_NAME] [args=\"ARGS\"]$(NC)"
	@echo ""
	@echo -e "$(GREEN)🚀 CORE COMMANDS:$(NC)"
	@echo -e "  $(YELLOW)up$(NC)               Start all services (Traefik + BoilerFab)"
	@echo -e "  $(YELLOW)down$(NC)             Stop all services gracefully"
	@echo -e "  $(YELLOW)restart$(NC)          Restart all services"
	@echo -e "  $(YELLOW)status$(NC)           Show service status" 
	@echo -e "  $(YELLOW)logs$(NC)             Follow all logs"
	@echo ""
	@echo -e "$(GREEN)🌐 TRAEFIK & MONITORING:$(NC)"
	@echo -e "  $(YELLOW)monitoring$(NC)       Enable monitoring stack (Dozzle + Uptime Kuma)"
	@echo -e "  $(YELLOW)traefik$(NC)          Open Traefik dashboard"
	@echo -e "  $(YELLOW)get-api-key$(NC)      Display API key"
	@echo -e "  $(YELLOW)client-setup$(NC)     Install global CLI client"
	@echo ""
	@echo -e "$(GREEN)🏭 DEPLOYMENT:$(NC)"
	@echo -e "  $(YELLOW)dev$(NC)              Development mode with hot-reload"
	@echo -e "  $(YELLOW)prod$(NC)             Production deployment with SSL"
	@echo -e "  $(YELLOW)build$(NC)            Build all images"
	@echo -e "  $(YELLOW)test$(NC)             Run full test suite"
	@echo ""
	@echo -e "$(YELLOW)🏭 Examples (Factorio Efficiency):$(NC)"
	@echo -e "  make dev                    # Clean development start"
	@echo -e "  make prod                   # Production deployment"
	@echo -e "  make monitoring             # With lightweight monitoring"
	@echo -e "  make logs service=boilerfab-service"
	@echo -e "  make ssh service=boilerfab-service"

# ======================================================================================
# ORGANIZED QUICK-START TARGETS
# ======================================================================================

dev: ## Start development environment with organized paths
	@echo -e "$(GREEN)🔧 Starting BoilerFab development environment...$(NC)"
	@$(COMPOSE) -f $(COMPOSE_DEV_FILE) up -d
	@echo -e "$(GREEN)✅ Development environment ready!$(NC)"
	@echo -e "   📊 API: http://localhost:8000"
	@echo -e "   📚 Docs: http://localhost:8000/docs"

prod: ## Start production environment
	@echo -e "$(GREEN)🚀 Starting BoilerFab production environment...$(NC)"
	@$(COMPOSE) -f $(COMPOSE_PROD_FILE) up -d
	@echo -e "$(GREEN)✅ Production environment ready!$(NC)"

# ======================================================================================
# VALIDATION
# ======================================================================================

validate-compose: ## Validate compose file syntax
	@echo -e "$(BLUE)Validating $(COMPOSE_FILE) syntax...$(NC)"
	@$(COMPOSE) config --quiet && echo -e "$(GREEN)✓ Compose file is valid$(NC)" || (echo -e "$(RED)✗ Compose file validation failed$(NC)" && exit 1)

check-running: ## Check which services are currently running
	@echo -e "$(BLUE)Checking running services for project $(PROJECT_NAME)...$(NC)"
	@_running=$$($(COMPOSE) ps --services --filter "status=running" 2>/dev/null); \
	if [ -z "$$_running" ]; then \
		echo -e "$(YELLOW)No services currently running.$(NC)"; \
	else \
		echo -e "$(GREEN)Running services:$(NC)"; \
		echo "$$_running" | sed 's/^/  - /'; \
	fi

# ======================================================================================
# CORE STACK MANAGEMENT
# ======================================================================================

up: validate-compose ## Start all services (Traefik + BoilerFab)
	@echo "🏭 Starting BoilerFab factory with Traefik..."
	$(COMPOSE) up -d
	@sleep 3
	@echo "✅ BoilerFab factory is operational!"
	@echo ""
	@echo "🌐 Access Points:"
	@echo "   🔥 BoilerFab API:    http://localhost:8090/api/v1/templates"
	@echo "   📚 Documentation:    http://localhost:8090/docs"
	@echo "   🛠️ Traefik Dashboard: http://localhost:8080"
	@echo "   📊 Service Health:   http://localhost:8090/health"
	@echo ""
	@echo "🎯 Quick Start:"
	@echo "   make get-api-key                    # Get your API key"
	@echo "   client/boilerfab-client list       # List templates"
	@echo "   make monitoring                     # Enable monitoring"

start: up ## Alias for up

down: ## Stop and remove all services and networks defined in the compose file
	@echo -e "$(RED)Shutting down services from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) down --remove-orphans
	@echo -e "$(GREEN)✓ Services stopped.$(NC)"

stop: ## Stop all services without removing them
	@echo -e "$(YELLOW)Stopping services for $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) stop $(service)
	@echo -e "$(GREEN)✓ Services stopped (containers preserved).$(NC)"

restart: ## Restart all services
	@echo -e "$(YELLOW)Restarting services...$(NC)"
	@$(COMPOSE) restart $(service)
	@echo -e "$(GREEN)✓ Services restarted.$(NC)"

re: down build up ## Rebuild images and restart all services

rere: down no-cache up ## Rebuild images without cache and restart all services

rebuild: re ## Alias for re

pull: ## Pull latest images from registry
	@echo -e "$(BLUE)Pulling latest images from registry...$(NC)"
	@$(COMPOSE) pull $(service)
	@echo -e "$(GREEN)✓ Images pulled.$(NC)"

# ======================================================================================
# BUILDING IMAGES
# ======================================================================================

build: validate-compose ## Build (or rebuild) images for specified service, or all if none specified
	@echo -e "$(BLUE)Building images for $(or $(service),all services) from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) build $(service)
	@echo -e "$(GREEN)✓ Build complete.$(NC)"

no-cache: validate-compose ## Build images without using cache for specified service, or all
	@echo -e "$(YELLOW)Building (no cache) for $(or $(service),all services) from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) build --no-cache $(service)
	@echo -e "$(GREEN)✓ Build complete.$(NC)"

# ======================================================================================
# INFORMATION & DEBUGGING
# ======================================================================================

status: ## Show status of running services
	@echo -e "$(BLUE)System Status for $(COMPOSE_FILE):$(NC)"
	@$(COMPOSE) ps $(service)

ps: status ## Alias for status

logs: ## Follow logs for specified service, or all if none specified
	@echo -e "$(BLUE)Tailing logs for $(or $(service),all services) from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) logs -f --tail="100" $(service)

health: ## Check health status of services
	@echo -e "$(BLUE)Health check for services:$(NC)"
	@for service in $$($(COMPOSE) ps --services 2>/dev/null); do \
		_health=$$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}no healthcheck{{end}}' "$$($(COMPOSE) ps -q $$service 2>/dev/null)" 2>/dev/null); \
		if [ "$$_health" = "healthy" ]; then \
			echo -e "  $(GREEN)✓$(NC) $$service: $$_health"; \
		elif [ "$$_health" = "unhealthy" ]; then \
			echo -e "  $(RED)✗$(NC) $$service: $$_health"; \
		else \
			echo -e "  $(YELLOW)○$(NC) $$service: $$_health"; \
		fi \
	done

config: validate-compose ## Validate and display effective Docker Compose configuration
	@echo -e "$(BLUE)Effective Configuration for $(COMPOSE_FILE):$(NC)"
	@$(COMPOSE) config

ssh: ## Get an interactive shell into a running service container
	@if [ -z "$(service)" ]; then \
		echo -e "$(RED)Error: Service name required. Usage: make ssh service=<service_name>$(NC)"; \
		exit 1; \
	fi
	@echo -e "$(GREEN)Connecting to $(service) from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) exec $(service) /bin/bash || $(COMPOSE) exec $(service) /bin/sh || echo -e "$(RED)Failed to find shell in $(service).$(NC)"

it: ssh ## Alias for ssh

exec: ## Execute a command in a running service container
	@if [ -z "$(service)" ] || [ -z "$(args)" ]; then \
		echo -e "$(RED)Error: Service name and command required. Usage: make exec service=<service_name> args=\"<command>\"$(NC)"; \
		exit 1; \
	fi
	@echo -e "$(GREEN)Executing in $(service) (from $(COMPOSE_FILE)): $(args)$(NC)"
	@$(COMPOSE) exec $(service) $(args)

# ======================================================================================
# TRAEFIK & MONITORING COMMANDS
# ======================================================================================

traefik: ## Open Traefik dashboard
	@echo "Opening Traefik dashboard..."
	@command -v xdg-open > /dev/null && xdg-open http://localhost:8080 || echo "Visit: http://localhost:8080"

get-api-key: ## Display API key for client usage
	@echo "BoilerFab API Key:"
	@if [ -f runtime/api_config.json ]; then \
		grep -o '"ftk_[^"]*"' runtime/api_config.json | head -1 | sed 's/"//g'; \
	elif [ -f api_config.json ]; then \
		grep -o '"ftk_[^"]*"' api_config.json | head -1 | sed 's/"//g'; \
	else \
		echo "No API key found. Start the service first: make up"; \
	fi

client-setup: ## Setup global CLI client
	@echo "Setting up BoilerFab CLI client..."
	@if [ -f client/install.sh ]; then \
		cd client && ./install.sh; \
	else \
		echo "Client installer not found. Please check client/ directory."; \
	fi
	@echo "CLI client setup complete! Use 'boilerfab-client --help'"

monitoring: ## Enable lightweight monitoring stack (Dozzle + Uptime Kuma)
	@echo "Starting lightweight monitoring stack..."
	$(COMPOSE) -f deployment/docker-compose.monitoring.yml up -d
	@sleep 3
	@echo "Monitoring stack is ready!"
	@echo ""
	@echo "Monitoring Access:"
	@echo "   Container Logs:   http://localhost:8090/logs"
	@echo "   Uptime Monitor:   http://localhost:8090/status" 
	@echo "   Metrics:          http://localhost:8090/metrics"
	@echo "   Traefik Metrics:  http://localhost:8080"

monitoring-down: ## Stop monitoring stack
	@echo "Stopping monitoring stack..."
	$(COMPOSE) -f deployment/docker-compose.monitoring.yml down

nginx-config: ## Generate Nginx Proxy Manager configuration
	@echo "Nginx Proxy Manager Configuration:"
	@echo ""
	@echo "Add these subdomains pointing to your server:"
	@echo "  boilerfab.yourdomain.com  -> http://your-server:8090"
	@echo "  traefik.yourdomain.com    -> http://your-server:8080"
	@echo "  logs.yourdomain.com       -> http://your-server:8090/logs"
	@echo "  status.yourdomain.com     -> http://your-server:8090/status"
	@echo ""
	@echo "Enable SSL in NPM for production!"

# ======================================================================================
# TESTING
# ======================================================================================

test: ## Run full test suite
	@echo "Running BoilerFab test suite..."
	@if [ -f scripts/test_suite.sh ]; then \
		./scripts/test_suite.sh; \
	else \
		echo "Running basic health checks..."; \
		make health; \
	fi

# ======================================================================================
# CLEANING & PRUNING
# ======================================================================================

clean: ## Remove stopped service containers and default network
	@echo -e "$(RED)Cleaning containers and networks from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) down --remove-orphans
	@echo -e "$(GREEN)✓ Clean complete.$(NC)"

fclean: ## Remove containers, networks, volumes, and images defined in compose file
	@echo -e "$(RED)Deep cleaning: containers, networks, volumes, and images from $(COMPOSE_FILE)...$(NC)"
	@read -p "This will remove ALL project data including volumes. Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) down --volumes --remove-orphans --rmi local; \
		echo -e "$(GREEN)✓ Deep clean complete.$(NC)"; \
	else \
		echo -e "$(YELLOW)Aborted.$(NC)"; \
	fi

prune: ## Prune all unused Docker resources (DANGEROUS - system-wide)
	@echo -e "$(RED)WARNING: This will prune ALL unused Docker resources system-wide!$(NC)"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker system prune -af --volumes; \
		docker builder prune -af; \
		echo -e "$(GREEN)✓ System prune complete.$(NC)"; \
	else \
		echo -e "$(YELLOW)Aborted.$(NC)"; \
	fi

# ======================================================================================
# VARIABLE HANDLING
# ======================================================================================
ifneq ($(file),)
    COMPOSE_FILE := $(file)
    COMPOSE := docker compose -f $(COMPOSE_FILE)
endif