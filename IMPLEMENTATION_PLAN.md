Con# Implementation Plan: API Test Case Generator & Testing Framework

## Project Overview

**Objective:** Create an automated test case generation system for the Hospital Management API that:

1. Manually generate comprehensive test cases (valid & invalid scenarios)
2. Execute tests on Postman and validate responses
3. Build an AI model that automatically generates test cases from OpenAPI Specification (OAS) documents

---

## Phase 1: Manual Test Case Generation & Postman Testing

### 1.1 Identify API Endpoints

**Source:** Hospital Management API (SpringFox Swagger 2)

- Base URL: `http://localhost:8080`
- Documented in: `src/main/resources/GestaoHospitalar.postman_collection.json`

**Key Endpoints:**

- **Hospitals**
  - `POST /v1/hospitais/` - Create hospital
  - `GET /v1/hospitais/` - List all hospitals
  - `GET /v1/hospitais/{id}` - Get single hospital
  - `PUT /v1/hospitais/{id}` - Update hospital
  - `DELETE /v1/hospitais/{id}` - Delete hospital (if available)
  - `GET /v1/hospitais/{id}/leitos` - Get beds for hospital
  - `GET /v1/hospitais/maisProximo` - Find nearest hospital

- **Inventory**
  - `POST /v1/hospitais/{hospitalId}/estoque` - Add product
  - `GET /v1/hospitais/{hospitalId}/estoque` - List inventory
  - `PUT /v1/hospitais/{hospitalId}/estoque/{productId}` - Update product
  - `DELETE /v1/hospitais/{hospitalId}/estoque/{productId}` - Delete product

- **Patients**
  - `POST /v1/pacientes/` - Create patient
  - `GET /v1/pacientes/` - List patients
  - `GET /v1/pacientes/{id}` - Get patient details

### 1.2 Test Case Design Framework

#### **A. Valid Test Cases** ✅

For each endpoint, create tests with:

- **Happy Path:** Valid input → Expected success response
- **Edge Cases:** Boundary values, minimum/maximum inputs
- **Data Variations:** Different data types, special characters (handled properly)

#### **B. Invalid Test Cases** ❌

For each endpoint, create tests with:

- **Missing Required Fields:** Null/empty mandatory fields
- **Invalid Data Types:** String instead of number, etc.
- **Out-of-Range Values:** Negative numbers, excessive string lengths
- **Non-existent Resources:** IDs that don't exist in database
- **Malformed Requests:** Invalid JSON, missing headers
- **Business Logic Violations:** e.g., available beds > total beds

### 1.3 Test Case Template

```
Test ID: HC-001
Endpoint: POST /v1/hospitais/
Method: POST
Test Category: Valid - Create Hospital
Test Priority: High
Expected Status Code: 201 (Created) or 200 (Success)

Request Body:
{
  "id": 100,
  "name": "Hospital Central",
  "address": "Rua Principal, 123",
  "beds": 50,
  "availableBeds": 30,
  "latitude": "-23.593438",
  "longitude": "-46.710462"
}

Expected Response:
{
  "id": 100,
  "name": "Hospital Central",
  ...
}

Assertions:
- Status Code == 201 or 200
- Response contains id
- Response name matches request name
- Hospital is created in database
```

### 1.4 Test Cases to Generate

**Phase 1A: Hospital Management Tests (20-25 test cases)**

Valid Tests:

1. Create hospital with all required fields
2. Create hospital with minimal fields
3. Create hospital with special characters in name
4. Create hospital with different coordinate formats
5. Get all hospitals (empty list, multiple items)
6. Get single hospital by valid ID
7. Update hospital with all fields
8. Update hospital with only name change
9. Find nearest hospital (various coordinates)
10. Find nearest hospital with radius filter

Invalid Tests:

1. Create hospital with missing name
2. Create hospital with missing address
3. Create hospital with negative bed count
4. Create hospital with available > total beds
5. Create hospital with empty string name
6. Create hospital with invalid coordinates (non-numeric)
7. Get hospital with non-existent ID
8. Update hospital with non-existent ID
9. Create hospital with duplicate ID
10. Get nearest hospital with missing coordinates

**Phase 1B: Inventory Management Tests (15-20 test cases)**

Valid Tests:

1. Add product to hospital inventory
2. List all inventory items for hospital
3. Update product quantity
4. Update product type
5. Delete product from inventory

