# Government Pharmaceutical Compliance System - Flow Documentation

## Overview

This document provides a comprehensive analysis of the data flow, system architecture, and processing workflows within the Government Pharmaceutical Compliance System. The system implements a sophisticated RAG (Retrieval Augmented Generation) pipeline for pharmaceutical regulatory compliance analysis.

## System Architecture Flow

### 1. High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    GOVERNMENT PHARMACEUTICAL COMPLIANCE SYSTEM           │
├──────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────┐│
│  │   CLIENT    │───▶│  API GATEWAY │───▶│ RAG PIPELINE│───▶│   LLM      ││
│  │ (curl/web)  │    │ (Port 8001)  │    │ (Pathway)   │    │(OpenRouter)││ 
│  └─────────────┘    └──────────────┘    └─────────────┘    └────────────┘│
│         │                   │                   │                │       │
│         │                   │                   ▼                │       │
│         │                   │            ┌─────────────┐         │       │
│         │                   │            │  Document   │         │       │
│         │                   │            │   Store     │         │       │
│         │                   │            │ (CDSCO PDFs)│         │       │
│         │                   │            └─────────────┘         │       │
│         │                   │                   │                │       │
│         │                   ▼                   ▼                ▼       │
│         │            ┌─────────────┐    ┌─────────────┐  ┌─────────────┐ │
│         └────────────│  Response   │◀───│   Vector    │◀─│ Government  │ │
│                      │ Formatter   │    │   Search    │  │   Prompt    │ │
│                      └─────────────┘    └─────────────┘  └─────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2. Detailed Component Flow

#### A. Request Processing Flow

1. **Client Request Initiation**
   - HTTP POST request to `/v1/pw_ai_answer`
   - JSON payload with pharmaceutical query
   - Authentication and validation

2. **API Gateway Processing**
   - Request validation and sanitization
   - Rate limiting and security checks
   - Route to appropriate handler

3. **RAG Pipeline Activation**
   - Query preprocessing and normalization
   - Context retrieval from document store
   - Prompt template application

4. **LLM Processing**
   - OpenRouter API call to Claude Sonnet 4
   - Government compliance analysis
   - Response generation

5. **Response Delivery**
   - JSON formatting and validation
   - Client response transmission
   - Logging and monitoring

## Data Flow Architecture

### 1. Document Ingestion Pipeline

```
CDSCO Regulatory Documents
         │
         ▼
┌─────────────────┐
│   PDF Files     │
│ ┌─────────────┐ │    ┌──────────────────┐
│ │ Banned Drug │ │───▶│ UnstructuredParser│
│ │    Lists    │ │    │   (Pathway)      │
│ └─────────────┘ │    └──────────────────┘
│ ┌─────────────┐ │              │
│ │  Gazette    │ │              ▼
│ │Notifications│ │    ┌──────────────────┐
│ └─────────────┘ │    │  Text Extraction │
│ ┌─────────────┐ │    │   & Processing   │
│ │ CDSCO Rules │ │    └──────────────────┘
│ └─────────────┘ │              │
└─────────────────┘              ▼
                        ┌──────────────────┐
                        │   Token Split    │
                        │ (600 token max)  │
                        └──────────────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ Vector Embedding │
                        │  & Indexing      │
                        └──────────────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │  Document Store  │
                        │ (Enhanced Cache) │
                        └──────────────────┘
```

### 2. Query Processing Pipeline

```
User Query: "Is Paracetamol banned in India?"
              │
              ▼
    ┌─────────────────┐
    │ Query Validation│
    │ & Sanitization  │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Semantic Search │
    │ (Vector Similarity)│
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Context Retrieval│
    │ (Top-K Documents)│
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Prompt Template │
    │   Application   │
    │ (Government AI) │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ LLM Processing  │
    │ (Claude Sonnet) │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Response Format │
    │ (JSON/Summary)  │
    └─────────────────┘
              │
              ▼
    JSON Response with Compliance Analysis
```

## Regulatory Analysis Workflow

### S1-S6 Regulatory Categories Framework

