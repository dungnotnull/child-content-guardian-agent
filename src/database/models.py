from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()

class ChildProfile(Base):
    __tablename__ = 'child_profiles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    age_band = Column(String(20), nullable=False) # e.g., 'early_childhood', 'middle_childhood', 'adolescent'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    events = relationship('ContentEvent', back_populates='profile')

class ContentEvent(Base):
    __tablename__ = 'content_events'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('child_profiles.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Content details
    url = Column(String(2048))
    content_type = Column(String(20)) # 'text', 'image', 'video', 'audio'
    content_hash = Column(String(64), index=True) # SHA-256 of content for deduplication/audit
    
    # Classifier scores (normalized 0-1)
    toxicity_score = Column(Float, default=0.0)
    nsfw_score = Column(Float, default=0.0)
    violence_score = Column(Float, default=0.0)
    scam_score = Column(Float, default=0.0)
    brainrot_score = Column(Float, default=0.0)
    
    # Decision logic
    decision = Column(String(20)) # 'ALLOW', 'WARN', 'BLOCK'
    reason = Column(Text)
    
    profile = relationship('ChildProfile', back_populates='events')

class Allowlist(Base):
    __tablename__ = 'allowlist'
    
    id = Column(Integer, primary_key=True)
    pattern = Column(String(512), nullable=False, unique=True) # Regex or Domain
    description = Column(String(256))
    created_by_parent_id = Column(Integer) # simplified for now
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    # Using aiosqlite for async operations
    engine = create_async_engine('sqlite+aiosqlite:///./guardian.db')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine
