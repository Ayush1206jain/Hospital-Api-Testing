# Test Execution Guide - Phase 1: Manual Testing

## Overview

This document guides you through executing the comprehensive test suite for the Hospital Management API. The test suite includes **65 test cases** covering:

- **Hospital Management** (9 endpoints)
- **Inventory Management** (6 endpoints)
- **Patient Management** (7 endpoints)
- **Location & Proximity** (2 endpoints)

**Test Coverage:**

- Valid scenarios: 35 tests
- Invalid scenarios: 30 tests
- Total endpoints: 18

---

## Prerequisites

1. **Backend Service Running:** The Hospital Management API must be running on `http://localhost:8080`
2. **Database:** MongoDB must be running with the `HospitalDB` database
3. **Postman Installed:** Download from [getpostman.com](https://getpostman.com)
4. **Sample Data Loaded:** Backend auto-seeds sample data on startup

### Quick Backend Check

```powershell
# Check if backend is running
curl http://localhost:8080/v1/hospitais/
```

If you get hospital data back, the backend is ready.

---

## Method 1: Using Postman GUI (Recommended for Manual Testing)

### Step 1: Import the Postman Collection

1. Open **Postman**
2. Click **File > Import** (or Ctrl+O)
3. Choose **Upload Files** tab
4. Select `postman_collection.json` from `manual_testing/` folder
5. Click **Import**

### Step 2: Set Environment Variables

1. Click **Environments** in left panel
2. Create a new environment called "Hospital API Local"
3. Add this variable:
   - **Key:** `base_url`
   - **Value:** `http://localhost:8080`
4. Select the environment from the top-right dropdown

### Step 3: Run Individual Requests

1. Expand the collection in the left panel
2. Select a test (e.g., "Hospital Management" > "[VALID] List all hospitals")
3. Click **Send**
4. Check the response and test results in the **Tests** tab

### Step 4: Run the Entire Collection

1. Click on the collection name "Hospital Management System API Tests"
2. Click **Run** button (or right-click > Run collection)
3. This opens the Collection Runner
4. Select desired options:
   - **Environment:** Hospital API Local
   - **Iterations:** 1
   - **Delay:** 500ms (between requests)
   - **Deselect:** Any tests you want to skip
5. Click **Run Hospital Management System API Tests**

### Step 5: View Test Results

After the collection run completes:

- **Summary Panel** shows: Total runs, Pass/Fail count
- **Individual Request Results** show:
  - Status code
  - Response time
  - Assertions passed/failed
  - Response body

### Example Test Assertions (Built-in)

Each test includes automatic assertions like:

```javascript
✓ Status code should be 200
✓ Response should contain hospital data
✓ Hospital should be updated
```

---

## Method 2: Command-Line Testing with Newman

**Newman** is Postman's command-line runner. Great for CI/CD integration.

### Installation

```powershell
npm install -g newman
npm install -g newman-reporter-html
```

### Run All Tests

```powershell
cd manual_testing

newman run postman_collection.json `
  --environment postman_environment.json `
  --reporters cli,html `
  --reporter-html-export test-results.html
```

### Run Specific Test Suite

```powershell
# Hospital Management tests only
newman run postman_collection.json `
  --folder "Hospital Management" `
  --reporters cli
```

### Run with Delays

```powershell
# 1000ms delay between requests
newman run postman_collection.json `
  --delay-request 1000 `
  --reporters cli
```

### View HTML Report

After running with the HTML reporter, open the generated HTML file:

```powershell
start test-results.html
```

---

## Method 3: Manual Testing with REST Client (VS Code)

### Installation

Install the **REST Client** extension in VS Code.

### Using the `.rest` Files

We'll create example requests (optional). For now, use the test cases from `test_cases.json`.

### Example Request Format

Create a file `requests.rest`:

```
@baseUrl = http://localhost:8080

### TC-010: List all hospitals
GET {{baseUrl}}/v1/hospitais/

### TC-011: Get single hospital
GET {{baseUrl}}/v1/hospitais/1

### TC-001: Create hospital
POST {{baseUrl}}/v1/hospitais/
Content-Type: application/json

{
  "id": "100",
  "name": "Hospital Central",
  "address": "Rua Principal, 123",
  "beds": 50,
  "availableBeds": 30
}
```

Then click **Send Request** above each endpoint.

---

## Test Case Organization

### Test Files in `manual_testing/` folder

1. **test_cases.json** - All 65 test cases with:
   - Test ID (HC-001, HC-002, etc.)
   - Endpoint
   - HTTP Method
   - Request body
   - Expected response
   - Assertions

2. **postman_collection.json** - Postman-ready collection with:
   - Pre-written requests for key scenarios
   - Automated assertions
   - Environment variables
   - Test organization by resource

3. **TEST_EXECUTION_GUIDE.md** (this file)

---

## Sample Test Case Walkthrough

### Test: HC-010 - List All Hospitals

**Endpoint:** `GET /v1/hospitais/`

**Expected Status:** 200

**Test Assertion:**

```javascript
pm.test("Response should be an array", function () {
  var jsonData = pm.response.json();
  pm.expect(Array.isArray(jsonData)).to.be.true;
  pm.expect(jsonData.length).to.be.at.least(3);
});
```

**Execution in Postman:**

1. Select "Hospital Management" > "[VALID] List all hospitals"
2. Click **Send**
3. Response shows array of hospitals
4. Check **Tests** tab: ✓ All assertions pass

---

## Expected Test Results

### Valid Tests (35 cases)

These tests should **PASS**:

- Creating hospitals with valid data
- Updating hospitals
- Listing resources
- Adding products to inventory
- Checking in/out patients
- Finding nearest hospitals

**Expected Result:** ✅ Status 200 or 201

### Invalid Tests (30 cases)

These tests should receive **appropriate error responses**:

- Missing required fields → Status 400
- Non-existent IDs → Status 404
- Negative values → Status 400
- Invalid data types → Status 400

**Expected Result:** ✅ Status 400 or 404

---

## Common Issues & Troubleshooting

### Issue: "Connection refused" error

**Solution:**

- Ensure backend is running: `.\mvnw.cmd spring-boot:run`
- Check backend logs for startup errors
- Verify MongoDB is running

### Issue: Tests fail with 404 on valid requests

**Solution:**

- Confirm sample data is loaded (check MongoDB `HospitalDB` database)
- Use IDs "1", "2", "3" which are pre-populated
- For inventory tests, first add a product via `POST /v1/hospitais/1/estoque`

### Issue: CORS errors

**Solution:**

- Frontend should run on `http://localhost:4200`
- API allows CORS from `http://localhost:4200`
- If testing from other origin, backend allows it in `@CrossOrigin`

### Issue: Invalid JSON in request body

**Solution:**

- Verify JSON syntax in Postman request body
- Use Postman's JSON formatter (Ctrl+Shift+J)
- Check test_cases.json for correct request format

---

## Test Execution Checklist

Use this checklist to track test execution:

```
Phase 1 - Manual Testing Checklist
=====================================

SETUP
☐ Backend running on http://localhost:8080
☐ MongoDB running with HospitalDB
☐ Postman installed
☐ Postman collection imported
☐ Environment variables set (base_url)

HOSPITAL MANAGEMENT TESTS
☐ HC-001: Create hospital
☐ HC-010: List all hospitals
☐ HC-011: Get single hospital
☐ HC-013: Update hospital
☐ HC-020: Get available beds
☐ HC-022: Find nearest hospital
☐ HC-004-009: Invalid tests (missing fields, negative values)

INVENTORY MANAGEMENT TESTS
☐ HC-027: Add product
☐ HC-032: List inventory
☐ HC-034: Get product details
☐ HC-036: Update product
☐ HC-029-031: Invalid tests

PATIENT MANAGEMENT TESTS
☐ HC-041: List patients
☐ HC-043: Get patient details
☐ HC-045: Check in patient
☐ HC-049: Check out patient
☐ HC-052: Update patient
☐ HC-047-048: Invalid tests

LOCATION & PROXIMITY TESTS
☐ HC-055: Find near locations
☐ HC-057: Find nearby hospitals
☐ HC-059-061: Invalid tests

SUMMARY
☐ Total tests run: ___
☐ Total passed: ___
☐ Total failed: ___
☐ All valid tests passed: YES / NO
☐ All invalid tests received correct error codes: YES / NO
```

---

## Advanced Testing Features

### Custom Environment Variables

Add these to your Postman environment:

```json
{
  "base_url": "http://localhost:8080",
  "hospital_id": "1",
  "patient_id": "1",
  "timeout": 5000
}
```

Then use in requests:

```
GET {{base_url}}/v1/hospitais/{{hospital_id}}
```

### Pre-request Scripts

Example: Generate a timestamp for a request:

```javascript
const timestamp = new Date().toISOString();
pm.variables.set("timestamp", timestamp);
```

### Global Variables

Store data from one request for use in another:

```javascript
pm.test("Save hospital ID", function () {
  var jsonData = pm.response.json();
  pm.globals.set("created_hospital_id", jsonData.id);
});
```

Then use: `{{created_hospital_id}}`

---

## Reporting & Documentation

### Test Execution Report Template

After running tests, document results:

```
TEST EXECUTION REPORT
Date: [Date]
Tester: [Name]
Build: [Version]

SUMMARY
Total Test Cases: 65
Total Passed: [#]
Total Failed: [#]
Pass Rate: [%]

RESULTS BY CATEGORY
- Hospital Management: [Pass/Fail]
- Inventory Management: [Pass/Fail]
- Patient Management: [Pass/Fail]
- Location & Proximity: [Pass/Fail]

FAILURES
[List any failed tests and root cause]

NOTES
[Any observations or issues]
```

### Export Test Results

1. Run collection with HTML reporter: `newman run postman_collection.json --reporter-html-export report.html`
2. Share the HTML report with team
3. Save results for regression testing

---

## Next Steps

1. **Execute all 65 test cases** and document results
2. **Verify:** All valid tests return 200, invalid tests return 400/404
3. **Document:** Sample pass/fail scenarios and error messages
4. **Archive:** Keep test results for baseline comparison

---

## Resources

- **Postman Documentation:** https://learning.postman.com/docs/
- **Newman CLI:** https://www.npmjs.com/package/newman
- **REST API Best Practices:** https://restfulapi.net/
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes

---

## Support

For questions or issues:

1. Check the troubleshooting section above
2. Review test_cases.json for expected behavior
3. Check backend logs: `.\mvnw.cmd spring-boot:run`
4. Verify MongoDB is running and has sample data

---

**Last Updated:** February 2026
**Test Suite Version:** 1.0
**Status:** Ready for execution
