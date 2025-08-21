from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Float, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.db.base import Base
from app.core.config import settings

try:
    from geoalchemy2 import Geography
    GEO_AVAILABLE = True
except Exception:
    GEO_AVAILABLE = False

class Country(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    translations = Column(JSONB, nullable=False, server_default='{}')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    states = relationship("State", back_populates="country", cascade="all, delete-orphan")

class State(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("country.id", ondelete="CASCADE"), index=True, nullable=False)
    code: Mapped[str | None] = mapped_column(String(10), index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    translations = Column(JSONB, nullable=False, server_default='{}')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")

class City(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    state_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("state.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    code: Mapped[str | None] = mapped_column(String(20), index=True, nullable=True)
    translations = Column(JSONB, nullable=False, server_default='{}')
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    if settings.USE_POSTGIS:
        geom = Column('geom', __import__('geoalchemy2').geography.Geography(geometry_type='POINT', srid=4326), nullable=True)  # type: ignore
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    state = relationship("State", back_populates="cities")
    towns = relationship("Town", back_populates="city", cascade="all, delete-orphan")

class Town(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("city.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    code: Mapped[str | None] = mapped_column(String(20), index=True, nullable=True)
    translations = Column(JSONB, nullable=False, server_default='{}')
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    if settings.USE_POSTGIS:
        geom = Column('geom', __import__('geoalchemy2').geography.Geography(geometry_type='POINT', srid=4326), nullable=True)  # type: ignore
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    city = relationship("City", back_populates="towns")
