# Phase 2: AI Test Case Generator

## Overview

The AI Test Case Generator automatically creates comprehensive test cases from OpenAPI (OAS/Swagger) specifications using Large Language Models (LLMs).

## Features

- **Automatic Test Generation**: Generate valid and invalid test cases from OAS specifications
- **Multiple LLM Support**: Works with OpenAI GPT-4 and Anthropic Claude
- **Multiple Output Formats**: JSON, CSV, and Postman Collection formats
- **Validation**: Automatic validation of generated test cases
- **Flexible Configuration**: Configurable via environment variables or CLI arguments
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Architecture

```
OAS Specification
      ↓
OASParser (Extract endpoints, parameters, schemas)
      ↓
TestCaseGenerator (Orchestrate generation)
      ↓
LLMProcessor (Generate using AI)
      ↓
TestCaseValidator (Validate structure)
      ↓
OutputFormatter (Format output)
      ↓
JSON/CSV/Postman
```

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API key or Anthropic API key

### Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys and preferences
```

Or set them directly:

```bash
export OPENAI_API_KEY=your_key_here
export LLM_PROVIDER=openai
```

## Usage

### Basic Usage

Generate test cases from OAS specification:

```bash
python main.py path/to/openapi.yaml
```

### Advanced Usage

```bash
# Generate with Anthropic instead of OpenAI
python main.py path/to/openapi.yaml --provider anthropic

# Specify number of test cases
python main.py path/to/openapi.yaml --valid-per-endpoint 5 --invalid-per-endpoint 5

# Output as Postman collection
python main.py path/to/openapi.yaml --output-format postman

# Filter by specific endpoint tags
python main.py path/to/openapi.yaml --tags hospital inventory

# Verbose logging
python main.py path/to/openapi.yaml --verbose
```

### Command-Line Options

```
positional arguments:
  oas_file                        Path to OpenAPI specification file

optional arguments:
  --provider {openai,anthropic}   LLM provider (default: openai)
  --api-key API_KEY               API key for LLM provider
  --model MODEL                   LLM model to use
  --valid-per-endpoint NUM        Valid test cases per endpoint (default: 3)
  --invalid-per-endpoint NUM      Invalid test cases per endpoint (default: 3)
  --output-format {json,csv,postman}  Output format (default: json)
  --tags TAG [TAG...]             Filter endpoints by tags
  --verbose                       Enable verbose logging
```

## Configuration

### Environment Variables

```bash
# LLM Configuration
LLM_PROVIDER=openai                    # "openai" or "anthropic"
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
LLM_MODEL=gpt-4                       # Model to use
LLM_TEMPERATURE=0.7                   # Creativity level (0-1)

# API Configuration
HOSPITAL_API_BASE_URL=http://localhost:8080
HOSPITAL_API_VERSION=v1

# Test Generation
VALID_TESTS_PER_ENDPOINT=3             # Default valid test cases per endpoint
INVALID_TESTS_PER_ENDPOINT=3           # Default invalid test cases per endpoint
ENABLE_EDGE_CASES=true                 # Include edge case tests

# Output
OUTPUT_FORMAT=json                     # Format: json, csv, or postman
LOG_LEVEL=INFO                         # Logging level

# Features
ENABLE_POSTMAN_EXPORT=true             # Export to Postman format
ENABLE_CSV_EXPORT=true                 # Export to CSV format
VALIDATE_GENERATED_CASES=true          # Validate generated test cases
```

## Output Files

Generated test cases are saved in the `output/` directory:

- `generated_tests_json.json` - JSON format (includes metadata and statistics)
- `generated_tests_csv.csv` - CSV format (simple tabular format)
- `generated_tests_postman.json` - Postman Collection format

## Test Case Structure

Generated test cases follow this structure:

```json
{
  "testId": "HC-001",
  "endpoint": "/v1/hospitais/",
  "method": "POST",
  "category": "VALID",
  "description": "Create hospital with all required fields",
  "priority": "HIGH",
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

## Module Documentation

### oas_parser.py

Parses OpenAPI specifications and extracts:

- Endpoints (paths and methods)
- Parameters (path, query, header, body)
- Request/response schemas
- Required fields and data types
- Constraints (min/max, patterns, enums)

**Key Classes:**

- `OASParser` - Main parser class
- `Endpoint` - Represents an API endpoint
- `Parameter` - Represents an API parameter
- `ResponseSchema` - Represents response structure

### llm_processor.py

Handles LLM integration for test case generation:

- Supports OpenAI and Anthropic
- Prompt engineering for test generation
- Response parsing and JSON extraction
- Error handling and retry logic

**Key Classes:**

- `LLMProvider` - Abstract base class
- `OpenAIProvider` - OpenAI implementation
- `AnthropicProvider` - Anthropic implementation
- `LLMProcessor` - Main processor

### test_generator.py

Orchestrates the entire test generation process:

- Parses OAS specification
- Coordinates LLM processing
- Validates generated test cases
- Provides statistics and reporting

**Key Classes:**

- `TestCaseGenerator` - Main generator
- `TestCaseValidator` - Validates test case structure

### output_formatter.py

Formats and exports test cases to various formats:

- JSON format with metadata and statistics
- CSV format for spreadsheet use
- Postman Collection format for direct API testing

**Key Classes:**

- `OutputFormatter` - Abstract base class
- `JSONFormatter` - JSON export
- `CSVFormatter` - CSV export
- `PostmanFormatter` - Postman collection export
- `FormatterFactory` - Factory for creating formatters

## Examples

### Example 1: Generate JSON Test Cases

```bash
python main.py ../oas_docs/hospital-api.yaml \
  --provider openai \
  --valid-per-endpoint 3 \
  --invalid-per-endpoint 3 \
  --output-format json
```

### Example 2: Generate Postman Collection

```bash
python main.py ../oas_docs/hospital-api.yaml \
  --provider openai \
  --output-format postman
```

### Example 3: Filter by Tags

```bash
python main.py ../oas_docs/hospital-api.yaml \
  --tags hospital inventory patient
```

## Troubleshooting

### API Key Not Found

- Ensure `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is set
- Check `.env` file has correct values
- Use `--api-key` argument to override

### OAS Parsing Errors

- Validate OAS file format (YAML or JSON)
- Check file exists and is readable
- Ensure OAS specification is valid

### LLM Connection Errors

- Check internet connection
- Verify API key is valid
- Check API rate limits
- Review LLM provider status

### Invalid JSON in LLM Response

- LLM may have generated malformed JSON
- Try with different temperature setting
- Check LLM output in logs for details

## Performance Considerations

- **Model Selection**: GPT-4 is more accurate but slower; GPT-3.5 is faster
- **Test Cases Per Endpoint**: More cases = longer generation time
- **Batch Processing**: Generate for multiple endpoints in one run
- **Token Usage**: Monitor LLM API usage for cost management

## Test Case Quality

Generated test cases quality depends on:

- OAS specification quality and completeness
- LLM model capabilities
- Prompt engineering
- Validation filters applied

## Future Enhancements

- [ ] Support for more LLM providers (Llama, PaLM, etc.)
- [ ] Custom prompt templates
- [ ] Test execution integration
- [ ] Performance and load test generation
- [ ] Security test case generation (OWASP)
- [ ] GraphQL support
- [ ] Web UI for test generation
- [ ] CI/CD pipeline integration

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Write clear commit messages
2. Add tests for new features
3. Update documentation
4. Follow code style guidelines

## License

[Your License Here]

## Contact

For questions or support, please contact the project maintainers.
