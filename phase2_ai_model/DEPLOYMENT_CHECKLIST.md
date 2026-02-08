# Phase 2 Deployment & Testing Checklist

## Pre-Deployment Checklist

### Environment Setup

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Working directory: `phase2_ai_model/`
- [ ] Virtual environment created (recommended)
- [ ] Git repository initialized in parent directory

### Dependencies Installation

- [ ] `pip install -r requirements.txt` executed successfully
- [ ] All packages installed without errors
- [ ] Check with: `pip list | grep -E "openai|anthropic|pydantic"`

### Configuration

- [ ] `.env` file created (from `.env.example`)
- [ ] API keys configured:
  - [ ] OPENAI_API_KEY set (if using OpenAI)
  - [ ] ANTHROPIC_API_KEY set (if using Anthropic)
- [ ] LLM_PROVIDER specified correctly
- [ ] LLM_MODEL specified correctly
- [ ] All paths verified to exist

### Files & Structure

- [ ] `src/` directory has all modules:
  - [ ] `__init__.py`
  - [ ] `oas_parser.py`
  - [ ] `llm_processor.py`
  - [ ] `test_generator.py`
  - [ ] `output_formatter.py`
- [ ] `prompts/` directory has templates:
  - [ ] `valid_tests.txt`
  - [ ] `invalid_tests.txt`
- [ ] `config.py` exists
- [ ] `main.py` exists
- [ ] OAS spec exists at `../oas_docs/hospital-api.json`

## Testing Phase 1: Unit Tests

### Run Unit Tests

```bash
cd tests
pytest test_oas_parser.py -v
```

**Checklist:**

- [ ] All tests pass
- [ ] No import errors
- [ ] No assertion failures
- [ ] Coverage > 80%

**Expected Output:**

```
test_oas_parser_initialization PASSED
test_parse_endpoints PASSED
test_endpoint_attributes PASSED
test_get_endpoints_summary PASSED
```

## Testing Phase 2: Module Verification

### Test OAS Parser

```bash
python -c "from src.oas_parser import OASParser; p = OASParser('../oas_docs/hospital-api.json'); p.parse(); print(p.get_endpoint_summary())"
```

**Checklist:**

- [ ] OAS file loads without errors
- [ ] Endpoints parsed successfully
- [ ] Summary shows expected endpoints
- [ ] No parsing errors

**Expected Output:**

```json
{
  "api_title": "Hospital Management System API",
  "api_version": "1.0.0",
  "total_endpoints": 13,
  "methods": { "POST": 4, "GET": 6, "PUT": 2, "DELETE": 1 }
}
```

### Test LLM Configuration

```bash
python -c "from config import OPENAI_API_KEY; print(f'API Key configured: {bool(OPENAI_API_KEY)}')"
```

**Checklist:**

- [ ] API key is configured
- [ ] No errors loading config
- [ ] Environment variables loaded correctly

### Test Output Formatters

```bash
python -c "from src.output_formatter import FormatterFactory; f = FormatterFactory.create_formatter('json'); print(f'JSON Formatter created: {type(f).__name__}')"
```

**Checklist:**

- [ ] All formatters load correctly
- [ ] Factory pattern working
- [ ] No import errors

## Testing Phase 3: Integration Test

### Generate Sample Test Cases

```bash
python main.py ../oas_docs/hospital-api.json --verbose
```

**Checklist:**

- [ ] Command executes without errors
- [ ] OAS file is parsed
- [ ] LLM is called successfully
- [ ] Test cases are generated
- [ ] Output files created in `output/` directory
- [ ] Logs written to `logs/ai_generator.log`

**Expected Behavior:**

1. Reads OAS specification
2. Parses endpoints
3. Connects to LLM
4. Generates test cases
5. Validates test cases
6. Exports results
7. Displays summary

**Expected Output:**

```
============================================================
✓ Generated 78 test cases

Output: phase2_ai_model/output/generated_tests_json.json

Statistics:
  total_test_cases: 78
  valid_test_cases: 39
  invalid_test_cases: 39
  endpoints_covered: 13
  endpoints_total: 13
  avg_cases_per_endpoint: 6.0
============================================================
```

## Testing Phase 4: Output Validation

### Check Generated JSON

```bash
python -c "import json; data = json.load(open('output/generated_tests_json.json')); print(f'Test cases: {len(data[\"testCases\"])}')"
```

**Checklist:**

- [ ] JSON file is valid
- [ ] Contains testCases array
- [ ] Each test case has required fields
- [ ] No syntax errors

### Validate Test Case Structure

```bash
python -c "
import json
data = json.load(open('output/generated_tests_json.json'))
tc = data['testCases'][0]
required = ['testId', 'endpoint', 'method', 'category', 'expectedStatusCode']
print('Valid structure:', all(k in tc for k in required))
"
```

**Checklist:**

- [ ] All test cases have required fields
- [ ] Categories are VALID or INVALID
- [ ] Endpoints start with /v1/
- [ ] Methods are valid HTTP verbs

### Compare with Phase 1 Tests

```bash
python -c "
import json
phase1 = json.load(open('../manual_testing/test_cases.json'))
phase2 = json.load(open('output/generated_tests_json.json'))
print(f'Phase 1: {len(phase1[\"testCases\"])} test cases')
print(f'Phase 2: {len(phase2[\"testCases\"])} test cases')
"
```

**Checklist:**

- [ ] Phase 2 generated reasonable number of tests
- [ ] Similar structure to Phase 1
- [ ] Both valid and invalid categories present

## Testing Phase 5: Export Formats

### Test JSON Export

```bash
ls -lh output/generated_tests_json.json
```

**Checklist:**

- [ ] File exists
- [ ] File size > 10KB (reasonable size)
- [ ] File is valid JSON

