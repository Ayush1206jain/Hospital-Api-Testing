# Manual Testing Folder - Hospital Management API

## 📖 Overview

This folder contains **complete manual testing resources** for the Hospital Management System API. It includes 98 comprehensive test cases, Postman collection, execution guides, and result templates.

**Status:** ✅ Phase 1 Complete  
**Test Cases:** 98 (56 valid + 42 invalid)  
**Endpoints Covered:** 13/13 (100%)  
**Documentation:** Complete

---

## 📂 Folder Structure & File Guide

```
manual_testing/
├── API_Endpoints_Coverage.html        # Visual endpoint documentation (NEW)
├── test_cases.json                    # All 98 test cases (main resource)
├── GestaoHospitalar.postman_collection.json  # Postman import file
├── test_results_template.json         # Template for documenting results
├── TEST_EXECUTION_GUIDE.md            # Step-by-step test execution guide
├── ENDPOINT_DOCUMENTATION.md          # Detailed API endpoint reference
├── PHASE_1_SUMMARY.md                 # Complete Phase 1 summary
└── README.md                          # This file
```

**📌 Key Files for Postman:**

- **Import This File:** `GestaoHospitalar.postman_collection.json`
- **Location:** `GestaoHospital/src/main/resources/GestaoHospitalar.postman_collection.json`
- **Size:** ~50KB
- **Contains:** 18 test requests + 4 test folders + assertions
- **Format:** Postman Collection v2.1

---

## 🚀 Quick Start (5 Minutes)

### 1. Import to Postman

**Option A: Desktop Postman (Recommended)**

```bash
Step 1: Open Postman desktop application
Step 2: Click File menu → Import
Step 3: Click "Upload Files" button
Step 4: Navigate to: GestaoHospital/src/main/resources/GestaoHospitalar.postman_collection.json
Step 5: Select the file and click "Open"
Step 6: Click "Import" button
Step 7: Success! Collection appears in sidebar
```

**Option B: Postman Web**

```bash
Step 1: Go to https://web.postman.co/
Step 2: Click "Import" button
Step 3: Choose "Upload Files" and select GestaoHospitalar.postman_collection.json
Step 4: Click Import
```

### 2. Configure Environment Variables

```bash
In Postman - Create New Environment:
1. Click "Environments" (left sidebar)
2. Click "+" button to create new
3. Name: "Hospital-API-Testing"
4. Add these variables:
   - baseURL = http://localhost:8080
   - hospitalId = (leave empty)
   - productId = (leave empty)
   - patientId = (leave empty)
5. Click "Save"

Select Environment for Testing:
1. Click dropdown (top right corner)
2. Select: "Hospital-API-Testing"
```

### 3. Run Your First Test

```bash
Step 1: Click collection: "Hospital Management API - Complete Test Suite"
Step 2: Click folder: "01 - HOSPITAL MANAGEMENT"
Step 3: Click request: "HC-001: Create Hospital - Valid"
Step 4: Verify environment selected (top right)
Step 5: Click "Send" button
Step 6: Check Response tab:
       - Status: 201 Created
       - Body contains hospital data with id
       - hospitalId auto-saved for next tests

Success! You're ready to test all endpoints! ✅
```

---

## � Postman Import Quick Reference

### File Details

- **Filename:** `GestaoHospitalar.postman_collection.json`
- **Location:** `GestaoHospital/src/main/resources/`
- **Size:** ~50KB
- **Format:** Postman Collection v2.1
- **Requests:** 18 HTTP requests
- **Folders:** 3 organized categories
- **Tests:** Automated assertions included

### 3-Step Import Process

1. **Open Postman → File → Import**
2. **Select:** `GestaoHospitalar.postman_collection.json`
3. **Click Import** ✅ Done!

### What You Get After Import

