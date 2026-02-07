# Test Execution Guide - Hospital Management API

## Prerequisites

### 1. System Requirements

- Postman (Desktop or Web) - for test execution
- Hospital Management API running on `http://localhost:8080`
- MongoDB connection active
- Network access to the API server

### 2. Setup Requirements ✅

#### Start the API Server

```powershell
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\GestaoHospital\"

# Option 1: Using Maven wrapper
.\mvnw.cmd spring-boot:run

# Option 2: Using built JAR
.\mvnw.cmd package
java -jar target\gestaohospitalar-0.0.1.jar
```

**Expected Output:**

```
2026-02-07 10:00:00 - Application started successfully
Server running at: http://localhost:8080
Swagger UI: http://localhost:8080/swagger-ui.html
```

#### Verify API is Running

```bash
# Test connectivity
curl http://localhost:8080/v1/hospitais/

# Expected: 200 OK response with hospital list
```

---

## Postman Setup

### 1. Import Test Cases Collection

1. Open **Postman**
2. Click **Import** (or Ctrl+O)
3. Select file: `postman_collection.json` from `manual_testing/` folder
4. Click **Import**

### 2. Configure Environment Variables

1. In Postman, click **Environments** (left sidebar)
2. Create new environment: `Hospital-API-Testing`
3. Add variables:

| Variable     | Value                    | Scope  |
| ------------ | ------------------------ | ------ |
| `baseURL`    | http://localhost:8080    | Global |
| `hospitalId` | 1                        | Global |
| `productId`  | 5cac077fa9c6543dc892fdf1 | Global |
| `patientId`  | 1                        | Global |

### 3. Select Active Environment

- Click environment dropdown (top-right)
- Select `Hospital-API-Testing`

---

## Running Tests

### Method 1: Manual Testing in Postman UI

#### Step 1: Run a Single Test Case

1. Open collection: **Hospital Management System**
2. Select a test folder (e.g., **Hospitals - Valid Cases**)
3. Click on a test request
4. Click **Send** button
5. Review Response:
   - **Status Code** - Should match expected
   - **Response Body** - Validate returned data
   - **Time** - Check response time (< 500ms ideal)

#### Step 2: Test Categorization

**Valid Test Cases:**

- Expected Status: `200` or `201`
- Response contains requested data
- No error messages

**Invalid Test Cases:**

- Expected Status: `400` or `404`
- Response contains error message
- Explains validation failure

#### Step 3: Document Results

For each test, record:

- ✅ PASS - Status and response match expectations
- ✅ PASS with notes - Minor deviations
- ❌ FAIL - Unexpected status or response
- ⚠️ ERROR - Connection or timeout issues

### Method 2: Automated Testing with Newman

#### Installation

```powershell
# Install Newman globally
npm install -g newman

# Verify installation
newman --version
```

#### Run All Tests

```powershell
# Change to manual_testing directory
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\manual_testing"

# Run collection with HTML report
newman run postman_collection.json `
  -e Hospital-API-Testing.postman_environment.json `
  -r html `
  --reporter-html-export "test-results.html"
```

#### Run Specific Folder

```powershell
# Run only hospital tests
newman run postman_collection.json `
  --folder "Hospitals - Valid Cases"
```

#### Run with Detailed Output

```powershell
# Show all request/response details
newman run postman_collection.json `
  -e Hospital-API-Testing.postman_environment.json `
  --verbose
```

---

## Test Execution Workflow

### Phase 1: Valid Test Cases

1. **Start with Happy Path Tests**
   - Create hospital with all fields ✓
   - Get hospital by ID ✓
   - List all hospitals ✓

2. **Edge Cases**
   - Minimum bed counts
   - Maximum bed counts
   - Special characters in names

3. **Business Logic**
   - Available beds validation
   - Coordinate requirements

### Phase 2: Invalid Test Cases

1. **Missing Fields**
   - Required field: name
   - Required field: address
   - Check error response

2. **Invalid Data Types**
   - String where number expected
   - Non-numeric coordinates
   - Invalid email format

3. **Boundary Violations**
   - Negative values
   - Available > Total beds
   - Invalid status codes

### Phase 3: Integration Tests

1. **Multi-step Scenarios**
   - Create hospital → Get hospital → Update hospital
   - Create hospital → Add inventory → List inventory
   - Find nearest hospital after creation

---

## Expected Response Codes

### Success Responses

| Code  | Meaning    | Test Examples                    |
| ----- | ---------- | -------------------------------- |
| `200` | OK         | GET requests, successful updates |
| `201` | Created    | POST requests for new resources  |
| `204` | No Content | Successful DELETE                |

### Error Responses

| Code  | Meaning      | Test Examples                |
| ----- | ------------ | ---------------------------- |
| `400` | Bad Request  | Invalid data, missing fields |
| `404` | Not Found    | Non-existent resource ID     |
| `500` | Server Error | Unexpected server issues     |

---

## Test Case Execution Checklist

### For Each Test Case:

- [ ] **Request Phase**
  - [ ] Verify method (GET/POST/PUT/DELETE)
  - [ ] Verify endpoint URL
  - [ ] Verify request body (if applicable)
  - [ ] Verify headers (Content-Type, etc.)

- [ ] **Execution Phase**
  - [ ] Click Send
  - [ ] Note response time
  - [ ] Check network status

- [ ] **Validation Phase**
  - [ ] Verify status code matches expected
  - [ ] Check response body structure
  - [ ] Validate error messages (for invalid cases)
  - [ ] Confirm data persistence (for creates/updates)

- [ ] **Documentation Phase**
  - [ ] Record result (PASS/FAIL)
  - [ ] Note any deviations
  - [ ] Add screenshots if issues found
  - [ ] Update test results template

