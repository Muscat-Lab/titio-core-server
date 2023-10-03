from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.models.model import Performance


class PerformanceRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        
    async def save_performance(self, performance: Performance) -> Performance:
        self.session.add(instance=performance)
        self.session.commit()
        self.session.refresh(instance=performance)
        
        return performance
        
        
    async def get_performance_list(self) -> list[Performance]:
        return list(
            (
                self.session.scalars(
                    select(Performance).order_by(Performance.created_at.desc()).limit(10)
                )
            ).all()
        )
        