# Government Pharmaceutical Compliance System - Visual Flow Diagram

## Master System Architecture Flow Diagram

```
                    GOVERNMENT PHARMACEUTICAL COMPLIANCE SYSTEM
    ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   CLIENTS   │         │ API GATEWAY │         │RAG PIPELINE │         │ OPENROUTER  │
    │             │         │             │         │             │         │     LLM     │
    │ Web Browser │────────▶│  Port 8001  │────────▶│   Pathway   │────────▶│Claude Sonnet│
    │ curl/API    │         │ HTTP Server │         │ Framework   │         │     4.0     │
    │ Mobile Apps │         │             │         │             │         │             │
    └─────────────┘         └─────────────┘         └─────────────┘         └─────────────┘
           │                        │                        │                        │
           │                        │                        ▼                        │
           │                        │              ┌─────────────────┐                │
           │                        │              │   DOCUMENT      │                │
           │                        │              │     STORE       │                │
           │                        │              │ ┌─────────────┐ │                │
           │                        │              │ │CDSCO PDFs   │ │                │
           │                        │              │ │Gazette Docs │ │                │
           │                        │              │ │Banned Lists │ │                │
           │                        │              │ │Schedule Info│ │                │
           │                        │              │ └─────────────┘ │                │
           │                        │              └─────────────────┘                │
           │                        │                        │                        │
           │                        ▼                        ▼                        ▼
    ┌─────────────────────────────────────────────────────────────────────────────────────────┐
    │                              RESPONSE PROCESSING LAYER                                   │
    ├─────────────────────────────────────────────────────────────────────────────────────────┤
    │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐               │
    │  │   VECTOR    │    │ GOVERNMENT  │    │ COMPLIANCE  │    │  RESPONSE   │               │
    │  │   SEARCH    │───▶│   PROMPT    │───▶│  ANALYSIS   │───▶│ FORMATTER   │               │
    │  │  Engine     │    │  Template   │    │ S1-S6/P1-P8 │    │JSON/Summary │               │
    │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘               │
    └─────────────────────────────────────────────────────────────────────────────────────────┘
           ▲                                                                        │
           │                                                                        │
           └────────────────────────────────────────────────────────────────────────┘
```

## Detailed Request Processing Flow

```
                                 REQUEST PROCESSING PIPELINE
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    CLIENT REQUEST                           API PROCESSING                        LLM PROCESSING
    ┌─────────────┐                         ┌─────────────┐                      ┌─────────────┐
    │             │   POST /v1/pw_ai_answer │             │    RAG Retrieval     │             │
    │   HTTP      │────────────────────────▶│    API      │─────────────────────▶│ OpenRouter  │
    │  Request    │                         │  Gateway    │                      │     API     │
    │             │                         │             │                      │             │
    │ ┌─────────┐ │                         │ ┌─────────┐ │                      │ ┌─────────┐ │
    │ │ Headers │ │                         │ │Validate │ │                      │ │Claude   │ │
    │ │ JSON    │ │                         │ │Sanitize │ │                      │ │Sonnet 4 │ │
    │ │ Auth    │ │                         │ │Route    │ │                      │ │Model    │ │
    │ └─────────┘ │                         │ └─────────┘ │                      │ └─────────┘ │
    └─────────────┘                         └─────────────┘                      └─────────────┘
           │                                       │                                     │
           │                                       ▼                                     │
           │                            ┌─────────────────┐                             │
           │                            │   RAG PIPELINE  │                             │
           │                            │                 │                             │
           │                            │ ┌─────────────┐ │                             │
           │                            │ │Query Preproc│ │                             │
           │                            │ └─────────────┘ │                             │
           │                            │ ┌─────────────┐ │                             │
           │                            │ │Doc Retrieval│ │                             │
           │                            │ └─────────────┘ │                             │
           │                            │ ┌─────────────┐ │                             │
           │                            │ │Context Build│ │                             │
           │                            │ └─────────────┘ │                             │
           │                            │ ┌─────────────┐ │                             │
           │                            │ │Prompt Inject│ │                             │
           │                            │ └─────────────┘ │                             │
           │                            └─────────────────┘                             │
           │                                       │                                     │
           │                                       └─────────────────────────────────────┘
           │                                                                             │
           │                                                                             ▼
           │                                                               ┌─────────────────┐
           │                                                               │ ANALYSIS ENGINE │
           │                                                               │                 │
           │                                                               │ ┌─────────────┐ │
           │                                                               │ │Regulatory   │ │
           │                                                               │ │Classification│ │
           │                                                               │ └─────────────┘ │
           │                                                               │ ┌─────────────┐ │
           │                                                               │ │Compliance   │ │
           │                                                               │ │Workflow     │ │
           │                                                               │ └─────────────┘ │
           │                                                               │ ┌─────────────┐ │
           │                                                               │ │JSON Output  │ │
           │                                                               │ │Generation   │ │
           │                                                               │ └─────────────┘ │
           │                                                               └─────────────────┘
           │                                                                             │
           │                                                                             ▼
           │                                                               ┌─────────────────┐
           │                                                               │ RESPONSE BUILD  │
           │                                ┌─────────────────┐           │                 │
           │                                │  HTTP RESPONSE  │◀──────────│ ┌─────────────┐ │
           │                                │                 │           │ │Format Check │ │
           │◀───────────────────────────────│ ┌─────────────┐ │           │ └─────────────┘ │
           │                                │ │Status: 200  │ │           │ ┌─────────────┐ │
           │                                │ │Content-Type │ │           │ │Error Handle │ │
           │                                │ │JSON Body    │ │           │ └─────────────┘ │
           │                                │ └─────────────┘ │           │ ┌─────────────┐ │
           │                                └─────────────────┘           │ │Security Hdrs│ │
           │                                                               │ └─────────────┘ │
           ▼                                                               └─────────────────┘
    ┌─────────────┐
    │   CLIENT    │
    │  RECEIVES   │
    │ COMPLIANCE  │
    │  ANALYSIS   │
    └─────────────┘
```

