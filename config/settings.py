"""Configuration loader for Azure OpenAI settings."""
from __future__ import annotations
import os
from typing import Optional

class Settings:
    def __init__(self) -> None:
        self.azure_openai_endpoint: Optional[str] = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_deployment: Optional[str] = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
        self.azure_openai_api_key: Optional[str] = os.environ.get("AZURE_OPENAI_API_KEY")

    def validate(self) -> None:
        if not self.azure_openai_endpoint or not self.azure_openai_deployment:
            raise RuntimeError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT must be set")

def get_settings() -> Settings:
    return Settings()
