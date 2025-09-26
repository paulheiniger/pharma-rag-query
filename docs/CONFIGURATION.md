# 📋 Configuration Guide - Enhanced Pharmaceutical Compliance System

This document provides comprehensive documentation for the YAML configuration files used in the Pharmaceutical Compliance RAG System.

## 🔧 Configuration Files Overview

### Primary Configuration Files

1. **`app_openrouter_enhanced.yaml`** - Enhanced version with Government prompts (Port 8001)
2. **`app_openrouter.yaml`** - Standard version (Port 8000)  
3. **`system_prompt.txt`** - Government compliance system prompt source

## 📄 Enhanced Configuration Structure

### Document Sources Configuration
```yaml
# Data source configuration for CDSCO regulatory documents
$sources:
  - !pw.io.fs.read
    path: "./data"                    # Directory containing regulatory PDFs
    format: "binary"                  # Binary format for PDF processing
    with_metadata: true               # Include file metadata (timestamps, names)
```

**Purpose**: Defines the source of regulatory documents for processing
- **Path**: `./data` directory containing CDSCO banned drug lists, gazette notifications
- **Format**: Binary format enables PDF document processing
- **Metadata**: Preserves file information for tracking document sources

### LLM Configuration  
```yaml
# OpenRouter LLM integration with Claude Sonnet 4
$llm: !pw.xpacks.llm.llms.LiteLLMChat
  model: "anthropic/claude-sonnet-4"  # High-quality model for pharmaceutical analysis
  temperature: 0.1                    # Low temperature for consistent regulatory analysis
  max_tokens: 1000                    # Sufficient tokens for detailed compliance reports
  api_key: $OPENROUTER_API_KEY       # Environment variable for API authentication
  api_base: $OPENROUTER_API_BASE     # OpenRouter API base URL
  custom_llm_provider: "openrouter"   # LiteLLM provider specification
```

**Key Parameters:**
- **Model**: `anthropic/claude-sonnet-4` - Advanced reasoning for complex regulatory analysis
- **Temperature**: `0.1` - Low randomness for consistent, factual pharmaceutical compliance responses  
- **Max Tokens**: `1000` - Adequate length for comprehensive drug analysis summaries
- **API Integration**: Uses environment variables for secure credential management

### Embedding Configuration
```yaml
# Semantic embeddings for document similarity search  
$embedder: !pw.xpacks.llm.embedders.SentenceTransformerEmbedder
  model: "sentence-transformers/all-MiniLM-L6-v2"
```

**Purpose**: Creates vector embeddings for semantic document search
- **Model**: `all-MiniLM-L6-v2` - Balanced performance and accuracy for pharmaceutical text
- **Use Case**: Enables semantic matching of drug names, regulatory terms, and compliance queries

### Document Splitting Configuration
```yaml
# Enhanced token splitting for bigger context windows
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter
  max_tokens: 600                     # Enhanced: Bigger chunks for better context
```

**Enhanced Features:**
- **Token Count**: `600` tokens per chunk (vs. 400 in standard version)
- **Benefit**: Preserves more context for complex pharmaceutical regulatory analysis
- **Use Case**: Better handling of multi-paragraph gazette notifications and drug descriptions

### Document Parser Configuration  
```yaml
# Unstructured document parsing for PDFs and text files
$parser: !pw.xpacks.llm.parsers.UnstructuredParser
```

**Capabilities:**
- **PDF Processing**: Extracts text from CDSCO gazette notifications and ban lists
- **Text Preservation**: Maintains document structure and formatting
- **Metadata Extraction**: Preserves document dates, titles, and gazette references

### Vector Search Configuration
```yaml
# High-performance vector similarity search
$retriever_factory: !pw.stdlib.indexing.UsearchKnnFactory
  reserved_space: 1000                # Memory allocation for pharmaceutical document index
  embedder: $embedder                 # Links to sentence transformer embeddings
  metric: !pw.stdlib.indexing.USearchMetricKind.COS  # Cosine similarity metric
```

**Performance Optimizations:**
- **Reserved Space**: `1000` documents capacity for CDSCO regulatory files
- **Similarity Metric**: Cosine similarity for pharmaceutical text matching
- **Efficiency**: Optimized for real-time compliance query responses

