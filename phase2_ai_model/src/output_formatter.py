"""
Output Formatter - Formats generated test cases for various output formats
"""
import json
import csv
import logging
from typing import Dict, List, Any, Union
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

logger = logging.getLogger(__name__)


class OutputFormatter(ABC):
    """Abstract base class for output formatters"""
    
    @abstractmethod
    def format(self, test_cases: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Any:
        """Format test cases"""
        pass
    
    @abstractmethod
    def write(self, output_path: Union[str, Path], formatted_data: Any) -> None:
        """Write formatted data to file"""
        pass


class JSONFormatter(OutputFormatter):
    """Format test cases as JSON"""
    
    def format(self, test_cases: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Format test cases as JSON structure"""
        return {
            "metadata": metadata,
            "summary": self._create_summary(test_cases),
            "testCases": test_cases
        }
    
    def write(self, output_path: Union[str, Path], formatted_data: Dict[str, Any]) -> None:
        """Write JSON to file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2)
        
        logger.info(f"JSON output written to {output_path}")
    
    @staticmethod
    def _create_summary(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create summary statistics"""
        valid_count = len([tc for tc in test_cases if tc.get('category') == 'VALID'])
        invalid_count = len([tc for tc in test_cases if tc.get('category') == 'INVALID'])
        
        endpoints = set(tc.get('endpoint') for tc in test_cases)
        methods = {}
        priorities = {}
        
        for tc in test_cases:
            method = tc.get('method', 'UNKNOWN')
            methods[method] = methods.get(method, 0) + 1
            
            priority = tc.get('priority', 'MEDIUM')
            priorities[priority] = priorities.get(priority, 0) + 1
        
        return {
            "totalTestCases": len(test_cases),
            "validTestCases": valid_count,
            "invalidTestCases": invalid_count,
            "endpoints": len(endpoints),
            "methods": methods,
            "priorities": priorities
        }


class CSVFormatter(OutputFormatter):
    """Format test cases as CSV"""
    
    def format(self, test_cases: List[Dict[str, Any]], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format test cases for CSV output"""
        return test_cases
    
    def write(self, output_path: Union[str, Path], formatted_data: List[Dict[str, Any]]) -> None:
        """Write CSV to file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not formatted_data:
            logger.warning("No test cases to export to CSV")
            return
        
        # Define CSV columns
        csv_columns = [
            'testId', 'endpoint', 'method', 'category', 'description',
            'priority', 'expectedStatusCode'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore')
            writer.writeheader()
            
            for test_case in formatted_data:
                row = {}
                for col in csv_columns:
                    value = test_case.get(col, '')
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    row[col] = value
                writer.writerow(row)
        
        logger.info(f"CSV output written to {output_path}")


class PostmanFormatter(OutputFormatter):
    """Format test cases as Postman Collection"""
    
    def format(self, test_cases: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Format test cases as Postman collection"""
        return {
            "info": {
                "name": metadata.get("projectName", "Generated API Tests"),
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": self._create_postman_items(test_cases),
            "variable": self._create_postman_variables(metadata)
        }
    
    def write(self, output_path: Union[str, Path], formatted_data: Dict[str, Any]) -> None:
        """Write Postman collection to file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2)
        
        logger.info(f"Postman collection written to {output_path}")
    
    @staticmethod
    def _create_postman_items(test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert test cases to Postman request items"""
        items = []
        
        for tc in test_cases:
            item = {
                "name": f"{tc.get('testId')} - {tc.get('description', '')}",
                "event": [{
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": PostmanFormatter._create_test_script(tc)
                    }
                }],
                "request": {
                    "method": tc.get('method', 'GET'),
                    "header": PostmanFormatter._create_headers(tc.get('requestHeaders', {})),
                    "body": PostmanFormatter._create_body(tc.get('requestBody')),
                    "url": {
                        "raw": "{{baseUrl}}" + tc.get('endpoint', '/'),
                        "host": ["{{baseUrl}}"],
                        "path": tc.get('endpoint', '/').strip('/').split('/')
                    }
                },
                "response": []
            }
            items.append(item)
        
        return items
    
    @staticmethod
    def _create_postman_variables(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create Postman variables"""
        return [
            {
                "key": "baseUrl",
                "value": metadata.get("baseUrl", "http://localhost:8080"),
                "type": "string"
            },
            {
                "key": "apiVersion",
                "value": metadata.get("apiVersion", "v1"),
                "type": "string"
            }
        ]
    
    @staticmethod
    def _create_test_script(test_case: Dict[str, Any]) -> List[str]:
        """Create Postman test script"""
        assertions = test_case.get('assertions', [])
        scripts = []
        
        # Add status code assertion
        expected_status = test_case.get('expectedStatusCode', 200)
        scripts.append(f"pm.test('Status code is {expected_status}', function() {{\n    pm.response.to.have.status({expected_status});\n}});")
        
        # Add custom assertions
        for assertion in assertions:
            scripts.append(f"pm.test('{assertion}', function() {{\n    {assertion}\n}});")
        
        return scripts
    
    @staticmethod
    def _create_headers(headers: Dict[str, str]) -> List[Dict[str, str]]:
        """Convert headers dict to Postman headers array"""
        return [
            {"key": k, "value": v, "type": "text"}
            for k, v in (headers or {}).items()
        ]
    
    @staticmethod
    def _create_body(body: Union[Dict, str, None]) -> Dict[str, Any]:
        """Convert body to Postman body format"""
        if not body:
            return {}
        
        if isinstance(body, dict):
            return {
                "mode": "raw",
                "raw": json.dumps(body),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            }
        
        return {
            "mode": "raw",
            "raw": body
        }


class FormatterFactory:
    """Factory for creating output formatters"""
    
    _formatters = {
        "json": JSONFormatter,
        "csv": CSVFormatter,
        "postman": PostmanFormatter
    }
    
    @classmethod
    def create_formatter(cls, format_name: str) -> OutputFormatter:
        """Create formatter for given format"""
        formatter_class = cls._formatters.get(format_name.lower())
        if not formatter_class:
            raise ValueError(f"Unknown format: {format_name}")
        return formatter_class()
    
    @classmethod
    def register_formatter(cls, format_name: str, formatter_class: type) -> None:
        """Register a custom formatter"""
        cls._formatters[format_name.lower()] = formatter_class
