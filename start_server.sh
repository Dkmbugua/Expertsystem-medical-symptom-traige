#!/bin/bash
# Start the Medical Triage Expert System

set -e

echo "=================================="
echo "Medical Triage Expert System"
echo "Starting Local Server..."
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check if database exists
if [ ! -f "data.db" ]; then
    echo "Initializing database..."
    python3 seed_symptoms_rules.py
    echo "✓ Database initialized"
fi

# Stop any existing server
echo "Checking for existing server..."
pkill -f "python app.py" 2>/dev/null || true

# Start the server
echo ""
echo "=================================="
echo "Starting Flask Server..."
echo "=================================="
python3 app.py &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Check if server is running
if curl -s http://127.0.0.1:5000/health > /dev/null 2>&1; then
    echo ""
    echo "=================================="
    echo "✅ SERVER RUNNING SUCCESSFULLY!"
    echo "=================================="
    echo ""
    echo "🌐 Access the application:"
    echo "   Main App:    http://127.0.0.1:5000/simple.html"
    echo "   Admin Panel: http://127.0.0.1:5000/admin.html"
    echo "   Health:      http://127.0.0.1:5000/health"
    echo ""
    echo "📊 Expert System Components:"
    echo "   ✓ CLIPS Inference Engine loaded"
    echo "   ✓ Medical knowledge base (50+ rules)"
    echo "   ✓ Live hospital fetching (OpenStreetMap)"
    echo "   ✓ Interactive maps (Leaflet)"
    echo "   ✓ Geocoding with caching"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo "=================================="
    echo ""
    
    # Keep the script running
    wait $SERVER_PID
else
    echo "❌ Failed to start server"
    echo "Check the logs for errors"
    exit 1
fi
