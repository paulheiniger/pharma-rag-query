# 🚀 Deployment Guide - Pharmaceutical Compliance RAG System

This comprehensive guide covers all deployment scenarios for the Government Pharmaceutical Compliance RAG System.

## 📋 Deployment Overview

### Deployment Options
1. **Development**: Local development environment
2. **Production**: Single server deployment  
4. **Cloud**: AWS/GCP/Azure cloud deployment
5. **Systemd**: Linux system service deployment

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores, 2.4 GHz
- **RAM**: 4GB (8GB recommended)
- **Storage**: 10GB free space
- **OS**: Ubuntu 18.04+, CentOS 7+, macOS 10.14+, Windows 10
- **Python**: 3.8+ (3.10+ recommended)
- **Network**: Internet connection for OpenRouter API

#### Production Requirements  
- **CPU**: 4+ cores, 3.0+ GHz
- **RAM**: 16GB+ (for enhanced performance)
- **Storage**: 50GB+ SSD (for document cache)
- **Network**: High-speed internet, reverse proxy (nginx)
- **Monitoring**: System monitoring and logging

## 🛠️ Development Deployment

### 1. Local Development Setup

```bash
# Clone repository
git clone <repository-url>
cd pharma-rag-query

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies  
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenRouter API credentials

# Prepare data directory
mkdir -p data
# Copy CDSCO regulatory documents to data/

# Start development server
python app_openrouter_enhanced.py
```

### 2. Development Environment Variables
```bash
# Development .env configuration
OPENROUTER_API_KEY=your_development_api_key
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
PATHWAY_LOG_LEVEL=INFO
PATHWAY_PHARMA_MODE=true
```

### 3. Development Testing
```bash
# Test server functionality
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test Paracetamol compliance"}'

# Run test suite
python -m pytest test_*.py -v

# Performance test
python test_live_server.py
```

## 🏭 Production Deployment

### 1. Production Server Setup

#### System Preparation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3.10-dev -y

# Install system dependencies
sudo apt install git nginx supervisor curl -y

# Create application user
sudo useradd -m -s /bin/bash pharma-rag
sudo usermod -aG sudo pharma-rag
```

#### Application Installation
```bash
# Switch to application user
sudo su - pharma-rag

# Clone application
git clone <repository-url> /home/pharma-rag/pharma-rag-query
cd /home/pharma-rag/pharma-rag-query

# Create production virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create production directories
mkdir -p logs data Cache_Enhanced
```

### 2. Production Configuration

#### Environment Variables
```bash
# Production .env configuration
cat > .env << EOF
# OpenRouter Production Configuration
OPENROUTER_API_KEY=your_production_api_key
OPENROUTER_API_BASE=https://openrouter.ai/api/v1

# Performance Optimization
PATHWAY_PHARMA_MODE=true
PATHWAY_REGULATORY_FOCUS=drug_bans,scheduling,compliance,safety_alerts
PATHWAY_LOG_LEVEL=INFO

# Production Settings
PHARMA_ENV=production
PHARMA_HOST=0.0.0.0
PHARMA_PORT=8001
EOF

