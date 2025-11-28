#!/bin/bash
# Cleanup Script - Remove Redundant Files
# This script moves redundant files to a backup folder instead of deleting

set -e

echo "=================================="
echo "Medical Triage Expert System"
echo "Cleanup Script"
echo "=================================="
echo ""

BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"

# Create backup directory
echo "Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Move redundant documentation files
echo "Moving redundant documentation files..."
[ -f "ADMIN_GUIDE.md" ] && mv "ADMIN_GUIDE.md" "$BACKUP_DIR/" && echo "  ✓ Moved ADMIN_GUIDE.md"
[ -f "HOW_TO_USE.md" ] && mv "HOW_TO_USE.md" "$BACKUP_DIR/" && echo "  ✓ Moved HOW_TO_USE.md"
[ -f "USER_GUIDE.md" ] && mv "USER_GUIDE.md" "$BACKUP_DIR/" && echo "  ✓ Moved USER_GUIDE.md"
[ -f "SYSTEM_READY.md" ] && mv "SYSTEM_READY.md" "$BACKUP_DIR/" && echo "  ✓ Moved SYSTEM_READY.md"

# Move old/unused files
echo "Moving old/unused files..."
[ -f "index.html" ] && mv "index.html" "$BACKUP_DIR/" && echo "  ✓ Moved index.html (root)"
[ -f "TriageApp.jsx" ] && mv "TriageApp.jsx" "$BACKUP_DIR/" && echo "  ✓ Moved TriageApp.jsx"
[ -f "static/index.html" ] && mv "static/index.html" "$BACKUP_DIR/" && echo "  ✓ Moved static/index.html"

# Move log files (they'll regenerate)
echo "Moving old log files..."
[ -f "alerts.log" ] && mv "alerts.log" "$BACKUP_DIR/" && echo "  ✓ Moved alerts.log"
[ -f "server.log" ] && mv "server.log" "$BACKUP_DIR/" && echo "  ✓ Moved server.log"

echo ""
echo "=================================="
echo "Cleanup Complete!"
echo "=================================="
echo ""
echo "Redundant files moved to: $BACKUP_DIR"
echo ""
echo "Essential files retained:"
echo "  ✓ app.py - Flask backend"
echo "  ✓ db.py - Database layer"
echo "  ✓ location_service.py - Location services"
echo "  ✓ knowledge_base/ - CLIPS rules (EXPERT SYSTEM BRAIN)"
echo "  ✓ static/simple.html - Main UI"
echo "  ✓ static/admin.html - Admin panel"
echo "  ✓ data.db - Database"
echo "  ✓ README.md - Documentation"
echo ""
echo "If you need any backed-up files, they're in: $BACKUP_DIR"
echo ""
