"""
Main entry point for AI Test Case Generator
"""
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, LLM_PROVIDER, LLM_MODEL,
    LLM_TEMPERATURE, OUTPUT_FORMAT, OUTPUT_DIR, VALID_TESTS_PER_ENDPOINT,
    INVALID_TESTS_PER_ENDPOINT, LOG_LEVEL, LOG_FILE, OLLAMA_SERVER
)
from test_generator import TestCaseGenerator
from output_formatter import FormatterFactory

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_llm_config(provider: str, api_key: str = "", model: str = "", temperature: float = 0.7, server_url: str = ""):
    """Setup LLM configuration"""
    if provider.lower() == "ollama":
        config = {
            "model": model or LLM_MODEL,
            "temperature": temperature or LLM_TEMPERATURE,
            "server_url": server_url or OLLAMA_SERVER
        }
    else:
        config = {
            "api_key": api_key or (OPENAI_API_KEY if provider == "openai" else ANTHROPIC_API_KEY),
            "model": model or LLM_MODEL,
            "temperature": temperature or LLM_TEMPERATURE
        }
        
        if not config["api_key"]:
            raise ValueError(f"API key not provided for {provider}. Set {provider.upper()}_API_KEY environment variable.")
    
    return config


def generate_tests(
    oas_file: Path,
    provider: str = LLM_PROVIDER,
    llm_config: Optional[dict] = None,
    valid_per_endpoint: int = VALID_TESTS_PER_ENDPOINT,
    invalid_per_endpoint: int = INVALID_TESTS_PER_ENDPOINT,
    tags: Optional[list] = None,
    output_format: str = OUTPUT_FORMAT
) -> dict:
    """
    Generate test cases from OAS specification
    
    Args:
        oas_file: Path to OAS specification file
        provider: LLM provider (openai or anthropic)
        llm_config: LLM configuration dict
        valid_per_endpoint: Number of valid test cases per endpoint
        invalid_per_endpoint: Number of invalid test cases per endpoint
        tags: Filter by endpoint tags
        output_format: Output format (json, csv, postman)
    
    Returns:
        Dictionary with results
    """
    try:
        logger.info(f"Starting test case generation for {oas_file}")
        
        if not oas_file.exists():
            raise FileNotFoundError(f"OAS file not found: {oas_file}")
        
        # Setup LLM config
        if llm_config is None:
            llm_config = setup_llm_config(provider)
        
        # Initialize generator
        generator = TestCaseGenerator(
            oas_file_path=oas_file,
            llm_provider=provider,
            llm_config=llm_config
        )
        
        # Generate test cases
        test_cases = generator.generate_all_tests(
            valid_cases_per_endpoint=valid_per_endpoint,
            invalid_cases_per_endpoint=invalid_per_endpoint,
            filter_tags=tags,
            validate=True
        )
        
        # Export results
        output_file = OUTPUT_DIR / f"generated_tests_{output_format}.{output_format if output_format != 'postman' else 'json'}"
        
        formatter = FormatterFactory.create_formatter(output_format)
        metadata = {
            "projectName": generator.oas_parser.api_title,
            "apiVersion": generator.oas_parser.api_version,
            "baseUrl": "http://localhost:8080",
            "oasFile": str(oas_file)
        }
        
        formatted_data = formatter.format(test_cases, metadata)
        formatter.write(output_file, formatted_data)
        
        stats = generator.get_statistics()
        
        return {
            "success": True,
            "message": f"Generated {len(test_cases)} test cases",
            "output_file": str(output_file),
            "statistics": stats
        }
    
    except Exception as e:
        logger.error(f"Error generating test cases: {e}", exc_info=True)
        return {
            "success": False,
            "message": str(e),
            "error": type(e).__name__
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Test Case Generator for Hospital Management API"
    )
    
    parser.add_argument(
        "oas_file",
        type=Path,
        help="Path to OpenAPI specification file"
    )
    
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default=LLM_PROVIDER,
        help="LLM provider to use (default: openai)"
    )
    
    parser.add_argument(
        "--api-key",
        help="API key for LLM provider (overrides environment variable)"
    )
    
    parser.add_argument(
        "--model",
        default=LLM_MODEL,
        help="LLM model to use"
    )
    
    parser.add_argument(
        "--valid-per-endpoint",
        type=int,
        default=VALID_TESTS_PER_ENDPOINT,
        help="Number of valid test cases per endpoint"
    )
    
    parser.add_argument(
        "--invalid-per-endpoint",
        type=int,
        default=INVALID_TESTS_PER_ENDPOINT,
        help="Number of invalid test cases per endpoint"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["json", "csv", "postman"],
        default=OUTPUT_FORMAT,
        help="Output format for test cases"
    )
    
    parser.add_argument(
        "--tags",
        nargs="+",
        help="Filter endpoints by tags"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Setup LLM config
    llm_config = None
    if args.api_key:
        llm_config = {
            "api_key": args.api_key,
            "model": args.model,
            "temperature": LLM_TEMPERATURE
        }
    
    # Generate tests
    result = generate_tests(
        oas_file=args.oas_file,
        provider=args.provider,
        llm_config=llm_config,
        valid_per_endpoint=args.valid_per_endpoint,
        invalid_per_endpoint=args.invalid_per_endpoint,
        tags=args.tags,
        output_format=args.output_format
    )
    
    # Print results
    print("\n" + "="*60)
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"\nOutput: {result['output_file']}")
        print(f"\nStatistics:")
        for key, value in result["statistics"].items():
            print(f"  {key}: {value}")
    else:
        print(f"✗ Error: {result['message']}")
        sys.exit(1)
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
