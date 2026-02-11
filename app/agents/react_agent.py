from typing import List
from langchain_core.tools import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.agents import create_agent


def build_react_agent(llm: BaseChatModel, tools: List[BaseTool]):
    return create_agent(llm, tools)