### Test CSV Export

```bash
python main.py ../oas_docs/hospital-api.json --output-format csv
ls -lh output/generated_tests_csv.csv
```

**Checklist:**

- [ ] CSV file created
- [ ] Headers present
- [ ] Data rows present
- [ ] Readable in spreadsheet

### Test Postman Export

```bash
python main.py ../oas_docs/hospital-api.json --output-format postman
head -50 output/generated_tests_postman.json | grep -E '"name"|"method"'
```

**Checklist:**

- [ ] Postman collection created
- [ ] Contains request items
- [ ] Valid JSON structure
- [ ] Importable in Postman

## Testing Phase 6: Feature Tests

### Test Verbose Logging

```bash
python main.py ../oas_docs/hospital-api.json --verbose 2>&1 | head -20
```

**Checklist:**

- [ ] Debug messages displayed
- [ ] Detailed logging output
- [ ] No errors in logs

### Test Tag Filtering

```bash
python main.py ../oas_docs/hospital-api.json --tags Hospitals
```

**Checklist:**

- [ ] Only Hospital endpoints processed
- [ ] Generated fewer test cases
- [ ] Correct endpoints in output

### Test Custom Parameters

```bash
python main.py ../oas_docs/hospital-api.json --valid-per-endpoint 5 --invalid-per-endpoint 5
```

**Checklist:**

- [ ] Command accepts parameters
- [ ] Parameters are applied
- [ ] More test cases generated

### Test Different Models

```bash
python main.py ../oas_docs/hospital-api.json --model gpt-3.5-turbo
```

**Checklist:**

- [ ] Model parameter accepted
- [ ] Uses specified model
- [ ] Results are similar

## Performance Testing

### Measure Generation Time

```bash
time python main.py ../oas_docs/hospital-api.json > /dev/null
```

**Expected Results:**

- Single endpoint: < 10 seconds
- All endpoints (13): 2-5 minutes (depending on model)

**Checklist:**

- [ ] Generation completes within reasonable time
- [ ] No timeouts
- [ ] Consistent timing

### Monitor Token Usage

```bash
grep "tokens_used" logs/ai_generator.log
```

**Checklist:**

- [ ] Token usage logged
- [ ] Reasonable token consumption
- [ ] Cost estimate available

## Error Recovery Testing

### Test with Missing OAS File

```bash
python main.py /nonexistent/file.yaml
```

**Expected**: Error message about file not found  
**Checklist:**

- [ ] Graceful error handling
- [ ] Helpful error message
- [ ] Exit code non-zero

### Test with Invalid API Key

```bash
export OPENAI_API_KEY=invalid_key
python main.py ../oas_docs/hospital-api.json
```

**Expected**: API authentication error  
**Checklist:**

- [ ] Error is caught
- [ ] Helpful message provided
- [ ] Logs contain error details

### Test with missing dependencies

```bash
# Simulate by temporarily removing package
pip uninstall openai -y
python main.py ../oas_docs/hospital-api.json
pip install openai  # reinstall
```

**Expected**: ImportError message  
**Checklist:**

- [ ] Error is informative
- [ ] Suggests solution
- [ ] Doesn't crash with traceback

## Documentation Verification

### Check All Documentation Files

- [ ] README.md - Comprehensive guide
  - [ ] Installation section
  - [ ] Usage examples
  - [ ] Configuration options
  - [ ] Troubleshooting section

- [ ] GETTING_STARTED.md - Quick start
  - [ ] 5-minute setup
  - [ ] Common issues & solutions
  - [ ] Example commands

- [ ] ARCHITECTURE.md - System design
  - [ ] Component diagrams
  - [ ] Data flow
  - [ ] Module interactions

- [ ] PHASE2_IMPLEMENTATION_SUMMARY.md - Overview
  - [ ] What's created
  - [ ] How to use
  - [ ] Next steps

### Code Documentation

- [ ] Module docstrings present
- [ ] Function docstrings present
- [ ] Type hints where applicable
- [ ] Comments for complex logic

## Final Validation Checklist

### Core Functionality

- [ ] OAS parsing works
- [ ] LLM integration works
- [ ] Test generation works
- [ ] Validation works
- [ ] Export to JSON works
- [ ] Export to CSV works
- [ ] Export to Postman works

### Robustness

- [ ] Handles missing files
- [ ] Handles invalid input
- [ ] Handles API errors
- [ ] Handles network errors
- [ ] Proper error messages

### Code Quality

- [ ] No syntax errors
- [ ] No import errors
- [ ] Proper logging
- [ ] Configuration management
- [ ] Code follows PEP 8

### Documentation

- [ ] README complete
- [ ] Setup guide complete
- [ ] API documented
- [ ] Examples provided
- [ ] Troubleshooting included

## Deployment Sign-Off

**Phase 2 Ready for Use When:**

- [ ] All unit tests pass
- [ ] Integration test succeeds
- [ ] Output files valid
- [ ] Documentation complete
- [ ] Team approval obtained
- [ ] Version tagged in git

**Sign-Off Date**: ******\_\_\_\_******  
**Tested By**: ******\_\_\_\_******  
**Approved By**: ******\_\_\_\_******

## Next Steps After Deployment

1. **Monitor**: Keep `logs/ai_generator.log` for anomalies
2. **Iterate**: Fine-tune prompts based on results
3. **Share**: Distribute generated test cases to QA team
4. **Execute**: Run test cases in Postman
5. **Report**: Document results for Phase 1 comparison
6. **Improve**: Update prompts based on feedback
7. **Phase 3**: Plan integration with Phase 3

---

**Estimated Deployment Time**: 30-45 minutes  
**Estimated Testing Time**: 2-3 hours  
**Total**: 3-4 hours for full deployment and testing
