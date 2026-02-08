# API Data Types Reference Guide

Complete guide to all field types, constraints, and valid values for the Hospital Management API.

---

## 1. Hospital Resource

### Hospital Object

**Source File:** `src/main/java/br/com/codenation/hospital/domain/Hospital.java`

| Field           | Type    | Required | Constraints               | Example                                 |
| --------------- | ------- | -------- | ------------------------- | --------------------------------------- |
| `id`            | String  | ✅ Yes   | Unique identifier         | "1", "100", "hospital-001"              |
| `name`          | String  | ✅ Yes   | Not empty, not null       | "Hospital Central", "Hospital São Luiz" |
| `address`       | String  | ✅ Yes   | Not empty, not null       | "Rua Principal, 123"                    |
| `beds`          | Integer | ✅ Yes   | Must be ≥ 0               | 10, 50, 100                             |
| `availableBeds` | Integer | ✅ Yes   | 0 ≤ availableBeds ≤ beds  | 5, 30                                   |
| `location`      | Object  | ❌ No    | See Location object below | {...}                                   |
| `patients`      | Array   | ❌ No    | Array of Patient objects  | [{...}, {...}]                          |
| `products`      | Array   | ❌ No    | Array of Product objects  | [{...}, {...}]                          |

**Validation Rules:**

```
✓ id: Must be unique, string
✓ name: Cannot be empty or null
✓ address: Cannot be empty or null
✓ beds: Integer ≥ 0 (throws "Não possui leitos disponiveis" if < 0)
✓ availableBeds: Integer ≥ 0 AND ≤ beds
  - If availableBeds > beds: INVALID (400 Bad Request)
  - If availableBeds < 0: INVALID (RuntimeException)
```

**Request Example:**

```json
{
  "id": "100",
  "name": "Hospital Central",
  "address": "Rua Principal, 123",
  "beds": 50,
  "availableBeds": 30,
  "location": {
    "referenceId": "Rua Principal, 123",
    "locationCategory": "HOSPITAL",
    "name": "Hospital Central",
    "latitude": -23.593438,
    "longitude": -46.710462
  }
}
```

**Response Example:**

```json
{
  "id": "100",
  "name": "Hospital Central",
  "address": "Rua Principal, 123",
  "beds": 50,
  "availableBeds": 30,
  "location": {...},
  "patients": [],
  "products": []
}
```

---

## 2. Location Resource

### Location Object

**Source File:** `src/main/java/br/com/codenation/hospital/domain/Location.java`

| Field              | Type              | Required | Constraints            | Example                     |
| ------------------ | ----------------- | -------- | ---------------------- | --------------------------- |
| `id`               | String (ObjectId) | ✅ Yes\* | MongoDB ObjectId       | "507f1f77bcf86cd799439011"  |
| `referenceId`      | String            | ✅ Yes   | Full address reference | "Rua Principal, 123"        |
| `locationCategory` | Enum              | ✅ Yes   | HOSPITAL \| PATIENT    | "HOSPITAL"                  |
| `name`             | String            | ✅ Yes   | Location name          | "Hospital Central", "Maria" |
| `latitude`         | Double            | ✅ Yes   | Valid GPS latitude     | -23.593438                  |
| `longitude`        | Double            | ✅ Yes   | Valid GPS longitude    | -46.710462                  |

**LocationCategory Enum Values:**

```java
public enum LocationCategory {
    HOSPITAL,  // For hospital locations
    PATIENT    // For patient home locations
}
```

**Validation Rules:**

```
✓ referenceId: Non-empty string (full address)
✓ locationCategory: Must be "HOSPITAL" or "PATIENT" (case-sensitive if enum)
✓ name: Non-empty string
✓ latitude: Double between -90 and 90
✓ longitude: Double between -180 and 180
```

**Request Example (Hospital Location):**

```json
{
  "referenceId": "Rua Principal, 123 - São Paulo",
  "locationCategory": "HOSPITAL",
  "name": "Hospital Central",
  "latitude": -23.593438,
  "longitude": -46.710462
}
```

**Request Example (Patient Location):**

```json
{
  "referenceId": "Avenida Paulista, 1000 - São Paulo",
  "locationCategory": "PATIENT",
  "name": "João Silva",
  "latitude": -23.596438,
  "longitude": -46.656462
}
```

---

## 3. Patient Resource

### Patient Object

**Source File:** `src/main/java/br/com/codenation/hospital/domain/Patient.java`

