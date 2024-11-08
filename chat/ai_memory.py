from langchain_core.messages import trim_messages
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import os


class Memory:
    def __init__(self, chat_id : str, user_id:str,  max_tokens: int, token_counter, include_system: bool, allow_partial: bool, start_on: str):
        self.trim_messages = trim_messages(
            max_tokens=max_tokens,
            strategy='last',
            token_counter=token_counter,
            include_system=include_system,
            allow_partial=allow_partial,
            start_on=start_on
        )
        self.chat_id = chat_id
        self.user_id = user_id
        self.messages = self.get_trimmed_messages()
    
    def get_trimmed_messages(self):
        return self.trim_messages.invoke(self.sql_history_obj.messages)
        
    def add_user_message(self, message: str):
        self.sql_history_obj.add_user_message(message)
        self.messages = self.get_trimmed_messages()
    
    def add_ai_message(self, message: str):
        self.sql_history_obj.add_ai_message(message)
        self.messages = self.get_trimmed_messages()
        
    def add_messages(*args, **kwargs):
        pass
        
    @classmethod
    def get_memory(cls, session_id:str, user_id:str, max_tokens: int, token_counter, include_system: bool, allow_partial: bool, start_on: str) -> BaseChatMessageHistory:
        message_history = SQLChatMessageHistory(session_id=session_id, connection_string=os.getenv('MEMORY_DATABASE_URL'), table_name = user_id)
        message_history_trimmed = cls(message_history, max_tokens, token_counter, include_system, allow_partial, start_on) if len(message_history.messages) > 0 else message_history
        return message_history_trimmed