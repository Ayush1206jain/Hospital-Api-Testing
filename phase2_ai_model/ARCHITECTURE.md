# Architecture & Data Flow Guide

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                  AI Test Case Generator System                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                       INPUT LAYER                                 │
├──────────────────────────────────────────────────────────────────┤
│  OpenAPI Specification (.json or .yaml)                          │
│  - Hospital API spec: ../oas_docs/hospital-api.json              │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    PARSING LAYER                                  │
├──────────────────────────────────────────────────────────────────┤
│  OASParser (src/oas_parser.py)                                   │
│  ├─ Extract endpoints                                             │
│  ├─ Parse parameters                                              │
│  ├─ Analyze request/response schemas                              │
│  └─ Identify constraints (min/max, required fields, etc.)         │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│               GENERATION ORCHESTRATION LAYER                      │
├──────────────────────────────────────────────────────────────────┤
│  TestCaseGenerator (src/test_generator.py)                       │
│  ├─ Iterate through endpoints                                     │
│  ├─ Coordinate LLM processing                                     │
│  ├─ Validate generated test cases                                 │
│  └─ Collect statistics                                            │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                 LLM PROCESSING LAYER                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────┐      ┌──────────────────────┐          │
│  │  LLMProcessor        │      │  LLMFactory          │          │
│  │  (Orchestration)     │      │  (Provider mgmt)     │          │
│  └──────────────────────┘      └──────────────────────┘          │
│           │                            │                          │
│           ├────────────────────────────┤                          │
│           │                            │                          │
│    ┌──────▼─────────┐         ┌────────▼──────┐                 │
│    │  OpenAIProvider │         │ AnthropicProvider             │
│    │  (GPT-4)        │         │ (Claude)       │                 │
│    └─────────────────┘         └────────────────┘                 │
│           │                            │                          │
│           └────────┬───────────────────┘                          │
│                    ▼                                               │
│          ┌──────────────────┐                                     │
│          │  LLM Provider    │                                     │
│          │  (Selected)      │                                     │
│          └──────────────────┘                                     │
│                    │                                               │
└────────────────────┼────────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   External LLM APIs     │
        ├─────────────────────────┤
        │ OpenAI / Anthropic      │
        │ with HTTP requests      │
        └────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   Generated Test Cases  │
        │   (JSON format)         │
        └────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────┐
│                 VALIDATION LAYER                                  │
├──────────────────────────────────────────────────────────────────┤
│  TestCaseValidator (src/test_generator.py)                       │
│  ├─ Verify required fields                                        │
│  ├─ Check data types                                              │
│  ├─ Validate structure                                            │
│  └─ Remove invalid cases                                          │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                OUTPUT FORMATTING LAYER                            │
├──────────────────────────────────────────────────────────────────┤
│  OutputFormatter (src/output_formatter.py)                       │
│           │                                                        │
│    ┌──────┴────────┬─────────────┐                               │
│    │               │             │                               │
│    ▼               ▼             ▼                               │
│ ┌──────┐      ┌──────┐      ┌──────────┐                        │
│ │ JSON │      │ CSV  │      │ Postman  │                        │
│ └──────┘      └──────┘      └──────────┘                        │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                                 │
├──────────────────────────────────────────────────────────────────┤
│  Generated Test Cases in:                                         │
│  ├─ output/generated_tests_json.json                              │
│  ├─ output/generated_tests_csv.csv                                │
│  └─ output/generated_tests_postman.json                           │
│                                                                    │
│  Logs in:                                                         │
│  └─ logs/ai_generator.log                                         │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Step 1: Parse OAS Specification

```
Input:  ../oas_docs/hospital-api.json
        {
          "paths": {
            "/v1/hospitais/": {
              "post": {
                "summary": "Create hospital",
                "parameters": [...],
                "requestBody": {...},
                "responses": {...}
              }
            }
          }
        }

Output: List[Endpoint]
        [
          Endpoint(
            path="/v1/hospitais/",
            method="POST",
            parameters=[...],
            request_body_schema={...},
            ...
          ),
          ...
        ]
```

### Step 2: Generate Test Cases via LLM

```
Input:  Endpoint information
        {
          "path": "/v1/hospitais/",
          "method": "POST",
          "parameters": [...],
          "requestBodySchema": {...},
          "requiredFields": ["name", "address", "beds"]
        }

        + Prompt Template (prompts/valid_tests.txt)

Output: List[Dict] - Generated test cases
        [
          {
            "testId": "HC-001",
            "endpoint": "/v1/hospitais/",
            "method": "POST",
            "category": "VALID",
            "description": "Create hospital with all fields",
            "requestBody": {...},
            "expectedStatusCode": 201,
            ...
          },
          ...
        ]
```

### Step 3: Validate Test Cases

```
Input:  Generated test cases

Validation:
  - Check required fields present
  - Verify data types
  - Validate status codes
  - Check structure

Output: Validated List[Dict]
        (Invalid cases removed)
```

