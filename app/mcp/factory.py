from typing import List, Tuple
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.mcp.client.redis import RedisMCPConfig, build_redis_mcp_client


async def create_redis_client_and_tools(
        config: RedisMCPConfig,
) -> Tuple[MultiServerMCPClient, List[BaseTool]]:
    """
    返回 (client, tools)，调用方拿到 tools 就可以喂给 agent。
    """
    client = build_redis_mcp_client(config)
    tools = await client.get_tools()
    return client, tools
