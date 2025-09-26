# 🧬 Pharmaceutical Compliance RAG System

An advanced **Retrieval Augmented Generation (RAG)** system specifically designed for pharmaceutical regulatory compliance in India. This system helps **Government** analyze drug regulations, bans, scheduling, and compliance status according to **CDSCO (Central Drugs Standard Control Organisation)** guidelines.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)  
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [File Descriptions](#-file-descriptions)
- [Regulatory Categories](#-regulatory-categories)
- [Troubleshooting](#-troubleshooting)

## 🚀 Features

### Core Capabilities
- **Government Pharmaceutical Compliance Analysis**: Automated drug regulatory status checking
- **CDSCO Regulatory Document Processing**: Analysis of official Indian drug regulations  
- **Drug Ban Detection**: Identifies banned substances according to latest gazette notifications
- **Schedule Classification**: Determines Schedule H/H1/X drug categories
- **Controlled Substance Analysis**: NDPS Act compliance checking
- **Gazette Notification Processing**: Real-time regulatory updates processing
- **Enhanced Context Processing**: Bigger context windows for complex pharmaceutical queries

### Technical Features  
- **Pathway AI Framework**: Advanced RAG implementation with pharmaceutical optimizations
- **OpenRouter LLM Integration**: Claude Sonnet 4 model for intelligent analysis
- **Semantic Search**: SentenceTransformer embeddings for accurate document retrieval
- **Professional REST API**: Comprehensive endpoints for pharmaceutical compliance queries
- **Comprehensive Logging**: Structured logging for compliance monitoring and debugging
- **Persistent Caching**: Enhanced performance with intelligent caching system

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Applications                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP REST API
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Pathway RAG Server (Port 8001)                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   API Layer     │  │  Query Router   │  │ Response Handler│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RAG Pipeline                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Document Store  │  │   Embeddings    │  │ Vector Search   │ │
│  │ (CDSCO Files)   │  │(SentenceTransf.)│  │   (USearch)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              OpenRouter LLM Integration                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Claude Sonnet  │  │Government Prompt │  │  Compliance     │ │
│  │      4 Model    │  │    Template     │  │   Analysis      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
pharma-rag-query/
├── 🧬 Core Application Files
│   ├── app_openrouter_enhanced.py      # Main enhanced application (Port 8001)
│   ├── app_openrouter_enhanced.yaml    # Enhanced configuration with Government prompts
│   ├── app_openrouter.py              # Standard application (Port 8000)
│   ├── app_openrouter.yaml            # Standard configuration
│   └── system_prompt.txt              # Government compliance system prompt
│
├── 📊 Data & Documents
│   └── data/                          # CDSCO regulatory documents
│       ├── cdsco_banned_*.pdf         # Drug ban notifications by date
│       ├── cdsco_scheduled_*.pdf      # Schedule H/H1/X drug lists  
│       ├── delhi.pdf                  # Delhi-specific drug regulations
│       └── sample-gazette-*.txt       # Sample gazette notifications
│
├── 🧪 Testing & Validation
│   ├── test_*.py                      # Comprehensive test suites
│   ├── example_custom_prompt.py       # Prompt customization examples
│   └── final_demo.py                  # Production demonstration script
│
├── 🔧 Configuration & Deployment  
│   ├── requirements.txt               # Python dependencies
│   ├── .env                          # Environment variables (create this)
│   └── deploy.sh                     # Production deployment script
│
├── 📁 Cache & Logs
│   ├── Cache/                        # Standard version cache
│   ├── Cache_Enhanced/               # Enhanced version cache  
│   ├── *.log                        # Application logs
│   └── systemd/                     # System service configurations
│
└── 📚 Documentation
    ├── README.md                     # This comprehensive guide
    └── HACKATHON_SUMMARY.md         # Development history and insights
```

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** (Recommended: Python 3.10+)
- **4GB+ RAM** (8GB+ recommended for enhanced version)  
- **2GB+ Storage** (for document cache and embeddings)
- **Internet Connection** (for OpenRouter API and model downloads)

### API Requirements  
- **OpenRouter Account**: [Sign up at openrouter.ai](https://openrouter.ai)
- **OpenRouter API Key**: Required for LLM functionality
- **Claude Sonnet 4 Access**: Included with OpenRouter subscription

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd pharma-rag-query
```

### 2. Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import pathway; print('Pathway installed successfully')"
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1

# Optional: Additional configurations
PATHWAY_PHARMA_MODE=true
PATHWAY_REGULATORY_FOCUS=drug_bans,scheduling,compliance,safety_alerts
```

### 5. Prepare Regulatory Documents
```bash
# Ensure data directory exists with CDSCO documents
ls -la data/
# Should contain:
# - cdsco_banned_*.pdf files
# - cdsco_scheduled_*.pdf files  
# - gazette notifications and regulatory documents
```

## ⚙️ Configuration

### Enhanced Configuration (Recommended)
The **enhanced version** (`app_openrouter_enhanced.yaml`) provides:
- **Bigger context windows** (600 tokens per chunk)
- **Government-specific system prompts** 
- **Professional pharmaceutical compliance analysis**
- **Enhanced caching and performance**

### Key Configuration Parameters

#### LLM Settings
```yaml
$llm: !pw.xpacks.llm.llms.LiteLLMChat
  model: "anthropic/claude-sonnet-4"    # High-quality pharmaceutical analysis
  temperature: 0.1                      # Low temperature for consistent regulatory analysis
  max_tokens: 1000                      # Sufficient for detailed compliance reports
```

#### Document Processing
```yaml
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter
  max_tokens: 600                       # Enhanced: Bigger chunks for better context

$embedder: !pw.xpacks.llm.embedders.SentenceTransformerEmbedder  
  model: "sentence-transformers/all-MiniLM-L6-v2"  # Fast, accurate embeddings
```

## 🚀 Usage

### Starting the Enhanced Server (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Start enhanced pharmaceutical compliance system
python app_openrouter_enhanced.py
```

**Server Details:**
- **URL**: `http://localhost:8001`
- **Features**: Government compliance analysis, enhanced context
- **Cache**: `Cache_Enhanced/` directory

### Starting the Standard Server  
```bash
# Activate virtual environment
source venv/bin/activate

# Start standard pharmaceutical system
python app_openrouter.py
```

**Server Details:**
- **URL**: `http://localhost:8000`  
- **Features**: Basic pharmaceutical queries
- **Cache**: `Cache/` directory

## 🔌 API Reference

### POST /v1/pw_ai_answer
**Primary endpoint for pharmaceutical compliance analysis**

#### Request Format
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your pharmaceutical compliance query here"}'
```

#### Example Requests

**Drug Ban Analysis:**
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is Tramadol banned in India according to CDSCO regulations?"}'
```

**Government Compliance:**
```bash
curl -X POST "http://localhost:8001/v1/pw_ai_answer" \
  -H "Content-Type: application/json" \  
  -d '{"prompt": "Analyze Paracetamol for Government listing compliance"}'
```

#### Response Format
```json
{
  "response": "Concise 1-2 line pharmaceutical compliance summary focusing on regulatory status, ban status, scheduling information, and Government listing recommendations."
}
```

## 📄 File Descriptions

### Core Application Files

#### `app_openrouter_enhanced.py`
**Main enhanced application server (Port 8001)**
- **Purpose**: Production-ready pharmaceutical compliance system with Government integration
- **Features**: Enhanced context windows, professional compliance analysis, comprehensive logging
- **Class**: `EnhancedPharmaComplianceApp` with full pharmaceutical domain optimization
- **Usage**: `python app_openrouter_enhanced.py`

#### `app_openrouter_enhanced.yaml` 
**Enhanced configuration with Government system prompts**
- **Purpose**: Complete configuration for pharmaceutical compliance analysis
- **Contains**: Government system prompt with S1-S6 categories and P1-P8 processing workflow  
- **Features**: Optimized for drug ban detection, schedule classification, compliance analysis

#### `system_prompt.txt`
**Government pharmaceutical compliance system prompt**
- **Purpose**: Detailed instructions for pharmaceutical regulatory analysis
- **Content**: Complete Government compliance workflow with CDSCO guidelines
- **Categories**: S1-S6 regulatory focus areas
- **Process**: P1-P8 step-by-step pharmaceutical analysis workflow

### Configuration Files

#### `requirements.txt`
**Python package dependencies**
```
pathway[xpacks]>=0.13.0    # Core RAG framework with LLM extensions
sentence-transformers      # Semantic embeddings for document search
python-dotenv             # Environment variable management  
aiohttp                   # Async HTTP server framework
litellm                   # LLM integration layer for OpenRouter
```

## 🏥 Regulatory Categories

### S1-S6: Regulatory Analysis Categories

#### S1: New Banned Drugs
- **Focus**: Recently banned substances and FDCs (Fixed Dose Combinations)
- **Sources**: CDSCO gazette notifications, Ministry of Health publications

#### S2: Previously Banned, Now Approved  
- **Focus**: Drugs with lifted bans or revised regulatory status
- **Sources**: Gazette subsection (i) notifications for prohibition withdrawals

#### S3: Scheduled Drugs (Prescription Required)
- **Focus**: Schedule H, H1, and X classification  
- **Sources**: Updated Drugs Rules 1945, CDSCO scheduled drug lists

#### S4: Import Banned Drugs
- **Focus**: Substances prohibited for import but possibly allowed for domestic production
- **Sources**: Delhi drug department notifications, court judgments

#### S5: Controlled Substances  
- **Focus**: NDPS Act and other controlled substance regulations
- **Sources**: Department of Revenue gazette notifications

#### S6: Substandard Quality (NSQ)
- **Focus**: Not of Standard Quality alerts and safety notifications
- **Sources**: Monthly CDSCO NSQ alerts, safety bulletins

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Server Won't Start
```bash
# Check if port is already in use
lsof -i :8001

# Kill existing processes  
pkill -f "python.*app_openrouter_enhanced.py"

# Check environment variables
grep OPENROUTER .env
```

#### 2. API Key Issues
```bash
# Verify API key is set
echo $OPENROUTER_API_KEY

# Test API key validity
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models
```

#### 3. Dependencies Problems
```bash  
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Pathway installation
python -c "import pathway.xpacks.llm; print('LLM xpack available')"
```

### Error Codes and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused (port 8001)` | Server not started | Run `python app_openrouter_enhanced.py` |
| `API key invalid` | Missing/incorrect OpenRouter key | Check `.env` file configuration |
| `ModuleNotFoundError: pathway` | Missing dependencies | Run `pip install -r requirements.txt` |

---

**⚠️ Important Notice**: This system is designed for regulatory compliance assistance. Always verify critical pharmaceutical regulatory decisions with official CDSCO sources and qualified regulatory professionals.

**🏥 Disclaimer**: This system provides analysis based on available regulatory documents. For legal compliance decisions, consult qualified pharmaceutical regulatory experts and refer to official CDSCO notifications.