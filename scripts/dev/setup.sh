#!/bin/bash

# BoilerFab Development Setup Script (Organized Edition)
# Sets up development environment with organized directory structure

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

print_info "🏭 Setting up BoilerFab development environment (Organized Edition)..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { print_error "Docker is required"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { print_error "Docker Compose is required"; exit 1; }
command -v make >/dev/null 2>&1 || { print_error "Make is required"; exit 1; }

# Create environment file if it doesn't exist (organized path)
if [[ ! -f config/.env ]]; then
    print_info "Creating config/.env file from template..."
    cp config/.env.example config/.env
    print_success "Created config/.env file"
else
    print_info "config/.env file already exists"
fi

# Create necessary directories (organized structure)
print_info "Creating organized directory structure..."
mkdir -p runtime/{logs,backups} build config client deployment
print_success "Organized directories created"

# Set up git hooks if in git repository
if [[ -d .git ]]; then
    print_info "Setting up git hooks..."
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Auto-format code before commit (organized edition)
make format 2>/dev/null || echo "Formatting skipped (make format not available)"
EOF
    chmod +x .git/hooks/pre-commit
    print_success "Git hooks configured"
fi

# Install client globally for development (organized path)
print_info "Installing BoilerFab client for development..."
cd client && ./install.sh << 'EOF' || print_warning "Client installation failed (continuing anyway)"
2
EOF
cd ..

# Build development images (organized compose files)
print_info "Building development Docker images..."
make dev

print_success "🏭 Organized development environment setup complete!"
echo ""
print_info "🚀 Next steps:"
echo "  1. Start development: make dev"
echo "  2. Check health: make health"  
echo "  3. View logs: make logs"
echo "  4. Run tests: make test"
echo ""
print_info "📁 Organized structure:"
echo "  build/      - Build configurations"
echo "  config/     - All settings and configs"  
echo "  client/     - CLI tools and installers"
echo "  deployment/ - Docker Compose files"
echo "  runtime/    - Logs and runtime data"
echo ""
print_info "🏭 Factorio-approved organization activated!"
print_info "Run 'make help' to see organized commands."