# Secure environment file
chmod 600 .env
```

#### Nginx Reverse Proxy
```bash
# Create nginx configuration
sudo tee /etc/nginx/sites-available/pharma-rag << EOF
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Rate limiting
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/m;
    
    location / {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeout settings for LLM processing
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 120s;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://127.0.0.1:8001;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/pharma-rag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Process Management with Supervisor

```bash
# Create supervisor configuration
sudo tee /etc/supervisor/conf.d/pharma-rag.conf << EOF
[program:pharma-rag-enhanced]
command=/home/pharma-rag/pharma-rag-query/venv/bin/python app_openrouter_enhanced.py
directory=/home/pharma-rag/pharma-rag-query
user=pharma-rag
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/pharma-rag/pharma-rag-query/logs/app.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=5
environment=HOME="/home/pharma-rag",USER="pharma-rag"

[program:pharma-rag-monitor]
command=/home/pharma-rag/pharma-rag-query/scripts/monitor.sh
directory=/home/pharma-rag/pharma-rag-query
user=pharma-rag
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/pharma-rag/pharma-rag-query/logs/monitor.log
EOF

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start pharma-rag-enhanced
```

### 4. Production Monitoring Script

```bash
# Create monitoring script
mkdir -p scripts
cat > scripts/monitor.sh << 'EOF'
#!/bin/bash

# Production monitoring script for Pharmaceutical Compliance RAG System

LOG_FILE="/home/pharma-rag/pharma-rag-query/logs/monitor.log"
API_URL="http://localhost:8001/v1/pw_ai_answer"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

check_api_health() {
    local response=$(curl -s -w "%{http_code}" -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d '{"prompt": "Health check"}' \
        --max-time 30 -o /dev/null)
    
    if [ "$response" = "200" ]; then
        log_message "✅ API health check passed"
        return 0
    else
        log_message "❌ API health check failed: HTTP $response"
        return 1
    fi
}

check_disk_space() {
    local usage=$(df /home/pharma-rag/pharma-rag-query | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$usage" -gt 80 ]; then
        log_message "⚠️ Disk usage high: ${usage}%"
    fi
}

check_memory_usage() {
    local mem_usage=$(free | awk 'NR==2{printf "%.1f", $3*100/$2}')
    if (( $(echo "$mem_usage > 85.0" | bc -l) )); then
        log_message "⚠️ Memory usage high: ${mem_usage}%"
    fi
}

# Main monitoring loop
while true; do
    check_api_health
    check_disk_space  
    check_memory_usage
    
    # Check every 5 minutes
    sleep 300
done
EOF

chmod +x scripts/monitor.sh
```



# Multi-stage build for production optimization
FROM python:3.10-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Production stage
FROM python:3.10-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash pharma-rag

# Copy virtual environment from builder
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=pharma-rag:pharma-rag . .

# Create necessary directories
RUN mkdir -p Cache_Enhanced logs data

# Switch to non-root user
USER pharma-rag

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8001/v1/pw_ai_answer \
        -X POST -H "Content-Type: application/json" \
        -d '{"prompt": "Health check"}' || exit 1

# Start application
CMD ["python", "app_openrouter_enhanced.py"]
```

```yaml
version: '3.8'

services:
  pharma-rag:
    build: .
    container_name: pharma-rag-enhanced
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - OPENROUTER_API_BASE=${OPENROUTER_API_BASE}
      - PATHWAY_PHARMA_MODE=true
    volumes:
      - ./data:/app/data:ro
      - ./Cache_Enhanced:/app/Cache_Enhanced
      - ./logs:/app/logs
    networks:
      - pharma-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/v1/pw_ai_answer"]
      interval: 60s
      timeout: 30s
      retries: 3
      start_period: 30s

  nginx:
    image: nginx:alpine
    container_name: pharma-rag-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - pharma-rag
    networks:
      - pharma-network

  redis:
    image: redis:alpine
    container_name: pharma-rag-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - pharma-network
    command: redis-server --appendonly yes

networks:
  pharma-network:
    driver: bridge

volumes:
  redis_data:
```


```bash
# Build and start services

# View logs

# Scale for high availability (if needed)

# Update deployment

# Backup data
    -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Instance Setup
```bash
# Launch EC2 instance (recommended: t3.large or larger)
# Security groups: Allow ports 80, 443, 22

# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip



# Deploy application
git clone <repository-url>
cd pharma-rag-query
cp .env.example .env
# Configure .env with production settings
```

#### Application Load Balancer
```bash
# Create ALB with target groups
# Target group: pharma-rag-tg (port 8001)
# Health check: /v1/pw_ai_answer (POST)

# Route 53 DNS configuration
# Create A record pointing to ALB
```

### Google Cloud Platform Deployment

#### Cloud Run Deployment
```yaml
# cloudbuild.yaml
steps:
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/pharma-rag:$COMMIT_SHA', '.']
    args: ['push', 'gcr.io/$PROJECT_ID/pharma-rag:$COMMIT_SHA']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'pharma-rag-service'
      - '--image=gcr.io/$PROJECT_ID/pharma-rag:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--memory=4Gi'
      - '--cpu=2'
      - '--max-instances=10'
      - '--port=8001'
```

## 🔧 System Service Deployment

### 1. Systemd Service Configuration

```bash
# Create systemd service
sudo tee /etc/systemd/system/pharma-rag.service << EOF
[Unit]
Description=Pharmaceutical Compliance RAG System
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=pharma-rag
Group=pharma-rag
WorkingDirectory=/home/pharma-rag/pharma-rag-query
ExecStart=/home/pharma-rag/pharma-rag-query/venv/bin/python app_openrouter_enhanced.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=pharma-rag
KillMode=mixed
KillSignal=SIGTERM

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/home/pharma-rag/pharma-rag-query/Cache_Enhanced
ReadWritePaths=/home/pharma-rag/pharma-rag-query/logs

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable pharma-rag
sudo systemctl start pharma-rag

# Check status
sudo systemctl status pharma-rag
```

### 2. Log Rotation Configuration

```bash
# Configure log rotation
sudo tee /etc/logrotate.d/pharma-rag << EOF
/home/pharma-rag/pharma-rag-query/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 pharma-rag pharma-rag
    postrotate
        sudo systemctl reload pharma-rag
    endscript
}
EOF
```

## 📊 Production Monitoring

### 1. System Monitoring

#### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'pharma-rag'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

#### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "Pharmaceutical Compliance RAG System",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "http_request_duration_seconds{job=\"pharma-rag\"}"
          }
        ]
      },
      {
        "title": "Cache Hit Rate", 
        "type": "stat",
        "targets": [
          {
            "expr": "rate(pharma_cache_hits_total[5m])"
          }
        ]
      }
    ]
  }
}
```

### 2. Application Monitoring

#### Health Check Script
```python
#!/usr/bin/env python3
import requests
import json
import time
import sys