| Field       | Type    | Required | Constraints                          | Example                        |
| ----------- | ------- | -------- | ------------------------------------ | ------------------------------ |
| `id`        | String  | ✅ Yes   | Unique identifier                    | "1", "200", "patient-100"      |
| `name`      | String  | ✅ Yes   | Not empty, not null                  | "Maria Silva", "José da Silva" |
| `cpf`       | String  | ✅ Yes   | 11 digits (optional validation)      | "12345678901"                  |
| `birthDate` | Date    | ✅ Yes   | Date in format "dd/MM/yyyy"          | "16/07/1990"                   |
| `gender`    | String  | ✅ Yes   | "masculino" \| "feminino"            | "feminino", "masculino"        |
| `entryDate` | Date    | ✅ Yes   | Check-in timestamp                   | "16/07/2019"                   |
| `exitDate`  | Date    | ❌ No    | Check-out timestamp (auto-populated) | "18/07/2019"                   |
| `active`    | Boolean | ❌ No    | Auto-managed (false on creation)     | true, false                    |
| `location`  | Object  | ❌ No    | Patient's location/address           | {...}                          |

**Validation Rules:**

```
✓ id: Unique string identifier
✓ name: Cannot be empty or null
✓ cpf: String format "XXXXXXXXXXX" (11 digits, no validation of real CPF)
✓ birthDate: Date object (auto-converted from "dd/MM/yyyy" string)
✓ gender: Must be "masculino" or "feminino" (case-sensitive)
✓ entryDate: Date object (set on checkin)
✓ exitDate: Null until checkout, then populated with exit timestamp
✓ active: False on creation, managed by system
```

**Request Example (Checkin):**

```json
{
  "id": "200",
  "name": "José Silva",
  "cpf": "12345678901",
  "gender": "masculino",
  "birthDate": "1990-05-15"
}
```

**Note:** `entryDate`, `exitDate`, and `active` are managed by API on checkin/checkout

**Request Example (Update):**

```json
{
  "name": "Maria Silva Atualizada",
  "cpf": "98765432100",
  "gender": "feminino",
  "birthDate": "1985-03-20"
}
```

---

## 4. Product / Inventory Resource

### Product Object

**Source File:** `src/main/java/br/com/codenation/hospital/domain/Product.java`

| Field                      | Type              | Required | Constraints                 | Example                                      |
| -------------------------- | ----------------- | -------- | --------------------------- | -------------------------------------------- |
| `id`                       | String (ObjectId) | ✅ Yes\* | MongoDB ObjectId hex string | "507f1f77bcf86cd799439011"                   |
| `name`                     | String            | ✅ Yes   | Product name                | "Dipirona 500mg", "Sangue O+"                |
| `description` / `category` | String            | ✅ Yes   | Product category            | "Medicamento", "Banco de Sangue", "Alimento" |
| `quantity`                 | Integer           | ✅ Yes   | Must be ≥ 0                 | 100, 50, 10                                  |
| `productType`              | Enum              | ✅ Yes   | COMMON \| BLOOD             | "COMMON", "BLOOD"                            |

**ProductType Enum Values:**

```java
public enum ProductType {
    COMMON,  // Regular products (food, medicine, supplies)
    BLOOD    // Blood bank products
}
```

**Validation Rules:**

```
✓ id: Generated as MongoDB ObjectId (auto on creation) - read-only
✓ name: Non-empty string
✓ description: Non-empty string (product category)
✓ quantity: Integer ≥ 0
  - If quantity < 0: INVALID (400 Bad Request)
✓ productType: Must be "COMMON" or "BLOOD" (enum)
```

**Request Example (Add Product):**

```json
{
  "category": "Medicamento",
  "name": "Dipirona 500mg",
  "quantity": 100,
  "productType": "COMMON"
}
```

**Request Example (Blood Product):**

```json
{
  "category": "Banco de Sangue",
  "name": "Sangue O+",
  "quantity": 10,
  "productType": "BLOOD"
}
```

**Request Example (Update Product):**

```json
{
  "category": "Medicamento",
  "name": "Dipirona 500mg",
  "quantity": 150,
  "productType": "COMMON"
}
```

**Note:** The `id` field is auto-generated and read-only. When updating, include all fields.

---

## 5. Data Type Summary by Java Type

### String Fields

```
Hospital: id, name, address
Patient: id, name, cpf, gender
Product: id, name, description
Location: id, referenceId, name, locationCategory (enum → string)
```

**Constraints:**

- Cannot be null
- Cannot be empty (for required fields)
- Should not contain only whitespace

### Integer Fields

```
Hospital: beds, availableBeds
Product: quantity
```

**Constraints:**

- Must be whole numbers (no decimals)
- Must be ≥ 0
- Cannot exceed Integer.MAX_VALUE (2,147,483,647)

