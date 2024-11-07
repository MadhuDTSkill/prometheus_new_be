from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from .ai_memory import Memory
import os
from langchain_core.chat_history import BaseChatMessageHistory

apikey = os.getenv('GROQ_API_KEY')


class GPTSource:
    def __init__(self, config:dict, user_id:str, chat_id:str, system_prompt) -> None:
        self.config = config
        self.llm = ChatGroq(api_key=apikey, **self.config)
        self.user_id = user_id
        self.chat_id = chat_id
        self.system_prompt = system_prompt
        self.qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", self.system_prompt),
                    # MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{prompt}"),
                ]
            )

        self.chain = self.qa_prompt | self.llm
        
    def get_response(self, prompt: str):
        input = {
            'prompt' : prompt, 
            }
        return self.chain.invoke(input)
        
