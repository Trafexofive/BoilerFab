# ======================================================================================
# {{PROJECT_NAME}} - Universal Docker Compose Makefile
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
	@echo -e " {{PROJECT_NAME}} - Universal Docker Compose Makefile "
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
	@echo -e "$(GREEN){{PROJECT_NAME}} Specific:$(NC)"
	@echo -e "  api-gateway         - Start API gateway service only."
	@echo -e "  auth-service        - Start authentication service only."
	@echo -e "  web-client          - Start web client service only."
	@echo -e "  test                - Run all tests."
	@echo -e "  format              - Format all code."
	@echo -e "  lint                - Run linting on all code."
	@echo ""
	@echo -e "$(GREEN)Cleaning & Pruning:$(NC)"
	@echo -e "  clean               - Remove stopped service containers and default network."
	@echo -e "  fclean              - Remove containers, networks, volumes, and images."
	@echo -e "  prune               - Prune all unused Docker resources (DANGEROUS)."
	@echo ""
	@echo -e "$(YELLOW)Examples:$(NC)"
	@echo -e "  make up"
	@echo -e "  make logs service=api-gateway"
	@echo -e "  make ssh service=auth-service"
	@echo -e "  make exec service=api-gateway args=\"ls -la\""
	@echo -e "  make build file=docker-compose.dev.yml"
	@echo -e "$(BLUE)========================================================================="
	@echo -e " Help Section End "
	@echo -e "=========================================================================$(NC)"

# ======================================================================================
# CORE STACK MANAGEMENT
# ======================================================================================

validate-compose: ## Validate compose file syntax
	@echo -e "$(BLUE)Validating $(COMPOSE_FILE) syntax...$(NC)"
	@$(COMPOSE) config --quiet && echo -e "$(GREEN)✓ Compose file is valid$(NC)" || (echo -e "$(RED)✗ Compose file validation failed$(NC)" && exit 1)

up: validate-compose ## Start all services in detached mode
	@echo -e "$(GREEN)Starting all services from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) up -d
	@echo -e "$(GREEN)✓ All services started. Use 'make logs' to view logs.$(NC)"

start: up ## Alias for up

down: ## Stop and remove all services and default network
	@echo -e "$(YELLOW)Stopping all services from $(COMPOSE_FILE)...$(NC)"
	@$(COMPOSE) down --remove-orphans
	@echo -e "$(GREEN)✓ All services stopped and removed.$(NC)"

restart: ## Restart all services (down + up)
	@echo -e "$(YELLOW)Restarting all services...$(NC)"
	@$(MAKE) down
	@$(MAKE) up
	@echo -e "$(GREEN)✓ All services restarted.$(NC)"

pull: ## Pull latest images from registry
	@echo -e "$(BLUE)Pulling latest images...$(NC)"
	@$(COMPOSE) pull
	@echo -e "$(GREEN)✓ Images updated.$(NC)"

stop: ## Stop all services without removing them
	@echo -e "$(YELLOW)Stopping services without removing...$(NC)"
	@$(COMPOSE) stop
	@echo -e "$(GREEN)✓ Services stopped.$(NC)"

# ======================================================================================
# {{PROJECT_NAME}} SPECIFIC SERVICES
# ======================================================================================

api-gateway: ## Start API gateway service only
	@echo -e "$(GREEN)Starting API gateway service...$(NC)"
	@$(COMPOSE) up -d --build api-gateway && make logs service=api-gateway

auth-service: ## Start authentication service only
	@echo -e "$(GREEN)Starting authentication service...$(NC)"
	@$(COMPOSE) up -d --build auth-service && make logs service=auth-service

web-client: ## Start web client service only
	@echo -e "$(GREEN)Starting web client service...$(NC)"
	@$(COMPOSE) up -d --build web-client && make logs service=web-client

# ======================================================================================
# DEVELOPMENT & TESTING
# ======================================================================================

test: ## Run all tests
	@echo -e "$(YELLOW)Running all tests...$(NC)"
	@$(COMPOSE) exec api-gateway python -m pytest tests/ -v
	@echo -e "$(GREEN)✓ All tests completed.$(NC)"

format: ## Format all code
	@echo -e "$(YELLOW)Formatting code...$(NC)"
	@$(COMPOSE) exec api-gateway black .
	@$(COMPOSE) exec auth-service black .
	@echo -e "$(GREEN)✓ Code formatting completed.$(NC)"

lint: ## Run linting on all code
	@echo -e "$(YELLOW)Linting code...$(NC)"
	@$(COMPOSE) exec api-gateway flake8 .
	@$(COMPOSE) exec auth-service flake8 .
	@echo -e "$(GREEN)✓ Linting completed.$(NC)"

# Include the rest of the universal makefile functionality...
# (Rest of the makefile content from MYSTARTERMAKEFILE)

# ======================================================================================
# VARIABLE HANDLING
# ======================================================================================
ifneq ($(file),)
    COMPOSE_FILE := $(file)
    COMPOSE := docker compose -f $(COMPOSE_FILE)
endif