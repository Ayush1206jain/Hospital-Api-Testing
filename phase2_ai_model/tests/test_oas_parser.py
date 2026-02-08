"""
Unit tests for OAS Parser
"""
import pytest
import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from oas_parser import OASParser, Endpoint, Parameter


class TestOASParser:
    """Test OAS Parser functionality"""
    
    @pytest.fixture
    def sample_oas_json(self):
        """Create a sample OAS JSON document"""
        return {
            "swagger": "2.0",
            "info": {
                "title": "Hospital API",
                "version": "1.0.0"
            },
            "basePath": "/api",
            "paths": {
                "/hospitals": {
                    "post": {
                        "summary": "Create hospital",
                        "operationId": "createHospital",
                        "tags": ["hospitals"],
                        "consumes": ["application/json"],
                        "produces": ["application/json"],
                        "parameters": [
                            {
                                "name": "body",
                                "in": "body",
                                "required": True,
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "address": {"type": "string"}
                                    },
                                    "required": ["name", "address"]
                                }
                            }
                        ],
                        "responses": {
                            "201": {
                                "description": "Hospital created",
                                "schema": {"type": "object"}
                            }
                        }
                    }
                }
            }
        }
    
    @pytest.fixture
    def oas_file(self, sample_oas_json):
        """Create temporary OAS file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_oas_json, f)
            tmp_path = f.name
        
        yield tmp_path
        
        # Cleanup
        Path(tmp_path).unlink()
    
    def test_oas_parser_initialization(self, oas_file):
        """Test OAS parser can be initialized"""
        parser = OASParser(oas_file)
        assert parser.api_title == "Hospital API"
        assert parser.api_version == "1.0.0"
    
    def test_parse_endpoints(self, oas_file):
        """Test parsing endpoints"""
        parser = OASParser(oas_file)
        endpoints = parser.parse()
        
        assert len(endpoints) > 0
        assert any(e.path == "/hospitals" for e in endpoints)
    
    def test_endpoint_attributes(self, oas_file):
        """Test endpoint attributes are parsed correctly"""
        parser = OASParser(oas_file)
        endpoints = parser.parse()
        
        hospital_endpoint = [e for e in endpoints if e.path == "/hospitals"][0]
        
        assert hospital_endpoint.method == "POST"
        assert hospital_endpoint.summary == "Create hospital"
        assert "hospitals" in hospital_endpoint.tags
    
    def test_get_endpoints_summary(self, oas_file):
        """Test getting endpoints summary"""
        parser = OASParser(oas_file)
        parser.parse()
        
        summary = parser.get_endpoint_summary()
        
        assert summary["api_title"] == "Hospital API"
        assert summary["total_endpoints"] > 0
        assert "POST" in summary["methods"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
