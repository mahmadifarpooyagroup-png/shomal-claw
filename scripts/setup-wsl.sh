#!/usr/bin/env bash
# =============================================================================
# Shomal / Atrin — WSL Development Environment Setup
# =============================================================================
# Run this script inside WSL2 Ubuntu to set up the complete development stack.
#
# Usage:
#   chmod +x scripts/setup-wsl.sh
#   ./scripts/setup-wsl.sh
#
# Prerequisites: WSL2 Ubuntu with sudo access.
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${CYAN}[SETUP]${NC} $*"; }
ok()   { echo -e "${GREEN}[OK]${NC}    $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()  { echo -e "${RED}[ERR]${NC}   $*"; exit 1; }

# ---------------------------------------------------------------------------
# Step 0 — Detect environment
# ---------------------------------------------------------------------------
log "Detecting environment..."

if ! grep -qi microsoft /proc/version 2>/dev/null; then
    warn "This does not appear to be WSL. The script is designed for WSL2 Ubuntu."
    warn "Continuing anyway, but some paths may differ."
fi

BENCH_DIR="${HOME}/frappe-bench"
SITE_NAME="shomal.local"
MARIADB_ROOT_PASS="${MARIADB_ROOT_PASS:-admin}"
SHOMAL_REPO="https://github.com/mahmadifarpooyagroup-png/shomal.git"
FRAPPE_BRANCH="version-15"

# ---------------------------------------------------------------------------
# Step 1 — System dependencies
# ---------------------------------------------------------------------------
log "Step 1/8 — Installing system dependencies..."

sudo apt update -qq

sudo apt install -y -qq \
    git \
    python3 python3-pip python3-venv python3-dev \
    mariadb-server mariadb-client libmariadb-dev \
    redis-server \
    nodejs npm \
    curl wget \
    xvfb libfontconfig \
    build-essential \
    libssl-dev \
    wkhtmltopdf

# Ensure Node 18 is available (Frappe 15 requirement)
NODE_MAJOR=$(node -v 2>/dev/null | cut -d. -f1 | tr -d 'v' || echo "0")
if [ "$NODE_MAJOR" -lt 18 ]; then
    warn "Node version $(node -v) is older than 18. Installing Node 18 via n..."
    npm install -g n 2>/dev/null || true
    sudo n 18 2>/dev/null || {
        warn "Could not install Node 18 via n. Please install manually."
    }
fi

sudo npm install -g yarn 2>/dev/null || true

ok "System dependencies installed."

# ---------------------------------------------------------------------------
# Step 2 — Start services
# ---------------------------------------------------------------------------
log "Step 2/8 — Starting MariaDB and Redis..."

sudo service mariadb start 2>/dev/null || sudo systemctl start mariadb 2>/dev/null || true
sudo service redis-server start 2>/dev/null || sudo systemctl start redis-server 2>/dev/null || true

# Ensure MariaDB root password
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '${MARIADB_ROOT_PASS}'; FLUSH PRIVILEGES;" 2>/dev/null || true

ok "Services started."

# ---------------------------------------------------------------------------
# Step 3 — Install Frappe Bench
# ---------------------------------------------------------------------------
log "Step 3/8 — Installing Frappe Bench..."

python3 -m pip install --user --upgrade pip setuptools wheel
python3 -m pip install --user frappe-bench

# Ensure bench is on PATH
export PATH="${HOME}/.local/bin:${PATH}"

bench --version || err "Frappe Bench installation failed. Check PATH."

ok "Frappe Bench $(bench --version) installed."

# ---------------------------------------------------------------------------
# Step 4 — Initialize Bench
# ---------------------------------------------------------------------------
log "Step 4/8 — Initializing Frappe Bench (branch: ${FRAPPE_BRANCH})..."

if [ -d "${BENCH_DIR}" ]; then
    warn "Bench directory already exists: ${BENCH_DIR}"
    warn "Skipping bench init. Remove the directory if you want a fresh init."
else
    bench init --frappe-branch "${FRAPPE_BRANCH}" "${BENCH_DIR}"
    ok "Bench initialized at ${BENCH_DIR}"
fi

cd "${BENCH_DIR}"

# ---------------------------------------------------------------------------
# Step 5 — Create site
# ---------------------------------------------------------------------------
log "Step 5/8 — Creating site: ${SITE_NAME}..."

if bench list-sites 2>/dev/null | grep -q "${SITE_NAME}"; then
    warn "Site ${SITE_NAME} already exists. Skipping creation."
else
    bench new-site "${SITE_NAME}" \
        --mariadb-root-password "${MARIADB_ROOT_PASS}" \
        --admin-password admin \
        --no-mariadb-socket
    ok "Site ${SITE_NAME} created."
fi

bench use "${SITE_NAME}"

# ---------------------------------------------------------------------------
# Step 6 — Install ERPNext and Helpdesk
# ---------------------------------------------------------------------------
log "Step 6/8 — Installing ERPNext and Frappe Helpdesk..."

# ERPNext
if bench list-apps 2>/dev/null | grep -q "^erpnext$"; then
    warn "ERPNext already installed. Skipping."
else
    bench get-app --branch "${FRAPPE_BRANCH}" erpnext
    bench --site "${SITE_NAME}" install-app erpnext
    ok "ERPNext installed."
fi

# Helpdesk
if bench list-apps 2>/dev/null | grep -q "^helpdesk$"; then
    warn "Helpdesk already installed. Skipping."
else
    bench get-app helpdesk
    bench --site "${SITE_NAME}" install-app helpdesk
    ok "Frappe Helpdesk installed."
fi

# ---------------------------------------------------------------------------
# Step 7 — Install Atrin app
# ---------------------------------------------------------------------------
log "Step 7/8 — Installing Atrin application..."

if bench list-apps 2>/dev/null | grep -q "^atrin$"; then
    warn "Atrin already installed. Skipping."
else
    bench get-app "${SHOMAL_REPO}"
    bench --site "${SITE_NAME}" install-app atrin
    ok "Atrin installed."
fi

# ---------------------------------------------------------------------------
# Step 8 — Migrate and verify
# ---------------------------------------------------------------------------
log "Step 8/8 — Running migrations..."

bench --site "${SITE_NAME}" migrate

ok "Migrations complete."

# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
log "=============================================="
log "Verification"
log "=============================================="

echo ""
echo "  Bench version : $(bench version)"
echo "  Site          : ${SITE_NAME}"
echo "  Apps          :"
bench --site "${SITE_NAME}" list-apps 2>/dev/null | sed 's/^/    - /'
echo ""
echo "  Start command : cd ${BENCH_DIR} && bench start"
echo ""

# Check critical DocTypes
log "Checking critical upstream DocTypes..."
bench --site "${SITE_NAME}" console <<EOF 2>/dev/null || true
import frappe
for dt in ["Appointment", "HD Ticket"]:
    exists = frappe.db.exists("DocType", dt)
    print(f"  {dt}: {'EXISTS' if exists else 'MISSING — verify installation'}")
EOF

ok "=============================================="
ok "Setup complete!"
ok "Run: cd ${BENCH_DIR} && bench start"
ok "Then open: http://shomal.local:8000"
ok "=============================================="