✅ **01 - HOSPITAL MANAGEMENT** folder with 8 tests  
✅ **02 - INVENTORY MANAGEMENT** folder with 5 tests  
✅ **03 - PATIENT MANAGEMENT** folder with 5 tests  
✅ **4 Environment Variables** (baseURL, hospitalId, productId, patientId)  
✅ **Test Assertions** on every request (automatic validation)  
✅ **Response Examples** for reference  
✅ **Ready-to-Send Requests** (just click Send!)

### After Import - Next Actions

1. Create/Select "Hospital-API-Testing" environment
2. Set baseURL = `http://localhost:8080`
3. Start running tests (click any request → Send)

---

### 1. `test_cases.json`

**Purpose:** Complete test case repository  
**Contains:** 98 test cases in JSON format  
**Use:** Reference for all test scenarios

**Structure:**

```json
{
  "testCases": [
    {
      "testId": "HC-001",
      "endpoint": "/v1/hospitais/",
      "method": "POST",
      "category": "VALID",
      "priority": "HIGH",
      "description": "...",
      "expectedStatusCode": 201,
      "requestBody": {...},
      "assertions": {...}
    }
  ]
}
```

**How to use:**

- Search for specific test by testId (e.g., "HC-001")
- Filter by category (VALID/INVALID)
- Filter by priority (HIGH/MEDIUM/LOW)
- Review assertions for expected behavior

---

### 2. `GestaoHospitalar.postman_collection.json`

**File Location:** `src/main/resources/GestaoHospitalar.postman_collection.json`

**Purpose:** Complete ready-to-import Postman test collection  
**Contains:** 20+ pre-built HTTP requests with full assertions  
**Use:** Run all tests directly in Postman with automatic validation

**Key Features:**

- ✅ Pre-configured HTTP headers (Content-Type: application/json)
- ✅ Complete request body samples with realistic data
- ✅ Environment variables for reusable test data
- ✅ Automated test assertions for every request
- ✅ Valid case scenarios (happy path testing)
- ✅ Invalid case scenarios (error handling testing)
- ✅ Auto-capture variables from responses
- ✅ Response status code verification
- ✅ Data field validation

**Complete Collection Structure:**

```
Hospital Management API - Complete Test Suite
│
├─ 01 - HOSPITAL MANAGEMENT (8 tests)
│  ├─ HC-001: Create Hospital - Valid (201)
│  ├─ HC-006: Create Hospital - Missing Name (400)
│  ├─ HC-014: Get All Hospitals (200)
│  ├─ HC-015: Get Hospital by ID - Valid (200)
│  ├─ HC-016: Get Hospital - Invalid ID (404)
│  ├─ HC-018: Update Hospital (200)
│  ├─ HC-023: Get Hospital Beds Info (200/404)
│  └─ HC-025: Find Nearest Hospital (200)
│
├─ 02 - INVENTORY MANAGEMENT (5 tests)
│  ├─ EST-001: Get Inventory (200)
│  ├─ EST-003: Add Product - Valid (201)
│  ├─ EST-007: Add Product - Negative Qty (400)
│  ├─ EST-012: Update Product (200)
│  └─ EST-016: Delete Product (200/204)
│
└─ 03 - PATIENT MANAGEMENT (5 tests)
   ├─ PAC-001: Create Patient - Valid (201)
   ├─ PAC-005: Create Patient - No Name (400)
   ├─ PAC-011: Get All Patients (200)
   ├─ PAC-012: Get Patient - Valid (200)
   └─ PAC-013: Get Patient - Invalid ID (404)
```

**Running Tests in Postman:**

```bash
SINGLE TEST:
1. Click the request in collection
2. Review request details
3. Click "Send"
4. Check Response tab (status & body)
5. Check Tests tab for assertions

ENTIRE FOLDER:
1. Right-click folder (e.g. "01 - HOSPITAL MANAGEMENT")
2. Click "Run Folder"
3. Select environment: "Hospital-API-Testing"
4. Click "Run" to execute all tests in folder

ENTIRE COLLECTION:
1. Click collection settings icon
2. Click "Run" button
3. Select environment: "Hospital-API-Testing"
4. Set iterations: 1
5. Click "Run Hospital Management API"
6. All 18+ tests run automatically
```