## Regulatory Analysis Workflow (S1-S6 Framework)

```
                              PHARMACEUTICAL REGULATORY ANALYSIS FRAMEWORK
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    INPUT: Drug Query                                              OUTPUT: Compliance Classification
    ┌─────────────┐                                               ┌─────────────────────────────┐
    │ Drug Name   │                                               │ Status: banned/controlled/  │
    │ Specification│──────────────────────┐                      │         scheduled/open      │
    │ Description │                      │                      │ Reasoning: Detailed         │
    │ Image Data  │                      │                      │ Sources: Files/Gazette/Web  │
    └─────────────┘                      │                      │ Dates: Ban/Approval         │
                                         │                      │ Schedule: H/H1/X            │
                                         ▼                      │ Compliance: Government      │
                            ┌─────────────────────┐             └─────────────────────────────┘
                            │  S1: BAN STATUS     │                              ▲
                            │     ANALYSIS        │                              │
                            │ ┌─────────────────┐ │                              │
                            │ │CDSCO Banned DB  │ │                              │
                            │ │Gazette Part II  │ │                              │
                            │ │Sub-section (ii) │ │                              │
                            │ │FDC Restrictions │ │                              │
                            │ └─────────────────┘ │                              │
                            └─────────────────────┘                              │
                                         │                                       │
                                         ▼                                       │
                            ┌─────────────────────┐                              │
                            │  S2: APPROVAL       │                              │
                            │   VERIFICATION      │                              │
                            │ ┌─────────────────┐ │                              │
                            │ │Withdrawal Check │ │                              │
                            │ │Gazette Part II  │ │                              │
                            │ │Sub-section (i)  │ │                              │
                            │ │Date Validation  │ │                              │
                            │ └─────────────────┘ │                              │
                            └─────────────────────┘                              │
                                         │                                       │
                                         ▼                                       │
                            ┌─────────────────────┐                              │
                            │  S3: SCHEDULE       │                              │
                            │  CLASSIFICATION     │                              │
                            │ ┌─────────────────┐ │                              │
                            │ │Schedule H/H1/X  │ │                              │
                            │ │Prescription Req │ │                              │
                            │ │Image Rx Symbols │ │                              │
                            │ │Drugs Rules 1945 │ │                              │
                            │ └─────────────────┘ │                              │
                            └─────────────────────┘                              │
                                         │                                       │
                                         ▼                                       │
                            ┌─────────────────────┐                              │
                            │  S4: IMPORT         │                              │
                            │   RESTRICTIONS      │                              │
                            │ ┌─────────────────┐ │                              │
                            │ │Delhi Dept Bans  │ │                              │
                            │ │Court Judgments  │ │                              │
                            │ │Import vs Domestic│ │                              │
                            │ │Ministry Notices │ │                              │
                            │ └─────────────────┘ │                              │
                            └─────────────────────┘                              │
                                         │                                       │
                                         ▼                                       │
                            ┌─────────────────────┐                              │
                            │  S5: CONTROLLED     │                              │
                            │   SUBSTANCES        │                              │
                            │ ┌─────────────────┐ │                              │
                            │ │NDPS Act Check   │ │                              │
                            │ │Narcotic Classes │ │                              │
                            │ │Revenue Dept     │ │                              │
                            │ │Special Licenses │ │                              │
                            │ └─────────────────┘ │                              │
                            └─────────────────────┘                              │
                                         │                                       │
                                         ▼                                       │
                            ┌─────────────────────┐                              │
                            │  S6: QUALITY        │                              │
                            │   STANDARDS         │                              │
                            │ ┌─────────────────┐ │                              │
                            │ │NSQ Alerts       │ │                              │
                            │ │Monthly Reports  │ │                              │
                            │ │Substandard ID   │ │                              │
                            │ │Quality Checks   │ │                              │
                            │ └─────────────────┘ │                              │
                            └─────────────────────┘                              │
                                         │                                       │
                                         └───────────────────────────────────────┘
```

