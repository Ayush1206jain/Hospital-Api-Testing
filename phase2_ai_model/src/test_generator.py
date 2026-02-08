"""
Test Case Generator - Orchestrates test case generation using OAS parser and LLM
"""
import logging
import json
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

from oas_parser import OASParser, Endpoint
from llm_processor import LLMProcessor, LLMFactory

logger = logging.getLogger(__name__)


class TestCaseValidator:
    """Validates generated test cases"""
    
    @staticmethod
    def validate_test_case(test_case: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate test case structure
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        required_fields = ['testId', 'endpoint', 'method', 'category', 'description', 'expectedStatusCode']
        
        for field in required_fields:
            if field not in test_case:
                errors.append(f"Missing required field: {field}")
        
        if 'category' in test_case and test_case['category'] not in ['VALID', 'INVALID']:
            errors.append(f"Invalid category: {test_case['category']}. Must be 'VALID' or 'INVALID'")
        
        if 'priority' in test_case and test_case['priority'] not in ['HIGH', 'MEDIUM', 'LOW']:
            errors.append(f"Invalid priority: {test_case['priority']}. Must be 'HIGH', 'MEDIUM', or 'LOW'")
        
        return len(errors) == 0, errors


class TestCaseGenerator:
    """Main test case generator using LLM and OAS"""
    
    def __init__(
        self,
        oas_file_path: Union[str, Path],
        llm_provider: str = "openai",
        llm_config: Optional[Dict[str, str]] = None
    ):
        """
        Initialize test case generator
        
        Args:
            oas_file_path: Path to OAS specification
            llm_provider: "openai" or "anthropic"
            llm_config: LLM configuration dict with api_key, model, temperature
        """
        self.oas_parser = OASParser(oas_file_path)
        self.endpoints = self.oas_parser.parse()
        
        # Initialize LLM
        if llm_config is None:
            llm_config = {}
        
        self.llm_provider_name = llm_provider
        self.llm = LLMFactory.create_provider(llm_provider, **llm_config)
        self.llm_processor = LLMProcessor(self.llm)
        
        self.generated_test_cases: List[Dict[str, Any]] = []
        self.validator = TestCaseValidator()
    
    def generate_all_tests(
        self,
        valid_cases_per_endpoint: int = 3,
        invalid_cases_per_endpoint: int = 3,
        filter_tags: Optional[List[str]] = None,
        validate: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate test cases for all endpoints
        
        Args:
            valid_cases_per_endpoint: Number of valid test cases per endpoint
            invalid_cases_per_endpoint: Number of invalid test cases per endpoint
            filter_tags: Only generate for endpoints with these tags
            validate: Whether to validate generated test cases
        
        Returns:
            List of all generated test cases
        """
        self.generated_test_cases = []
        endpoints_to_process = self.endpoints
        
        if filter_tags:
            endpoints_to_process = [
                e for e in self.endpoints
                if any(tag in (e.tags or []) for tag in filter_tags)
            ]
        
        logger.info(f"Generating test cases for {len(endpoints_to_process)} endpoints")
        
        for endpoint in endpoints_to_process:
            endpoint_cases = self.generate_tests_for_endpoint(
                endpoint,
                valid_cases_per_endpoint,
                invalid_cases_per_endpoint
            )
            
            if validate:
                endpoint_cases = self._validate_and_filter_cases(endpoint_cases)
            
            self.generated_test_cases.extend(endpoint_cases)
            logger.info(f"Generated {len(endpoint_cases)} test cases for {endpoint.path}")
        
        logger.info(f"Total generated test cases: {len(self.generated_test_cases)}")
        return self.generated_test_cases
    
    def generate_tests_for_endpoint(
        self,
        endpoint: Endpoint,
        num_valid: int = 3,
        num_invalid: int = 3
    ) -> List[Dict[str, Any]]:
        """Generate test cases for a specific endpoint"""
        endpoint_info = {
            'path': endpoint.path,
            'method': endpoint.method,
            'summary': endpoint.summary,
            'description': endpoint.description,
            'parameters': [asdict(p) for p in (endpoint.parameters or [])],
            'requestBodySchema': endpoint.request_body_schema,
            'requiredFields': endpoint.request_required_fields or []
        }
        
        test_cases = self.llm_processor.generate_test_cases_for_endpoint(
            endpoint_info,
            num_valid,
            num_invalid
        )
        
        return test_cases
    
    def _validate_and_filter_cases(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate test cases and remove invalid ones"""
        valid_cases = []
        
        for test_case in test_cases:
            is_valid, errors = self.validator.validate_test_case(test_case)
            
            if is_valid:
                valid_cases.append(test_case)
            else:
                logger.warning(f"Invalid test case: {errors}")
        
        return valid_cases
    
    def export_to_json(self, output_path: Union[str, Path]) -> None:
        """Export test cases to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        output_data = {
            "projectName": self.oas_parser.api_title,
            "apiVersion": self.oas_parser.api_version,
            "generatedAt": datetime.now().isoformat(),
            "generatorInfo": {
                "type": "AI-Generated",
                "llmProvider": self.llm_provider_name,
                "oasFile": str(self.oas_parser.file_path)
            },
            "totalTestCases": len(self.generated_test_cases),
            "testCases": self.generated_test_cases
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"Exported {len(self.generated_test_cases)} test cases to {output_path}")
    
    def export_to_csv(self, output_path: Union[str, Path]) -> None:
        """Export test cases to CSV format"""
        import csv
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.generated_test_cases:
            logger.warning("No test cases to export")
            return
        
        # Get all possible keys from test cases
        all_keys = set()
        for tc in self.generated_test_cases:
            all_keys.update(tc.keys())
        
        # Define CSV columns (simplified)
        csv_columns = [
            'testId', 'endpoint', 'method', 'category', 'description',
            'priority', 'expectedStatusCode'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=csv_columns,
                extrasaction='ignore'
            )
            writer.writeheader()
            
            for test_case in self.generated_test_cases:
                # Convert complex fields to strings
                row = {}
                for col in csv_columns:
                    value = test_case.get(col, '')
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    row[col] = value
                writer.writerow(row)
        
        logger.info(f"Exported {len(self.generated_test_cases)} test cases to {output_path}")
    
    def export_to_postman(self, output_path: Union[str, Path]) -> None:
        """Export test cases to Postman collection format"""
        # This would create a Postman collection JSON
        # Implementation depends on Postman collection schema
        logger.warning("Postman export not yet implemented")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated test cases"""
        valid_count = len([tc for tc in self.generated_test_cases if tc.get('category') == 'VALID'])
        invalid_count = len([tc for tc in self.generated_test_cases if tc.get('category') == 'INVALID'])
        
        endpoints_covered = set(tc.get('endpoint') for tc in self.generated_test_cases)
        
        return {
            "total_test_cases": len(self.generated_test_cases),
            "valid_test_cases": valid_count,
            "invalid_test_cases": invalid_count,
            "endpoints_covered": len(endpoints_covered),
            "endpoints_total": len(self.endpoints),
            "avg_cases_per_endpoint": len(self.generated_test_cases) / len(self.endpoints) if self.endpoints else 0
        }
