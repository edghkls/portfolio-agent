# Start Dynamic Portfolio Optimization Agent
# This script activates the virtual environment and starts the Flask app

Write-Host "======================================================================"
Write-Host "Starting Portfolio Optimization Agent" -ForegroundColor Cyan
Write-Host "======================================================================"
Write-Host ""

# Get the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if venv exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"

# Check if required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Gray
try {
    python -c "import flask" 2>$null
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Set PYTHONPATH for proper imports
$env:PYTHONPATH = "."

# Display startup information
Write-Host ""
Write-Host "======================================================================"
Write-Host "Portfolio Agent starting on http://localhost:5000" -ForegroundColor Green
Write-Host "======================================================================"
Write-Host ""
Write-Host "Access the dashboard at:" -ForegroundColor Cyan
Write-Host "  Local:   http://localhost:5000" -ForegroundColor White
Write-Host "  Network: http://$env:COMPUTERNAME`:5000" -ForegroundColor White
Write-Host ""
Write-Host "Available Features:" -ForegroundColor Cyan
Write-Host "  • Dashboard - Portfolio overview & KPIs"
Write-Host "  • Portfolio - Treaty details & filtering"
Write-Host "  • Scenarios - Monte Carlo & stress tests"
Write-Host "  • Recommendations - Optimization suggestions"
Write-Host "  • Reports - Generate reports"
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the agent
python web_ui/app.py
