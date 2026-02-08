"""
OpenAPI Specification (OAS) Parser
Extracts endpoints, parameters, schemas, and constraints from OAS documents
"""
import json
import yaml
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class Parameter:
    """Represents an API parameter"""
    name: str
    in_: str  # "path", "query", "header", "body"
    required: bool
    data_type: str
    description: str = ""
    example: Any = None
    enum_values: List[str] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None


@dataclass
class ResponseSchema:
    """Represents API response schema"""
    status_code: int
    content_type: str = "application/json"
    schema: Dict[str, Any] = None


@dataclass
class Endpoint:
    """Represents an API endpoint"""
    path: str
    method: str
    summary: str = ""
    description: str = ""
    operation_id: str = ""
    tags: List[str] = None
    parameters: List[Parameter] = None
    request_body_schema: Dict[str, Any] = None
    request_required_fields: List[str] = None
    responses: List[ResponseSchema] = None
    produces: List[str] = None
    consumes: List[str] = None

    def to_dict(self):
        return asdict(self)


class OASParser:
    """Parse OpenAPI/Swagger specifications"""

    def __init__(self, oas_file_path: Union[str, Path]):
        """
        Initialize OAS Parser
        
        Args:
            oas_file_path: Path to OAS file (YAML or JSON)
        """
        self.file_path = Path(oas_file_path)
        self.oas_doc = self._load_oas_document()
        self.endpoints: List[Endpoint] = []
        self.api_version = self.oas_doc.get("info", {}).get("version", "1.0.0")
        self.base_path = self.oas_doc.get("basePath", "")
        self.api_title = self.oas_doc.get("info", {}).get("title", "API")

    def _load_oas_document(self) -> Dict[str, Any]:
        """Load OAS document from YAML or JSON file"""
        try:
            if self.file_path.suffix.lower() in ['.yaml', '.yml']:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:  # JSON
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load OAS document: {e}")
            raise

    def parse(self) -> List[Endpoint]:
        """Parse all endpoints from OAS document"""
        paths = self.oas_doc.get("paths", {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                    continue
                
                endpoint = self._parse_operation(path, method.upper(), operation)
                self.endpoints.append(endpoint)
        
        logger.info(f"Parsed {len(self.endpoints)} endpoints from OAS document")
        return self.endpoints

    def _parse_operation(self, path: str, method: str, operation: Dict[str, Any]) -> Endpoint:
        """Parse a single operation/endpoint"""
        parameters = self._parse_parameters(operation.get("parameters", []))
        request_body_schema, required_fields = self._parse_request_body(operation.get("requestBody"))
        responses = self._parse_responses(operation.get("responses", {}))

        endpoint = Endpoint(
            path=path,
            method=method,
            summary=operation.get("summary", ""),
            description=operation.get("description", ""),
            operation_id=operation.get("operationId", ""),
            tags=operation.get("tags", []),
            parameters=parameters,
            request_body_schema=request_body_schema,
            request_required_fields=required_fields or [],
            responses=responses,
            produces=operation.get("produces", ["application/json"]),
            consumes=operation.get("consumes", ["application/json"])
        )
        return endpoint

    def _parse_parameters(self, parameters: List[Dict[str, Any]]) -> List[Parameter]:
        """Parse endpoint parameters"""
        parsed_params = []
        
        for param in parameters:
            schema = param.get("schema", {})
            param_type = param.get("type", schema.get("type", "string"))
            
            parsed_param = Parameter(
                name=param.get("name", ""),
                in_=param.get("in", ""),
                required=param.get("required", False),
                data_type=param_type,
                description=param.get("description", ""),
                example=param.get("example", schema.get("example")),
                enum_values=param.get("enum", schema.get("enum")),
                minimum=param.get("minimum", schema.get("minimum")),
                maximum=param.get("maximum", schema.get("maximum")),
                min_length=param.get("minLength", schema.get("minLength")),
                max_length=param.get("maxLength", schema.get("maxLength")),
                pattern=param.get("pattern", schema.get("pattern"))
            )
            parsed_params.append(parsed_param)
        
        return parsed_params

    def _parse_request_body(self, request_body: Dict[str, Any]) -> tuple[Optional[Dict], Optional[List[str]]]:
        """Parse request body schema"""
        if not request_body:
            return None, None
        
        content = request_body.get("content", {})
        schema = None
        required_fields = []

        # Try to get schema from JSON content
        if "application/json" in content:
            json_content = content["application/json"]
            schema = json_content.get("schema", {})
            required_fields = schema.get("required", [])

        return schema, required_fields

    def _parse_responses(self, responses: Dict[str, Any]) -> List[ResponseSchema]:
        """Parse response schemas"""
        parsed_responses = []
        
        for status_code, response_obj in responses.items():
            try:
                code = int(status_code)
            except ValueError:
                continue
            
            content = response_obj.get("content", {})
            schema = None
            
            if "application/json" in content:
                schema = content["application/json"].get("schema")
            
            parsed_response = ResponseSchema(
                status_code=code,
                content_type="application/json",
                schema=schema
            )
            parsed_responses.append(parsed_response)
        
        return parsed_responses

    def get_all_endpoints(self) -> List[Endpoint]:
        """Get all parsed endpoints"""
        return self.endpoints

    def get_endpoints_by_tag(self, tag: str) -> List[Endpoint]:
        """Get endpoints filtered by tag"""
        return [e for e in self.endpoints if tag in (e.tags or [])]

    def get_endpoint_summary(self) -> Dict[str, Any]:
        """Get summary of parsed endpoints"""
        methods = {}
        for endpoint in self.endpoints:
            method = endpoint.method
            if method not in methods:
                methods[method] = 0
            methods[method] += 1
        
        return {
            "api_title": self.api_title,
            "api_version": self.api_version,
            "total_endpoints": len(self.endpoints),
            "methods": methods,
            "tags": list(set(tag for e in self.endpoints for tag in (e.tags or [])))
        }

    def export_endpoints_json(self, output_path: Union[str, Path]) -> None:
        """Export parsed endpoints to JSON file"""
        output_path = Path(output_path)
        endpoints_data = {
            "api_title": self.api_title,
            "api_version": self.api_version,
            "endpoints": [asdict(e) for e in self.endpoints]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(endpoints_data, f, indent=2, default=str)
        
        logger.info(f"Exported {len(self.endpoints)} endpoints to {output_path}")
