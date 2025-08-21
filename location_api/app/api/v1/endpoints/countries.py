from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from app.db.session import get_db
from app.schemas.common import Pagination

from app.schemas.location import CountryOut, CountryCreate, CountryUpdate
from app.db import models
from app.repositories import location_repo as repo
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=dict)
@cache(expire=settings.CACHE_TTL)
def list_countries(
    q: str | None = Query(None, description="Search by name/code"),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    items, total = repo.list_countries(db, q, limit, offset)
    return {"total": total, "count": len(items), "items": [CountryOut.model_validate(i) for i in items]}

@router.get("/{country_id}", response_model=CountryOut)
def get_country(country_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Country, country_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Country not found")
    return CountryOut.model_validate(obj)
