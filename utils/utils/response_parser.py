import json
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ParsedResponse:
    text: str
    raw_response: Any
    metadata: Dict[str, Any]
    provider: str
    model: str

class ResponseParser:
    """Parser for different LLM response formats."""
    @staticmethod
    def clean_text(text: str) -> str:
        text = " ".join(text.split())
        text = text.replace("```", "")
        return text.strip()

    @staticmethod
    def extract_json(text: str) -> Optional[Dict]:
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from response")
        return None

    @staticmethod
    def parse_openai(response: Any) -> ParsedResponse:
        try:
            text = response.choices[0].message.content
            metadata = {"finish_reason": response.choices[0].finish_reason, "usage": response.usage._asdict() if hasattr(response, "usage") else {}, "model": response.model}
            return ParsedResponse(text=ResponseParser.clean_text(text), raw_response=response, metadata=metadata, provider="openai", model=response.model)
        except Exception as e:
            logger.error(f"Error parsing OpenAI response: {str(e)}")
            raise

    @staticmethod
    def parse_anthropic(response: Any) -> ParsedResponse:
        try:
            text = response.content[0].text
            metadata = {"stop_reason": response.stop_reason, "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}, "model": response.model}
            return ParsedResponse(text=ResponseParser.clean_text(text), raw_response=response, metadata=metadata, provider="anthropic", model=response.model)
        except Exception as e:
            logger.error(f"Error parsing Anthropic response: {str(e)}")
            raise

    @staticmethod
    def parse_local(response: Any) -> ParsedResponse:
        try:
            if isinstance(response, dict):
                text = response.get("response", "")
                metadata = {"model": response.get("model", "unknown"), "total_duration": response.get("total_duration", 0), "load_duration": response.get("load_duration", 0)}
            else:
                text = str(response)
                metadata = {"model": "unknown"}
            return ParsedResponse(text=ResponseParser.clean_text(text), raw_response=response, metadata=metadata, provider="local", model=metadata["model"])
        except Exception as e:
            logger.error(f"Error parsing local model response: {str(e)}")
            raise