---

## Detailed Test Scenarios

### Hospital Management Tests

#### HC-001: Create Hospital (Valid)

**Steps:**

1. Open Postman request: `Hospitals > Create Hospital Valid`
2. Verify request body has all fields
3. Send request
4. **Expected:** Status 201, response contains hospital ID
5. **Verify:** New hospital appears in GET all hospitals

#### HC-006: Create Hospital Missing Name (Invalid)

**Steps:**

1. Open Postman request: `Hospitals > Create Hospital Invalid - Missing Name`
2. Body has address, beds, but no name
3. Send request
4. **Expected:** Status 400, error mentions "name required"
5. **Validate:** Error message is user-friendly

### Inventory Tests

#### EST-003: Add Product to Hospital (Valid)

**Steps:**

1. Use existing hospital ID (e.g., 1)
2. Send POST with product details
3. **Expected:** Status 201, response has product ID
4. **Verify:** Product appears in inventory list GET

#### EST-007: Add Product to Non-existent Hospital (Invalid)

**Steps:**

1. Use invalid hospital ID (99999)
2. Send POST with product details
3. **Expected:** Status 404, error mentions hospital not found
4. **Verify:** No product created in database

### Patient Tests

#### PAC-001: Create Patient (Valid)

**Steps:**

1. Send POST with firstName, lastName, email
2. **Expected:** Status 201, response has patient ID
3. **Verify:** Patient retrievable via GET

#### PAC-007: Create Patient Invalid Email (Invalid)

**Steps:**

1. Send POST with invalid email format
2. **Expected:** Status 400, error about email format
3. **Verify:** Patient not created

---

## Common Issues & Solutions

### Issue: "Connection refused" error

**Cause:** API server not running
**Solution:**

```powershell
# Verify server is running
curl http://localhost:8080/swagger-ui.html

# If not, start it
.\mvnw.cmd spring-boot:run
```

### Issue: "404 Not Found" on valid endpoint

**Cause:** Incorrect endpoint path or base URL
**Solution:**

- Verify URL in environment variable
- Check spelling of endpoint
- Refer to Swagger UI: http://localhost:8080/swagger-ui.html

### Issue: "400 Bad Request" unexpectedly

**Cause:** Invalid request format or data type
**Solution:**

- Check Content-Type header is application/json
- Validate JSON syntax (use online JSON validator)
- Verify data types match expected

### Issue: MongoDB connection error

**Cause:** MongoDB service not running
**Solution:**

```powershell
# Start MongoDB
mongod

# Verify connection
mongo
> show dbs
```

---

## Test Results Documentation

### How to Document Results

After each test execution, record in `test_results_template.json`:

```json
{
  "testId": "HC-001",
  "executionDate": "2026-02-07",
  "status": "PASS",
  "actualStatusCode": 201,
  "expectedStatusCode": 201,
  "responseTime": "245ms",
  "notes": "Hospital created successfully",
  "environment": "Local Development"
}
```

### Results Summary

After all tests, analyze:

- Total tests executed
- Pass rate percentage
- Failed tests analysis
- Issues found
- Recommendations

---

## Test Execution Timeline

### Quick Test (30 minutes)

```
1. Valid Hospital Creation: 5 tests → 5 mins
2. Invalid Hospital Creation: 5 tests → 5 mins
3. Hospital Retrieval: 4 tests → 5 mins
4. Inventory Creation: 4 tests → 5 mins
5. Patient Creation: 3 tests → 5 mins
Total: 21 tests in 30 mins
```

### Comprehensive Test (2-3 hours)

```
1. Hospital Management: All 30 tests → 45 mins
2. Inventory Management: All 20 tests → 45 mins
3. Patient Management: All 14 tests → 30 mins
4. Integration Tests: 8 tests → 15 mins
5. Documentation: → 15 mins
Total: 72 tests in ~2.5 hours
```

---

## Post-Test Activities

### 1. Generate Test Report

```powershell
# Using Newman HTML reporter
newman run postman_collection.json `
  -r html `
  --reporter-html-export "test-report-$(Get-Date -Format 'yyyy-MM-dd-HHmm').html"
```

### 2. Analyze Results

- [ ] Identify failed tests
- [ ] Document error patterns
- [ ] Categorize issues (data validation, logic, etc.)
- [ ] Prioritize fixes

### 3. Create Bug Reports

For each failure:

- Test ID
- Expected vs Actual behavior
- Steps to reproduce
- Error logs/screenshots
- Severity level

### 4. Iterate & Retest

- Fix identified issues
- Re-run affected tests
- Verify fixes with full test suite

---

## Best Practices

✅ **Do:**

- Test after API changes
- Run full suite before deployment
- Document all findings
- Use consistent naming
- Keep test data clean
- Version control test cases

❌ **Don't:**

- Modify production data
- Run tests concurrently (database conflicts)
- Skip invalid case tests
- Leave test data in database
- Ignore error messages
- Test without API running

---

## Next Steps

1. **Complete Manual Testing**
   - Execute all 98 test cases
   - Document results
   - Identify issues

2. **Generate Test Report**
   - Summary of results
   - Pass/fail breakdown
   - Issues and recommendations

3. **Phase 2 Preparation**
   - Extract API OpenAPI specification
   - Prepare for AI model development
   - Plan test case auto-generation

---

## Contact & Support

**Issues or Questions?**

- Check Swagger UI: http://localhost:8080/swagger-ui.html
- Review request logs in Postman console
- Verify MongoDB is running
- Check API server logs

**Resources:**

- Postman Documentation: https://learning.postman.com
- API Project README: [GestaoHospital/README.md](../../GestaoHospital/README.md)
- Implementation Plan: [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md)