```
Input: Drug Information
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    S1: BAN STATUS ANALYSIS                  │
├─────────────────────────────────────────────────────────────┤
│ • Query CDSCO banned drug databases                         │
│ • Search gazette notifications (Part II, Sec 3, Sub (ii))  │
│ • Validate FDC (Fixed Dose Combination) restrictions       │
│ • Cross-reference with PIL and news sources                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                S2: APPROVAL STATUS VERIFICATION             │
├─────────────────────────────────────────────────────────────┤
│ • Check withdrawal of prohibitions                          │
│ • Gazette notifications (Part II, Sec 3, Sub (i))          │
│ • Validate approval dates vs. ban dates                    │
│ • Verify current regulatory standing                       │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│            S3: SCHEDULE CLASSIFICATION ASSESSMENT           │
├─────────────────────────────────────────────────────────────┤
│ • Determine Schedule H/H1/X status                         │
│ • Prescription requirement analysis                         │
│ • Image-based schedule verification (Rx symbols)           │
│ • Updated Drugs Rules 1945 compliance                      │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              S4: IMPORT RESTRICTION ANALYSIS               │
├─────────────────────────────────────────────────────────────┤
│ • Delhi drugs department import bans                        │
│ • Court judgments and legal restrictions                   │
│ • Domestic production vs. import permissions               │
│ • Ministry notifications validation                        │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│            S5: CONTROLLED SUBSTANCE EVALUATION             │
├─────────────────────────────────────────────────────────────┤
│ • NDPS Act compliance checking                             │
│ • Narcotic and psychotropic classifications                │
│ • Department of Revenue notifications                      │
│ • Special licensing requirements                           │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              S6: QUALITY STANDARDS ASSESSMENT              │
├─────────────────────────────────────────────────────────────┤
│ • NSQ (Not of Standard Quality) alerts                    │
│ • CDSCO monthly quality reports                           │
│ • Substandard drug identification                         │
│ • Quality compliance verification                          │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
    Final Classification: banned/controlled/scheduled/open
```

### P1-P8 Processing Workflow

```
P1: DRUG INPUT PARSING
    │
    ├─ Drug Name Extraction
    ├─ Specification Analysis  
    ├─ Description Processing
    └─ Image Data Handling
    │
    ▼
P2: INDIVIDUAL DRUG PROCESSING
    │
    ├─ Sequential Analysis Loop
    ├─ Batch Processing Management
    └─ Error Handling & Recovery
    │
    ▼
P3: IMAGE-NAME MATCHING
    │
    ├─ Visual Drug Identification
    ├─ Package Label Analysis
    ├─ Brand Name Verification
    └─ Match Confidence Scoring
    │
    ▼
P4: BAN STATUS DETERMINATION (Using S1 + S4)
    │
    ├─ Primary Source Check (Files)
    ├─ Secondary Source Search (Internet/Gazette)
    ├─ FDC Specific Analysis
    └─ Date-based Validity Check
    │
    ▼
P5: APPROVAL VERIFICATION (Using S2)
    │
    ├─ Post-ban Approval Search
    ├─ Chronological Analysis
    ├─ Gazette Cross-referencing
    └─ Current Status Determination
    │
    ▼
P6: SCHEDULE CLASSIFICATION (Using S3)
    │
    ├─ Prescription Category Assignment
    ├─ Image-based Schedule Detection
    ├─ Regulatory File Verification
    └─ Final Schedule Determination
    │
    ▼
P7: CONTROLLED SUBSTANCE CHECK (Using S5)
    │
    ├─ NDPS Act Compliance
    ├─ Special License Requirements
    ├─ Regulatory Authority Validation
    └─ Control Status Assignment
    │
    ▼
P8: FINAL OUTPUT GENERATION
    │
    ├─ 21-Column Structure Population
    ├─ JSON Format Compliance
    ├─ Summary Generation
    └─ Quality Assurance Check
```

## Technical Implementation Flow

### 1. Application Startup Sequence

```
System Initialization
         │
         ▼
┌─────────────────┐
│Load Configuration│
│ (YAML Parsing)  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Initialize Logging│
│ & Error Handling│
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Setup Document   │
│ Store & Parser  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Configure LLM    │
│ (OpenRouter)    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Load Government  │
│ System Prompt   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Initialize RAG   │
│  Pipeline       │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Start HTTP Server│
│ (Port 8001)     │
└─────────────────┘
         │
         ▼
   Ready for Requests
```

### 2. Request-Response Cycle

```
HTTP Request (POST /v1/pw_ai_answer)
         │
         ▼
┌─────────────────┐
│Request Validation│
│ • JSON Structure│
│ • Required Fields│
│ • Input Sanitize│
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Extract Query    │
│ • Prompt Field  │
│ • Model Field   │
│ • Parameters    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│RAG Pipeline     │
│ • Doc Retrieval │
│ • Context Build │
│ • Prompt Inject │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│LLM API Call     │
│ • OpenRouter    │
│ • Claude Sonnet │
│ • Token Mgmt    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Response Process │
│ • Format Check  │
│ • JSON Validate │
│ • Error Handle  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│HTTP Response    │
│ • Status Code   │
│ • JSON Body     │
│ • Headers       │
└─────────────────┘
         │
         ▼
   Client Receives Response
```

## Data Persistence & Caching Flow

### 1. Enhanced Caching System

```
Document Processing Request
         │
         ▼
┌─────────────────┐
│Cache Key Gen    │
│ (Hash-based)    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Cache Lookup     │
│(Cache_Enhanced/)│
└─────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌─────────┐
│ HIT   │  │  MISS   │
└───────┘  └─────────┘
    │         │
    │         ▼
    │  ┌─────────────────┐
    │  │Process Document │
    │  │ • Parse PDF     │
    │  │ • Extract Text  │
    │  │ • Generate Vec  │
    │  └─────────────────┘
    │         │
    │         ▼
    │  ┌─────────────────┐
    │  │Cache Storage    │
    │  │ • Store Result  │
    │  │ • Update Index  │
    │  └─────────────────┘
    │         │
    └─────────┘
         │
         ▼
   Return Processed Result
```

