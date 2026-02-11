import asyncio
import os

from agents.re_act_agent import ReActAgent


async def main():
    # 构建agent
    agent = ReActAgent()

    try:
        # 连接高德mcp服务
        await agent.connect_to_streamable_http_server(
            url=f"https://mcp.amap.com/mcp?key={os.getenv('AMAP_API_KEY')}",
            headers={}
        )

        # 循环对话
        await agent.chat_loop()
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    import dotenv
    # 加载环境变量
    dotenv.load_dotenv()
    asyncio.run(main())
