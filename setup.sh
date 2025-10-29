#!/bin/bash
# Setup script for UAB Research Computing Documentation MCP Server
# This script automates the installation and configuration process

set -e  # Exit on error

echo "=========================================="
echo "UAB RC Documentation MCP Server Setup"
echo "=========================================="
echo ""

# Check for Python
echo "Checking for Python 3.10+..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ Python 3.10 or higher is required. Found: $(python3 --version)"
    exit 1
fi

echo "✅ Found Python $(python3 --version)"
echo ""

# Check for uv
echo "Checking for uv package manager..."
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed."
    echo "Installing uv..."
    
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "Please install uv manually from: https://github.com/astral-sh/uv"
        exit 1
    fi
    
    # Source the shell configuration to get uv in PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    if ! command -v uv &> /dev/null; then
        echo "❌ uv installation failed. Please install manually and try again."
        exit 1
    fi
fi

echo "✅ Found uv"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
uv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
uv pip install -e .
echo "✅ Dependencies installed"
echo ""

# Run tests
echo "Running tests to verify installation..."
python test_server.py
echo ""

# Get absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
UV_PATH=$(which uv)

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "✅ All dependencies installed successfully"
echo "✅ Tests passed"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Claude Desktop with this MCP server"
echo "2. Add the following to your Claude Desktop config:"
echo ""
echo "   File: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "   {"
echo "     \"mcpServers\": {"
echo "       \"uab-research-computing\": {"
echo "         \"command\": \"$UV_PATH\","
echo "         \"args\": ["
echo "           \"--directory\","
echo "           \"$SCRIPT_DIR\","
echo "           \"run\","
echo "           \"uab_docs_server.py\""
echo "         ]"
echo "       }"
echo "     }"
echo "   }"
echo ""
echo "3. Restart Claude Desktop"
echo "4. Look for the 🔌 icon to verify connection"
echo ""
echo "For detailed instructions, see README.md"
echo "For configuration examples, see CLAUDE_DESKTOP_CONFIG.md"
echo ""