def comprehensive_health_check():
    """Comprehensive production health check"""
    base_url = "http://localhost:8001"
    
    tests = [
        ("API Connectivity", lambda: test_api_connectivity(base_url)),
        ("Document Processing", lambda: test_document_processing(base_url)),
        ("LLM Integration", lambda: test_llm_integration(base_url)),
        ("Response Quality", lambda: test_response_quality(base_url))
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            print(f"✅ {test_name}: PASSED")
        except Exception as e:
            results[test_name] = False
            print(f"❌ {test_name}: FAILED - {e}")
    
    # Overall health status
    overall_health = all(results.values())
    
    if overall_health:
        print("🟢 Overall System Health: HEALTHY")
        return 0
    else:
        print("🔴 Overall System Health: UNHEALTHY")
        return 1

def test_api_connectivity(base_url):
    response = requests.post(
        f"{base_url}/v1/pw_ai_answer",
        json={"prompt": "Health check"},
        timeout=10
    )
    return response.status_code == 200

def test_document_processing(base_url):
    response = requests.post(
        f"{base_url}/v1/pw_list_documents",
        json={},
        timeout=5
    )
    data = response.json()
    return "documents" in data and len(data["documents"]) > 0

def test_llm_integration(base_url):
    response = requests.post(
        f"{base_url}/v1/pw_ai_answer",
        json={"prompt": "Test pharmaceutical compliance analysis"},
        timeout=30
    )
    data = response.json()
    return "response" in data and len(data["response"]) > 10

def test_response_quality(base_url):
    response = requests.post(
        f"{base_url}/v1/pw_ai_answer", 
        json={"prompt": "Is Paracetamol banned in India?"},
        timeout=30
    )
    data = response.json()
    response_text = data.get("response", "").lower()
    
    # Check for pharmaceutical compliance keywords
    quality_indicators = [
        "paracetamol" in response_text,
        "banned" in response_text or "open" in response_text,
        "india" in response_text or "cdsco" in response_text
    ]
    
    return sum(quality_indicators) >= 2

if __name__ == "__main__":
    exit_code = comprehensive_health_check()
    sys.exit(exit_code)
```

## 🔒 Security Configuration

### 1. SSL/TLS Configuration

```bash
# Install Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw deny 8001  # Block direct access to application port
```

### 3. API Security

```bash
# Rate limiting configuration (already in nginx config)
# Additional security headers
# API key rotation procedures
# Access logging and monitoring
```

## 📈 Performance Optimization

### 1. System Optimization

```bash
# Optimize system for production
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'net.core.somaxconn=1024' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. Application Optimization

```yaml
# Production YAML configuration optimizations
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter
  max_tokens: 400  # Reduce for faster processing in high-volume environments

$llm: !pw.xpacks.llm.llms.LiteLLMChat
  max_tokens: 500  # Shorter responses for faster generation
  temperature: 0.05  # More deterministic for production consistency
```

---

## 📞 Deployment Support

### Troubleshooting Common Issues

1. **Port Conflicts**: Check for processes using ports 8001, 80, 443
2. **Permission Issues**: Ensure proper file permissions for pharma-rag user
3. **Memory Issues**: Monitor RAM usage, adjust container limits
4. **SSL Issues**: Check certificate validity and renewal
5. **API Rate Limits**: Monitor OpenRouter usage and billing

### Deployment Checklist

- [ ] System requirements met
- [ ] Environment variables configured  
- [ ] CDSCO documents uploaded to data directory
- [ ] SSL certificates installed (production)
- [ ] Monitoring and logging configured
- [ ] Backup procedures established
- [ ] Health checks passing
- [ ] Performance testing completed
- [ ] Security audit completed

This comprehensive deployment guide ensures reliable, secure, and scalable deployment of the Pharmaceutical Compliance RAG System for production use.