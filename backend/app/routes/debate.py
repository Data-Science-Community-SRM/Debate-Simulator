from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from ..agents import ProponentAgent, OpponentAgent
import logging
from ..core.debate_manager import DebateManager
from pydantic import BaseModel
from ..core.connection_manager import ConnectionManager

router=APIRouter()
manager=ConnectionManager()

class RoleRequest(BaseModel):
    role: str

@router.post("/test/generate")
async def test_generation(request: RoleRequest):
    role=request.role
    print(f"Role parameter received: {role}")
    test_state={"motion":"AI will benefit humanity","current_round":1,"proponent_arguments":[],"opponent_arguments":[]}
    if role=="proponent":
        print("Proponent agent invoked")
        agent=ProponentAgent()
        result=await agent.process(test_state)
    elif role=="opponent":
        print("Opponent agent invoked")
        agent=OpponentAgent()
        result=await agent.process(test_state)
    else:
        print(f"Invalid role provided: {role}")
        raise HTTPException(400,"Invalid role")
    return result

class FactCheckRequest(BaseModel):
    claim: str

@router.post("/test/fact_check")
async def test_fact_check(request: FactCheckRequest):
    debate_manager=DebateManager()
    result=await debate_manager.run_fact_check(request.claim)
    return result

@router.websocket("/live")
async def debate_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    debate_state={}
    try:
        while True:
            data=await websocket.receive_json()
            logging.info(f"Received data: {data}")
            if data["type"]=="start_debate":
                motion=data["motion"]
                logging.info(f"Starting debate with motion: {motion}")
                debate_state={"motion":motion,"current_round":1,"proponent_arguments":[],"opponent_arguments":[]}
                await process_debate_round(websocket,debate_state)
            elif data["type"]=="next_round":
                debate_state["current_round"]=data["round"]
                await process_debate_round(websocket,debate_state)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logging.info(f"Client disconnected")
    except Exception as e:
        logging.error(f"Error in websocket handler: {str(e)}")
        manager.disconnect(websocket)

async def process_debate_round(websocket: WebSocket, debate_state: dict):
    try:
        proponent_agent=ProponentAgent()
        proponent_response=await proponent_agent.process(debate_state)
        logging.info(f"Proponent response: {proponent_response}")
        await websocket.send_json({"type":"argument","role":"proponent","content":proponent_response.get("content","No response generated"),"round":debate_state["current_round"]})
        debate_state["proponent_arguments"].append(proponent_response.get("content",""))
        opponent_agent=OpponentAgent()
        opponent_response=await opponent_agent.process(debate_state)
        logging.info(f"Opponent response: {opponent_response}")
        await websocket.send_json({"type":"argument","role":"opponent","content":opponent_response.get("content","No response generated"),"round":debate_state["current_round"]})
        debate_state["opponent_arguments"].append(opponent_response.get("content",""))
    except Exception as e:
        logging.error(f"Error processing debate turn: {str(e)}")
        await websocket.send_json({"type":"error","content":"Failed to generate debate response"})