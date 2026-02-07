# Hospital Management API - Endpoint Documentation

## Base URL

```
http://localhost:8080/v1
```

## Authentication

Currently **No Authentication Required** (can be added in future)

---

## 📋 Hospital Management Endpoints

### 1. Create Hospital

**Endpoint:** `POST /hospitais/`  
**Priority:** HIGH  
**Description:** Create a new hospital in the system

**Request Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "id": 100,
  "name": "Hospital Name",
  "address": "Full Address",
  "beds": 50,
  "availableBeds": 30,
  "latitude": "-23.593438",
  "longitude": "-46.710462"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes | Unique hospital identifier |
| `name` | String | Yes | Hospital name (non-empty) |
| `address` | String | Yes | Hospital physical address |
| `beds` | Integer | Yes | Total number of beds (>= 1) |
| `availableBeds` | Integer | Yes | Available beds (<= total beds) |
| `latitude` | String/Float | Yes | Latitude coordinate |
| `longitude` | String/Float | Yes | Longitude coordinate |

**Validation Rules:**

- ❌ `name` cannot be empty or null
- ❌ `beds` must be >= 1
- ❌ `availableBeds` cannot be > `beds`
- ❌ `latitude` and `longitude` must be numeric

**Response - Success (201 Created):**

```json
{
  "id": 100,
  "name": "Hospital Name",
  "address": "Full Address",
  "beds": 50,
  "availableBeds": 30,
  "latitude": "-23.593438",
  "longitude": "-46.710462"
}
```

**Response - Error (400 Bad Request):**

```json
{
  "error": "validation_error",
  "message": "Field 'name' is required",
  "status": 400
}
```

**Test Cases:** HC-001 to HC-013

---

### 2. Get All Hospitals

**Endpoint:** `GET /hospitais/`  
**Priority:** HIGH  
**Description:** Retrieve list of all hospitals

**Request Headers:**

```
Accept: application/json
```

**Query Parameters:** None

**Response - Success (200 OK):**

```json
[
  {
    "id": 1,
    "name": "Hospital A",
    "address": "Address 1",
    "beds": 100,
    "availableBeds": 50,
    "latitude": "-23.5",
    "longitude": "-46.6"
  },
  {
    "id": 2,
    "name": "Hospital B",
    "address": "Address 2",
    "beds": 75,
    "availableBeds": 40,
    "latitude": "-23.55",
    "longitude": "-46.65"
  }
]
```

**Test Cases:** HC-014

---

### 3. Get Single Hospital

**Endpoint:** `GET /hospitais/{id}`  
**Priority:** HIGH  
**Description:** Retrieve details of a specific hospital

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | Integer | Yes | Hospital ID |

**Response - Success (200 OK):**

```json
{
  "id": 1,
  "name": "Hospital A",
  "address": "Address 1",
  "beds": 100,
  "availableBeds": 50,
  "latitude": "-23.5",
  "longitude": "-46.6"
}
```

**Response - Error (404 Not Found):**

```json
{
  "error": "not_found",
  "message": "Hospital with id 99999 not found",
  "status": 404
}
```

**Test Cases:** HC-015, HC-016, HC-017

---

### 4. Update Hospital

**Endpoint:** `PUT /hospitais/{id}`  
**Priority:** HIGH  
**Description:** Update hospital information

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | Integer | Yes | Hospital ID |

**Request Body (all fields optional):**

```json
{
  "name": "Updated Hospital Name",
  "address": "Updated Address",
  "beds": 75,
  "availableBeds": 50,
  "latitude": "-23.6",
  "longitude": "-46.7"
}
```

**Validation Rules:**

- ❌ `availableBeds` cannot exceed `beds`
- ❌ `name` cannot be empty if provided

**Response - Success (200 OK):**

```json
{
  "id": 1,
  "name": "Updated Hospital Name",
  "address": "Updated Address",
  "beds": 75,
  "availableBeds": 50,
  "latitude": "-23.6",
  "longitude": "-46.7"
}
```

**Test Cases:** HC-018 to HC-022

---

### 5. Get Hospital Beds

**Endpoint:** `GET /hospitais/{id}/leitos`  
**Priority:** MEDIUM  
**Description:** Retrieve bed information for hospital

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | Integer | Yes | Hospital ID |

**Response - Success (200 OK):**

```json
[
  {
    "id": 1,
    "hospitalId": 1,
    "available": true,
    "type": "STANDARD"
  },
  {
    "id": 2,
    "hospitalId": 1,
    "available": false,
    "type": "ICU"
  }
]
```

**Test Cases:** HC-023, HC-024

---

### 6. Find Nearest Hospital

