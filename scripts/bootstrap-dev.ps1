$ErrorActionPreference = "Stop"

Write-Host "=== Shomal / Atrin development bootstrap ===" -ForegroundColor Cyan
Write-Host "This script prepares a Frappe Bench and creates the Atrin app."
Write-Host ""

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required. Install Git first."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is required. Install a Frappe-supported Python version first."
}

Write-Host "Detected Git: $(git --version)"
Write-Host "Detected Python: $(python --version)"
Write-Host ""
Write-Host "Frappe Bench is normally run in a Linux-based environment."
Write-Host "For Windows, use WSL2 Ubuntu rather than native Windows Python."
Write-Host ""
Write-Host "Next commands (run inside WSL2 Ubuntu):"
Write-Host "  cd ~"
Write-Host "  python3 -m venv ~/shomal-venv"
Write-Host "  source ~/shomal-venv/bin/activate"
Write-Host "  pip install frappe-bench"
Write-Host "  bench init --frappe-branch version-15 ~/shomal-bench"
Write-Host "  cd ~/shomal-bench"
Write-Host "  bench new-site shomal.local"
Write-Host "  bench get-app https://github.com/mahmadifarpooyagroup-png/shomal.git"
Write-Host "  bench start"