## P1-P8 Processing Workflow

```
                                    PROCESSING WORKFLOW PIPELINE
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    P1: INPUT PARSING          P2: DRUG PROCESSING       P3: IMAGE MATCHING        P4: BAN ANALYSIS
    ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐      ┌─────────────────┐
    │ ┌─────────────┐ │       │ ┌─────────────┐ │       │ ┌─────────────┐ │      │ ┌─────────────┐ │
    │ │Drug Name    │ │────▶  │ │Sequential   │ │────▶  │ │Visual ID    │ │────▶ │ │Primary Check│ │
    │ │Specification│ │       │ │Processing   │ │       │ │Package Label│ │      │ │File Sources │ │
    │ │Description  │ │       │ │Loop Control │ │       │ │Brand Verify │ │      │ │FDC Analysis │ │
    │ │Image Data   │ │       │ │Error Handle │ │       │ │Confidence   │ │      │ │Date Valid   │ │
    │ └─────────────┘ │       │ └─────────────┘ │       │ └─────────────┘ │      │ └─────────────┘ │
    └─────────────────┘       └─────────────────┘       └─────────────────┘      └─────────────────┘
              │                         │                         │                        │
              │                         │                         │                        │
              ▼                         ▼                         ▼                        ▼
    
    P5: APPROVAL CHECK         P6: SCHEDULE CLASS       P7: CONTROLLED CHECK      P8: OUTPUT GEN
    ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐      ┌─────────────────┐
    │ ┌─────────────┐ │       │ ┌─────────────┐ │       │ ┌─────────────┐ │      │ ┌─────────────┐ │
    │ │Post-ban     │ │────▶  │ │Prescription │ │────▶  │ │NDPS Act     │ │────▶ │ │21-Column    │ │
    │ │Approval     │ │       │ │Category     │ │       │ │Compliance   │ │      │ │Structure    │ │
    │ │Chronological│ │       │ │Image Rx     │ │       │ │Special      │ │      │ │JSON Format  │ │
    │ │Validation   │ │       │ │Schedule Det │ │       │ │Licensing    │ │      │ │Summary Gen  │ │
    │ └─────────────┘ │       │ └─────────────┘ │       │ └─────────────┘ │      │ └─────────────┘ │
    └─────────────────┘       └─────────────────┘       └─────────────────┘      └─────────────────┘
              │                         │                         │                        │
              └─────────────────────────┼─────────────────────────┼────────────────────────┘
                                        │                         │
                                        └─────────────────────────┘
                                                   │
                                                   ▼
                                        ┌─────────────────┐
                                        │  FINAL OUTPUT   │
                                        │                 │
                                        │ ┌─────────────┐ │
                                        │ │Compliance   │ │
                                        │ │Status       │ │
                                        │ └─────────────┘ │
                                        │ ┌─────────────┐ │
                                        │ │Detailed     │ │
                                        │ │Analysis     │ │
                                        │ └─────────────┘ │
                                        │ ┌─────────────┐ │
                                        │ │Government   │ │
                                        │ │Recommendation│ │
                                        │ └─────────────┘ │
                                        └─────────────────┘
```

