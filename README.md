# Hospital Management System

## Objective

The objective of the project is to create an API to organize a public health care system.

## Background

The Unified Health System (SUS) is one of the largest and most complex public health systems in the world, encompassing everything from simple consultations for blood pressure evaluation through primary care to organ transplantation, guaranteeing comprehensive, universal, and free access for the entire population of the country. With its creation, the SUS provided universal access to the public health system without discrimination. Comprehensive health care, not just medical assistance, became the right of all Brazilians from conception throughout their lives, with a focus on health with quality of life, aimed at disease prevention and health promotion. The objective of this project is to create a tool to assist the SUS, avoid waste, and optimize resources for patients.

At the end of the program, in addition to presenting the created API, each team should expose what improvement opportunities exist and what would be the next steps for the project if they were to proceed further.

## Mandatory Technical Requirements

For the project, it is necessary that teams utilize the learning provided by the AceleraDev program, therefore the solution must be built according to the following requirements:

- Database
- Backend development and APIs with Java Spring Boot
- Unit tests are mandatory

## System Definitions

- Every hospital has an inventory containing various products.
- An inventory has products and their respective quantities.
- The inventory also contains a blood bank.
- The hospital also has beds (leitos).
- When finding a patient, it is important to recommend them to the nearest hospital that has available beds.
- If a hospital needs a product, for example, blood bank supplies, it is important to arrange transfer from the nearest hospital.
- If a hospital has only 4 items or 4 liters, it will have just enough for its own use.

## API Call Examples:

Using the API that manages hospitals within the public health system, the user will be able to, for example:

- Register a hospital
- Based on the patient's location, indicate the nearest hospital
- Perform patient check-in/check-out at the hospital
- Check how many beds are available at the hospital
- Register products and their respective quantities
- Register and manage blood bank supplies

### /v1/hospitais/{id}

Method: GET
Returns hospital information, for example:

- Name
- Address
- Number of beds
- Number of available beds

### /v1/hospitais/{id}/estoque

Method: GET
Returns information about existing products in inventory, for example.

### /v1/hospitais/{id}/estoque/{produto}

Method: GET
Returns more details about a product.

- Name
- Description
- Quantity

### /v1/hospitais/{id}/pacientes

Method: GET
Returns the names of patients at the hospital.

### /v1/hospitais/{id}/pacientes/{paciente}

Method: GET
Returns all information about the registered patient, for example:

- Full name
- CPF (Brazilian tax ID)
- Date of birth
- Gender/Sex
- Hospital admission date