Invalid Tests:

1. Add product to non-existent hospital
2. Add product with missing name
3. Add product with negative quantity
4. Update product in non-existent hospital
5. Delete product from non-existent hospital

**Phase 1C: Patient Management Tests (10-15 test cases)**

Valid Tests:

1. Create patient with all fields
2. Get all patients list
3. Get single patient details

Invalid Tests:

1. Create patient with missing name
2. Create patient with invalid email
3. Get patient with non-existent ID

---

## Phase 2: AI Model Development

### 2.1 AI Model Architecture

**Framework:** Python-based AI model using:

- **Input:** OpenAPI/Swagger JSON/YAML specification
- **Processing:** LLM (GPT, Claude, or Llama) + Custom logic
- **Output:** Structured test case JSON

**Technology Stack:**

- `langchain` - LLM orchestration
- `openai` / `anthropic` - LLM API
- `pydantic` - Data validation
- `pyyaml` / `json` - OAS parsing
- `python-dotenv` - Configuration management

### 2.2 Model Workflow

```
┌─────────────────────┐
│  OAS Document       │ (YAML/JSON)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ OAS Parser          │ Extract endpoints, parameters, schemas
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ AI Model Processor  │ LLM + Business Logic
│ (LangChain + LLM)   │ Generate test cases
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Test Case Generator │ Create valid/invalid scenarios
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Output: JSON/CSV    │ Exportable test cases
│ Postman Format      │ Can import to Postman
└─────────────────────┘
```

### 2.3 AI Model Implementation Steps

1. **OAS Parser Module**
   - Parse OpenAPI document
   - Extract: endpoints, methods, parameters, request/response schemas
   - Identify: required fields, data types, constraints

2. **Test Case Generation Rules**
   - For each endpoint:
     - Generate 3-5 valid test cases
     - Generate 3-5 invalid test cases
   - For each parameter:
     - Test valid values
     - Test boundary values
     - Test missing/null values
     - Test wrong data types

3. **Prompt Engineering**
   - Create LLM prompts that understand:
     - API semantics (what endpoint does)
     - Data constraints (min/max, patterns)
     - HTTP standards (status codes, headers)
4. **Post-Processing**
   - Validate generated test cases
   - Remove duplicates
   - Ensure proper JSON/CSV format
   - Add descriptive names and assertions

### 2.4 Expected Output Format

```json
{
  "testCases": [
    {
      "testId": "HC-001",
      "endpoint": "/v1/hospitais/",
      "method": "POST",
      "category": "VALID",
      "description": "Create hospital with all required fields",
      "priority": "HIGH",
      "requestHeaders": {
        "Content-Type": "application/json"
      },
      "requestBody": {
        "name": "Hospital Central",
        "address": "Rua Principal, 123",
        "beds": 50,
        "availableBeds": 30,
        "latitude": "-23.593438",
        "longitude": "-46.710462"
      },
      "expectedStatusCode": 201,
      "expectedResponseFields": ["id", "name", "address"],
      "assertions": [
        "status == 201",
        "response.name == request.name",
        "response.id exists"
      ]
    }
  ]
}
```

---

## Phase 3: Implementation Details

### 3.1 Directory Structure

```
Hospital-Testing-System/
├── phase1_manual_tests/
│   ├── test_cases.json         # All manual test cases
│   ├── postman_collection.json # Updated Postman collection
│   └── test_results.json       # Results from Postman execution
│
├── phase2_ai_model/
│   ├── src/
│   │   ├── main.py             # Entry point
│   │   ├── oas_parser.py        # Parse OAS documents
│   │   ├── test_generator.py    # Generate test cases
│   │   ├── llm_processor.py      # LLM integration
│   │   └── output_formatter.py   # Format output
│   │
│   ├── prompts/
│   │   ├── valid_tests.txt      # Prompt for valid test generation
│   │   └── invalid_tests.txt    # Prompt for invalid test generation
│   │
│   ├── requirements.txt          # Python dependencies
│   ├── config.py                 # Configuration (API keys, etc)
│   └── tests.py                  # Unit tests for model
│
├── oas_docs/
│   ├── Hospital-API-OpenAPI.yaml # OAS specification
│   └── Hospital-API-OpenAPI.json # OAS JSON format
│
├── README.md                      # Project documentation
└── TEST_EXECUTION_GUIDE.md        # How to run tests
```