## Data Flow Architecture

```
                                     DATA FLOW ARCHITECTURE
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    DOCUMENT INGESTION                    PROCESSING PIPELINE                    STORAGE & RETRIEVAL
    ┌─────────────────┐                  ┌─────────────────┐                   ┌─────────────────┐
    │ CDSCO SOURCES   │                  │ PATHWAY PARSER  │                   │ ENHANCED CACHE  │
    │                 │                  │                 │                   │                 │
    │ ┌─────────────┐ │                  │ ┌─────────────┐ │                   │ ┌─────────────┐ │
    │ │Banned Lists │ │─────────────────▶│ │Unstructured │ │─────────────────▶ │ │Vector Store │ │
    │ │Gazette PDFs │ │                  │ │Parser       │ │                   │ │Embeddings   │ │
    │ │CDSCO Rules  │ │                  │ │Text Extract │ │                   │ │Metadata     │ │
    │ │Delhi Dept   │ │                  │ │Token Split  │ │                   │ │Index        │ │
    │ └─────────────┘ │                  │ └─────────────┘ │                   │ └─────────────┘ │
    └─────────────────┘                  └─────────────────┘                   └─────────────────┘
              │                                    │                                     │
              │                                    │                                     │
              ▼                                    ▼                                     ▼
    
    ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
    │                              QUERY PROCESSING LAYER                                          │
    ├─────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                             │
    │  Query Input                    Semantic Search                    Context Building        │
    │  ┌─────────────┐               ┌─────────────────┐               ┌─────────────────┐       │
    │  │User Query   │──────────────▶│Vector Similarity│──────────────▶│Top-K Documents  │       │
    │  │Sanitization │               │Cosine Distance  │               │Relevance Ranking│       │
    │  │Normalization│               │Retrieval Engine │               │Context Assembly │       │
    │  └─────────────┘               └─────────────────┘               └─────────────────┘       │
    │         │                              │                                │                  │
    │         │                              │                                │                  │
    │         ▼                              ▼                                ▼                  │
    │                                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────────────────────┐   │
    │  │                         GOVERNMENT PROMPT TEMPLATE                                  │   │
    │  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│   │
    │  │ │S1-S6        │  │P1-P8        │  │Context      │  │Regulatory   │  │Output       ││   │
    │  │ │Categories   │  │Workflow     │  │Integration  │  │Guidelines   │  │Format       ││   │
    │  │ └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘│   │
    │  └─────────────────────────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                                   ┌─────────────────────┐
                                   │   LLM PROCESSING    │
                                   │                     │
                                   │ ┌─────────────────┐ │
                                   │ │OpenRouter API   │ │
                                   │ │Claude Sonnet 4  │ │
                                   │ │Token Management │ │
                                   │ │Error Handling   │ │
                                   │ └─────────────────┘ │
                                   └─────────────────────┘
                                                 │
                                                 ▼
                                   ┌─────────────────────┐
                                   │  RESPONSE FORMAT    │
                                   │                     │
                                   │ ┌─────────────────┐ │
                                   │ │JSON Structure   │ │
                                   │ │Summary Extract  │ │
                                   │ │Compliance Check │ │
                                   │ │Error Validation │ │
                                   │ └─────────────────┘ │
                                   └─────────────────────┘
```

## System Integration Flow

