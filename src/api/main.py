from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.database.repo import GuardianRepository
from src.core.decision_engine import DecisionEngine

# Database Setup
DATABASE_URL = \"sqlite+aiosqlite:///./guardian.db\"
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI(title=\"Child Content Guardian API\")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"*\"],
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)

class ContentRequest(BaseModel):
    profile_id: int
    url: str
    content_type: str
    payload: str

class DecisionResponse(BaseModel):
    decision: str
    reason: str
    scores: Dict[str, float]

async def get_db():
    async with async_session() as session:
        yield session

@app.on_event(\"startup\")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post(\"/filter\", response_model=DecisionResponse)
async def filter_content(request: ContentRequest, db: AsyncSession = Depends(get_db), x_api_key: str = Header(None)):
    # Authentication
    if x_api_key != \"secret-parent-key\":
        raise HTTPException(status_code=403, detail=\"Forbidden\")
    
    repo = GuardianRepository(db)
    engine = DecisionEngine()
    
    # 1. Check Allowlist
    if await repo.is_allowlisted(request.url):
        return DecisionResponse(decision=\"ALLOW\", reason=\"Domain is allowlisted\", scores={})
    
    # 2. Process via AI Engine
    decision, reason, scores = await engine.process_content(
        request.profile_id, 
        request.content_type, 
        request.payload
    )
    
    # 3. Async Log to Database
    await repo.create_event({
        \"profile_id\": request.profile_id,
        \"url\": request.url,
        \"content_type\": request.content_type,
        \"decision\": decision,
        \"reason\": reason,
        **{f\"{k}_score\": v for k, v in scores.items()} # Dynamically map scores to columns
    })
    
    return DecisionResponse(decision=decision, reason=reason, scores=scores)

if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(app, host=\"0.0.0.0\", port=8765)
