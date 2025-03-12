from .base import DebateAgent
from ..core.config import settings
from openai import AsyncOpenAI
from typing import Dict,Any

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class ProponentAgent(DebateAgent):
    def __init__(self):
        system_prompt = """You are a professional debater arguing in FAVOR of the motion. 
        Your strategies:
        1. Use logical reasoning with factual evidence
        2. Anticipate counterarguments
        3. Maintain respectful tone
        4. Keep responses under 150 words"""
        
        super().__init__(
            name="Proponent",
            llm=None,  # Override base LLM
            system_prompt=system_prompt
        )

    async def process(self, state: Dict[str, Any], context: dict = None) -> dict:
        try:
            motion = state["motion"]
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"MOTION: {motion}\nLast opponent argument: {state['opponent_arguments'][-1] if state['opponent_arguments'] else 'None'}"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return {
                "role": "proponent",
                "content": response.choices[0].message.content,
                "round": state["current_round"]
            }

        except Exception as e:
            return {
                "role": "system",
                "content": f"Proponent error: {str(e)}",
                "round": state["current_round"]
            }