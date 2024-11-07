import operator
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict, Annotated
from typing import Sequence, Any, Final

MODELS : Final = {
    "Google": ["gemma-7b-it", "gemma2-9b-it"],
    "Meta": [
            "llama3-8b-8192",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama-3.1-70b-versatile",
    ],
    "Mistral": [
            "mixtral-8x7b-32768",
    ],
}


DEFAULT_MODEL_NAME = 'llama3-70b-8192'
DEFAULT_TEMPARATURE = 0.3
DEFAULT_MAX_TOKENS = 5000

class WorkFlowState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    consumer: Any
    
MAIN_SYSTEM_PROMPT = """
    You are Bujji, an advanced helful assistant developed by Madhu. 
"""