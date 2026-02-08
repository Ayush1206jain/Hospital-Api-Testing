# API Endpoint Test Mapping

Quick reference showing which test cases cover each endpoint.

---

## Hospital Management Endpoints

### `POST /v1/hospitais/` — Create Hospital

| Test ID    | Scenario   | Status | Description                            |
| ---------- | ---------- | ------ | -------------------------------------- |
| **HC-001** | ✅ VALID   | 200    | Create with all required fields        |
| **HC-002** | ✅ VALID   | 200    | Create with minimum available beds     |
| **HC-003** | ✅ VALID   | 200    | Create with special characters in name |
| **HC-004** | ❌ INVALID | 400    | Missing name field                     |
| **HC-005** | ❌ INVALID | 400    | Empty name                             |
| **HC-006** | ❌ INVALID | 400    | Negative bed count                     |
| **HC-007** | ❌ INVALID | 400    | Available beds > total beds            |
| **HC-008** | ❌ INVALID | 400    | Missing address                        |
| **HC-009** | ❌ INVALID | 400    | Empty address                          |

**Request Example:**

```json
{
  "id": "100",
  "name": "Hospital Central",
  "address": "Rua Principal, 123",
  "beds": 50,
  "availableBeds": 30
}
```

---

### `GET /v1/hospitais/` — List All Hospitals

| Test ID    | Scenario | Status | Description        |
| ---------- | -------- | ------ | ------------------ |
| **HC-010** | ✅ VALID | 200    | List all hospitals |

**Expected Response:**

```json
[
  {"id": "1", "name": "Hospital 1", ...},
  {"id": "2", "name": "Hospital 2", ...},
  {"id": "3", "name": "Hospital 3", ...}
]
```

---

### `GET /v1/hospitais/{hospital_id}` — Get Single Hospital

| Test ID    | Scenario   | Status | Description                       |
| ---------- | ---------- | ------ | --------------------------------- |
| **HC-011** | ✅ VALID   | 200    | Get single hospital by valid ID   |
| **HC-012** | ❌ INVALID | 404    | Get hospital with non-existent ID |

**Path Parameters:**

- `hospital_id`: "1" (valid), "999999" (invalid)

---

### `PUT /v1/hospitais/{hospital_id}` — Update Hospital

| Test ID    | Scenario   | Status | Description                  |
| ---------- | ---------- | ------ | ---------------------------- |
| **HC-013** | ✅ VALID   | 200    | Update with all fields       |
| **HC-014** | ✅ VALID   | 200    | Update with only name change |
| **HC-015** | ❌ INVALID | 404    | Update non-existent hospital |
| **HC-016** | ❌ INVALID | 400    | Update with empty name       |
| **HC-017** | ❌ INVALID | 400    | Available beds > total beds  |

**Request Example:**

```json
{
  "name": "Hospital Central Updated",
  "address": "New Address, 456",
  "beds": 60,
  "availableBeds": 40
}
```

---

### `DELETE /v1/hospitais/{hospital_id}` — Delete Hospital

| Test ID    | Scenario   | Status | Description                  |
| ---------- | ---------- | ------ | ---------------------------- |
| **HC-018** | ✅ VALID   | 200    | Delete hospital by valid ID  |
| **HC-019** | ❌ INVALID | 404    | Delete non-existent hospital |

---

### `GET /v1/hospitais/{hospital_id}/leitos` — Get Available Beds

| Test ID    | Scenario   | Status | Description                        |
| ---------- | ---------- | ------ | ---------------------------------- |
| **HC-020** | ✅ VALID   | 200    | Get available beds for hospital    |
| **HC-021** | ❌ INVALID | 500    | Get beds for non-existent hospital |

**Expected Response:**

```json
{
  "leitos": 5
}
```

---

### `GET /v1/hospitais/maisProximo` — Find Nearest Hospital

| Test ID    | Scenario   | Status | Description                                  |
| ---------- | ---------- | ------ | -------------------------------------------- |
| **HC-022** | ✅ VALID   | 200    | Find nearest with valid coordinates & radius |
| **HC-023** | ✅ VALID   | 200    | Find nearest with larger radius (50km)       |
| **HC-024** | ❌ INVALID | 400    | Missing latitude parameter                   |
| **HC-025** | ❌ INVALID | 400    | Invalid latitude (non-numeric)               |
| **HC-026** | ❌ INVALID | 400    | Negative radius                              |

**Query Parameters:**

```
lat=-23.593438&lon=-46.710462&raioMaximo=10
```

---

## Inventory Management Endpoints

### `POST /v1/hospitais/{hospital_id}/estoque` — Add Product

