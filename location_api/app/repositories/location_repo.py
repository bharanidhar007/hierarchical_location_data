from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from typing import Sequence, Tuple
from app.db import models

def paginate(stmt, limit: int, offset: int):
    return stmt.limit(limit).offset(offset)

def search_filter(model, q: str):
    if not q:
        return True
    like = f"%{q}%"
    if hasattr(model, 'code'):
        return or_(model.name.ilike(like), model.code.ilike(like))
    return model.name.ilike(like)

def list_countries(db: Session, q: str | None, limit: int, offset: int) -> Tuple[Sequence[models.Country], int]:
    base = select(models.Country).where(search_filter(models.Country, q or ""))
    total = db.execute(select(models.Country.id).where(search_filter(models.Country, q or ""))).all()
    items = db.execute(paginate(base.order_by(models.Country.name.asc()), limit, offset)).scalars().all()
    return items, len(total)

def list_states(db: Session, country_id: int | None, q: str | None, limit: int, offset: int):
    conds = []
    if country_id:
        conds.append(models.State.country_id == country_id)
    if q:
        conds.append(search_filter(models.State, q))
    stmt = select(models.State).where(*conds)
    total = db.execute(select(models.State.id).where(*conds)).all()
    items = db.execute(paginate(stmt.order_by(models.State.name.asc()), limit, offset)).scalars().all()
    return items, len(total)

def list_cities(db: Session, state_id: int | None, q: str | None, limit: int, offset: int):
    conds = []
    if state_id:
        conds.append(models.City.state_id == state_id)
    if q:
        conds.append(search_filter(models.City, q))
    stmt = select(models.City).where(*conds)
    total = db.execute(select(models.City.id).where(*conds)).all()
    items = db.execute(paginate(stmt.order_by(models.City.name.asc()), limit, offset)).scalars().all()
    return items, len(total)

def list_towns(db: Session, city_id: int | None, q: str | None, limit: int, offset: int):
    conds = []
    if city_id:
        conds.append(models.Town.city_id == city_id)
    if q:
        conds.append(search_filter(models.Town, q))
    stmt = select(models.Town).where(*conds)
    total = db.execute(select(models.Town.id).where(*conds)).all()
    items = db.execute(paginate(stmt.order_by(models.Town.name.asc()), limit, offset)).scalars().all()
    return items, len(total)