**Endpoint:** `GET /hospitais/maisProximo`  
**Priority:** HIGH  
**Description:** Find nearest hospital based on coordinates and radius

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lat` | Float | Yes | Latitude coordinate |
| `lon` | Float | Yes | Longitude coordinate |
| `raioMaximo` | Integer | No | Maximum radius in kilometers (default: 10) |

**Example Request:**

```
GET /hospitais/maisProximo?lat=-23.593438&lon=-46.710462&raioMaximo=50
```

**Validation Rules:**

- ❌ `lat` is required and must be numeric
- ❌ `lon` is required and must be numeric
- ❌ `raioMaximo` must be positive if provided

**Response - Success (200 OK):**

```json
{
  "id": 1,
  "name": "Nearest Hospital",
  "address": "Address",
  "distance": 5.5,
  "beds": 100,
  "availableBeds": 50
}
```

**Response - Error (400 Bad Request):**

```json
{
  "error": "invalid_parameter",
  "message": "Missing required parameter: lat",
  "status": 400
}
```

**Test Cases:** HC-025 to HC-030

---

## 📦 Inventory Management Endpoints

### 1. Get Hospital Inventory

**Endpoint:** `GET /hospitais/{hospitalId}/estoque`  
**Priority:** HIGH  
**Description:** Get all products in hospital inventory

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hospitalId` | Integer | Yes | Hospital ID |

**Response - Success (200 OK):**

```json
[
  {
    "id": "5cac077fa9c6543dc892fdf1",
    "name": "Curativos",
    "description": "Medical bandages",
    "quantity": 100,
    "productType": "COMMON"
  },
  {
    "id": "5cac077fa9c6543dc892fdf2",
    "name": "Blood Type O+",
    "description": "O+ blood units",
    "quantity": 50,
    "productType": "BLOOD"
  }
]
```

**Test Cases:** EST-001, EST-002

---

### 2. Add Product to Inventory