```
                                   SYSTEM INTEGRATION ARCHITECTURE
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    EXTERNAL SYSTEMS              INTEGRATION LAYER              INTERNAL COMPONENTS
    ┌─────────────────┐          ┌─────────────────┐            ┌─────────────────┐
    │ GOVERNMENT      │          │ API GATEWAY     │            │ APPLICATION     │
    │ PLATFORM        │          │                 │            │ CORE            │
    │                 │          │ ┌─────────────┐ │            │                 │
    │ ┌─────────────┐ │◀────────▶│ │Load Balancer│ │◀──────────▶│ ┌─────────────┐ │
    │ │Web Portal   │ │          │ │SSL/TLS      │ │            │ │RAG Pipeline │ │
    │ │Mobile App   │ │          │ │Rate Limiting│ │            │ │Config Mgmt  │ │
    │ │Admin Panel  │ │          │ │Auth Layer   │ │            │ │Error Handler│ │
    │ └─────────────┘ │          │ └─────────────┘ │            │ └─────────────┘ │
    └─────────────────┘          └─────────────────┘            └─────────────────┘
              │                            │                             │
              │                            │                             │
              ▼                            ▼                             ▼
    
    ┌─────────────────┐          ┌─────────────────┐            ┌─────────────────┐
    │ OPENROUTER      │          │ MONITORING      │            │ DATA LAYER      │
    │ SERVICE         │          │ & LOGGING       │            │                 │
    │                 │          │                 │            │                 │
    │ ┌─────────────┐ │          │ ┌─────────────┐ │            │ ┌─────────────┐ │
    │ │Claude API   │ │◀────────▶│ │System Logs  │ │◀──────────▶│ │Document     │ │
    │ │Token Mgmt   │ │          │ │Performance  │ │            │ │Store        │ │
    │ │Rate Limits  │ │          │ │Health Check │ │            │ │Vector DB    │ │
    │ └─────────────┘ │          │ └─────────────┘ │            │ └─────────────┘ │
    └─────────────────┘          └─────────────────┘            └─────────────────┘
              │                            │                             │
              │                            │                             │
              ▼                            ▼                             ▼
    
    ┌─────────────────┐          ┌─────────────────┐            ┌─────────────────┐
    │ CDSCO           │          │ SECURITY        │            │ CACHING         │
    │ DATA SOURCES    │          │ LAYER           │            │ SYSTEM          │
    │                 │          │                 │            │                 │
    │ ┌─────────────┐ │          │ ┌─────────────┐ │            │ ┌─────────────┐ │
    │ │Gazette API  │ │◀────────▶│ │Input Valid  │ │◀──────────▶│ │Enhanced     │ │
    │ │Document Feed│ │          │ │SQL Injection│ │            │ │Cache        │ │
    │ │Update Stream│ │          │ │XSS Prevent  │ │            │ │Runtime Calls│ │
    │ └─────────────┘ │          │ └─────────────┘ │            │ └─────────────┘ │
    └─────────────────┘          └─────────────────┘            └─────────────────┘
```

## Error Handling & Recovery Flow

```
                                ERROR HANDLING & RECOVERY SYSTEM
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    NORMAL OPERATION                     ERROR DETECTION                    RECOVERY ACTIONS
    ┌─────────────────┐                 ┌─────────────────┐              ┌─────────────────┐
    │ REQUEST         │                 │ ERROR           │              │ RECOVERY        │
    │ PROCESSING      │                 │ CLASSIFICATION  │              │ STRATEGIES      │
    │                 │                 │                 │              │                 │
    │ ┌─────────────┐ │                 │ ┌─────────────┐ │              │ ┌─────────────┐ │
    │ │API Calls    │ │────┐    ┌──────▶│ │Network Error│ │─────────────▶│ │Retry Logic  │ │
    │ │Data Process │ │    │    │       │ │Config Error │ │              │ │Exponential  │ │
    │ │LLM Requests │ │    │    │       │ │LLM API Error│ │              │ │Backoff      │ │
    │ └─────────────┘ │    │    │       │ │Parse Error  │ │              │ └─────────────┘ │
    └─────────────────┘    │    │       │ └─────────────┘ │              └─────────────────┘
              │            │    │       └─────────────────┘                        │
              ▼            │    │                 │                                │
         SUCCESS ──────────┘    │                 ▼                                │
              │                 │       ┌─────────────────┐                       │
              │                 │       │ ERROR           │                       │
              │                 │       │ LOGGING         │                       │
              │                 │       │                 │                       │
              │                 │       │ ┌─────────────┐ │                       │
              │                 └──────▶│ │Timestamp    │ │                       │
              │              ERROR      │ │Stack Trace  │ │                       │
              │                 │       │ │Context Info │ │                       │
              │                 │       │ │Severity     │ │                       │
              │                 │       │ └─────────────┘ │                       │
              │                 │       └─────────────────┘                       │
              │                 │                 │                               │
              │                 │                 ▼                               │
              │                 │       ┌─────────────────┐                       │
              │                 │       │ ALERTING        │                       │
              │                 │       │ SYSTEM          │                       │
              │                 │       │                 │                       │
              │                 │       │ ┌─────────────┐ │                       │
              │                 │       │ │Critical     │ │                       │
              │                 │       │ │Alerts       │ │                       │
              │                 │       │ │Notifications│ │                       │
              │                 │       │ │Dashboard    │ │                       │
              │                 │       │ └─────────────┘ │                       │
              │                 │       └─────────────────┘                       │
              │                 │                 │                               │
              │                 │                 └───────────────────────────────┘
              │                 │                           │
              ▼                 ▼                           ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                    SYSTEM RESILIENCE                            │
    ├─────────────────────────────────────────────────────────────────┤
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
    │  │Circuit      │  │Graceful     │  │Fallback     │             │
    │  │Breaker      │  │Degradation  │  │Responses    │             │
    │  │Pattern      │  │Mode         │  │Cache Serve  │             │
    │  └─────────────┘  └─────────────┘  └─────────────┘             │
    └─────────────────────────────────────────────────────────────────┘
```

