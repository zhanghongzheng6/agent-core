# 如果没有openAPi key 可以使用下面的代理 使用gpt-3.5-turbo 非常便宜
[代理网站](https://api.laozhang.ai/register/?aff_code=lSea)

# mcp server 示例
## [server_http.py](app/mcp/server/server_http_weather.py) 

# 使用langchain的 mcp client 示例
## [langchain_client.py](app/mcp/client/langchain_client_weather.py)

# 使用langchain的 直接集成了高德mcp api 
## [langchain_client_amap.py](app/mcp/client/langchain_client_amap.py)

# 使用 mysql mcp 示例
## [langchain_client_mysql.py](app/mcp/client/langchain_client_mysql.py)

# 使用 redis mcp 示例
## [redis_client_mcp_test.py](tests/redis_client_mcp_test.py)

# 简单的聊天机器人 示例
## [简单聊天机器人](tests/react_agent_chat_test.py)

# 对外如何发布a2a 卡片,供其他agent调用示例 
## run [a2a_agent_card_test.py](tests/a2a_agent_card_test.py) 后 在游览器访问 http://127.0.0.1:8888/.well-known/agent-card.json
## 使用 [a2a_client_test.py](tests/a2a_client_test.py) 进行连接 agent card 测试
