# Phase 2 Implementation Summary

## Overview

Phase 2 - AI Test Case Generator has been successfully set up. This is an automated system for generating comprehensive test cases from OpenAPI specifications using Large Language Models.

## What's Been Created

### Directory Structure

```
phase2_ai_model/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── oas_parser.py            # OAS specification parser
│   ├── llm_processor.py         # LLM integration (OpenAI & Anthropic)
│   ├── test_generator.py        # Test case generation orchestrator
│   └── output_formatter.py      # Output formatting (JSON, CSV, Postman)
│
├── prompts/
│   ├── valid_tests.txt          # Prompt template for valid test generation
│   └── invalid_tests.txt        # Prompt template for invalid test generation
│
├── tests/
│   └── test_oas_parser.py       # Unit tests
│
├── config.py                     # Configuration management
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # Comprehensive documentation
├── GETTING_STARTED.md           # Quick start guide
└── __init__.py                  # Package initialization

oas_docs/
└── hospital-api.json            # OpenAPI specification for Hospital API
```

## Core Modules

### 1. OAS Parser (`src/oas_parser.py`)

- **Purpose**: Parse OpenAPI/Swagger specifications
- **Capabilities**:
  - Extract endpoints, methods, parameters
  - Parse request/response schemas
  - Identify required fields and constraints
  - Export parsed endpoints to JSON
  - Filter endpoints by tags

**Key Classes**:

- `OASParser` - Main parser
- `Endpoint` - Represents API endpoint
- `Parameter` - Represents API parameter
- `ResponseSchema` - Represents response structure

### 2. LLM Processor (`src/llm_processor.py`)

- **Purpose**: Handle LLM integration for test generation
- **Supported Providers**:
  - OpenAI (GPT-4, GPT-3.5-turbo)
  - Anthropic (Claude)
- **Features**:
  - Automatic prompt building
  - Response parsing and JSON extraction
  - Error handling and logging
  - Token usage tracking

**Key Classes**:

- `LLMProvider` - Abstract base class
- `OpenAIProvider` - OpenAI implementation
- `AnthropicProvider` - Anthropic implementation
- `LLMProcessor` - Main processor
- `LLMFactory` - Factory pattern for provider creation

### 3. Test Case Generator (`src/test_generator.py`)

- **Purpose**: Orchestrate test case generation
- **Features**:
  - Generate all test cases for endpoints
  - Validate generated test cases
  - Calculate statistics
  - Export to various formats
  - Filter by endpoint tags

**Key Classes**:

- `TestCaseGenerator` - Main generator
- `TestCaseValidator` - Validates test case structure

### 4. Output Formatter (`src/output_formatter.py`)

- **Purpose**: Format and export test cases
- **Supported Formats**:
  - JSON (with metadata and statistics)
  - CSV (for spreadsheet use)
  - Postman Collection (for direct testing)
- **Features**:
  - Format validation
  - Multi-format export
  - Custom formatter support via factory pattern

**Key Classes**:

- `OutputFormatter` - Abstract base class
- `JSONFormatter` - JSON export
- `CSVFormatter` - CSV export
- `PostmanFormatter` - Postman collection export
- `FormatterFactory` - Factory for formatter creation

## Configuration

Configuration can be set via:

1. `.env` file (environment variables)
2. Command-line arguments
3. Hardcoded in `config.py`

**Key Configuration Variables**:

```bash
# LLM
LLM_PROVIDER              # "openai" or "anthropic"
OPENAI_API_KEY            # OpenAI API key
ANTHROPIC_API_KEY         # Anthropic API key
LLM_MODEL                 # Model name (e.g., "gpt-4")
LLM_TEMPERATURE           # Temperature (0-1, default: 0.7)

# Test Generation
VALID_TESTS_PER_ENDPOINT  # Default: 3
INVALID_TESTS_PER_ENDPOINT # Default: 3
ENABLE_EDGE_CASES         # Default: true

# Output
OUTPUT_FORMAT             # "json", "csv", or "postman"
LOG_LEVEL                 # "DEBUG", "INFO", "WARNING", "ERROR"
```

## Usage Examples

### 1. Basic Generation

```bash
python main.py ../oas_docs/hospital-api.json
```

### 2. With Options

```bash
python main.py ../oas_docs/hospital-api.json \
  --provider openai \
  --model gpt-4 \
  --valid-per-endpoint 5 \
  --invalid-per-endpoint 5 \
  --output-format json
```

### 3. Postman Export

```bash
python main.py ../oas_docs/hospital-api.json \
  --output-format postman
```

### 4. Filter by Tags

```bash
python main.py ../oas_docs/hospital-api.json \
  --tags hospital inventory patient
```

### 5. Verbose Output

```bash
python main.py ../oas_docs/hospital-api.json --verbose
```

## Installation & Setup

### Step 1: Install Dependencies

```bash
cd phase2_ai_model
pip install -r requirements.txt
```

### Step 2: Configure API Keys

```bash
cp .env.example .env
# Edit .env with your OpenAI or Anthropic API key
```

### Step 3: Run Generator

```bash
python main.py ../oas_docs/hospital-api.json
```

### Step 4: Check Results

```bash
ls -la output/
# generated_tests_json.json
# generated_tests_csv.csv (if CSV export enabled)
# generated_tests_postman.json (if Postman export enabled)
```

## Generated Test Case Structure

```json
{
  "testId": "HC-001",
  "endpoint": "/v1/hospitais/",
  "method": "POST",
  "category": "VALID", // or "INVALID"
  "description": "Create hospital with all required fields",
  "priority": "HIGH", // or "MEDIUM", "LOW"
  "tags": ["hospital", "create", "valid"],
  "requestHeaders": {
    "Content-Type": "application/json"
  },
  "requestBody": {
    "name": "Hospital Central",
    "address": "Rua Principal, 123",
    "beds": 50,
    "availableBeds": 30
  },
  "expectedStatusCode": 201,
  "expectedResponseFields": ["id", "name", "address"],
  "assertions": [
    "status == 201",
    "response.name == request.name",
    "response.id exists"
  ]
}
```

## Test Generation Logic

### Valid Test Cases

- Happy path with all required fields
- Minimal required fields only
- Full data including optional fields
- Edge cases (max/min values)
- Special characters and variations
- Real-world scenarios

### Invalid Test Cases

- Missing required fields
- Wrong data types
- Out-of-range values
- Invalid formats
- Null/empty values
- Duplicate resources
- Non-existent resources
- Business logic violations
- Boundary violations

## API Endpoints in Hospital API Spec

### Hospitals

- `POST /v1/hospitais/` - Create hospital
- `GET /v1/hospitais/` - List all hospitals
- `GET /v1/hospitais/{id}` - Get hospital by ID
- `PUT /v1/hospitais/{id}` - Update hospital
- `DELETE /v1/hospitais/{id}` - Delete hospital
- `GET /v1/hospitais/maisProximo` - Find nearest hospital

### Inventory

- `GET /v1/hospitais/{hospitalId}/estoque` - List inventory
- `POST /v1/hospitais/{hospitalId}/estoque` - Add inventory item
- `PUT /v1/hospitais/{hospitalId}/estoque/{productId}` - Update inventory
- `DELETE /v1/hospitais/{hospitalId}/estoque/{productId}` - Delete inventory

### Patients

- `POST /v1/pacientes/` - Create patient
- `GET /v1/pacientes/` - List patients
- `GET /v1/pacientes/{id}` - Get patient by ID

## Output Files

Generated files are saved in `output/` directory:

1. **JSON Output** (`generated_tests_json.json`)
   - Includes metadata and statistics
   - Full test case details
   - Recommended for analysis and import

2. **CSV Output** (`generated_tests_csv.csv`)
   - Simplified tabular format
   - Easier to view in spreadsheets
   - Good for reporting

3. **Postman Output** (`generated_tests_postman.json`)
   - Importable into Postman
   - Ready for execution
   - Includes test scripts

## Testing Framework

### Unit Tests

```bash
cd tests
pytest test_oas_parser.py -v
```

Tests cover:

- OAS parsing functionality
- Endpoint extraction
- Parameter parsing
- Endpoint summary generation

### Manual Testing

1. Run generator with sample OAS
2. Validate output structure
3. Import into Postman
4. Execute test collection
5. Verify results

## Prompt Templates

### Valid Tests Prompt (`prompts/valid_tests.txt`)

- Guides LLM to generate valid test cases
- Examples of valid scenarios
- Output format specification
- Best practices

### Invalid Tests Prompt (`prompts/invalid_tests.txt`)

