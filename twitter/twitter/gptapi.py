from openai import OpenAI
from twitter.settings import OPENAI_API_KEY

class GPTAPI:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY,
                            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
                            )
    def get_cn_response(self, prompt):
        completion = self.client.chat.completions.create(
        model="qwen-plus",
        extra_body={"enable_search": True},
        messages=[{'role': 'system', 'content': "You're a crypto enthusiast and like to respond to other people's tweets in one sentence and in a positive way and in a positive way"},
                  {'role': 'user', 'content': prompt}]
        )
        return completion.model_dump_json()
    def get_en_response(self, prompt):
        completion = self.client.chat.completions.create(
        model="qwen-plus",
        messages=[{'role': 'system', 'content': "You're a crypto enthusiast and like to respond to other people's tweets in one sentence and in a positive way, in English"},
                  {'role': 'user', 'content': prompt}]
        )
        return completion.model_dump_json()
    
    def get_random_content(self):
        completion = self.client.chat.completions.create(
        model="qwen-plus",
        messages=[{'role': 'system', 'content': "You're a crypto enthusiast"},
                  {'role': 'user', 'content': "Please tell me about a random crypto event, less than 50 waords"}]
        )
        return completion.model_dump_json()