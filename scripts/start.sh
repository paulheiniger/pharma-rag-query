#!/bin/bash

# Pharmaceutical Compliance RAG - Quick Start Script
# This script sets up and starts the pharmaceutical regulatory document monitoring system

set -e  # Exit on any error

echo "🏥 Pharmaceutical Compliance RAG - Quick Start"
echo "=============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is available
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8+ to continue."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l) -eq 1 ]] 2>/dev/null || [[ "$PYTHON_VERSION" > "3.7" ]]; then
        print_success "Python $PYTHON_VERSION detected"
    else
        print_error "Python 3.8+ is required. Found: $PYTHON_VERSION"
        exit 1
    fi
}

# Check if virtual environment exists
setup_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Create necessary directories
setup_directories() {
    print_status "Setting up directories..."
    mkdir -p data cache logs
    print_success "Directories created"
}

# Copy environment file if it doesn't exist
setup_env() {
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Environment file created from template"
            print_warning "Please review and update .env file with your configuration"
        else
            print_warning "No .env.example file found"
        fi
    else
        print_status "Environment file already exists"
    fi
}

# Check for sample documents
check_sample_data() {
    if [ -z "$(ls -A data 2>/dev/null)" ]; then
        print_warning "No documents found in data/ directory"
        print_status "To test the system, add some PDF documents to the data/ directory"
        print_status "For pharmaceutical compliance, add Gazette of India PDFs or regulatory documents"
    else
        DOC_COUNT=$(ls -1 data | wc -l)
        print_success "Found $DOC_COUNT document(s) in data/ directory"
    fi
}

# Start the application
start_application() {
    print_status "Starting Pharmaceutical Compliance RAG application..."
    print_status "The application will be available at http://localhost:8000"
    print_status "Press Ctrl+C to stop the application"
    echo ""
    print_status "API Endpoints:"
    echo "  - POST /v1/retrieve - Query pharmaceutical documents"
    echo "  - GET /v1/statistics - View system statistics"
    echo "  - GET /v1/inputs - List indexed documents"
    echo ""
    
    # Start the application
    $PYTHON_CMD app.py
}

# Test the application (optional)
test_application() {
    if [ "$1" = "--test" ]; then
        print_status "Testing API endpoints..."
        sleep 5  # Give the application some time to start
        $PYTHON_CMD test_api.py --wait 10
    fi
}

        
            exit 1
        fi
        
        else
        fi
        exit 0
    fi
}

# Main execution
main() {
    
    # Standard setup
    check_python
    setup_venv
    install_dependencies
    setup_directories
    setup_env
    check_sample_data
    
    # Check for test option
    if [ "$1" = "--test" ]; then
        print_status "Will run tests after starting the application"
        start_application &
        APP_PID=$!
        sleep 15  # Wait for application to start
        test_application "$1"
        kill $APP_PID
    else
        start_application
    fi
}

# Handle command line arguments
case "$1" in
    --help|-h)
        echo "Pharmaceutical Compliance RAG - Quick Start Script"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --test         Start and run API tests"
        echo "  (no option)    Standard start"
        echo ""
        echo "Examples:"
        echo "  $0                 # Standard start"
        echo "  $0 --test          # Start and test"
        exit 0
        ;;
    *)
        main "$1"
        ;;
esac