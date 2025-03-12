from ..agents.proponent import ProponentAgent
from ..agents.opponent import OpponentAgent
from ..agents.fact_checker import FactCheckerAgent
from typing import Dict, Any
from ..agents.types import DebateState 
import logging
logger = logging.getLogger(__name__)

class DebateManager:
    def __init__(self):
        self.proponent = ProponentAgent()
        self.fact_checker = FactCheckerAgent()
        self.opponent = OpponentAgent()
        self.workflow = self._create_workflow()
    

    def initialize_fact_checker(self):
        initial_data = [
            "Artificial intelligence is being used in healthcare diagnostics",
            "AI systems can exhibit bias based on training data",
            "Machine learning requires large datasets for training"
        ]
        self.fact_checker.add_context(initial_data)

    async def process_argument(self, argument: str):
        return await self.fact_checker.process(argument)

    def _create_workflow(self):
        async def proponent_step(state):
            return await self.proponent.process(state)
        
        async def opponent_step(state):
            return await self.opponent.process(state)
        
        async def fact_checker_step(state):
            return await self.fact_checker.process(state)
        
        workflow = StateGraph(DebateState)
        workflow.add_node("proponent", proponent_step)
        workflow.add_node("opponent", opponent_step)
        workflow.add_node("fact_checker", fact_checker_step)
        workflow.set_entry_point("proponent")
        workflow.add_edge("proponent", "fact_checker")
        workflow.add_edge("opponent", "fact_checker")
        workflow.add_edge("fact_checker", "proponent")  #i thought about looping to prop
        return workflow.compile()

    async def run_fact_check(self, claim: str):
        return await self.fact_checker.process(claim)
    
    async def run_debate_round(self, state: DebateState) -> DebateState:
        async def run_debate_round(self, state: DebateState) -> DebateState:
            logger.info(f"Starting debate round {state['current_round']}")
            try:
                new_state = await self.workflow.invoke(state)
                logger.debug(f"New state: {new_state}")
                return new_state
            except Exception as e:
                logger.error(f"Debate round failed: {str(e)}")
                raise