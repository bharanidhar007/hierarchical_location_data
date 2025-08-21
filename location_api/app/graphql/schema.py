import strawberry
from typing import List, Optional
from app.db.session import get_db, SessionLocal
from app.db import models

@strawberry.type
class Country:
    id: int
    code: str
    name: str

@strawberry.type
class State:
    id: int
    country_id: int
    code: Optional[str]
    name: str

@strawberry.type
class City:
    id: int
    state_id: int
    code: Optional[str]
    name: str
    latitude: Optional[float]
    longitude: Optional[float]

@strawberry.type
class Town:
    id: int
    city_id: int
    code: Optional[str]
    name: str
    latitude: Optional[float]
    longitude: Optional[float]

@strawberry.type
class Query:
    @strawberry.field
    def countries(self, q: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[Country]:
        db = SessionLocal()
        try:
            stmt = db.query(models.Country)
            if q:
                stmt = stmt.filter(models.Country.name.ilike(f"%{q}%"))
            return stmt.order_by(models.Country.name).limit(limit).offset(offset).all()
        finally:
            db.close()
