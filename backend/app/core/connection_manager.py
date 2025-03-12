from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.debate_state = {}
        self.votes = {"proponent": 0, "opponent": 0}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def start_debate(self, motion: str):
        debate_manager = DebateManager()
        initial_state = await debate_manager.initialize_debate(motion)
        self.debate_state = initial_state
        
        await self.broadcast({
            "type": "status",
            "content": "Debate initialized",
            "state": initial_state
        })
        
        while self.debate_state["current_round"] < self.debate_state["max_rounds"]:
            new_state = await debate_manager.run_debate_round(self.debate_state)
            await self.broadcast({
                "type": "argument",
                "role": new_state["last_role"],
                "content": new_state["last_argument"],
                "round": new_state["current_round"]
            })
            
            await self.broadcast({
                "type": "fact_check",
                "content": new_state["fact_checks"]
            })
            
            self.debate_state = new_state
    
    async def handle_vote(self, vote: str):
        if vote in self.votes:
            self.votes[vote] += 1
            await self.broadcast({
                "type": "vote_update",
                "content": self.votes
            })
