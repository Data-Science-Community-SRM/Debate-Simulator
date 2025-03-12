from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import debate

app = FastAPI(
    title="Debate Simulator API",
    description="API for Real-Time AI Debate Simulator",
    version="0.1.0"
)

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  #flask
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(debate.router, prefix="/api/v1/debate")
# app.include_router(debate.router)
@app.get("/")
async def root():
    return {
        "message": "Debate Simulator API is running",
        "docs_url": "/docs",
        "version": "0.1.0"
    }
