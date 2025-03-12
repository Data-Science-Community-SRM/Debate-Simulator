from .base import DebateAgent
from .types import Role,DebateState
import time

class ModeratorAgent(DebateAgent):
    def __init__(self,llm):
        super().__init__(
            name="Moderator",
            llm=llm
            system_prompt="""You are a professional debate moderator. Your role is to:
            1. Introduce the debate topic
            2. Ensure each speaker stays on topic
            3. Maintain civil discourse
            4. Summarize key points
            5. Enforce time limits
            
            Be firm but fair, and ensure the debate remains focused and productive."""
        )

        async def process(self,state:DebateState,context:dict=None)->dict:
            if state["current_round"]==0:
                return {
                    "role":Role.MODERATOR,
                    "content": self._generate_introduction(state["motion"]),
                    "round": 0,
                    "timestamp": time.time()
            }
            return await self._moderate_debate(state)
        
        def _generate_introduction(self,motion:str)->str:
            template=ChatPromptTemplate.from_messages([
                ("system",self.system_prompt),
                ("user",f"Generate a formal introduction for a debate on the motion:'{motion}")

            ])
            response=self.llm.invoke(template)
            return response.content
        
        async def _moderate_debate(self,state:DebateState)->dict:
            pass
            
        