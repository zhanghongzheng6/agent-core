# langchain_client_weather.py
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()  # 自动读取 .env
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent


async def main():
    # 连接一个 HTTP MCP server（streamable-http）
    client = MultiServerMCPClient(
        {
            "amap": {
                "transport": "http",
                "url": "https://mcp.amap.com/mcp?key="+os.getenv("AMAP_API_KEY"),
            },
        }
    )

    tools = await client.get_tools()
    print("=== Tools loaded ===")
    for t in tools:
        print(f"- name: {t.name}")
        print(f"  description: {t.description}")

        print()

    #这里的模型字符串按你自己的 LangChain 配置来（OpenAI/Anthropic 等）
    agent = create_agent(
        model="openai:gpt-3.5-turbo",
        tools=tools,
    )

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "帮我随便获取 一个美国地区的天气预警"}]}
    )
    print("=== raw result ===")
    print(result)
    print(type(result))

    if isinstance(result, dict):
        print("\n=== messages ===")
        for m in result.get("messages", []):
            print(m)

        print("\n=== output ===")
        print(result.get("output"))

if __name__ == "__main__":
    asyncio.run(main())
