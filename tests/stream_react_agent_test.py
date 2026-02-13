import traceback

from agents.stream_react_agent import StreamReActAgent

def chat_loop(self):
    """运行循环对话"""
    while True:
        try:
            # 获取用户的输入
            query = input("Query: ").strip()
            if query.lower() == "quit":
                break
            self.process_query(query)
        except Exception as e:
            print(traceback.format_exc())
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

    chat_loop(StreamReActAgent())
