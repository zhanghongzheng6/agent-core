import os

from openai import OpenAI
from pydantic import BaseModel, Field, EmailStr

class UserInfo(BaseModel):
    """传递用户的信息进行数据提取&处理，涵盖name、age、email"""
    name: str = Field(..., description="用户名字")
    age: int = Field(..., gt=0, description="用户年龄，必须是正整数")
    phone: str = Field(..., description="用户手机")
    email: EmailStr = Field(..., description="用户的电子邮件")



def completions_create():

    client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"),
                    api_key=os.getenv("OPENAI_API_KEY"),)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "我叫hongzheng，今年30岁，我的联系方式是+8613261643812  hz_test@133.com"}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": UserInfo.__name__,
                    "description": UserInfo.__doc__,
                    "parameters": UserInfo.model_json_schema(),
                }
            }
        ],
        tool_choice={"type": "function", "function": {"name": UserInfo.__name__}}
    )

    user_info = UserInfo.model_validate_json(response.choices[0].message.tool_calls[0].function.arguments)
    print(user_info)


if __name__ == "__main__":
    import dotenv
    # 加载环境变量
    dotenv.load_dotenv()
    completions_create()