### Document Store Configuration
```yaml
# Integrated document processing pipeline
$document_store: !pw.xpacks.llm.document_store.DocumentStore
  docs: $sources                      # Links to document sources
  parser: $parser                     # Links to PDF parser
  splitter: $splitter                 # Links to token splitter  
  retriever_factory: $retriever_factory  # Links to vector search
```

**Integration**: Combines all processing components into unified pharmaceutical document pipeline

## 🧬 Government System Prompt Configuration

### Prompt Template Structure
```yaml
# Government Pharmaceutical Compliance System Prompt
$prompt_template: |
  <OBJECTIVE_AND_PERSONA>
  # Government platform compliance requirements
  # CDSCO regulatory framework
  # Pharmaceutical domain expertise
  
  <INSTRUCTIONS>  
  # P1-P8 processing workflow
  # S1-S6 regulatory categories
  # Systematic drug analysis methodology
  
  <CONSTRAINTS>
  # Summary-only output format
  # Professional compliance language
  # Regulatory accuracy requirements
```

### Key Prompt Components

#### OBJECTIVE_AND_PERSONA Section
- **Platform Context**: Government pharmaceutical marketplace requirements
- **Regulatory Framework**: CDSCO guidelines and Indian pharmaceutical law
- **Domain Expertise**: Specialized knowledge of drug bans, scheduling, and compliance

#### INSTRUCTIONS Section (P1-P8 Workflow)
1. **P1-P2**: Input processing and drug identification
2. **P3**: Image-name consistency verification  
3. **P4**: Ban status analysis using S1 and S4 methodologies
4. **P5**: Approval status verification using S2 methodology  
5. **P6**: Schedule classification using S3 methodology
6. **P7**: Controlled substance checking using S5 methodology
7. **P8**: Quality and miscellaneous factors using S6 methodology

#### CONSTRAINTS Section
- **Output Format**: Professional summary format (1-2 lines)
- **Language Requirements**: Lowercase formatting, professional terminology
- **Accuracy Standards**: Regulatory compliance and factual precision

### Regulatory Categories (S1-S6)

#### S1: New Banned Drugs
```yaml
# Focus: Recently banned substances and FDCs
# Sources: CDSCO gazette notifications under Part II, Section 3, subsection (ii)
# Keywords: "prohibition", "prohibited", "FDC", "fixed dose combination", "restricted"
```

#### S2: Previously Banned, Now Approved  
```yaml
# Focus: Drugs with lifted bans or revised regulatory status
# Sources: Gazette notifications under Part II, Section 3, subsection (i)  
# Keywords: "drugs", "revised", "withdraw"
```

#### S3: Scheduled Drugs
```yaml
# Focus: Schedule H, H1, and X classification requirements
# Sources: Updated Drugs Rules 1945, CDSCO scheduled drug lists
# Keywords: "Schedule", "Schedule H", "Schedule H1", "Schedule X", "Drugs Cosmetic Act"
```

#### S4: Import Banned Drugs
```yaml
# Focus: Import restrictions vs. domestic production allowances
# Sources: Delhi drug department, court judgments, import notifications
# Keywords: "court", "judgement", "judgment", "import"
```

#### S5: Controlled Substances
```yaml
# Focus: NDPS Act and controlled substance regulations  
# Sources: Department of Revenue, Ministry of Finance gazette notifications
# Keywords: NDPS Act compliance, controlled substance schedules
```

#### S6: Substandard Quality (NSQ)
```yaml
# Focus: Quality compliance and safety alerts
# Sources: Monthly CDSCO NSQ alerts, safety bulletins
# Keywords: "NSQ", "not of standard quality", safety alerts
```

## 🔌 Question Answerer Configuration

### RAG Pipeline Integration
```yaml
# Enhanced question answerer with Government prompt integration
question_answerer: !pw.xpacks.llm.question_answering.BaseRAGQuestionAnswerer
  llm: $llm                          # Links to OpenRouter LLM configuration
  indexer: $document_store           # Links to pharmaceutical document store  
  prompt_template: $prompt_template  # Links to Government compliance prompt
```

**Integration Benefits:**
- **Custom Prompts**: Replaces default Pathway prompts with pharmaceutical-specific instructions
- **Domain Optimization**: Specialized for CDSCO regulatory analysis and Government compliance
- **Consistency**: Ensures all responses follow Government compliance requirements

