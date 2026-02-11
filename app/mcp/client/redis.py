import os
from dataclasses import dataclass
from langchain_mcp_adapters.client import MultiServerMCPClient


@dataclass(frozen=True)
class RedisMCPConfig:
    redis_url: str
    # 你已经把 redis-mcp-server 加到依赖里，所以用 uv run 最稳
    uv_command: str = "uv"
    server_cmd: str = "redis-mcp-server"
    transport: str = "stdio"


def build_redis_mcp_client(config: RedisMCPConfig) -> MultiServerMCPClient:
    """
    只负责构建 MultiServerMCPClient（不做 await）。
    """
    return MultiServerMCPClient(
        {
            "redis": {
                "transport": config.transport,
                "command": config.uv_command,
                "args": ["run", config.server_cmd, "--url", config.redis_url],
            }
        }
    )


def load_redis_config_from_env(env_key: str = "REDIS_URL") -> RedisMCPConfig:
    redis_url = os.getenv(env_key)
    if not redis_url:
        raise RuntimeError(f"Missing env var: {env_key}")
    return RedisMCPConfig(redis_url=redis_url)