### 3.2 Implementation Timeline

**Week 1: Phase 1 (Manual Testing)**

- [ ] Extract all API endpoints
- [ ] Design test case templates
- [ ] Generate valid test cases (40 cases)
- [ ] Generate invalid test cases (40 cases)
- [ ] Create/update Postman collection
- [ ] Execute tests and document results

**Week 2: Phase 2 (AI Model Development)**

- [ ] Set up Python environment
- [ ] Implement OAS parser
- [ ] Implement test case generator
- [ ] Integrate LLM (OpenAI/Anthropic)
- [ ] Create output formatters
- [ ] Test with Hospital API's OAS spec

**Week 3: Phase 3 (Integration & Refinement)**

- [ ] Create command-line interface (CLI)
- [ ] Add configuration management
- [ ] Create documentation
- [ ] Add error handling and validation
- [ ] Create example runs
- [ ] Package for distribution

---

## Phase 4: Technologies & Tools

### Backend Testing

- **Postman** - Manual API testing, test automation
- **Newman** - Command-line Postman runner
- **REST Client** (VS Code extension) - Quick testing

### AI/ML Stack

- **Python 3.9+**
- **LangChain** - LLM framework
- **OpenAI API** / **Anthropic Claude** - LLM provider
- **Pydantic** - Data validation
- **PyYAML** - YAML parsing
- **Requests** - HTTP client for API testing

### Validation & Quality

- **Pytest** - Unit testing AI model
- **JSON Schema Validator** - Validate generated test cases
- **Black** - Code formatting

---

## Phase 5: Success Criteria

### Phase 1 Success

- [ ] 80+ manual test cases created and documented
- [ ] 100% of endpoints have valid + invalid tests
- [ ] Postman collection updated with all tests
- [ ] All tests executable in Postman
- [ ] Test results documented (pass/fail/edge cases)

### Phase 2 Success

- [ ] AI model successfully parses OAS documents
- [ ] Generates 3-5 test cases per endpoint automatically
- [ ] Output format matches manual test case structure
- [ ] Model generates both valid and invalid test cases
- [ ] Generated test cases are executable in Postman

### Overall Success

- [ ] Fully automated test case generation from any OAS spec
- [ ] Testable on any REST API with OAS documentation
- [ ] Comprehensive documentation for users
- [ ] CLI tool for easy usage
- [ ] Extensible architecture for future improvements

---

## Phase 6: Future Enhancements

1. **Advanced AI Features**
   - Learn from manual test execution results
   - Auto-discover API contracts
   - Generate performance test cases
   - Generate security test cases (OWASP)

2. **Integration**
   - CI/CD pipeline integration (GitHub Actions, Jenkins)
   - API gateway integration
   - Test result database
   - Dashboard for test analytics

3. **Extended Testing**
   - Load testing scenario generation
   - Security testing (SQL injection, XSS)
   - Compatibility testing across API versions
   - GraphQL API support

4. **Deployment**
   - Docker containerization
   - Cloud deployment (AWS, Azure, GCP)
   - Web UI for test generation
   - API endpoint for test generation as a service

---

## Next Steps

1. **Immediate Action:** Confirm Phase 1 approach
2. **Week 1 Focus:** Generate all manual test cases for Hospital API
3. **Testing:** Execute on Postman and document results
4. **Week 2 Focus:** Start AI model development
5. **Integration:** Create CLI tool that ties everything together

---

## Success Metrics

| Metric                     | Target        | Phase   |
| -------------------------- | ------------- | ------- |
| Test Cases Generated       | 80+           | Phase 1 |
| Endpoint Coverage          | 100%          | Phase 1 |
| Valid Cases Per Endpoint   | 3-5           | Both    |
| Invalid Cases Per Endpoint | 3-5           | Both    |
| AI Model Accuracy          | 85%+          | Phase 2 |
| Postman Integration        | Complete      | Phase 1 |
| Documentation              | Comprehensive | Phase 3 |

---

## Questions for Your Guide

1. Do you want integration with a specific LLM (OpenAI, Claude, open-source)?
2. Should test cases include performance/load testing?
3. Do you want a web UI or CLI-only tool?
4. Should the model be fine-tuned on API testing data?
5. Do you need test execution reports/dashboards?
