#!/bin/bash

# Pharmaceutical RAG System - Production Deployment Script
# Run this script on your server to deploy the system

set -e  # Exit on any error

echo "🧬 Pharmaceutical RAG System - Production Deployment"
echo "====================================================="

    exit 1
fi

fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p data logs cache

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating environment configuration..."
    cat > .env << EOF
# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://imllm.intermesh.net/v1

# Application Configuration
PATHWAY_HOST=0.0.0.0
PATHWAY_PORT=8000
UPLOAD_PORT=8001
PYTHONUNBUFFERED=1

# Security
MAX_UPLOAD_SIZE=100MB
ALLOWED_EXTENSIONS=.pdf,.txt,.doc,.docx

# Logging
LOG_LEVEL=INFO
EOF
    echo "⚠️  Please edit .env file with your actual OpenRouter API key!"
fi

# Build and deploy

echo "🚀 Starting services..."

echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🔍 Checking service health..."
if curl -f http://localhost/health &> /dev/null; then
    echo "✅ Services are healthy!"
else
    echo "❌ Health check failed. Checking logs..."
    exit 1
fi

echo ""
echo "🎉 Deployment Complete!"
echo "====================================="
echo "📡 RAG API Endpoint: http://your-server-ip/v1/pw_ai_answer"
echo "📁 Upload Endpoint: http://your-server-ip/v1/upload"
echo "🔍 Health Check: http://your-server-ip/health"
echo ""
echo "📋 Usage Examples:"
echo "# Upload a document:"
echo "curl -X POST -F 'file=@document.pdf' http://your-server-ip/v1/upload"
echo ""
echo "# Query the system:"
echo "curl -X POST http://your-server-ip/v1/pw_ai_answer \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"prompt\": \"What drugs are banned?\"}'"
echo ""
echo "📊 Monitor logs:"
echo ""
echo "🛑 Stop services:"
