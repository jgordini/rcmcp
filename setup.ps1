# Setup script for UAB Research Computing Documentation MCP Server (Windows)
# Run this script in PowerShell with: .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "UAB RC Documentation MCP Server Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check for Python
Write-Host "Checking for Python 3.10+..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
            Write-Host "❌ Python 3.10 or higher is required. Found: $pythonVersion" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Found $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.10 or higher." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check for uv
Write-Host "Checking for uv package manager..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version 2>&1
    Write-Host "✅ Found uv" -ForegroundColor Green
} catch {
    Write-Host "❌ uv is not installed." -ForegroundColor Red
    Write-Host "Installing uv..." -ForegroundColor Yellow
    
    try {
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        $uvVersion = uv --version 2>&1
        Write-Host "✅ uv installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install uv. Please install manually from: https://github.com/astral-sh/uv" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
uv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Run tests
Write-Host "Running tests to verify installation..." -ForegroundColor Yellow
python test_server.py
Write-Host ""

# Get absolute path
$scriptDir = $PSScriptRoot
$uvPath = (Get-Command uv).Source

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ All dependencies installed successfully" -ForegroundColor Green
Write-Host "✅ Tests passed" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure Claude Desktop with this MCP server"
Write-Host "2. Add the following to your Claude Desktop config:"
Write-Host ""
Write-Host "   File: $env:APPDATA\Claude\claude_desktop_config.json" -ForegroundColor Cyan
Write-Host ""
Write-Host "   {" -ForegroundColor Gray
Write-Host "     `"mcpServers`": {" -ForegroundColor Gray
Write-Host "       `"uab-research-computing`": {" -ForegroundColor Gray
Write-Host "         `"command`": `"$uvPath`"," -ForegroundColor Gray
Write-Host "         `"args`": [" -ForegroundColor Gray
Write-Host "           `"--directory`"," -ForegroundColor Gray
Write-Host "           `"$scriptDir`"," -ForegroundColor Gray
Write-Host "           `"run`"," -ForegroundColor Gray
Write-Host "           `"uab_docs_server.py`"" -ForegroundColor Gray
Write-Host "         ]" -ForegroundColor Gray
Write-Host "       }" -ForegroundColor Gray
Write-Host "     }" -ForegroundColor Gray
Write-Host "   }" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Restart Claude Desktop"
Write-Host "4. Look for the 🔌 icon to verify connection"
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Yellow
Write-Host "For configuration examples, see CLAUDE_DESKTOP_CONFIG.md" -ForegroundColor Yellow
Write-Host ""
