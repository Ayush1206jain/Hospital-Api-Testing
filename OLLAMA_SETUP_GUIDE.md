# Hospital Management System - Ollama Setup & Run Guide

## Prerequisites

Your project uses **Ollama** (local AI) instead of OpenAI or Claude. Make sure you have:

1. **Ollama** installed - Download from https://ollama.ai
2. **Java 11+** - For backend
3. **Node.js 14+** - For frontend (Angular)
4. **Python 3.8+** - For AI model
5. **Maven** - For Java build (included in project)

---

## System Architecture Overview

```
Hospital Management System
├── Backend (Java/Spring Boot) - Port 8080
│   ├── Hospital Management API
│   ├── Patient Management
│   └── Inventory System
│
├── Frontend (Angular) - Port 4200
│   ├── Web UI
│   └── API Integration
│
└── AI Model (Python) - Test Case Generation
    ├── OAS Parser
    ├── LLM Processor (Ollama)
    └── Test Generator
```

---

## Step 1: Start Ollama Server

**IMPORTANT: Start Ollama FIRST before running the AI model**

### On Windows:

1. **Open PowerShell or CMD** as Administrator
2. **Start Ollama service:**

   ```powershell
   ollama serve
   ```

   - This will start the server on `http://localhost:11434`
   - Keep this terminal open

3. **In another terminal, verify installation:**

   ```powershell
   ollama list
   ```

   - You should see available models

4. **Pull the required model** (if not already installed):
   ```powershell
   ollama pull llama3:8b-instruct
   ```

   - This downloads the llama3 model (~4.7 GB)
   - Wait for completion

---

## Step 2: Start Backend (Java API)

### 1. Open new terminal at project root

```powershell
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\GestaoHospital"
```

### 2. Build the project

```powershell
./mvnw clean install
```

- Or on Windows:

```powershell
mvnw.cmd clean install
```

- Wait for build to complete (this may take 5-10 minutes first time)

### 3. Start the backend server

```powershell
./mvnw spring-boot:run
```

- Or:

```powershell
mvnw.cmd spring-boot:run
```

**Expected output:**

```
Started [GestaoHospitalarApplication] in 12.345 seconds
Tomcat started on port 8080
```

**Verify:** Open http://localhost:8080/swagger-ui.html in your browser

---

## Step 3: Start Frontend (Angular)

### 1. Open new terminal at hospital-ui directory

```powershell
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\GestaoHospital\hospital-ui"
```

### 2. Install dependencies

```powershell
npm install
```

- This installs all Node packages (first time takes ~2-5 minutes)

### 3. Start Angular development server

```powershell
npm start
```

- Or:

```powershell
ng serve
```

**Expected output:**

```
Compiled successfully.
Application bundle generated successfully.
Local: http://localhost:4200/
```

**Verify:** Open http://localhost:4200 in your browser

---

## Step 4: Configure & Run AI Test Generator (Python/Ollama)

### 1. Open new terminal at phase2_ai_model directory

```powershell
cd "d:\NIT-K 2nd Sem\mini project\oasdocuments\Hospital Managament System\GestaoHospital\phase2_ai_model"
```

### 2. Create Python virtual environment (if not exists)

```powershell
python -m venv venv
```

### 3. Activate virtual environment

```powershell
# On Windows:
.\venv\Scripts\Activate.ps1
```

If you get execution policy error:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activate again.

### 4. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 5. Verify your .env file configuration

```powershell
# Your .env file should have:
cat .env
```

**Expected content:**

```
LLM_PROVIDER=ollama
LLM_MODEL=llama3:8b-instruct
OLLAMA_SERVER=http://localhost:11434
HOSPITAL_API_BASE_URL=http://localhost:8080
HOSPITAL_API_VERSION=v1
VALID_TESTS_PER_ENDPOINT=3
INVALID_TESTS_PER_ENDPOINT=3
```

### 6. Run the AI test generator

```powershell
python main.py
```

**Expected flow:**

1. Reads OAS specification from `../oas_docs/hospital-api.json`
2. Parses API endpoints
3. Connects to Ollama server (`http://localhost:11434`)
4. Loads model `llama3:8b-instruct`
5. Generates test cases for each endpoint
6. Outputs results to `output/` directory in JSON format

