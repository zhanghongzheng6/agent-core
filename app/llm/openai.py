import os
from dataclasses import dataclass
from langchain_openai import ChatOpenAI


@dataclass(frozen=True)
class OpenAIConfig:
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    api_key_env: str = "OPENAI_API_KEY"
    base_url_env: str = "OPENAI_BASE_URL"


def build_openai_llm(cfg: OpenAIConfig) -> ChatOpenAI:
    # ChatOpenAI 会自己从环境变量读 OPENAI_API_KEY
    if not os.getenv(cfg.api_key_env):
        raise RuntimeError(f"Missing env var: {cfg.api_key_env}")
    return ChatOpenAI(model=cfg.model,
                      temperature=cfg.temperature,
                      base_url=os.getenv(cfg.base_url_env)
                      )
