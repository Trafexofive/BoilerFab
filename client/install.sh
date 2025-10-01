#!/bin/bash

# BoilerFab Client Installation Script
# Installs the standalone BoilerFab client for system-wide or user access

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Print functions
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_PATH="$SCRIPT_DIR/boilerfab-client"

# Check if client exists
if [[ ! -f "$CLIENT_PATH" ]]; then
    print_error "boilerfab-client not found at $CLIENT_PATH"
    exit 1
fi

print_info "BoilerFab Client Installer"
echo

# Installation options
echo "Installation options:"
echo "1. System-wide installation (/usr/local/bin) - requires sudo"
echo "2. User installation (~/.local/bin) - no sudo required"
echo "3. Current directory symlink (./boilerfab-client)"
echo "4. Custom path"
echo "5. Just show instructions"

read -p "Choose installation type (1-5): " choice

case $choice in
    1)
        print_info "Installing system-wide to /usr/local/bin..."
        if sudo cp "$CLIENT_PATH" /usr/local/bin/boilerfab-client; then
            sudo chmod +x /usr/local/bin/boilerfab-client
            print_success "Installed to /usr/local/bin/boilerfab-client"
            print_info "You can now run: boilerfab-client --help"
        else
            print_error "Installation failed"
            exit 1
        fi
        ;;
    2)
        print_info "Installing to user directory ~/.local/bin..."
        mkdir -p ~/.local/bin
        cp "$CLIENT_PATH" ~/.local/bin/boilerfab-client
        chmod +x ~/.local/bin/boilerfab-client
        print_success "Installed to ~/.local/bin/boilerfab-client"
        
        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
            print_info "~/.local/bin is already in your PATH"
            print_info "You can now run: boilerfab-client --help"
        else
            print_warning "~/.local/bin is not in your PATH"
            echo "Add this to your ~/.bashrc or ~/.zshrc:"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo
            print_info "After adding to PATH, run: boilerfab-client --help"
        fi
        ;;
    3)
        print_info "Creating symlink in current directory..."
        ln -sf "$CLIENT_PATH" ./boilerfab-client
        print_success "Created symlink: ./boilerfab-client"
        print_info "You can now run: ./boilerfab-client --help"
        ;;
    4)
        read -p "Enter custom installation path: " custom_path
        if [[ -z "$custom_path" ]]; then
            print_error "No path provided"
            exit 1
        fi
        
        # Expand ~ to home directory
        custom_path="${custom_path/#\~/$HOME}"
        
        print_info "Installing to $custom_path..."
        mkdir -p "$(dirname "$custom_path")"
        cp "$CLIENT_PATH" "$custom_path"
        chmod +x "$custom_path"
        print_success "Installed to $custom_path"
        print_info "Make sure $(dirname "$custom_path") is in your PATH"
        ;;
    5)
        echo
        print_info "Manual installation instructions:"
        echo
        echo "System-wide installation:"
        echo "  sudo cp $CLIENT_PATH /usr/local/bin/boilerfab-client"
        echo "  sudo chmod +x /usr/local/bin/boilerfab-client"
        echo
        echo "User installation:"
        echo "  mkdir -p ~/.local/bin"
        echo "  cp $CLIENT_PATH ~/.local/bin/boilerfab-client"
        echo "  chmod +x ~/.local/bin/boilerfab-client"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"  # Add to ~/.bashrc"
        echo
        echo "Direct usage:"
        echo "  $CLIENT_PATH --help"
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo
print_success "Installation completed!"
echo
print_info "Next steps:"
echo "1. Run: boilerfab-client setup    # Configure API key"
echo "2. Run: boilerfab-client health   # Test connection"
echo "3. Run: boilerfab-client list     # List templates"
echo
print_info "For help: boilerfab-client --help"