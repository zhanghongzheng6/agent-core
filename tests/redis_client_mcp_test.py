import asyncio

from dotenv import load_dotenv

from agents.react_agent import build_react_agent
from app.mcp.client.redis import load_redis_config_from_env
from app.mcp.factory import create_redis_client_and_tools
from llm.openai import OpenAIConfig, build_openai_llm


def pretty_print_tools(tools):
    print("=== Tools loaded ===")
    for t in tools:
        print(f"- name: {t.name}")
        print(f"  description: {t.description}\n")

async def create_redis_client_mcp():
    cfg = load_redis_config_from_env("REDIS_URL")
    client, tools = await create_redis_client_and_tools(cfg)
    pretty_print_tools(tools)

    llm = build_openai_llm(OpenAIConfig())
    agent = build_react_agent(llm, tools)

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "帮我将 key=foo  value 设置成 tttt  "}]}
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
    load_dotenv()
    asyncio.run(create_redis_client_mcp())