## 🌐 Server Configuration

### Network Settings
```yaml
# Server hosting configuration
host: "0.0.0.0"                     # Accept connections from any IP address
port: 8001                          # Enhanced version port (vs. 8000 for standard)
```

**Production Considerations:**
- **Host**: `0.0.0.0` enables external access for Government integration
- **Port**: `8001` distinguishes enhanced version from standard `8000`
- **Security**: Use reverse proxy (nginx) and SSL certificates in production

## 🚀 Performance Optimization

### Enhanced vs. Standard Configuration Comparison

| Parameter | Standard Version | Enhanced Version | Impact |
|-----------|------------------|------------------|---------|
| **Max Tokens (Splitter)** | 400 | 600 | +50% context preservation |
| **Port** | 8000 | 8001 | Parallel operation capability |
| **Cache Directory** | `Cache/` | `Cache_Enhanced/` | Separate performance optimization |
| **System Prompt** | Basic | Government Compliance | +Professional pharmaceutical analysis |

### Memory and Performance Tuning

#### For High-Volume Production:
```yaml
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter
  max_tokens: 400                    # Faster processing, lower memory

$llm: !pw.xpacks.llm.llms.LiteLLMChat
  max_tokens: 500                    # Shorter responses, faster generation
  temperature: 0.05                  # More deterministic responses
```

#### For Comprehensive Analysis:
```yaml  
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter
  max_tokens: 800                    # Better context, comprehensive analysis

$llm: !pw.xpacks.llm.llms.LiteLLMChat  
  max_tokens: 1500                   # Detailed compliance reports
  temperature: 0.1                   # Balanced accuracy and reasoning
```

## 🔧 Environment Variables Integration

### Required Environment Variables
```bash
# OpenRouter API Configuration (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here      # Authentication for LLM access
OPENROUTER_API_BASE=https://openrouter.ai/api/v1     # OpenRouter API base URL

# Optional: Performance Optimizations  
PATHWAY_PHARMA_MODE=true                              # Enable pharmaceutical domain mode
PATHWAY_REGULATORY_FOCUS=drug_bans,scheduling,compliance,safety_alerts
```

### Security Best Practices
- **API Key Management**: Store in `.env` file, never commit to version control
- **Access Control**: Use environment-specific API keys for development/production
- **Monitoring**: Log API usage for compliance auditing and cost management

## 🧪 Testing Configuration

### Configuration Validation Script
```python
# Validate configuration loading and prompt integration
import pathway as pw

def test_enhanced_config():
    """Test enhanced configuration loading and prompt integration"""
    with open("app_openrouter_enhanced.yaml") as f:
        config = pw.load_yaml(f)
    
    # Verify Government prompt is loaded
    assert "Government" in config["prompt_template"]
    assert "CDSCO" in config["prompt_template"]  
    assert "S1" in config["prompt_template"]  # Regulatory categories
    assert "P1" in config["prompt_template"]  # Processing workflow
    
    print("✅ Enhanced configuration validated")
```

### Performance Testing Configuration
```yaml
# Testing-optimized configuration for rapid iteration
$llm: !pw.xpacks.llm.llms.LiteLLMChat
  model: "anthropic/claude-sonnet-4"
  temperature: 0.1
  max_tokens: 200                    # Shorter responses for faster testing
  
$splitter: !pw.xpacks.llm.splitters.TokenCountSplitter  
  max_tokens: 300                    # Smaller chunks for faster processing
```

---

## 📞 Configuration Support

### Common Configuration Issues

1. **YAML Syntax Errors**: Use proper indentation and validate YAML format
2. **Environment Variable Issues**: Ensure `.env` file is in project root  
3. **Model Access Issues**: Verify OpenRouter API key has Claude Sonnet 4 access
4. **Performance Issues**: Adjust `max_tokens` parameters based on system resources

### Configuration Validation
```bash
# Test configuration loading
python -c "import pathway as pw; pw.load_yaml(open('app_openrouter_enhanced.yaml'))"

# Verify environment variables
python -c "import os; print(os.getenv('OPENROUTER_API_KEY') is not None)"
```

This comprehensive configuration guide ensures proper setup and optimization of the Pharmaceutical Compliance RAG System for Government regulatory analysis.