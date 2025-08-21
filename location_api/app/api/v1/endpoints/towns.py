from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from app.db.session import get_db
from app.schemas.common import Pagination

from app.schemas.location import TownOut
from app.repositories import location_repo as repo
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=dict)
@cache(expire=settings.CACHE_TTL)
def list_towns(
    city_id: int | None = Query(None),
    q: str | None = Query(None),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    items, total = repo.list_towns(db, city_id, q, limit, offset)
    return {"total": total, "count": len(items), "items": [TownOut.model_validate(i) for i in items]}

@router.get("/{town_id}", response_model=TownOut)
def get_town(town_id: int, db: Session = Depends(get_db)):
    from app.db import models
    obj = db.get(models.Town, town_id)
    if not obj:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Town not found")
    return TownOut.model_validate(obj)