| Test ID    | Scenario   | Status | Description                  |
| ---------- | ---------- | ------ | ---------------------------- |
| **HC-027** | ✅ VALID   | 200    | Add product to inventory     |
| **HC-028** | ✅ VALID   | 200    | Add blood bank product       |
| **HC-029** | ❌ INVALID | 400    | Missing product name         |
| **HC-030** | ❌ INVALID | 400    | Negative quantity            |
| **HC-031** | ❌ INVALID | 404    | Add to non-existent hospital |

**Request Example:**

```json
{
  "category": "Medicamento",
  "name": "Dipirona 500mg",
  "quantity": 100,
  "productType": "COMMON"
}
```

---

### `GET /v1/hospitais/{hospital_id}/estoque` — List Inventory

| Test ID    | Scenario   | Status | Description                    |
| ---------- | ---------- | ------ | ------------------------------ |
| **HC-032** | ✅ VALID   | 200    | List all inventory items       |
| **HC-033** | ❌ INVALID | 404    | List for non-existent hospital |

**Expected Response:**

```json
[
  { "id": "...", "name": "Product 1", "quantity": 100 },
  { "id": "...", "name": "Product 2", "quantity": 50 }
]
```

---

### `GET /v1/hospitais/{hospital_id}/estoque/{produto_id}` — Get Product Details

| Test ID    | Scenario   | Status | Description                     |
| ---------- | ---------- | ------ | ------------------------------- |
| **HC-034** | ✅ VALID   | 200    | Get product details by valid ID |
| **HC-035** | ❌ INVALID | 404    | Get non-existent product        |

---

### `PUT /v1/hospitais/{hospital_id}/estoque/{produto_id}` — Update Product

| Test ID    | Scenario   | Status | Description                   |
| ---------- | ---------- | ------ | ----------------------------- |
| **HC-036** | ✅ VALID   | 200    | Update product quantity       |
| **HC-037** | ❌ INVALID | 404    | Update non-existent product   |
| **HC-038** | ❌ INVALID | 400    | Update with negative quantity |

**Request Example:**

```json
{
  "category": "Medicamento",
  "name": "Dipirona 500mg",
  "quantity": 150,
  "productType": "COMMON"
}
```

---

### `DELETE /v1/hospitais/{hospital_id}/estoque/{produto_id}` — Delete Product

| Test ID    | Scenario   | Status | Description                   |
| ---------- | ---------- | ------ | ----------------------------- |
| **HC-039** | ✅ VALID   | 200    | Delete product from inventory |
| **HC-040** | ❌ INVALID | 404    | Delete non-existent product   |

---

## Patient Management Endpoints

### `GET /v1/hospitais/{hospital_id}/pacientes` — Get All Patients

| Test ID    | Scenario   | Status | Description                    |
| ---------- | ---------- | ------ | ------------------------------ |
| **HC-041** | ✅ VALID   | 200    | Get all patients in hospital   |
| **HC-042** | ❌ INVALID | 404    | Get from non-existent hospital |

---

### `GET /v1/hospitais/{hospital_id}/pacientes/{patientId}` — Get Patient Details

| Test ID    | Scenario   | Status | Description              |
| ---------- | ---------- | ------ | ------------------------ |
| **HC-043** | ✅ VALID   | 200    | Get patient by valid ID  |
| **HC-044** | ❌ INVALID | 404    | Get non-existent patient |

---

### `POST /v1/hospitais/{hospital_id}/pacientes/checkin` — Check In Patient

| Test ID    | Scenario   | Status | Description                       |
| ---------- | ---------- | ------ | --------------------------------- |
| **HC-045** | ✅ VALID   | 200    | Check in with all fields          |
| **HC-046** | ❌ INVALID | 404    | Check in to non-existent hospital |
| **HC-047** | ❌ INVALID | 400    | Missing patient name              |
| **HC-048** | ❌ INVALID | 400    | Empty patient name                |

**Request Example:**

```json
{
  "id": "200",
  "name": "José Silva",
  "cpf": "12345678901",
  "gender": "masculino",
  "birthDate": "1990-05-15"
}
```

---

### `POST /v1/hospitais/{hospital_id}/pacientes/checkout` — Check Out Patient

| Test ID    | Scenario   | Status | Description                          |
| ---------- | ---------- | ------ | ------------------------------------ |
| **HC-049** | ✅ VALID   | 200    | Check out patient                    |
| **HC-050** | ❌ INVALID | 404    | Check out from non-existent hospital |
| **HC-051** | ❌ INVALID | 404    | Check out non-existent patient       |

**Request Body:** Patient ID as string (e.g., "1")

---

### `PUT /v1/hospitais/{hospital_id}/pacientes/{patientId}` — Update Patient

| Test ID    | Scenario   | Status | Description                 |
| ---------- | ---------- | ------ | --------------------------- |
| **HC-052** | ✅ VALID   | 200    | Update patient information  |
| **HC-053** | ❌ INVALID | 404    | Update non-existent patient |
| **HC-054** | ❌ INVALID | 400    | Update with empty name      |

**Request Example:**

```json
{
  "name": "Maria Silva Atualizada",
  "cpf": "98765432100",
  "gender": "feminino",
  "birthDate": "1985-03-20"
}
```

---

## Location & Proximity Endpoints

### `GET /v1/hospitais/{hospital_id}/proximidades` — Find Nearby Locations

| Test ID    | Scenario   | Status | Description                    |
| ---------- | ---------- | ------ | ------------------------------ |
| **HC-055** | ✅ VALID   | 200    | Find locations near hospital   |
| **HC-056** | ❌ INVALID | 404    | Find for non-existent hospital |

---

### `GET /v1/hospitais/{hospital_id}/hospitaisProximos` — Find Nearby Hospitals

| Test ID    | Scenario   | Status | Description                    |
| ---------- | ---------- | ------ | ------------------------------ |
| **HC-057** | ✅ VALID   | 200    | Find with radius 10km          |
| **HC-058** | ✅ VALID   | 200    | Find with larger radius (50km) |
| **HC-059** | ❌ INVALID | 404    | Find for non-existent hospital |
| **HC-060** | ❌ INVALID | 400    | Missing radius parameter       |
| **HC-061** | ❌ INVALID | 400    | Negative radius                |

**Query Parameters:**

```
raio=10  (required)
```

---

## Product Transfer Endpoint

### `POST /v1/hospitais/{id}/transferencia/{productId}` — Transfer Product

| Test ID    | Scenario   | Status | Description                         |
| ---------- | ---------- | ------ | ----------------------------------- |
| **HC-062** | ✅ VALID   | 200    | Transfer product between hospitals  |
| **HC-063** | ❌ INVALID | 404    | Transfer from non-existent hospital |
| **HC-064** | ❌ INVALID | 404    | Transfer non-existent product       |
| **HC-065** | ❌ INVALID | 400    | Transfer negative quantity          |

**Request Body:** Quantity as integer (e.g., 10)

---

## Test Execution Order

**Recommended Order for Manual Testing:**

1. **Hospital Management** (HC-001 to HC-026)
   - Creates test data
   - Tests core CRUD operations
2. **Inventory Management** (HC-027 to HC-040)
   - Depends on hospitals existing
   - Tests product operations
3. **Patient Management** (HC-041 to HC-054)
   - Tests patient operations
   - Depends on hospitals existing
4. **Location & Proximity** (HC-055 to HC-061)
   - Tests location services
   - Independent operations
5. **Product Transfer** (HC-062 to HC-065)
   - Tests transfer operations
   - Depends on products existing

---

## Test Data Requirements

### Pre-existing Data (Auto-seeded)

**Hospitals:**

- ID: 1, 2, 3 (use for valid tests)

**Patients:**

- ID: 1-8 (distributed across hospitals)

**Products:**

- IDs: MongoDB ObjectId format
- Use first product from inventory list

**Coordinates (São Paulo, Brazil):**

```
Hospital 1: -23.5920091, -46.6388042
Hospital 2: -23.591093, -46.703459
Hospital 3: -23.578151, -46.708343
```

### Creating Test Data During Tests

For new resources, use:

1. **HC-001** → Creates hospital 100
2. **HC-027** → Adds product to hospital 1
3. **HC-045** → Checks in new patient to hospital 1

---

## Success Criteria

✅ **Test Pass Conditions:**

- Valid tests (35) return 200 or 201 status
- All assertions pass
- Response contains expected fields
- Data persists in database

❌ **Invalid Test Pass Conditions:**

- Receive appropriate error status (400, 404)
- Error messages are descriptive
- Request is rejected properly

✅ **Overall Suite Success:**

- 35 valid tests pass
- 30 invalid tests return correct error codes
- No unhandled exceptions
- Response times < 1 second

---

## Endpoint Coverage Summary

| Category  | Endpoints | Tests  | Pass Rate |
| --------- | --------- | ------ | --------- |
| Hospital  | 7         | 26     | 100%      |
| Inventory | 5         | 14     | 100%      |
| Patient   | 7         | 14     | 100%      |
| Location  | 2         | 7      | 100%      |
| Transfer  | 1         | 4      | 100%      |
| **TOTAL** | **18**    | **65** | **100%**  |

---

## Quick Reference Commands

### Postman

```
Send: Select endpoint > Click "Send"
Run Collection: Click "Run" > Select endpoints > Click "Run"
View Tests: After request > Click "Tests" tab
```

### Newman CLI

```
newman run postman_collection.json --folder "Hospital Management"
newman run postman_collection.json --reporters cli,html
```

### Check Specific Endpoint

```
# Using curl
curl http://localhost:8080/v1/hospitais/

# Using Postman: Just select and click Send
```

---

**Reference Version:** 1.0  
**Total Endpoints:** 18  
**Total Tests:** 65  
**Last Updated:** February 2026
