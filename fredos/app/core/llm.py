"""LLM Client Factory — Phase 8 Track B."""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_llm_client() -> OpenAI:
    """Returns a configured OpenAI client.
    
    If OPENAI_BASE_URL is set, it overrides the default endpoint (e.g., for local Ollama).
    """
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY", "ollama")
    
    if base_url:
        return OpenAI(base_url=base_url, api_key=api_key)
    else:
        return OpenAI(api_key=api_key)

def get_default_model() -> str:
    return os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
