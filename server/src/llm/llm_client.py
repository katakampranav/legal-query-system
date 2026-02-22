"""LLM client for Groq API."""

import logging
from typing import Optional

from groq import Groq

from src.app.config import api_settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Groq LLM client wrapper."""

    def __init__(self) -> None:
        """Initialize LLM client."""
        self.client = Groq(api_key=api_settings.groq_api_key)
        self.model = api_settings.groq_model
        self.temperature = api_settings.llm_temperature

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Generate text using LLM.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override

        Returns:
            Generated text response
        """
        try:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_completion_tokens=8192,
            )

            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            raise

    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ):
        """Generate text using LLM with streaming.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override

        Yields:
            Streamed content chunks
        """
        try:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": prompt})

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_completion_tokens=8192,
                stream=True,
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"LLM streaming error: {e}")
            raise


# Singleton instance
llm_client = LLMClient()
