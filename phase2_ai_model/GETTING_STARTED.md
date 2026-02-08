# Quick Start Guide - Phase 2: AI Test Case Generator

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd phase2_ai_model
pip install -r requirements.txt
```

### 2. Set Up API Keys

Choose one of the following:

**Option A: Using OpenAI (Recommended)**

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI key
OPENAI_API_KEY=sk-... (your OpenAI API key)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
```

**Option B: Using Anthropic Claude**

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Anthropic key
ANTHROPIC_API_KEY=... (your Anthropic API key)
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-opus-20240229
```

### 3. Prepare OAS Specification

You need an OpenAPI specification for the Hospital API.

**Option A: Generate from Postman Collection**

```bash
# Use the existing Postman collection:
../manual_testing/postman/collections/Hospital\ Management\ System\ API\ Tests.postman_collection.json
```

**Option B: Create OAS Specification Manually**
Create `../oas_docs/hospital-api.yaml`:

```yaml
openapi: 3.0.0
info:
  title: Hospital Management API
  version: 1.0.0
servers:
  - url: http://localhost:8080
  - url: http://localhost:8080/api/v1
paths:
  /hospitais:
    post:
      summary: Create a hospital
      operationId: createHospital
      tags:
        - Hospitals
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                address:
                  type: string
                beds:
                  type: integer
              required:
                - name
                - address
      responses:
        "201":
          description: Hospital created successfully
```

### 4. Generate Test Cases

```bash
# Basic usage
python main.py ../oas_docs/hospital-api.yaml

# With options
python main.py ../oas_docs/hospital-api.yaml \
  --valid-per-endpoint 3 \
  --invalid-per-endpoint 3 \
  --output-format json

# As Postman collection
python main.py ../oas_docs/hospital-api.yaml \
  --output-format postman
```

### 5. Check Results

Generated test cases are in the `output/` folder:

```bash
ls -la output/
# generated_tests_json.json
# generated_tests_postman.json (if using Postman format)
```

## Common Issues & Solutions

### "API key not provided"

```bash
# Add API key to .env file:
OPENAI_API_KEY=your_actual_key_here
```

### "Module not found: openai"

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "OAS file not found"

```bash
# Check file path
ls -la ../oas_docs/hospital-api.yaml

# Use absolute path if needed
python main.py /full/path/to/hospital-api.yaml
```

### "Invalid OAS format"

- Ensure YAML or JSON is valid syntax
- Use yamllint for YAML validation: `pip install yamllint`
- Use jsonlint for JSON validation: `pip install jsonlint`

## Testing the Generator

Run unit tests:

```bash
cd tests
pytest test_oas_parser.py -v
```

## Next Steps

1. **Validate Generated Test Cases**
   - Check `output/generated_tests_json.json`
   - Verify test case structure

2. **Export to Postman**
   - Use `--output-format postman` flag
   - Import into Postman: File → Import → Choose JSON file

3. **Execute Tests**
   - In Postman: Click "Run Collection"
   - Check test execution results
   - Fix any API endpoint issues

4. **Iterate**
   - Adjust test parameters
   - Regenerate if needed
   - Compare with manual tests from Phase 1

## Understanding the Generation Process

```
OAS Specification
       ↓
    [OASParser]
       ↓
 Parsed Endpoints
       ↓
   [LLMProcessor]
       ↓
 Generated Test Cases
       ↓
  [TestCaseValidator]
       ↓
Validated Test Cases
       ↓
  [OutputFormatter]
       ↓
  JSON/CSV/Postman
```

## Monitoring Generation

Enable verbose logging to see what's happening:

```bash
python main.py ../oas_docs/hospital-api.yaml --verbose
```

Check logs in `logs/ai_generator.log`

## Example Output

Generated test case example:

```json
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
    "beds": 50
  },
  "expectedStatusCode": 201,
  "expectedResponseFields": ["id", "name", "address"],
  "assertions": ["status == 201", "response.name == 'Hospital Central'"]
}
```

## Configuration Options

All options can be set via:

1. `.env` file (persistent)
2. Command-line arguments (override .env)
3. Hardcoded in `config.py`

Common configurations:

```bash
# More test cases
python main.py file.yaml --valid-per-endpoint 5 --invalid-per-endpoint 5

# Different model
python main.py file.yaml --model gpt-3.5-turbo

# Specific endpoints
python main.py file.yaml --tags hospital inventory

# Different output
python main.py file.yaml --output-format csv
```

## Getting Help

1. Check logs: `tail -f logs/ai_generator.log`
2. Review README.md for detailed documentation
3. Check module docstrings: `python -c "import src.oas_parser; help(src.oas_parser)"`
4. Run with `--verbose` flag

---

**Next Phase**: Once tests are generated and validated, move to Phase 3: Integration & CLI Enhancement