**Output files created:**

```
output/
├── hospital_test_cases_<timestamp>.json
├── hospital_test_cases_<timestamp>.csv (if enabled)
└── hospital_test_cases_<timestamp>.postman_collection.json (if enabled)
```

---

## 5. Expected Ollama Behavior

When running with Ollama:

✓ **First run:** Ollama loads the model into memory (~5-15 seconds)
✓ **Generation:** AI generates test cases (slow at first, improves with warmup)
✓ **No API costs:** Everything runs locally
✓ **Privacy:** Your data never leaves your machine

**Typical generation time per endpoint:** 10-30 seconds

---

## Complete Terminal Setup (Quick Reference)

### Terminal 1: Ollama

```powershell
ollama serve
```

### Terminal 2: Backend

```powershell
cd GestaoHospital
mvnw.cmd clean install
mvnw.cmd spring-boot:run
```

### Terminal 3: Frontend

```powershell
cd hospital-ui
npm install
npm start
```

### Terminal 4: Python AI Model

```powershell
cd phase2_ai_model
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## Troubleshooting

### Problem: "Cannot connect to Ollama server"

**Solution:**

- Ensure Ollama is running: `ollama serve` in first terminal
- Verify server: Open http://localhost:11434/api/tags in browser
- Check .env: OLLAMA_SERVER should be `http://localhost:11434`

### Problem: "Model 'llama3:8b-instruct' not found"

**Solution:**

```powershell
ollama pull llama3:8b-instruct
# If that fails, try:
ollama list  # See available models
```

### Problem: "Backend won't start on port 8080"

**Solution:**

```powershell
# Check what's using port 8080:
netstat -ano | findstr :8080
# Kill process: taskkill /PID <PID> /F
```

### Problem: "Angular frontend not compiling"

**Solution:**

```powershell
cd hospital-ui
npm cache clean --force
npm install
npm start
```

### Problem: "Python packages not installing"

**Solution:**

```powershell
# Update pip first:
python -m pip install --upgrade pip
# Then:
pip install -r requirements.txt -v
```

---

## Testing the System

### 1. Test Backend API

```powershell
# Get hospitals list
curl -X GET "http://localhost:8080/v1/hospitais/"

# Or use Swagger UI:
Open http://localhost:8080/swagger-ui.html
```

### 2. Test Frontend

```
Open http://localhost:4200 in browser
```

### 3. Test AI Test Generator

```powershell
cd phase2_ai_model
python main.py
# Wait for output/ directory to be populated
dir output/
```

---

## Configuration Options

You can customize the AI test generation by editing `.env`:

```env
# Model configuration
LLM_MODEL=llama3:8b-instruct    # Try: llama2, mistral, neural-chat
LLM_TEMPERATURE=0.7             # 0=deterministic, 1=creative

# Test generation
VALID_TESTS_PER_ENDPOINT=3      # Increase for more test cases
INVALID_TESTS_PER_ENDPOINT=3    # Increase for more negative tests

# Output format
OUTPUT_FORMAT=json              # Options: json, csv, postman
ENABLE_POSTMAN_EXPORT=true      # Generate Postman collections
```

---

## Next Steps

1. ✅ All 3 services running (Ollama, Backend, Frontend, Python)
2. Go to http://localhost:4200 to access the web UI
3. Go to http://localhost:8080/swagger-ui.html for API documentation
4. Check `phase2_ai_model/output/` for generated test cases
5. Use the generated test cases in Postman for API testing

---

## Additional Commands

### View Ollama logs

```powershell
# Already running in terminal if you used 'ollama serve'
```

### View Backend logs

```powershell
# Check terminal where mvnw spring-boot:run is running
```

### View Python logs

```powershell
# Check phase2_ai_model/logs/ directory
type logs/ai_generator.log
```

### Stop all services

- Press `Ctrl+C` in each terminal to stop services
- Close all terminals when done

---

## Summary

Your Hospital Management System is now configured to use **Ollama** for local AI-powered test generation. The architecture provides:

- **No API costs** - Everything runs locally
- **Privacy** - Your data stays on your machine
- **Fast iteration** - No API latency
- **Full control** - Easy to modify prompts and parameters

Enjoy developing! 🚀
