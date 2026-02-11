# langchain_client_weather.py
import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()  # 自动读取 .env
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    # 连接一个 HTTP MCP server（streamable-http）
    client = MultiServerMCPClient(
        {
            "mysql": {
                "transport": "stdio",
                "command": sys.executable,
                "args": ["-m", "mcp_mysql_connect", os.getenv("MYSQL_DB_URL")],
            }
        }
    )

    tools = await client.get_tools()
    print("=== Tools loaded ===")
    for t in tools:
        print(f"- tools: {t}")
        print(f"- name: {t.name}")
        print(f"  description: {t.description}")

        print()



if __name__ == "__main__":
    asyncio.run(main())