## Performance Monitoring Flow

```
                                PERFORMANCE MONITORING SYSTEM
    ═══════════════════════════════════════════════════════════════════════════════════════════════════

    METRICS COLLECTION               DATA AGGREGATION                 ANALYSIS & ALERTING
    ┌─────────────────┐             ┌─────────────────┐              ┌─────────────────┐
    │ SYSTEM          │             │ METRICS         │              │ PERFORMANCE     │
    │ METRICS         │             │ AGGREGATOR      │              │ ANALYSIS        │
    │                 │             │                 │              │                 │
    │ ┌─────────────┐ │             │ ┌─────────────┐ │              │ ┌─────────────┐ │
    │ │Response Time│ │────────────▶│ │Time Series  │ │─────────────▶│ │Trend        │ │
    │ │Memory Usage │ │             │ │Database     │ │              │ │Analysis     │ │
    │ │CPU Usage    │ │             │ │Statistics   │ │              │ │Anomaly      │ │
    │ │Request Rate │ │             │ │Calculations │ │              │ │Detection    │ │
    │ └─────────────┘ │             │ └─────────────┘ │              │ └─────────────┘ │
    └─────────────────┘             └─────────────────┘              └─────────────────┘
              │                               │                                │
              ▼                               ▼                                ▼
    
    ┌─────────────────┐             ┌─────────────────┐              ┌─────────────────┐
    │ APPLICATION     │             │ REAL-TIME       │              │ DASHBOARD       │
    │ METRICS         │             │ PROCESSING      │              │ VISUALIZATION   │
    │                 │             │                 │              │                 │
    │ ┌─────────────┐ │             │ ┌─────────────┐ │              │ ┌─────────────┐ │
    │ │API Latency  │ │────────────▶│ │Stream       │ │─────────────▶│ │Real-time    │ │
    │ │Error Rates  │ │             │ │Processing   │ │              │ │Charts       │ │
    │ │Success Rates│ │             │ │Event        │ │              │ │Alerts       │ │
    │ │Throughput   │ │             │ │Correlation  │ │              │ │Reports      │ │
    │ └─────────────┘ │             │ └─────────────┘ │              │ └─────────────┘ │
    └─────────────────┘             └─────────────────┘              └─────────────────┘
              │                               │                                │
              ▼                               ▼                                ▼
    
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                          OPTIMIZATION FEEDBACK LOOP                              │
    ├─────────────────────────────────────────────────────────────────────────────────┤
    │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
    │  │Performance  │───▶│Bottleneck   │───▶│Optimization │───▶│Configuration│      │
    │  │Thresholds   │    │Identification│    │Recommendations│  │Updates      │      │
    │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
    └─────────────────────────────────────────────────────────────────────────────────┘
```

This comprehensive visual flow diagram provides a detailed understanding of the Government Pharmaceutical Compliance System's architecture, data flow, processing pipelines, and operational workflows at every level.