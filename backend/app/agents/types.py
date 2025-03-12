from typing import Dict, List, TypedDict, Annotated
from enum import Enum

class DebateState(TypedDict):
    motion:str
    current_round:int
    max_rounds:int
    proponent_arguments:List[str]
    moderator_arguments:List[str]
    opponent_arguments:List[str]
    fact_checks:Dict[str,bool]

class Role(str, Enum):
    MODERATOR = "moderator"
    PROPONENT = "proponent"
    OPPONENT = "opponent"   
    FACT_CHECKER = "fact_checker"

class Message(TypedDict):
    role:Role
    content:str
    round:int
    timestamp:float