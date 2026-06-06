from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Base, ChildProfile, ContentEvent, Allowlist

class GuardianRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_profile(self, profile_id: int) -> ChildProfile:
        result = await self.session.execute(select(ChildProfile).where(ChildProfile.id == profile_id))
        return result.scalar_one_or_none()

    async def create_event(self, event_data: dict) -> ContentEvent:
        new_event = ContentEvent(**event_data)
        self.session.add(new_event)
        await self.session.commit()
        await self.session.refresh(new_event)
        return new_event

    async def is_allowlisted(self, url: str) -> bool:
        # Simple substring match for blueprint, real run would use regex
        result = await self.session.execute(select(Allowlist).where(Allowlist.pattern.like(f'%%{url}%%')))
        return result.scalar_one_or_none() is not None

    async def log_override(self, event_id: int, new_decision: str):
        await self.session.execute(
            update(ContentEvent).where(ContentEvent.id == event_id).values(decision=new_decision)
        )
        await self.session.commit()
