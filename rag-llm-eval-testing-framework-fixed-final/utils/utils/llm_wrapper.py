import os
from typing import Any, Optional
from openai import OpenAI
from anthropic import Anthropic
from .retry import retry_with_exponential_backoff

class LLMWrapper:
    """A wrapper for various LLM provider APIs."""

    def __init__(self, provider: str, api_key: Optional[str] = None):
        self.provider = provider.lower()
        api_key = api_key or os.getenv(f"{self.provider.upper()}_API_KEY")

        if not api_key:
            raise ValueError(f"API key for provider '{self.provider}' not found.")

        if self.provider == 'openai':
            self.client = OpenAI(api_key=api_key)
        elif self.provider == 'anthropic':
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    @retry_with_exponential_backoff
    def get_completion(self, prompt: str, model: str, **kwargs) -> Any:
        if self.provider == 'openai':
            return self._get_openai_completion(prompt, model, **kwargs)
        elif self.provider == 'anthropic':
            return self._get_anthropic_completion(prompt, model, **kwargs)
        raise NotImplementedError(f"Completion logic not implemented for provider: {self.provider}")

    def _get_openai_completion(self, prompt: str, model: str, **kwargs) -> Any:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
        return response

    def _get_anthropic_completion(self, prompt: str, model: str, **kwargs) -> Any:
        max_tokens = kwargs.pop("max_tokens", 1024)
        response = self.client.messages.create(model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}], **kwargs)
        return response