### 2. Vector Store Management

```
Text Chunks (600 tokens max)
         │
         ▼
┌─────────────────┐
│Embedding Gen    │
│ (Semantic Vec)  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Vector Storage   │
│ • Similarity    │
│ • Index Update  │
│ • Metadata      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Query Processing │
│ • Cosine Sim    │
│ • Top-K Select  │
│ • Relevance Rank│
└─────────────────┘
         │
         ▼
   Context Retrieved for LLM
```

## Error Handling & Recovery Flow

### 1. Exception Management Pipeline

```
System Operation
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌─────────────┐
│SUCCESS  │ │   ERROR     │
└─────────┘ └─────────────┘
    │              │
    │              ▼
    │      ┌─────────────────┐
    │      │Error Classification│
    │      │ • Network Err   │
    │      │ • Config Err    │
    │      │ • LLM API Err   │
    │      │ • Parse Err     │
    │      └─────────────────┘
    │              │
    │              ▼
    │      ┌─────────────────┐
    │      │Logging & Alert  │
    │      │ • Error Level   │
    │      │ • Stack Trace   │
    │      │ • Context Info  │
    │      └─────────────────┘
    │              │
    │              ▼
    │      ┌─────────────────┐
    │      │Recovery Action  │
    │      │ • Retry Logic   │
    │      │ • Fallback      │
    │      │ • Circuit Break │
    │      └─────────────────┘
    │              │
    └──────────────┘
         │
         ▼
   Operation Complete/Failed
```

## Performance Optimization Flow

### 1. Request Processing Optimization

```
Incoming Request
         │
         ▼
┌─────────────────┐
│Request Analysis │
│ • Size Check    │
│ • Complexity    │
│ • Priority      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Resource Alloc   │
│ • Memory Mgmt   │
│ • CPU Usage     │
│ • Token Limits  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Processing Route │
│ • Fast Path     │
│ • Standard Path │
│ • Complex Path  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Performance Mon  │
│ • Response Time │
│ • Resource Usage│
│ • Success Rate  │
└─────────────────┘
         │
         ▼
   Optimized Response Delivery
```

## Security & Compliance Flow

### 1. Data Security Pipeline

```
Input Data
    │
    ▼
┌─────────────────┐
│Input Validation │
│ • SQL Injection │
│ • XSS Prevention│
│ • Size Limits   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│Authentication   │
│ • API Keys      │
│ • Rate Limiting │
│ • Access Control│
└─────────────────┘
    │
    ▼
┌─────────────────┐
│Data Sanitization│
│ • Special Chars │
│ • Encoding      │
│ • Format Valid  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│Secure Processing│
│ • Encrypted Comm│
│ • Audit Logging │
│ • Privacy Comp  │
└─────────────────┘
    │
    ▼
Secure Output Delivery
```

## Monitoring & Logging Flow

### 1. Comprehensive Monitoring System

```
System Events
         │
         ▼
┌─────────────────┐
│Event Classification│
│ • INFO          │
│ • WARNING       │
│ • ERROR         │
│ • CRITICAL      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Structured Logging│
│ • Timestamp     │
│ • Context Info  │
│ • Performance   │
│ • User Actions  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Log Aggregation  │
│ • File Rotation │
│ • Compression   │
│ • Retention     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Monitoring       │
│ • Real-time     │
│ • Alerting      │
│ • Dashboards    │
└─────────────────┘
         │
         ▼
   Operational Insights
```

## Integration Points

### 1. External System Integration

```
Government Platform
         │
         ▼
┌─────────────────┐
│API Gateway      │
│ • Load Balancer │
│ • SSL/TLS       │
│ • Rate Limiting │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│OpenRouter API   │
│ • Claude Sonnet │
│ • Token Mgmt    │
│ • Retry Logic   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│CDSCO Data       │
│ • Gazette API   │
│ • Document Feed │
│ • Update Stream │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Regulatory DB    │
│ • Real-time     │
│ • Compliance    │
│ • Audit Trail   │
└─────────────────┘
         │
         ▼
   Integrated Compliance System
```

## Deployment Flow

### 1. Virtual Environment Deployment

```
Development Complete
         │
         ▼
┌─────────────────┐
│Environment Setup│
│ • Python venv   │
│ • Dependencies  │
│ • Config Files  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Application Test │
│ • Unit Tests    │
│ • Integration   │
│ • Performance   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Production Deploy│
│ • Server Setup  │
│ • Process Mgmt  │
│ • Monitoring    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│Health Checks    │
│ • API Endpoints │
│ • System Status │
│ • Performance   │
└─────────────────┘
         │
         ▼
   Live Production System
```

This comprehensive flow documentation provides a detailed understanding of how the Government Pharmaceutical Compliance System operates at every level, from high-level architecture to detailed technical implementation flows.