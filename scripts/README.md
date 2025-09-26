# Scripts Directory

This directory contains automation scripts for deployment, testing, and system management of the Government Pharmaceutical Compliance System.

## Overview

Utility scripts for system operations, testing automation, and deployment management. Each script is designed for specific operational tasks.

## Available Scripts

- **`curl.sh`** - Comprehensive API testing script with multiple test scenarios
- **`deploy.sh`** - System deployment automation
- **`deploy-systemd.sh`** - SystemD service deployment
- **`start.sh`** - Server startup script
- **`stop.sh`** - Server shutdown script

## Quick Start

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run API tests
./scripts/curl.sh

# Start the server
./scripts/start.sh
```

📖 **[Complete Deployment Guide](../docs/DEPLOYMENT.md)**

## Requirements

- Python virtual environment activated
- Bash shell environment
- Network connectivity for API testing
- Proper file permissions for script execution

## Support

For detailed script usage, configuration options, and deployment procedures, refer to the complete deployment documentation linked above.