**Endpoint:** `POST /hospitais/{hospitalId}/estoque`  
**Priority:** HIGH  
**Description:** Add new product to hospital inventory

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hospitalId` | Integer | Yes | Hospital ID |

**Request Body:**

```json
{
  "name": "Product Name",
  "description": "Product Description",
  "quantity": 100,
  "productType": "COMMON"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Product name (non-empty) |
| `description` | String | No | Product description |
| `quantity` | Integer | Yes | Quantity in stock (>= 0) |
| `productType` | String | Yes | Type: COMMON, BLOOD, MEDICINE, etc. |

**Validation Rules:**

- ❌ `name` cannot be empty or null
- ❌ `quantity` cannot be negative
- ❌ `quantity` must be provided

**Response - Success (201 Created):**

```json
{
  "id": "5cac077fa9c6543dc892fdf3",
  "name": "Product Name",
  "description": "Product Description",
  "quantity": 100,
  "productType": "COMMON"
}
```

**Test Cases:** EST-003 to EST-011

---

### 3. Update Product in Inventory

**Endpoint:** `PUT /hospitais/{hospitalId}/estoque/{productId}`  
**Priority:** HIGH  
**Description:** Update product details or quantity

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hospitalId` | Integer | Yes | Hospital ID |
| `productId` | String | Yes | Product ID (MongoDB ObjectId) |

**Request Body (all fields optional):**

```json
{
  "name": "Updated Product Name",
  "description": "Updated Description",
  "quantity": 150,
  "productType": "COMMON"
}
```

**Validation Rules:**

- ❌ `quantity` cannot be negative if provided

**Response - Success (200 OK):**

```json
{
  "id": "5cac077fa9c6543dc892fdf3",
  "name": "Updated Product Name",
  "description": "Updated Description",
  "quantity": 150,
  "productType": "COMMON"
}
```

**Test Cases:** EST-012 to EST-016

---

### 4. Delete Product from Inventory

**Endpoint:** `DELETE /hospitais/{hospitalId}/estoque/{productId}`  
**Priority:** MEDIUM  
**Description:** Remove product from inventory

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hospitalId` | Integer | Yes | Hospital ID |
| `productId` | String | Yes | Product ID |

**Response - Success (204 No Content):**

```
No response body
```

**Response - Error (404 Not Found):**

```json
{
  "error": "not_found",
  "message": "Product not found",
  "status": 404
}
```

**Test Cases:** EST-017 to EST-019

---

## 👥 Patient Management Endpoints

### 1. Create Patient

**Endpoint:** `POST /pacientes/`  
**Priority:** HIGH  
**Description:** Create new patient record

**Request Body:**

```json
{
  "firstName": "João",
  "lastName": "Silva",
  "email": "joao.silva@email.com",
  "phone": "11987654321",
  "address": "Rua A, 100"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `firstName` | String | Yes | Patient first name (non-empty) |
| `lastName` | String | Yes | Patient last name (non-empty) |
| `email` | String | No | Valid email format if provided |
| `phone` | String | No | Phone number |
| `address` | String | No | Patient address |

**Validation Rules:**

- ❌ `firstName` cannot be empty or null
- ❌ `lastName` cannot be empty or null
- ❌ `email` must be valid format if provided

**Response - Success (201 Created):**

```json
{
  "id": "5cac077fa9c6543dc892fdf1",
  "firstName": "João",
  "lastName": "Silva",
  "email": "joao.silva@email.com",
  "phone": "11987654321",
  "address": "Rua A, 100"
}
```

**Test Cases:** PAC-001 to PAC-010

---

### 2. Get All Patients

**Endpoint:** `GET /pacientes/`  
**Priority:** HIGH  
**Description:** Retrieve list of all patients

**Response - Success (200 OK):**

```json
[
  {
    "id": "5cac077fa9c6543dc892fdf1",
    "firstName": "João",
    "lastName": "Silva",
    "email": "joao.silva@email.com",
    "phone": "11987654321"
  }
]
```

**Test Cases:** PAC-011

---

### 3. Get Single Patient

**Endpoint:** `GET /pacientes/{id}`  
**Priority:** HIGH  
**Description:** Retrieve patient details

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | String | Yes | Patient ID |

**Response - Success (200 OK):**

```json
{
  "id": "5cac077fa9c6543dc892fdf1",
  "firstName": "João",
  "lastName": "Silva",
  "email": "joao.silva@email.com",
  "phone": "11987654321",
  "address": "Rua A, 100"
}
```

**Test Cases:** PAC-012 to PAC-014

---

## Response Status Codes

### Success Codes

| Code  | Meaning    | Used In           |
| ----- | ---------- | ----------------- |
| `200` | OK         | GET, PUT requests |
| `201` | Created    | POST requests     |
| `204` | No Content | DELETE requests   |

### Error Codes

| Code  | Meaning      | Example Cause                         |
| ----- | ------------ | ------------------------------------- |
| `400` | Bad Request  | Invalid data, missing required fields |
| `404` | Not Found    | Resource ID doesn't exist             |
| `500` | Server Error | Unexpected server error               |

---

## Common Error Responses

### Missing Required Field

```json
{
  "status": 400,
  "error": "validation_error",
  "message": "Field 'name' is required"
}
```

### Invalid Data Type

```json
{
  "status": 400,
  "error": "validation_error",
  "message": "Field 'beds' must be numeric"
}
```

### Resource Not Found

```json
{
  "status": 404,
  "error": "not_found",
  "message": "Hospital with id 99999 not found"
}
```

---

## Data Types & Formats

### Integer

- Range: -2,147,483,648 to 2,147,483,647
- Examples: `1`, `50`, `100`
- Validation: Must be whole number

### String

- Text data
- Examples: `"Hospital Central"`, `"João Silva"`
- Validation: Non-empty in required fields

### Float

- Decimal numbers
- Examples: `-23.593438`, `46.710462`
- Format: Standard decimal notation

### Coordinates

- Latitude: -90 to +90
- Longitude: -180 to +180
- Format: Decimal degrees as strings or numbers

### Email

- Format: `user@domain.com`
- Validation: Must contain @ and valid domain

---

## Test Matrix Summary

| Endpoint                 | Method | Valid Tests | Invalid Tests | Total   |
| ------------------------ | ------ | ----------- | ------------- | ------- |
| `/hospitais/`            | POST   | 5           | 8             | 13      |
| `/hospitais/`            | GET    | 1           | 0             | 1       |
| `/hospitais/{id}`        | GET    | 1           | 2             | 3       |
| `/hospitais/{id}`        | PUT    | 2           | 3             | 5       |
| `/hospitais/{id}/leitos` | GET    | 1           | 1             | 2       |
| `/hospitais/maisProximo` | GET    | 2           | 4             | 6       |
| `/estoque`               | GET    | 1           | 1             | 2       |
| `/estoque`               | POST   | 4           | 5             | 9       |
| `/estoque/{productId}`   | PUT    | 2           | 2             | 4       |
| `/estoque/{productId}`   | DELETE | 1           | 2             | 3       |
| `/pacientes/`            | POST   | 4           | 6             | 10      |
| `/pacientes/`            | GET    | 1           | 0             | 1       |
| `/pacientes/{id}`        | GET    | 1           | 2             | 3       |
| **TOTAL**                |        | **26**      | **38**        | **64+** |

---

## Next Steps

1. ✅ **Review Endpoints** - Understand each endpoint thoroughly
2. ⏳ **Execute Tests** - Run test cases from test_cases.json
3. ⏳ **Document Results** - Fill in test_results_template.json
4. ⏳ **Analyze Findings** - Identify any issues
5. ⏳ **Phase 2** - Prepare for AI model development
