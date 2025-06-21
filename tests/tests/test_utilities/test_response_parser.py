import pytest
from unittest.mock import MagicMock
from typing import Dict, Any
from utils.utils.response_parser import ResponseParser, ParsedResponse

# --- Mock Response Fixtures ---

@pytest.fixture
def sample_openai_response() -> MagicMock:
    """Provides a mock OpenAI API response object."""
    return MagicMock(
        choices=[MagicMock(
            message=MagicMock(content="  This is a test response from OpenAI  ```code```"),
            finish_reason="stop"
        )],
        usage=MagicMock(_asdict=lambda: {"prompt_tokens": 10, "completion_tokens": 20}),
        model="gpt-3.5-turbo"
    )

@pytest.fixture
def sample_anthropic_response() -> MagicMock:
    """Provides a mock Anthropic API response object."""
    return MagicMock(
        content=[MagicMock(text="  This is a test response from Anthropic  ")],
        stop_reason="end_turn",
        usage=MagicMock(input_tokens=10, output_tokens=20),
        model="claude-2"
    )

@pytest.fixture
def sample_local_dict_response() -> Dict[str, Any]:
    """Provides a mock local model response as a dictionary."""
    return {
        "response": "This is a test response from a local model",
        "model": "llama2",
        "total_duration": 1.5,
        "load_duration": 0.5
    }

# --- Tests for Utility Functions ---

@pytest.mark.parametrize("input_text, expected_cleaned_text", [
    ("  This   is  a  test  ", "This is a test"),
    ("```json\n{\"key\": \"value\"}\n```", 'json {"key": "value"}'),
    ("\n\t  Leading and trailing whitespace\t\n  ", "Leading and trailing whitespace"),
    ("No extra whitespace", "No extra whitespace"),
])
def test_clean_text(input_text: str, expected_cleaned_text: str):
    """Tests the clean_text function with various inputs."""
    cleaned = ResponseParser.clean_text(input_text)
    assert cleaned == expected_cleaned_text, "Text cleaning did not produce the expected output."

@pytest.mark.parametrize("input_text, expected_json", [
    ('Some text before {"key": "value"} some text after', {"key": "value"}),
    ('{"nested": {"a": 1}}', {"nested": {"a": 1}}),
    ('No json here', None),
    ('Malformed {json: "here"}', None),
])
def test_extract_json(input_text: str, expected_json: Any):
    """Tests JSON extraction from text, including positive and negative cases."""
    json_data = ResponseParser.extract_json(input_text)
    assert json_data == expected_json, "JSON extraction did not produce the expected output."

# --- Tests for Provider-Specific Parsers ---

def test_parse_openai(sample_openai_response: MagicMock):
    """Tests that a valid OpenAI response is parsed correctly."""
    parsed = ResponseParser.parse_openai(sample_openai_response)
    
    assert isinstance(parsed, ParsedResponse)
    assert parsed.text == "This is a test response from OpenAI code"
    assert parsed.provider == "openai"
    assert parsed.model == "gpt-3.5-turbo"
    assert parsed.metadata["finish_reason"] == "stop"
    assert "usage" in parsed.metadata
    assert parsed.metadata["usage"]["prompt_tokens"] == 10
