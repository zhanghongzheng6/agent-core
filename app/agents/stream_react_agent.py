import json
from openai import OpenAI
from pydantic import BaseModel, Field
from openai.types.chat.chat_completion_chunk import ChoiceDeltaToolCall

class Calculator(BaseModel):
    """一个简单的计算器"""
    expression: str = Field(..., description="数学表达式")

    @classmethod
    def calculate(cls, expression: str):
        try:
            result = eval(expression)
            return json.dumps({"result": result})
        except Exception as e:
            return json.dumps({"error": f"无效表达式, 错误信息: {str(e)}"})




class StreamReActAgent:
    def __init__(self):
        self.client = OpenAI()
        self.messages = [
            {
                "role": "system",
                "content": """你是一个擅长逻辑推理的AI助手。
对于用户提出的任何需要解决的问题，你必须严格遵循以下格式进行回答：

1. 在`<think>`标签内，详细展示你的思考过程，将问题分解为多个步骤，并逐步进行推理和演算。
2. 在`<answer>`标签内，仅提供最终的、明确的答案。

确保你的回答不包含`<think>`和`<answer>`标签之外的任何多余文字。"""
            }
        ]
        self.model = "gpt-3.5-turbo"
        self.available_tools = {Calculator.calculate.__name__: Calculator.calculate}
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": Calculator.calculate.__name__,
                    "description": Calculator.__doc__,
                    "parameters": Calculator.model_json_schema(),
                }
            }
        ]

    def process_query(self, query: str) -> None:
        # 将用户传递的数据添加到消息列表中
        self.messages.append({"role": "user", "content": query})
        print("Assistant: ", end="", flush=True)

        # 调用deepseek发起请求
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            stream=True,
        )

        # 设置变量判断是否执行工具调用、组装content、组装tool_calls
        is_tool_calls = False
        content = ""
        tool_calls_obj: dict[str, ChoiceDeltaToolCall] = {}

        for chunk in response:
            # 叠加内容和工具调用
            chunk_content = chunk.choices[0].delta.content
            chunk_tool_calls = chunk.choices[0].delta.tool_calls

            if chunk_content:
                content += chunk_content
            if chunk_tool_calls:
                for chunk_tool_call in chunk_tool_calls:
                    if tool_calls_obj.get(chunk_tool_call.index) is None:
                        tool_calls_obj[chunk_tool_call.index] = chunk_tool_call
                    else:
                        tool_calls_obj[chunk_tool_call.index].function.arguments += chunk_tool_call.function.arguments

            # 如果是直接生成则流式打印输出的内容
            if chunk_content:
                print(chunk_content, end="", flush=True)

            # 如果还未区分出生成的内容是答案还是工具调用，则循环判断
            if is_tool_calls is False:
                if chunk_tool_calls:
                    is_tool_calls = True

        # 如果是工具调用，则需要将tool_calls_obj转换成列表
        tool_calls_json = [tool_call for tool_call in tool_calls_obj.values()]

        # 将模型第一次回复的内容添加到历史消息中
        self.messages.append({
            "role": "assistant",
            "content": content if content != "" else None,
            "tool_calls": tool_calls_json if tool_calls_json else None,
        })

        if is_tool_calls:
            # 循环调用对应的工具
            for tool_call in tool_calls_json:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                print("\nTool Call: ", tool_name)
                print("Tool Parameters: ", tool_args)
                function_to_call = self.available_tools[tool_name]

                # 调用工具
                result = function_to_call(**tool_args)
                print(f"Tool [{tool_name}] Result: {result}")

                # 将工具结果添加到历史消息中
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_name,
                    "content": result,
                })

            # 再次调用模型，让它基于工具调用的结果生成最终回复内容
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="none",
                stream=True,
            )
            print("Assistant: ", end="", flush=True)
            for chunk in second_response:
                print(chunk.choices[0].delta.content, end="", flush=True)

        print("\n")