### Double Fields

```
Location: latitude (-90 to 90), longitude (-180 to 180)
```

**Constraints:**

- Must be valid decimal numbers
- Latitude: -90.0 to 90.0
- Longitude: -180.0 to 180.0
- GPS coordinates format

### Date Fields

```
Patient: birthDate, entryDate, exitDate
```

**Format:**

- Accepted: `"dd/MM/yyyy"` (e.g., "16/07/1990")
- Internal: `java.util.Date`
- JSON Response: ISO format (auto-converted)

**Example Date Conversion:**

```
Request:  "16/07/1990"  (dd/MM/yyyy)
Response: "1990-07-16T00:00:00.000Z"  (ISO 8601)
```

### Enum Fields

```
Location: locationCategory (HOSPITAL | PATIENT)
Product: productType (COMMON | BLOOD)
```

**Constraints:**

- Must be exact case-sensitive value
- Valid values only
- Cannot be null (required)

### Object/Array Fields

```
Hospital: location (Location object), patients (Patient[]), products (Product[])
Patient: location (Location object)
```

**Constraints:**

- Objects must follow their own schema
- Arrays can be empty
- Elements must be valid objects

---

## 6. Field Validation Rules by Endpoint

### POST /v1/hospitais/ (Create Hospital)

**Required Fields:**

```json
{
  "id": "string (unique)",
  "name": "string (non-empty)",
  "address": "string (non-empty)",
  "beds": "integer (≥ 0)",
  "availableBeds": "integer (≤ beds)"
}
```

**Optional Fields:**

```json
{
  "location": "Location object"
}
```

**Field Validation:**

- ❌ Missing `id` → 400 Bad Request
- ❌ Empty `name` → 400 Bad Request
- ❌ Empty `address` → 400 Bad Request
- ❌ Negative `beds` → 400 Bad Request
- ❌ `availableBeds` > `beds` → 400 Bad Request

### POST /v1/hospitais/{hospital_id}/estoque (Add Product)

**Required Fields:**

```json
{
  "category": "string (e.g., 'Medicamento')",
  "name": "string (non-empty)",
  "quantity": "integer (≥ 0)",
  "productType": "enum (COMMON | BLOOD)"
}
```

**Field Validation:**

- ❌ Missing `name` → 400 Bad Request
- ❌ Negative `quantity` → 400 Bad Request
- ❌ Invalid `productType` → 400 Bad Request

### POST /v1/hospitais/{hospital_id}/pacientes/checkin (Check In Patient)

**Required Fields:**

```json
{
  "id": "string",
  "name": "string (non-empty)",
  "cpf": "string (11 digits)",
  "gender": "string (masculino | feminino)",
  "birthDate": "string (dd/MM/yyyy)"
}
```

**Field Validation:**

- ❌ Missing `name` → 400 Bad Request
- ❌ Empty `name` → 400 Bad Request
- ❌ Invalid `gender` → May cause error
- ❌ Non-existent hospital_id → 404 Not Found

### PUT /v1/hospitais/{hospital_id}/pacientes/{patientId} (Update Patient)

**Required Fields:**

```json
{
  "name": "string (non-empty)",
  "cpf": "string",
  "gender": "string (masculino | feminino)",
  "birthDate": "string (dd/MM/yyyy)"
}
```

**Field Validation:**

- ❌ Empty `name` → 400 Bad Request
- ❌ Non-existent patient_id → 404 Not Found

---

## 7. Where to Find This Information

### 1. **Swagger UI (Live API Documentation)**

- **URL:** `http://localhost:8080/swagger-ui.html`
- **After:** Backend is running
- **Shows:** All endpoints, request/response schemas, data types
- **Best for:** Interactive testing and real-time documentation

### 2. **Domain Classes** (Source of Truth)

```
src/main/java/br/com/codenation/hospital/domain/
- Hospital.java
- Patient.java
- Product.java
- Location.java
- ProductType.java (enum)
- LocationCategory.java (enum)
```

- **Best for:** Understanding implementation, field types, constraints

### 3. **DTO Classes** (API Contract)

```
src/main/java/br/com/codenation/hospital/dto/
- HospitalDTO.java
- PatientDTO.java (if exists)
- ProductDTO.java
- LocationDTO.java
```

- **Best for:** Request/response mapping, serialization

### 4. **Test Cases Documentation**

```
manual_testing/
- test_cases.json (65 test cases with request examples)
- ENDPOINT_TEST_MAPPING.md (field mapping by endpoint)
- postman_collection.json (executable examples)
```

- **Best for:** Practical examples, expected values

