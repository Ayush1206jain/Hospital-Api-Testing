# Project Overview

## What it does

- Backend API + frontend UI for a simple Hospital Management System: manage hospitals, patients, inventories (including blood bank), beds and location-based nearest-hospital lookups. The backend seeds sample data at startup.

## Tech stack

- Backend: Java 8, Spring Boot 2.1.3, Spring Web, Spring HATEOAS, Spring Data MongoDB
- Database: MongoDB
- Frontend: Angular 7, PrimeNG
- Build tools: Maven (mvnw wrapper provided) for backend, npm / Angular CLI for frontend
- API docs: springfox Swagger (swagger-ui)

## Key files

- Maven project descriptor: [pom.xml](pom.xml)
- Spring Boot application entry: [src/main/java/br/com/codenation/hospital/GestaohospitalarApplication.java](src/main/java/br/com/codenation/hospital/GestaohospitalarApplication.java)
- Data seeder (sample data on startup): [src/main/java/br/com/codenation/hospital/config/Instantiation.java](src/main/java/br/com/codenation/hospital/config/Instantiation.java)
- API controllers (REST resources): [src/main/java/br/com/codenation/hospital/resource/](src/main/java/br/com/codenation/hospital/resource/)
- MongoDB config: [src/main/resources/application.properties](src/main/resources/application.properties)
- Frontend (Angular) package: [hospital-ui/package.json](hospital-ui/package.json)

## Folder structure (high level)

- `src/main/java/.../hospital/` — Java sources: `resource/`, `services/`, `repository/`, `domain/`, `dto/`, `config/`, `integration/`, `constant/`
- `src/main/resources/` — runtime properties (MongoDB URI)
- `hospital-ui/` — Angular CLI project (frontend)
- `mvnw`, `mvnw.cmd` — Maven wrapper

## How to set up & run (Windows)

Prerequisites:

- JDK 8 installed and `JAVA_HOME` set
- MongoDB installed and running (default `mongod` on localhost)
- Node.js and npm installed
- (Optional) Angular CLI v7: `npm i -g @angular/cli@7`

1. Start MongoDB (ensure a `mongod` process running). The app expects `mongodb://localhost:27017/HospitalDB` by default (`application.properties`).

2. Run backend from project root (uses Maven wrapper):

```powershell
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\GestaoHospital\"
.\mvnw.cmd spring-boot:run
```

Or build and run the fat JAR:

```powershell
.\mvnw.cmd package
java -jar target\gestaohospitalar-0.0.1.jar
```

Default backend URL: `http://localhost:8080`.

3. Run frontend (in a separate terminal):

```powershell
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\GestaoHospital\hospital-ui"
npm install
npm start
```

Default frontend URL: `http://localhost:4200`.

## Quick checks & useful endpoints

- List hospitals: `GET http://localhost:8080/v1/hospitais/`
- Single hospital: `GET http://localhost:8080/v1/hospitais/{id}`
- Beds available: `GET http://localhost:8080/v1/hospitais/{id}/leitos`
- Nearest hospital search: `GET http://localhost:8080/v1/hospitais/maisProximo?lat={lat}&lon={lon}&raioMaximo={radius}`
- Swagger UI (API docs): `http://localhost:8080/swagger-ui.html`

## Notes

- The application seeds sample `Hospital`, `Patient`, `Location` and `Product` documents at startup (see `Instantiation`).
- CORS: controllers allow `http://localhost:4200` for the Angular dev server.
- If MongoDB URI or ports differ, update `src/main/resources/application.properties` or pass Spring Boot properties at runtime.

---

If you want, I can also:

- start the backend now in your terminal, or
- add a short `run.sh`/`run.ps1` helper, or
- add explicit `README` instructions in `hospital-ui/`.