---

### 3. `TEST_EXECUTION_GUIDE.md`

**Purpose:** Complete guide for running tests  
**Contains:** Setup, execution, and troubleshooting steps  
**Use:** Follow this to execute all tests

**Covers:**

- ✅ Prerequisites & setup
- ✅ Postman configuration
- ✅ Manual test execution
- ✅ Automated execution with Newman
- ✅ Test documentation
- ✅ Common issues & solutions
- ✅ Expected response codes

**Recommended Reading Order:**

1. Prerequisites section
2. Postman Setup section
3. Running Tests section
4. Report Generation section

---

### 4. `test_results_template.json`

**Purpose:** Template for documenting test results  
**Contains:** Result structure with all fields  
**Use:** Fill this after executing tests

**Includes:**

- Test execution summary
- Pass/fail statistics
- Detailed results per test
- Issue tracking
- Performance metrics
- API coverage analysis
- Sign-off section

**How to use:**

```bash
1. Copy test_results_template.json
2. Rename to: test_results_[DATE].json
3. Fill in execution details
4. Run each test
5. Record actual vs expected
6. Mark as PASS/FAIL/SKIP
7. Document any issues
8. Generate final report
```

---

### 5. `ENDPOINT_DOCUMENTATION.md`

**Purpose:** Detailed API endpoint reference  
**Contains:** Complete endpoint documentation  
**Use:** Understand API requirements

**Covers:**

- ✅ All 13 endpoints
- ✅ Request/response examples
- ✅ Parameter validation rules
- ✅ Error responses
- ✅ Status codes
- ✅ Data type specifications
- ✅ Test matrix

**For each endpoint:**

- Description & priority
- Request structure
- Response structure
- Validation rules
- Common errors
- Related test cases

---

### 6. `PHASE_1_SUMMARY.md`

**Purpose:** Final Phase 1 completion report  
**Contains:** Project statistics, metrics, and summary  
**Use:** Understand project completion status

**Includes:**

- Executive summary
- Test case breakdown
- Coverage analysis
- Quality checklist
- Technology stack
- Next steps for Phase 2

---

## ⚙️ Setup Before Testing

### Prerequisites

1. **API Server Running**

   ```bash
   cd GestaoHospital/
   .\mvnw.cmd spring-boot:run
   # Wait for: "Started GestaohospitalarApplication"
   ```

2. **MongoDB Running**

   ```bash
   # Ensure mongod is running on localhost:27017
   mongod  # If not already running
   ```

3. **Postman Installed**
   - Download from https://www.postman.com/downloads/
   - Or use web version

---

## 🧪 Test Execution Workflow

### Manual Testing (Recommended for First Run)

```
1. START
   ↓
2. Review TEST_EXECUTION_GUIDE.md
   ↓
3. Import postman_collection.json into Postman
   ↓
4. Select hospital management folder
   ↓
5. Run test HC-001 (Create hospital - valid)
   ↓
6. Verify Response:
   - Status Code: 201
   - Has id field
   - Name matches request
   ↓
7. Mark result: PASS ✅
   ↓
8. Continue with HC-002, HC-003, etc.
   ↓
9. Record results in test_results_template.json
   ↓
10. Fix any failures
   ↓
11. Generate final report
   ↓
12. END
```

### Automated Testing (Newman)

```bash
# Install Newman
npm install -g newman

# Run all tests
newman run postman_collection.json \
  -e hospital-environment.json \
  -r html --reporter-html-export results.html

# View results
open results.html
```

---

## 📊 Test Statistics

### By Category