### 5. **API Resources (Controllers)**

```
src/main/java/br/com/codenation/hospital/resource/
- HospitalResource.java
- ProductResource.java
- PatientResource.java
- LocationResource.java
```

- **Best for:** HTTP method mappings, request validation logic

---

## 8. Quick Reference: Invalid vs Valid Values

### Hospital Creation

**❌ INVALID Examples:**

```json
{
  "id": "100",
  "name": "", // ❌ Empty name
  "address": "Rua X",
  "beds": -10, // ❌ Negative beds
  "availableBeds": 5
}
```

```json
{
  "id": "100",
  "name": "Hospital",
  "address": "Rua X",
  "beds": 20,
  "availableBeds": 50 // ❌ Available > Total
}
```

**✅ VALID Examples:**

```json
{
  "id": "100",
  "name": "Hospital Central",
  "address": "Rua Principal, 123",
  "beds": 50,
  "availableBeds": 30
}
```

### Product Add

**❌ INVALID Examples:**

```json
{
  "category": "Medicamento",
  "name": "", // ❌ Empty name
  "quantity": 100,
  "productType": "COMMON"
}
```

```json
{
  "category": "Medicamento",
  "name": "Dipirona",
  "quantity": -50, // ❌ Negative quantity
  "productType": "COMMON"
}
```

**✅ VALID Examples:**

```json
{
  "category": "Medicamento",
  "name": "Dipirona 500mg",
  "quantity": 100,
  "productType": "COMMON"
}
```

### Patient Checkin

**❌ INVALID Examples:**

```json
{
  "id": "200",
  "name": "", // ❌ Empty name
  "cpf": "12345678901",
  "gender": "masculino",
  "birthDate": "1990-05-15"
}
```

```json
{
  "id": "200",
  "cpf": "12345678901",
  // ❌ Missing name
  "gender": "masculino",
  "birthDate": "1990-05-15"
}
```

**✅ VALID Examples:**

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

## 9. Common Data Type Mistakes

### Mistake 1: String vs Number

```
❌ "beds": "50"           // String instead of integer
✅ "beds": 50            // Correct integer
```

### Mistake 2: Enum Case Sensitivity

```
❌ "productType": "common"        // Lowercase
❌ "productType": "Common"        // Mixed case
✅ "productType": "COMMON"       // Uppercase (enum)
```

### Mistake 3: Date Format

```
❌ "birthDate": "1990/05/15"     // Wrong separator
❌ "birthDate": "05-15-1990"     // Wrong order
✅ "birthDate": "15/05/1990"     // Correct dd/MM/yyyy
```

### Mistake 4: Missing Required Fields

```
❌ { "name": "Hospital" }        // Missing id, address, beds
✅ { "id": "1", "name": "Hospital", "address": "...", "beds": 50, "availableBeds": 30 }
```

### Mistake 5: Latitude/Longitude Order

```
❌ "coordinates": { "lat": -46.710462, "lon": -23.593438 }  // Swapped!
✅ "coordinates": { "latitude": -23.593438, "longitude": -46.710462 }  // Correct
```

---

## 10. How to Check Data Types in Code

### Open Domain Classes to See Field Types

**File:** `src/main/java/br/com/codenation/hospital/domain/Hospital.java`

```java
public class Hospital {
    @Id
    private String id;              // ← Type: String
    private String name;            // ← Type: String
    private int beds;               // ← Type: Integer
    private Location location;      // ← Type: Location object
    private List<Patient> patients; // ← Type: Array of Patient objects
}
```

### Check Enums for Valid Values

**File:** `src/main/java/br/com/codenation/hospital/domain/ProductType.java`

```java
public enum ProductType {
    COMMON,  // ← Valid value
    BLOOD    // ← Valid value
}
```

### Check DTOs for API Contract

**File:** `src/main/java/br/com/codenation/hospital/dto/HospitalDTO.java`

Shows how data is serialized to/from JSON in API requests/responses.

---

## Summary

| Category           | How to Find                                                          |
| ------------------ | -------------------------------------------------------------------- |
| Data Types         | Domain classes in `src/main/java/br/com/codenation/hospital/domain/` |
| Valid Enum Values  | Enum files (e.g., `ProductType.java`)                                |
| Request Format     | DTO classes in `src/main/java/br/com/codenation/hospital/dto/`       |
| Live Documentation | Swagger UI at `http://localhost:8080/swagger-ui.html`                |
| Working Examples   | Test cases in `manual_testing/test_cases.json`                       |
| Field Constraints  | Domain class constructor validation + setters                        |

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Covers:** All 4 primary resources (Hospital, Patient, Product, Location)
