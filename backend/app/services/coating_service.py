from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional

from ..models.coating_data import CoatingData
from ..schemas import coating_schemas

class CoatingService:
    def get_coating_data(
        self,
        db: Session,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        body_area: Optional[str],
        skip: int = 0,
        limit: int = 20
    ) -> List[CoatingData]:
        query = db.query(CoatingData)
        
        if start_time:
            query = query.filter(CoatingData.timestamp >= start_time)
        if end_time:
            query = query.filter(CoatingData.timestamp <= end_time)
        if body_area:
            query = query.filter(CoatingData.body_area == body_area)
            
        return query.offset(skip).limit(limit).all()

    def create_coating_data(
        self,
        db: Session,
        data: coating_schemas.CoatingDataCreate
    ) -> CoatingData:
        db_data = CoatingData(**data.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data

    def get_latest_data(
        self,
        db: Session
    ) -> CoatingData:
        return db.query(CoatingData).order_by(desc(CoatingData.timestamp)).first()

coating_service = CoatingService() 