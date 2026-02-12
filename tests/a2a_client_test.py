import httpx
from a2a.client import ClientConfig, ClientFactory
from a2a.client.helpers import create_text_message_object

from a2a.types import TransportProtocol, Role


async def main() -> None:
    # 1.定义a2a基础url地址
    base_url = "http://localhost:8888"

    # 2.创建一个httpx客户端上下文
    async with httpx.AsyncClient(timeout=600) as httpx_client:
        config = ClientConfig(
            httpx_client=httpx_client,
            supported_transports=[
                TransportProtocol.jsonrpc,
                TransportProtocol.http_json,
            ],
        )
        client = await ClientFactory.connect(base_url, client_config=config)

        card = await client.get_card()
        print(card.model_dump(mode="json", exclude_none=True))


        msg = create_text_message_object(content="帮我看下北京今天的天气情况", role=Role.user)
        async for ev in client.send_message(msg):
            print(ev.model_dump(mode="json", exclude_none=True))



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
