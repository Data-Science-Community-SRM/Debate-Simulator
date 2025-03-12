from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import chromadb
import os
from serpapi import GoogleSearch
from typing import Dict, Any
import logging

logger=logging.getLogger(__name__)

class FactCheckerAgent:
    def __init__(self):
        try:
            self.nli_pipeline=pipeline("text-classification",model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",device=-1)
            self.sbert_model=SentenceTransformer("all-MiniLM-L6-v2")
            self.chroma_client=chromadb.PersistentClient(path="db")
            self.collection=self.chroma_client.get_or_create_collection("fact_checker")
            self.serp_api_key=os.getenv("SERPAPI_KEY","your_api_key_here")
        except Exception as e:
            logger.error(f"Failed to initialize FactCheckerAgent: {str(e)}")
            raise

    def add_context(self, documents: list):
        try:
            embeddings=self.sbert_model.encode(documents).tolist()
            ids=[f"doc_{i}" for i in range(len(documents))]
            self.collection.add(ids=ids,documents=documents,embeddings=embeddings)
        except Exception as e:
            logger.error(f"Error adding context: {str(e)}")

    def process(self, claim: str) -> Dict[str, Any]:
        try:
            local_context=self.query_local(claim)
            if local_context:
                return self.verify_claim(claim,local_context,"local")
            web_context=self.query_web(claim)
            if web_context:
                return self.verify_claim(claim,web_context,"web")
            return {"status":"unverified","message":"No supporting evidence found","confidence":0.0}
        except Exception as e:
            logger.error(f"Fact checking failed: {str(e)}")
            return {"status":"error","message":str(e),"confidence":0.0}

    def query_local(self, claim: str) -> str:
        try:
            results=self.collection.query(query_texts=[claim],n_results=1)
            return results['documents'][0][0] if results['documents'] else None
        except Exception as e:
            logger.error(f"Local query failed: {str(e)}")
            return None

    def query_web(self, claim: str) -> str:
        try:
            search=GoogleSearch({"q":claim,"api_key":self.serp_api_key,"num":1})
            results=search.get_dict()
            return results.get('organic_results', [{}])[0].get('snippet', '')
        except Exception as e:
            logger.error(f"Web query failed: {str(e)}")
            return ""

    def verify_claim(self, claim: str, context: str, source: str) -> Dict[str, Any]:
        try:
            result=self.nli_pipeline(f"Claim: {claim}. Context: {context}")
            if result[0]['label']=='ENTAILMENT' and result[0]['score']>0.7:
                return {"status":"verified","source":source,"context":context,"confidence":result[0]['score']}
            return {"status":"disputed","source":source,"context":context,"confidence":result[0]['score']}
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return {"status":"error","message":str(e),"confidence":0.0}