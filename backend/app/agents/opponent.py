# backend/app/agents/opponent.py
from llama_cpp import Llama
from .base import DebateAgent
from ..core.config import settings
import os
from typing import Dict, Any

class OpponentAgent(DebateAgent):
    def __init__(self):
        system_prompt = """You are a professional debater arguing AGAINST the motion.
        Your strategies:
        1. Find logical flaws in opponent's arguments
        2. Use counterexamples and statistics
        3. Maintain academic tone
        4. Keep responses under 150 words"""
        
        try:
            # Use direct path to model file
            model_path = r"C:\Users\kumar\OneDrive\Documents\debate-sim\backend\models\mistral-7b-v0.1.Q4_K_M.gguf"
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at: {model_path}")
                
            self.llm = Llama(
                model_path=model_path,
                n_gpu_layers=3,
                n_ctx=2048,
                n_threads=6,
                n_batch=256,
                verbose=True
            )
            
            super().__init__(
                name="Opponent",
                llm=self.llm,
                system_prompt=system_prompt
            )
        except Exception as e:
            raise Exception(f"Failed to initialize OpponentAgent: {str(e)}")

    async def process(self, state: Dict[str, Any], context: dict = None) -> dict:
        try:
            prompt = f"""[INST] <<SYS>>{self.system_prompt}<</SYS>>\n
            MOTION: {state['motion']}\n
            Last proponent argument: {state['proponent_arguments'][-1] if state['proponent_arguments'] else 'None'}
            [/INST]"""
            
            response = self.llm(
                prompt=prompt,
                max_tokens=200,
                temperature=0.7,
                stop=["</s>","<|im_end|>"]
            )
            
            return {
                "role": "opponent",
                "content": response["choices"][0]["text"].strip(),
                "round": state["current_round"]
            }

        except Exception as e:
            return {
                "role": "system",
                "content": f"Opponent error: {str(e)}",
                "round": state["current_round"]
            }
