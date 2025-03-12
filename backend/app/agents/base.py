from langchain_core.language_models import BaseLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

class DebateAgent:
    def __init__(
        self,
        name: str,
        llm: BaseLLM,
        system_prompt: str
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
    
    async def process(
        self,
        state: Dict[str, Any],
        context: Dict[str, Any] = None
    )-> Dict[str,Any]:
        raise NotImplementedError