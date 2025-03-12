from langgraph.graph import Graph, StateGraph
from typing import Dict, Any
from ..agents.types import Role, DebateState

def create_debate_workflow(
    moderator_agent,
    proponent_agent,
    opponent_agent,
    fact_checker_agent
) -> Graph:
    workflow = StateGraph(DebateState)

    workflow.add_node("moderator", moderator_agent.process)
    workflow.add_node("proponent", proponent_agent.process)
    workflow.add_node("opponent", opponent_agent.process)
    workflow.add_node("fact_checker", fact_checker_agent.process)
        
    workflow.add_edge("moderator", "proponent")
    workflow.add_edge("proponent", "fact_checker")
    workflow.add_edge("fact_checker", "opponent")
    workflow.add_edge("opponent", "fact_checker")
    workflow.add_edge("fact_checker", "moderator")
    
    #entry to this
    workflow.set_entry_point("moderator")
    
    return workflow.compile()