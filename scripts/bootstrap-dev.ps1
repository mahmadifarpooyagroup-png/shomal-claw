$ErrorActionPreference = "Stop"

Write-Host "=== Shomal / Atrin development bootstrap ===" -ForegroundColor Cyan
Write-Host "This script guides you through the development environment setup."
Write-Host ""
Write-Host "IMPORTANT: Frappe Bench requires a Linux environment."
Write-Host "On Windows, use WSL2 Ubuntu (not native Windows Python)."
Write-Host ""

# =============================================================================
# Pre-flight checks
# =============================================================================
$allOk = $true

# Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[MISSING] Git" -ForegroundColor Red
    $allOk = $false
} else {
    Write-Host "[OK] Git: $(git --version)" -ForegroundColor Green
}

# Check WSL
$wslAvailable = $false
try {
    $wslStatus = wsl --status 2>&1
    if ($LASTEXITCODE -eq 0) {
        $wslAvailable = $true
        Write-Host "[OK] WSL detected" -ForegroundColor Green
        Write-Host "     $($wslStatus | Select-Object -First 2)"
    } else {
        Write-Host "[MISSING] WSL2" -ForegroundColor Red
        $allOk = $false
    }
} catch {
    Write-Host "[MISSING] WSL2" -ForegroundColor Red
    $allOk = $false
}

if (-not $allOk) {
    Write-Host ""
    Write-Host "Please install the missing prerequisites before continuing." -ForegroundColor Yellow
    Write-Host "  - Git: https://git-scm.com/download/win"
    Write-Host "  - WSL2: wsl --install (from Admin PowerShell)"
    exit 1
}

# =============================================================================
# Target versions (synced with docs/development/VERSION-PINS.md)
# =============================================================================
$FRAPPE_BRANCH = "version-15"
$PYTHON_VERSION = "3.12"
$NODE_VERSION = "18"

Write-Host ""
Write-Host "Target versions:" -ForegroundColor Cyan
Write-Host "  Frappe : $FRAPPE_BRANCH"
Write-Host "  Python : $PYTHON_VERSION"
Write-Host "  Node   : $NODE_VERSION"
Write-Host ""

# =============================================================================
# WSL Setup Instructions
# =============================================================================
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Step 1: Copy setup script to WSL"
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The detailed setup script is at: scripts/setup-wsl.sh"
Write-Host ""
Write-Host "Run these commands in WSL Ubuntu:"
Write-Host ""
Write-Host "  # Navigate to the project (assuming repo is cloned in WSL)"
Write-Host "  cd ~/projects/shomal"
Write-Host ""
Write-Host "  # Make the script executable and run it"
Write-Host "  chmod +x scripts/setup-wsl.sh"
Write-Host "  ./scripts/setup-wsl.sh"
Write-Host ""
Write-Host "This will install:"
Write-Host "  - System dependencies (MariaDB, Redis, Node.js)"
Write-Host "  - Frappe Bench $FRAPPE_BRANCH"
Write-Host "  - ERPNext $FRAPPE_BRANCH"
Write-Host "  - Frappe Helpdesk"
Write-Host "  - Atrin application"
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Step 2: Start development"
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  cd ~/frappe-bench"
Write-Host "  bench start"
Write-Host ""
Write-Host "Then open: http://shomal.local:8000"
Write-Host "Credentials: Administrator / admin"
Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Step 3: Verify ERPNext + Helpdesk"
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  bench --site shomal.local console"
Write-Host "  >>> import frappe"
Write-Host "  >>> print(frappe.db.exists('DocType', 'Appointment'))  # should return truthy"
Write-Host "  >>> print(frappe.db.exists('DocType', 'HD Ticket'))     # should return truthy"
Write-Host ""
Write-Host "After verification, the Atrin integration layer can be implemented."
Write-Host ""
