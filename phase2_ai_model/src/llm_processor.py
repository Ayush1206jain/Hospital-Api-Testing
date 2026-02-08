"""
LLM Processor - Handles integration with OpenAI and Anthropic APIs
"""
import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    tokens_used: int = 0
    stop_reason: Optional[str] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 2000) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def parse_json_response(self, response: LLMResponse) -> Dict[str, Any]:
        """Parse JSON from LLM response"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize OpenAI provider
        
        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4)
            temperature: Temperature for response generation (0-1)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            return OpenAI(api_key=self.api_key)
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise
    
    def generate_response(self, prompt: str, max_tokens: int = 2000) -> LLMResponse:
        """Generate response from OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert API testing specialist. Generate test cases in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used,
                stop_reason=response.choices[0].finish_reason
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def parse_json_response(self, response: LLMResponse) -> Dict[str, Any]:
        """Parse JSON from OpenAI response"""
        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {response.content}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic Claude LLM Provider"""
    
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229", temperature: float = 0.7):
        """
        Initialize Anthropic provider
        
        Args:
            api_key: Anthropic API key
            model: Model name (default: claude-3-opus-20240229)
            temperature: Temperature for response generation (0-1)
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Anthropic client"""
        try:
            from anthropic import Anthropic
            return Anthropic(api_key=self.api_key)
        except ImportError:
            logger.error("Anthropic library not installed. Install with: pip install anthropic")
            raise
    
    def generate_response(self, prompt: str, max_tokens: int = 2000) -> LLMResponse:
        """Generate response from Anthropic Claude"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system="You are an expert API testing specialist. Generate test cases in JSON format.",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens if response.usage else 0
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used,
                stop_reason=response.stop_reason
            )
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    def parse_json_response(self, response: LLMResponse) -> Dict[str, Any]:
        """Parse JSON from Anthropic response"""
        try:
            # Extract JSON from markdown code blocks if present
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {response.content}")
            raise


class OllamaProvider(LLMProvider):
    """Ollama Local LLM Provider"""
    
    def __init__(self, model: str = "llama3:8b-instruct", temperature: float = 0.7, server_url: str = "http://localhost:11434"):
        """
        Initialize Ollama provider
        
        Args:
            model: Model name (default: llama3:8b-instruct)
            temperature: Temperature for response generation (0-1)
            server_url: URL of Ollama server (default: http://localhost:11434)
        """
        self.model = model
        self.temperature = temperature
        self.server_url = server_url.rstrip('/')
        self._verify_connection()
    
    def _verify_connection(self):
        """Verify connection to Ollama server"""
        try:
            import requests
            response = requests.get(f"{self.server_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"Ollama server returned status {response.status_code}")
            logger.info(f"Connected to Ollama server at {self.server_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama server at {self.server_url}: {e}")
            logger.info(f"Make sure Ollama is running. Start with: ollama serve")
            raise
    
    def generate_response(self, prompt: str, max_tokens: int = 2000) -> LLMResponse:
        """Generate response from Ollama"""
        try:
            import requests
            import json
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": self.temperature,
                "num_predict": max_tokens
            }
            
            response = requests.post(
                f"{self.server_url}/api/generate",
                json=payload,
                timeout=300  # 5 minutes timeout for generation
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.text}")
            
            result = response.json()
            content = result.get('response', '')
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=result.get('total_duration', 0),
                stop_reason=result.get('done_reason', 'stop')
            )
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise
    
    def parse_json_response(self, response: LLMResponse) -> Dict[str, Any]:
        """Parse JSON from Ollama response"""
        try:
            content = response.content
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response content: {response.content}")
            # Return a partial response structure if parsing fails
            return {}


class LLMFactory:
    """Factory for creating LLM providers"""
    
    @staticmethod
    def create_provider(provider_name: str, **kwargs) -> LLMProvider:
        """
        Create LLM provider
        
        Args:
            provider_name: "openai", "anthropic", or "ollama"
            **kwargs: Provider-specific arguments (api_key, model, temperature, server_url)
        
        Returns:
            LLMProvider instance
        """
        if provider_name.lower() == "openai":
            return OpenAIProvider(**kwargs)
        elif provider_name.lower() == "anthropic":
            return AnthropicProvider(**kwargs)
        elif provider_name.lower() == "ollama":
            return OllamaProvider(**kwargs)
        else:
            raise ValueError(f"Unknown LLM provider: {provider_name}")


class LLMProcessor:
    """Main LLM processor for test case generation"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize LLM processor
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
    
    def generate_test_cases_for_endpoint(
        self,
        endpoint_info: Dict[str, Any],
        num_valid_cases: int = 3,
        num_invalid_cases: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate test cases for an endpoint using LLM
        
        Args:
            endpoint_info: Information about the API endpoint
            num_valid_cases: Number of valid test cases to generate
            num_invalid_cases: Number of invalid test cases to generate
        
        Returns:
            List of generated test cases
        """
        prompt = self._build_test_generation_prompt(
            endpoint_info,
            num_valid_cases,
            num_invalid_cases
        )
        
        logger.info(f"Generating test cases for {endpoint_info.get('path')}")
        
        try:
            response = self.llm.generate_response(prompt, max_tokens=4000)
            test_cases = self.llm.parse_json_response(response)
            
            return test_cases.get("testCases", [])
        except Exception as e:
            logger.error(f"Error generating test cases: {e}")
            return []
    
    def _build_test_generation_prompt(
        self,
        endpoint_info: Dict[str, Any],
        num_valid_cases: int,
        num_invalid_cases: int
    ) -> str:
        """Build prompt for LLM test case generation"""
        prompt = f"""
You are an expert API testing specialist. Generate comprehensive test cases for the following API endpoint.

ENDPOINT INFORMATION:
Path: {endpoint_info.get('path', 'N/A')}
Method: {endpoint_info.get('method', 'N/A')}
Summary: {endpoint_info.get('summary', 'N/A')}
Description: {endpoint_info.get('description', 'N/A')}

Parameters:
{self._format_parameters(endpoint_info.get('parameters', []))}

Request Body Schema:
{json.dumps(endpoint_info.get('requestBodySchema', {}), indent=2)}

Required Fields:
{', '.join(endpoint_info.get('requiredFields', []))}

REQUIREMENTS:
1. Generate {num_valid_cases} VALID test cases (correct inputs, expected success)
2. Generate {num_invalid_cases} INVALID test cases (incorrect inputs, expected failures)
3. Include edge cases and boundary conditions
4. Each test case must be properly formatted JSON
5. Output MUST be valid JSON with structure: {{"testCases": [...]}}

For each test case, include:
- testId: Unique identifier
- endpoint: API endpoint path
- method: HTTP method
- category: "VALID" or "INVALID"
- description: Clear description of what's being tested
- priority: "HIGH", "MEDIUM", or "LOW"
- requestHeaders: HTTP headers
- requestBody: Request payload (if applicable)
- expectedStatusCode: Expected HTTP status code
- expectedResponseFields: Expected fields in response
- assertions: List of assertions to validate

Generate the test cases now in valid JSON format:
"""
        return prompt
    
    def _format_parameters(self, parameters: List[Dict[str, Any]]) -> str:
        """Format parameters for prompt"""
        if not parameters:
            return "None"
        
        formatted = []
        for param in parameters:
            formatted.append(
                f"- {param.get('name')}: "
                f"{param.get('dataType', 'unknown')} "
                f"(required={param.get('required', False)})"
            )
        
        return "\n".join(formatted)
