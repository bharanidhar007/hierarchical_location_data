from pydantic import BaseModel
from typing import Optional, Dict, Any

class CountryBase(BaseModel):
    code: str
    name: str
    translations: Dict[str, Any] = {}

class CountryCreate(CountryBase): pass
class CountryUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    translations: Optional[Dict[str, Any]] = None

class CountryOut(CountryBase):
    id: int
    class Config:
        from_attributes = True

class StateBase(BaseModel):
    country_id: int
    code: str | None = None
    name: str
    translations: Dict[str, Any] = {}

class StateCreate(StateBase): pass
class StateUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    translations: Dict[str, Any] | None = None

class StateOut(StateBase):
    id: int
    class Config:
        from_attributes = True

class CityBase(BaseModel):
    state_id: int
    name: str
    code: str | None = None
    translations: Dict[str, Any] = {}
    latitude: float | None = None
    longitude: float | None = None

class CityCreate(CityBase): pass
class CityUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    translations: Dict[str, Any] | None = None
    latitude: float | None = None
    longitude: float | None = None

class CityOut(CityBase):
    id: int
    class Config:
        from_attributes = True

class TownBase(BaseModel):
    city_id: int
    name: str
    code: str | None = None
    translations: Dict[str, Any] = {}
    latitude: float | None = None
    longitude: float | None = None

class TownCreate(TownBase): pass
class TownUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    translations: Dict[str, Any] | None = None
    latitude: float | None = None
    longitude: float | None = None

class TownOut(TownBase):
    id: int
    class Config:
        from_attributes = True