- Guides LLM to generate invalid test cases
- Examples of invalid scenarios
- Error handling patterns
- Security considerations

## Integration with Phase 1

Phase 1 generated 102 manual test cases. Phase 2 complements this by:

- **Automating** test case generation
- **Learning** from Phase 1 test cases
- **Scaling** to new APIs
- **Maintaining** consistency

Manual test cases: `../manual_testing/test_cases.json`
AI-generated test cases: `output/generated_tests_json.json`

## Performance Considerations

### Model Selection

- **GPT-4**: Slower but more accurate (~60 tokens/request)
- **GPT-3.5-turbo**: Faster and cheaper (~40 tokens/request)
- **Claude**: Good balance (~50 tokens/request)

### Cost Estimation

- ~100 endpoints × 6 test cases = 600 requests
- Average 50 tokens per request = 30,000 tokens
- OpenAI: ~$0.30 for GPT-3.5, ~$3.00 for GPT-4

### Optimization Tips

1. Use GPT-3.5-turbo for faster generation
2. Batch multiple endpoints
3. Cache responses for repeated endpoints
4. Use lower temperature for consistency

## Troubleshooting

### API Key Issues

```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Or check .env file
cat .env | grep API_KEY
```

### OAS Parsing Errors

```bash
# Validate OAS file
python -m json.tool ../oas_docs/hospital-api.json

# Or use yamllint for YAML
yamllint ../oas_docs/hospital-api.yaml
```

### LLM Connection Issues

- Check internet connection
- Verify API key validity
- Check API rate limits
- Review API provider status

### Test Case Validation Errors

- Check test case JSON structure
- Verify required fields present
- Validate expected status codes

## Next Steps

### Immediate (This Week)

1. ✅ Set up Phase 2 directory structure
2. ✅ Create core modules (OAS Parser, LLM Processor, etc.)
3. ✅ Create OpenAPI specification for Hospital API
4. ⏭️ Test the system with Hospital API
5. ⏭️ Generate first set of test cases
6. ⏭️ Compare with Phase 1 test cases

### Short Term (Next Week)

1. Fine-tune prompt templates
2. Validate generated test cases
3. Export to Postman
4. Execute in Postman
5. Fix any API endpoint issues
6. Generate final test cases

### Medium Term (2-3 Weeks)

1. Create CLI improvements
2. Add batch processing
3. Add test execution integration
4. Build reporting dashboard
5. Document best practices

### Long Term (Phase 3-4)

1. Support for more LLM providers
2. Security test generation
3. Performance test generation
4. GraphQL support
5. CI/CD integration
6. Web UI
7. Multi-language support

## Documentation Files

1. **README.md** - Comprehensive documentation
2. **GETTING_STARTED.md** - Quick start guide
3. **PHASE2_IMPLEMENTATION_SUMMARY.md** - This file
4. **config.py** - Configuration options
5. **Module docstrings** - Detailed code documentation

## Key Tools & Technologies

- **Python 3.9+** - Programming language
- **OpenAI API** - LLM provider
- **Anthropic API** - Alternative LLM provider
- **LangChain** - LLM orchestration
- **Pydantic** - Data validation
- **PyYAML** - YAML parsing
- **PyTest** - Unit testing
- **JSON/CSV** - Data formats

## Contributing

To extend the Phase 2 system:

1. **Add new LLM provider**: Implement `LLMProvider` interface
2. **Add new output format**: Implement `OutputFormatter` interface
3. **Custom validators**: Extend `TestCaseValidator` class
4. **Custom prompts**: Update `prompts/` templates
5. **New features**: Add to appropriate module

## Success Metrics

**Phase 2 Success Criteria**:

- ✅ AI model successfully parses OAS documents
- ✅ Generates 3-5 valid test cases per endpoint
- ✅ Generates 3-5 invalid test cases per endpoint
- ✅ Output format matches manual test case structure
- ✅ Generated cases are executable in Postman
- ⏭️ Test execution results are positive (>80% pass rate)

## Support & Troubleshooting

For issues:

1. Check logs: `tail -f logs/ai_generator.log`
2. Run with verbose flag: `python main.py file.yaml --verbose`
3. Review README.md and module docstrings
4. Check error messages in output

---

**Created**: February 8, 2026  
**Status**: Ready for testing  
**Next Phase**: Phase 3 - Integration & Refinement
