from base_app.consonants import MAIN_SYSTEM_PROMPT, DEFAULT_MODEL_NAME, DEFAULT_TEMPARATURE, DEFAULT_MAX_TOKENS
from base_app.consumers import BaseChatAsyncJsonWebsocketConsumer
from base_app.decorators import consumer_method_exception_handler
from .ai_chats import GPTSource
from .models import Chat
from .serializers import GPTResponseSerializer
from channels.db import database_sync_to_async
import asyncio


class ChatConsumer(BaseChatAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect() and await self.chat_connect():
            config = await self.get_llm_config()
            system_prompt = self.gpt.system_prompt if self.gpt else MAIN_SYSTEM_PROMPT
            self.gpt_source = GPTSource(config, str(self.user.id), str(self.chat.id), system_prompt)
    
    async def send_source_status(self, source:str):
        await self.send_json({
            'type': 'source_status',
            'source': source
        })
        await asyncio.sleep(0.1)
        
    async def get_llm_config(self):
        # if not hasattr(self, 'content'):
        #     self.content = {
        #         'llm_config': {
        #             'model': DEFAULT_MODEL_NAME,
        #             'temperature': DEFAULT_TEMPARATURE,
        #             'max_tokens': DEFAULT_MAX_TOKENS
        #         }
        #     }
        # llm_config = self.content.get('llm_config')
        # model = llm_config.get('model') or DEFAULT_MODEL_NAME
        # temperature = llm_config.get('temperature') or DEFAULT_TEMPARATURE
        # max_tokens = llm_config.get('max_tokens') or DEFAULT_MAX_TOKENS
        return {
            'model': DEFAULT_MODEL_NAME,
            'temperature': DEFAULT_TEMPARATURE,
            'max_tokens': DEFAULT_MAX_TOKENS
        }
        # return {
        #     'model': model,
        #     'temperature': temperature,
        #     'max_tokens': max_tokens
        # }

    # @consumer_method_exception_handler
    async def receive_json(self, content, **kwargs):
        self.content = content
        prompt = content.get('prompt')
        self.prompt = self.chat.first_prompt if prompt is None or prompt == '' else prompt
        await self.generate_response()
    
    async def generate_response(self):
        await asyncio.sleep(0.5)
        gpt_response : str = self.gpt_source.get_response(prompt=self.prompt)            
        await self.save_and_send_response(gpt_response)
    
    @database_sync_to_async
    def save_response(self, gpt_response_data):
        gpt_response_serializer = GPTResponseSerializer(data=gpt_response_data)
        gpt_response_serializer.is_valid(raise_exception=True)
        gpt_response_serializer.save()
        return gpt_response_serializer.data
    
    async def prepare_gpt_response_data(self, gpt_response):
        response = {
            "user": self.user.id,
            "chat": self.chat.id,
            "prompt": self.prompt,
            "response": gpt_response.content,
            "llm_config": await self.get_llm_config(),
            "token_usage" : gpt_response.usage_metadata
        }
        return response 
            
    async def send_response(self, response):
        response['id'] = str(response['id'])
        response['user'] = str(response['user'])
        response['chat'] = str(response['chat'])

        await self.send_json(response)
    
    async def save_and_send_response(self, gpt_response):
        gpt_response_data = await self.prepare_gpt_response_data(gpt_response)
        response = await self.save_response(gpt_response_data)
        await self.send_response(response)

    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        

        
      
        
{
  "Content": "Namaste! I am Bujji, a highly advanced and helpful assistant developed by the brilliant Madhu. I'm a cutting-edge language model designed to provide top-notch assistance, answer questions, and engage in conversations with users like you. My primary goal is to make your life easier, more efficient, and enjoyable.\n\nWith my advanced capabilities, I can help with a wide range of tasks, such as:\n\n1. Answering questions on various topics, from science and history to entertainment and culture.\n2. Generating ideas, suggestions, and solutions for your problems or projects.\n3. Assisting with language-related tasks, like language translation, grammar correction, and text summarization.\n4. Providing information on the latest news, trends, and updates from around the world.\n5. Offering helpful tips, advice, and guidance on various aspects of life, including health, wellness, and personal growth.\n\nI'm constantly learning and improving, so please bear with me if I make any mistakes. My purpose is to serve, assist, and provide value to you, and I'm committed to doing so with a smile and a helpful attitude!\n\nSo, how can I assist you today? ...",
  "additional_kwargs": {},
  "response_metadata": {
    "token_usage": {
      "completion_tokens": 236,
      "prompt_tokens": 37,
      "total_tokens": 273,
      "completion_time": 0.674285714,
      "prompt_time": 0.000495746,
      "queue_time": 0.043176423,
      "total_time": 0.67478146
    },
    "model_name": "llama3-70b-8192",
    "system_fingerprint": "fp_7ab5f7e105",
    "finish_reason": "stop",
    "logprobs": None
  },
  "id": "run-4df89746-484c-4eb1-8258-5bcf810e4fa3-0",
  "usage_metadata": {
    "input_tokens": 37,
    "output_tokens": 236,
    "total_tokens": 273
  }
}