| Category    | Valid  | Invalid | Total  |
| ----------- | ------ | ------- | ------ |
| Hospitals   | 13     | 17      | 30     |
| Inventory   | 10     | 10      | 20     |
| Patients    | 7      | 7       | 14     |
| Integration | 26     | 8       | 34     |
| **Total**   | **56** | **42**  | **98** |

### By Priority

| Priority | Count | Tests                    |
| -------- | ----- | ------------------------ |
| HIGH     | 38    | Must pass for deployment |
| MEDIUM   | 42    | Should pass              |
| LOW      | 18    | Nice to have             |

---

## ✅ Expected Test Results

### Valid Test Cases should return:

- ✅ Status: 200 or 201
- ✅ Response body with created/updated resource
- ✅ All expected fields present
- ✅ No error messages

### Invalid Test Cases should return:

- ✅ Status: 400, 404, or other error code
- ✅ Error message explaining issue
- ✅ No resource created/modified
- ✅ Clear error details

---

## 🔧 Troubleshooting

### API Not Responding

```
Error: "Connection refused"
Solution:
  1. Check API is running: curl http://localhost:8080/swagger-ui.html
  2. Start API: .\mvnw.cmd spring-boot:run
  3. Wait 30 seconds for startup
  4. Retry request
```

### MongoDB Connection Error

```
Error: "MongoDB connection refused"
Solution:
  1. Check MongoDB running: mongod --version
  2. Start MongoDB: mongod
  3. Verify connection: mongo
  4. Restart API server
```

### Postman Variables Not Working

```
Error: "{{baseURL}} not replaced"
Solution:
  1. Click Environments dropdown
  2. Select "Hospital-API-Testing"
  3. Verify baseURL variable exists
  4. Check variable value is set
  5. Retry request
```

### Postman Collection Import Issues

```
ERROR: "Cannot import collection"
SOLUTION:
  1. Ensure file: GestaoHospitalar.postman_collection.json exists
  2. Location: GestaoHospital/src/main/resources/
  3. File must be valid JSON (no syntax errors)
  4. Try importing from file system (not copy-paste)
  5. Check file permissions (readable)

ERROR: "Import successful but tests not visible"
SOLUTION:
  1. Click Collections tab on left sidebar
  2. Scroll down to find "Hospital Management API"
  3. Click to expand collection
  4. You should see 3 folders (Hospital, Inventory, Patient)
  5. Refresh browser if web Postman (F5)

ERROR: "Environment variables not auto-filling"
SOLUTION:
  1. Ensure "Hospital-API-Testing" environment selected
  2. Check dropdown at top right shows your environment
  3. Variables must be defined before running tests
  4. Some tests auto-populate variables from responses
  5. Check Tests tab to see variable assignments
```

---

## 📈 Running the Full Test Suite

### Time Estimates

- Quick test (30 min): 20 tests
- Standard test (1-2 hr): 50 tests
- Full test (2-3 hr): 98 tests

### Recommended Approach

```
Day 1: Valid test cases only (56 tests - 1.5 hours)
Day 2: Invalid test cases only (42 tests - 1 hour)
Day 3: Full test including edge cases (all 98 - 2 hours)
```

---

## 📝 Documenting Results

### For Each Test:

1. **Open test in Postman**
2. **Click Send**
3. **Review response**
4. **Record in test_results_template.json:**
   - testId
   - actualStatusCode
   - status (PASS/FAIL/SKIP)
   - responseTime
   - any errors

### Example Entry:

```json
{
  "testId": "HC-001",
  "status": "PASS",
  "expectedStatusCode": 201,
  "actualStatusCode": 201,
  "responseTime": "145ms",
  "notes": "Hospital created successfully"
}
```

---

## 🎯 Success Criteria

**Phase 1 Success = All items completed:**

- [x] 98 test cases created
- [x] Postman collection ready
- [x] Execution guide provided
- [x] Results template prepared
- [x] Documentation complete

**Testing Success = Metrics:**

