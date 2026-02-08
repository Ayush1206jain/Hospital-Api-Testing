"""
Configuration management for the AI Test Case Generator
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
TESTS_DIR = PROJECT_ROOT / "tests"
OAS_DOCS_DIR = PROJECT_ROOT.parent / "oas_docs"
MANUAL_TESTS_DIR = PROJECT_ROOT.parent / "manual_testing"

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # Options: "openai", "anthropic", "ollama"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# API Configuration
HOSPITAL_API_BASE_URL = os.getenv("HOSPITAL_API_BASE_URL", "http://localhost:8080")
HOSPITAL_API_VERSION = os.getenv("HOSPITAL_API_VERSION", "v1")

# Test Generation Configuration
VALID_TESTS_PER_ENDPOINT = int(os.getenv("VALID_TESTS_PER_ENDPOINT", "3"))
INVALID_TESTS_PER_ENDPOINT = int(os.getenv("INVALID_TESTS_PER_ENDPOINT", "3"))
ENABLE_EDGE_CASES = os.getenv("ENABLE_EDGE_CASES", "true").lower() == "true"

# Output Configuration
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")  # Options: "json", "csv", "postman"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "logs" / "ai_generator.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Feature Flags
ENABLE_POSTMAN_EXPORT = os.getenv("ENABLE_POSTMAN_EXPORT", "true").lower() == "true"
ENABLE_CSV_EXPORT = os.getenv("ENABLE_CSV_EXPORT", "true").lower() == "true"
VALIDATE_GENERATED_CASES = os.getenv("VALIDATE_GENERATED_CASES", "true").lower() == "true"