### Step 4: Format and Export

```
Input:  Validated test cases

Format: Choose output format
        - JSON (with metadata)
        - CSV (tabular)
        - Postman (importable)

Output: File written to output/ directory
```

## Module Interaction Diagram

```
main.py (CLI Entry Point)
  │
  ├──> config.py (Load configuration)
  │
  ├──> TestCaseGenerator
  │      │
  │      ├──> OASParser
  │      │      ├──> Parse YAML/JSON
  │      │      └──> Extract endpoints
  │      │
  │      ├──> LLMProcessor
  │      │      │
  │      │      ├──> LLMFactory.create_provider()
  │      │      │      ├──> OpenAIProvider or
  │      │      │      └──> AnthropicProvider
  │      │      │
  │      │      └──> generate_test_cases_for_endpoint()
  │      │             ├──> Build prompt
  │      │             ├──> Call LLM API
  │      │             └──> Parse JSON response
  │      │
  │      └──> TestCaseValidator
  │             ├──> validate_test_case()
  │             └──> Filter invalid cases
  │
  └──> OutputFormatter
         │
         ├──> FormatterFactory.create_formatter()
         │      ├──> JSONFormatter or
         │      ├──> CSVFormatter or
         │      └──> PostmanFormatter
         │
         └──> Write to output/
```

## Configuration & Secrets Management

```
.env (DO NOT COMMIT)
├─ OPENAI_API_KEY=sk-xxx
├─ ANTHROPIC_API_KEY=xxx
├─ LLM_PROVIDER=openai
├─ LLM_MODEL=gpt-4
└─ [other config]
     │
     ▼
config.py (Read .env & defaults)
     │
     ├─ OPENAI_API_KEY
     ├─ ANTHROPIC_API_KEY
     ├─ LLM_MODEL
     ├─ VALID_TESTS_PER_ENDPOINT
     ├─ OUTPUT_FORMAT
     └─ [all other configs]
     │
     ▼
main.py + Modules (Use config)
```

## Error Handling Flow

```
Error Occurs
    │
    ├─ Logging (logs/ai_generator.log)
    │  ├─ ERROR level log message
    │  ├─ Stack trace (debug mode)
    │  └─ Contextual information
    │
    ├─ User Feedback
    │  ├─ Console error message
    │  ├─ Suggested fixes
    │  └─ Exit code
    │
    └─ Recovery Options
       ├─ Retry (for transient errors)
       ├─ Manual fix (for configuration)
       └─ Support (contact developers)
```

## Performance Pipeline

```
Speed Optimizations:
  │
  ├─ Parallel endpoint processing
  │  (Future enhancement)
  │
  ├─ Response caching
  │  (For duplicate endpoints)
  │
  ├─ Batch LLM requests
  │  (Reduce API calls)
  │
  └─ Streaming responses
     (Real-time feedback)

Cost Optimizations:
  │
  ├─ Model selection (GPT-3.5 vs GPT-4)
  │
  ├─ Token optimization
  │  (Shorter prompts)
  │
  ├─ Request batching
  │  (Grouping endpoints)
  │
  └─ Caching results
     (Avoid reprocessing)
```

## Scalability Architecture

```
Single Operation:
  OAS File → Generator → Output Files

Multi-File Processing:
  [OAS File 1] ─┐
  [OAS File 2] ─├─> Generator Pool → [Output 1, 2, ...]
  [OAS File 3] ─┘

Batch Processing:
  [OAS File] → [Batch 1: Endpoints 1-5]  → [Output 1-5]
               [Batch 2: Endpoints 6-10] → [Output 6-10]
               [Batch 3: Endpoints 11+]  → [Output 11+]

Distributed Processing (Future):
  [OAS File] → Task Queue → [Worker 1: Endpoints A]
                             [Worker 2: Endpoints B]
                             [Worker 3: Endpoints C]
               → Result Aggregator → [Final Output]
```

## Test Execution Pipeline (Integration)

```
Generated Test Cases (JSON)
        │
        ▼
Postman Collection (JSON)
        │
        ▼
Postman Runner
  ├─ Parse requests
  ├─ Execute requests
  ├─ Validate responses
  └─ Generate reports
        │
        ▼
Test Results
  ├─ Passed: ✅
  ├─ Failed: ❌
  └─ Skipped: ⏭️
```

## Security Considerations

```
API Keys:
  ├─ Store in .env (NOT in code)
  ├─ Never commit to git
  ├─ Rotate periodically
  └─ Use least-privilege keys

Data Handling:
  ├─ Sanitize OAS input
  ├─ Validate LLM output
  ├─ Encrypt sensitive data
  └─ Log safely (no secrets)

Network:
  ├─ Use HTTPS only
  ├─ Verify SSL certificates
  ├─ Rate limit API calls
  └─ Monitor for suspicious activity
```

---

For detailed API documentation, see **README.md**  
For quick start guide, see **GETTING_STARTED.md**