- **Target:** 90%+ of tests pass
- **Valid case success:** 95%+
- **Invalid case success:** 85%+
- \*\*No timeout errors
- **Response times < 500ms**

---

## 🔗 Related Resources

### In This Folder

**Main Testing Files:**

- `GestaoHospitalar.postman_collection.json` - **⭐ Main Import File** (Ready to import into Postman)
- `test_cases.json` - All 98 test scenarios with details
- `API_Endpoints_Coverage.html` - Visual endpoint & test case documentation
- `TEST_EXECUTION_GUIDE.md` - Step-by-step execution instructions
- `ENDPOINT_DOCUMENTATION.md` - Detailed API reference
- `test_results_template.json` - Template for documenting results
- `PHASE_1_SUMMARY.md` - Project completion summary

### Project Level

- `IMPLEMENTATION_PLAN.md` - Overall project plan
- `GestaoHospital/README.md` - API setup instructions
- `GestaoHospital/PROJECT_OVERVIEW.md` - Project details
- `pom.xml` - Maven build configuration

### External

- **Postman Learning:** https://learning.postman.com
- **REST API Testing:** API testing best practices
- **JSON Documentation:** https://www.json.org
- **API Documentation:** http://localhost:8080/swagger-ui.html
- **API Documentation:** http://localhost:8080/swagger-ui.html

---

## 💡 Tips & Best Practices

### ✅ DO:

- Test valid cases first
- Document all results
- Test after API changes
- Use environment variables
- Keep test data clean
- Review error messages

### ❌ DON'T:

- Skip invalid tests
- Modify production data
- Run tests without API
- Ignore error messages
- Leave test data in DB
- Test without MongoDB

---

## 🚀 Next Steps

After completing Phase 1 testing:

1. **Analyze Results**
   - Calculate pass rate
   - Identify failing tests
   - Document issues

2. **Fix Issues**
   - Review error causes
   - Update test cases if needed
   - Retest failed cases

3. **Phase 2 Preparation**
   - Review IMPLEMENTATION_PLAN.md
   - Extract OpenAPI specification
   - Setup Python environment
   - Start AI model development

---

## 📞 Questions & Support

**For test execution issues:**

- Check TEST_EXECUTION_GUIDE.md troubleshooting section
- Verify API is running
- Review Postman configuration

**For test case details:**

- Reference test_cases.json
- Check ENDPOINT_DOCUMENTATION.md
- Review assertions in specific test

**For project questions:**

- See PHASE_1_SUMMARY.md
- Review IMPLEMENTATION_PLAN.md
- Check project README

---

## 📋 Checklist Before Starting

Before you begin testing, ensure:

- [ ] API server is running on http://localhost:8080
- [ ] MongoDB server is running
- [ ] Postman is installed (desktop or web version)
- [ ] **GestaoHospitalar.postman_collection.json is imported** ⭐
- [ ] "Hospital-API-Testing" environment is created
- [ ] baseURL variable = http://localhost:8080
- [ ] test_results_template.json is copied and ready
- [ ] You have read the "Quick Start" section
- [ ] You understand the 3 test categories
- [ ] You've reviewed TEST_EXECUTION_GUIDE.md (optional)

---

## 🎓 Quick Learning Path

1. **2 min:** Read "Quick Start" section above
2. **3 min:** Import postman_collection.json
3. **2 min:** Create "Hospital-API-Testing" environment
4. **5 min:** Run first test (HC-001)
5. **10 min:** Run complete folder (01 - HOSPITAL MANAGEMENT)
6. **Ready:** Run all 18+ tests!

**Total setup time: ~15-20 minutes**

---

**Ready to start? Follow the Quick Start section at the top of this file!** 🚀

---

_Last Updated: February 7, 2026_  
_Enhanced: Postman Import Instructions_  
_Phase: 1 (Manual Testing) - COMPLETE_  
_Next Phase: 2 (AI Model Development)_
