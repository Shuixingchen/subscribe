from openai import OpenAI
from twitter.settings import OPENAI_API_KEY
import json

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
        return self.parser_response(completion.model_dump_json())
    def get_en_response(self, prompt):
        completion = self.client.chat.completions.create(
        model="qwen-plus",
        extra_body={"enable_search": True},
        messages=[{'role': 'system', 'content': "You're a crypto enthusiast and like to respond to other people's tweets in one sentence and in a positive way, in English"},
                  {'role': 'user', 'content': prompt}]
        )
        return self.parser_response(completion.model_dump_json())
    
    def get_random_content(self):
        completion = self.client.chat.completions.create(
        model="qwen-plus",
        max_tokens=50,
        extra_body={"enable_search": True},
        messages=[{'role': 'system', 'content': "You're a crypto enthusiast"},
                  {'role': 'user', 'content': "Please tell me a random one sentence, must less than 50 words"}]
        )
        return self.parser_response(completion.model_dump_json())
    
    def parser_response(self, response:str):
        data = json.loads(response)
        message = data['choices'][0]['message']['content']
        if len(message) > 159:
            message = message[:159]
        
        return self.remove_non_bmp_characters(message)
    
    def remove_non_bmp_characters(text):
        # 移除非BMP字符
        return ''.join(char for char in text if ord(char) < 65536)