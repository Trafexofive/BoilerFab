#!/bin/bash

# Simple BoilerFab Monitoring Script (Organized Edition)
# Lightweight monitoring for organized repository structure

set -euo pipefail

# Colors  
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

API_URL="http://localhost:8000"
TIMEOUT=5

check_service() {
    local service_name="$1"
    local endpoint="$2"
    local expected_code="${3:-200}"
    
    if curl -s -f --max-time $TIMEOUT "$endpoint" > /dev/null 2>&1; then
        print_success "$service_name is healthy"
        return 0
    else
        print_error "$service_name is not responding"
        return 1
    fi
}

check_docker_service() {
    local service_name="$1"
    # Use organized compose file path
    if docker-compose -f deployment/docker-compose.yml ps --services --filter status=running | grep -q "^${service_name}$"; then
        print_success "Docker service $service_name is running"
        return 0
    else
        print_error "Docker service $service_name is not running"
        return 1
    fi
}

show_resource_usage() {
    print_info "Container resource usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" $(docker-compose -f deployment/docker-compose.yml ps -q) 2>/dev/null || print_warning "No containers running"
}

show_logs_summary() {
    print_info "Recent log summary (last 10 lines):"
    docker-compose -f deployment/docker-compose.yml logs --tail=10 2>/dev/null || print_warning "No logs available"
}

show_organized_structure() {
    print_info "🏭 Organized structure status:"
    echo "  📁 build/      - $(ls -1 build/ 2>/dev/null | wc -l || echo 0) files"
    echo "  📁 config/     - $(ls -1 config/ 2>/dev/null | wc -l || echo 0) files"  
    echo "  📁 client/     - $(ls -1 client/ 2>/dev/null | wc -l || echo 0) files"
    echo "  📁 deployment/ - $(ls -1 deployment/ 2>/dev/null | wc -l || echo 0) files"
    echo "  📁 runtime/    - $(find runtime/ -type f 2>/dev/null | wc -l || echo 0) files"
}

main() {
    print_info "🔍 BoilerFab Health Check (Organized Edition) - $(date)"
    echo ""
    
    # Check main service
    if check_service "BoilerFab API" "$API_URL/health"; then
        # Get additional service info
        response=$(curl -s --max-time $TIMEOUT "$API_URL/health" 2>/dev/null)
        if [[ -n "$response" ]]; then
            echo "   Response: $response"
        fi
    fi
    
    check_service "BoilerFab Root" "$API_URL/"
    
    echo ""
    print_info "Docker services status:"
    check_docker_service "boilerfab-service"
    
    # Check optional services
    if docker-compose -f deployment/docker-compose.yml ps --services --filter status=running | grep -q "redis"; then
        check_docker_service "redis"
    fi
    
    if docker-compose -f deployment/docker-compose.yml ps --services --filter status=running | grep -q "postgres"; then
        check_docker_service "postgres" 
    fi
    
    echo ""
    
    # Show organized structure
    if [[ "${1:-}" == "--structure" || "${1:-}" == "-s" ]]; then
        show_organized_structure
        echo ""
    fi
    
    # Show resource usage if requested
    if [[ "${1:-}" == "--detailed" || "${1:-}" == "-d" ]]; then
        show_resource_usage
        echo ""
        show_logs_summary
        echo ""
        show_organized_structure
    fi
    
    echo ""
    print_info "💡 Tips (Organized Edition):"
    echo "  - Run with --detailed for resource usage and logs"
    echo "  - Run with --structure to see organized directory status" 
    echo "  - Use 'make dev' for development environment"
    echo "  - Use 'make prod' for production environment"
    echo "  - Use 'make monitoring' for web dashboards"
    echo "  - Logs are in runtime/logs/"
    echo "  - Configs are in config/"
}

# Check if we're in the right directory (organized edition)
if [[ ! -f deployment/docker-compose.yml ]]; then
    print_error "deployment/docker-compose.yml not found. Run this from the BoilerFab root directory."
    print_info "Expected organized structure with deployment/ directory."
    exit 1
fi

main "$@"