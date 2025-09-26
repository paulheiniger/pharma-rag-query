#!/bin/bash

# Pharmaceutical RAG System - SystemD Deployment Script

set -e

echo "🧬 Pharmaceutical RAG System - SystemD Deployment"
echo "=================================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root. Run as regular user with sudo access."
   exit 1
fi

# Create pharma-rag user
echo "👤 Creating pharma-rag user..."
sudo useradd -r -s /bin/false -d /opt/pharma-rag pharma-rag 2>/dev/null || echo "User already exists"

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/pharma-rag/{data,logs,cache}
sudo cp -r . /opt/pharma-rag/
sudo chown -R pharma-rag:pharma-rag /opt/pharma-rag

# Install Python and dependencies
echo "🐍 Setting up Python environment..."
cd /opt/pharma-rag
sudo -u pharma-rag python3 -m venv venv
sudo -u pharma-rag ./venv/bin/pip install -r requirements.txt

# Install additional production dependencies
sudo -u pharma-rag ./venv/bin/pip install aiohttp aiofiles

# Install systemd services
echo "🔧 Installing systemd services..."
sudo cp systemd/pharma-rag-main.service /etc/systemd/system/
sudo cp systemd/pharma-rag-upload.service /etc/systemd/system/

# Reload systemd and enable services
sudo systemctl daemon-reload
sudo systemctl enable pharma-rag-main.service
sudo systemctl enable pharma-rag-upload.service

# Start services
echo "🚀 Starting services..."
sudo systemctl start pharma-rag-upload.service
sleep 5
sudo systemctl start pharma-rag-main.service

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 15

# Check service status
echo "🔍 Checking service status..."
sudo systemctl status pharma-rag-main.service --no-pager
sudo systemctl status pharma-rag-upload.service --no-pager

# Health check
echo "🏥 Running health check..."
if curl -f http://localhost:8001/v1/health &> /dev/null; then
    echo "✅ Upload service is healthy!"
else
    echo "❌ Upload service health check failed"
fi

if curl -f http://localhost:8000/v1/pw_list_documents &> /dev/null; then
    echo "✅ RAG service is healthy!"
else
    echo "❌ RAG service health check failed"
fi

echo ""
echo "🎉 SystemD Deployment Complete!"
echo "================================="
echo "📡 RAG API: http://your-server-ip:8000/v1/pw_ai_answer"
echo "📁 Upload API: http://your-server-ip:8001/v1/upload"
echo "🔍 Health Check: http://your-server-ip:8001/v1/health"
echo ""
echo "📊 Monitor services:"
echo "sudo journalctl -u pharma-rag-main.service -f"
echo "sudo journalctl -u pharma-rag-upload.service -f"
echo ""
echo "🛑 Control services:"
echo "sudo systemctl stop/start/restart pharma-rag-main.service"
echo "sudo systemctl stop/start/restart pharma-rag-upload.service"