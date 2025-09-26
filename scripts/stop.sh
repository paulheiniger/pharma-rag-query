#!/bin/bash

# Stop pharma RAG system services
echo "🛑 Stopping Pharmaceutical RAG System..."

# Read PIDs if they exist
if [ -f "logs/upload.pid" ]; then
    UPLOAD_PID=$(cat logs/upload.pid)
    if kill -0 $UPLOAD_PID 2>/dev/null; then
        kill $UPLOAD_PID
        echo "✅ Upload server stopped (PID: $UPLOAD_PID)"
    fi
    rm -f logs/upload.pid
fi

if [ -f "logs/rag.pid" ]; then
    RAG_PID=$(cat logs/rag.pid)
    if kill -0 $RAG_PID 2>/dev/null; then
        kill $RAG_PID
        echo "✅ RAG server stopped (PID: $RAG_PID)"
    fi
    rm -f logs/rag.pid
fi

# Fallback: kill by process name
pkill -f "upload_server.py" 2>/dev/null && echo "✅ Upload server processes killed"
pkill -f "app_openrouter.py" 2>/dev/null && echo "✅ RAG server processes killed"

echo "🔚 All services stopped"