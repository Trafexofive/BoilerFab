# ======================================================================================
# MISCELLANEOUS
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

COMPOSE_FILE ?= docker-compose.yml
COMPOSE_DEV_FILE ?= docker-compose.dev.yml
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
        format lint health pull push validate-compose check-running project-volumes project-networks

# ======================================================================================
# HELP & USAGE
# ======================================================================================

help:
	@echo -e "$(BLUE)========================================================================="
	@echo -e " Universal Docker Compose Makefile "
	@echo -e " Project: $(PROJECT_NAME)"
	@echo -e "=========================================================================$(NC)"
	@echo ""
	@echo -e "$(YELLOW)Usage: make [target] [service=SERVICE_NAME] [args=\"ARGS\"] [file=COMPOSE_FILE]$(NC)"
	@echo -e "  'service' specifies a single service for targets like logs, build, ssh, exec, inspect."
	@echo -e "  'args' specifies commands for 'exec'."
	@echo -e "  'file' specifies an alternative docker-compose file (default: docker-compose.yml)."
	@echo ""
	@echo -e "$(GREEN)Core Stack Management:$(NC)"
	@echo -e "  up                  - Start all services in detached mode (Alias: start)."
	@echo -e "  down                - Stop and remove all services and default network."
	@echo -e "  restart             - Restart all services (down + up)."
	@echo -e "  re                  - Rebuild images and restart all services (down + build + up)."
	@echo -e "  rere                - Rebuild images without cache and restart all services (down + no-cache + up)."
	@echo -e "  stop                - Stop all services without removing them."
	@echo -e "  pull                - Pull latest images from registry."
	@echo ""
	@echo -e "$(GREEN)Building Images:$(NC)"
	@echo -e "  build [service=<name>] - Build images (all or specific service)."
	@echo -e "  no-cache [service=<name>] - Build images without cache (all or specific service)."
	@echo ""
	@echo -e "$(GREEN)Information & Debugging:$(NC)"
	@echo -e "  status [service=<name>] - Show status of services (all or specific) (Alias: ps)."
	@echo -e "  logs [service=<name>]   - Follow logs (all or specific service)."
	@echo -e "  health [service=<name>] - Check health status of services."
	@echo -e "  config              - Validate and display effective Docker Compose configuration."
	@echo -e "  validate-compose    - Validate compose file syntax only."
	@echo -e "  check-running       - Check which services are currently running."
	@echo -e "  ssh service=<name>    - Get an interactive shell into a running service (Alias: it)."
	@echo -e "  exec service=<name> args=\"<cmd>\" - Execute a command in a running service."
	@echo -e "  inspect service=<name> - Inspect a running service container."
	@echo -e "  project-volumes     - List volumes for this project only."
	@echo -e "  project-networks    - List networks for this project only."
	@echo -e "  list-volumes        - List all Docker volumes."
	@echo -e "  list-networks       - List all Docker networks."
	@echo ""
	@echo -e "$(GREEN)Cleaning & Pruning:$(NC)"
	@echo -e "  clean               - Remove stopped service containers and default network."
	@echo -e "  fclean              - Remove containers, networks, volumes, and images."
	@echo -e "  prune               - Prune all unused Docker resources (DANGEROUS)."
	@echo ""
	@echo -e "$(YELLOW)Examples:$(NC)"
	@echo -e "  make up"
	@echo -e "  make logs service=backend"
	@echo -e "  make ssh service=backend"
	@echo -e "  make exec service=backend args=\"ls -la\""
	@echo -e "  make build file=docker-compose.dev.yml"
	@echo -e "$(BLUE)========================================================================="
	@echo -e " Help Section End "
	@echo -e "=========================================================================$(NC)"

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

up: validate-compose ## Start all services in detached mode
	@echo -e "$(GREEN)Starting services from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) up -d --remove-orphans $(service)
	@echo -e "$(GREEN)✓ Services are now running in detached mode.$(NC)"

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

inspect: ## Inspect a running service container
	@if [ -z "$(service)" ]; then \
		echo -e "$(RED)Error: Service name required. Usage: make inspect service=<service_name>$(NC)"; \
		exit 1; \
	fi
	@echo -e "$(BLUE)Inspecting $(service) (from $(COMPOSE_FILE))...$(NC)"
	@_container_id=$$($(COMPOSE) ps -q $(service) | head -n 1); \
	if [ -z "$$_container_id" ]; then \
		echo -e "$(RED)Service $(service) not found or not running.$(NC)"; \
		exit 1; \
	fi; \
	docker inspect $$_container_id

project-volumes: ## List volumes for this project only
	@echo -e "$(BLUE)Volumes for project $(PROJECT_NAME):$(NC)"
	@docker volume ls --filter label=com.docker.compose.project=$(PROJECT_NAME) --format "table {{.Driver}}\t{{.Name}}"

project-networks: ## List networks for this project only
	@echo -e "$(BLUE)Networks for project $(PROJECT_NAME):$(NC)"
	@docker network ls --filter label=com.docker.compose.project=$(PROJECT_NAME) --format "table {{.Driver}}\t{{.Name}}\t{{.Scope}}"

list-volumes: ## List all Docker volumes
	@echo -e "$(BLUE)All Docker Volumes:$(NC)"
	@docker volume ls

list-networks: ## List all Docker networks
	@echo -e "$(BLUE)All Docker Networks:$(NC)"
	@docker network ls

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
# APPLICATION SPECIFIC TARGETS (Commented out - uncomment and customize as needed)
# ======================================================================================

# backend: ## Start only backend service
# 	@$(COMPOSE) up -d --build backend && make logs service=backend

# ======================================================================================
# NPM/Language SCRIPTS (Commented out - uncomment and customize as needed)
# ======================================================================================

# format: ## Run code formatting
# 	@echo -e "$(YELLOW)Formatting code...$(NC)"
# 	@npm run format

# lint: ## Run linter
# 	@echo -e "$(YELLOW)Linting code...$(NC)"
# 	@npm run lint

# ======================================================================================
# VARIABLE HANDLING
# ======================================================================================
ifneq ($(file),)
    COMPOSE_FILE := $(file)
    COMPOSE := docker compose -f $(COMPOSE_FILE)
endif
