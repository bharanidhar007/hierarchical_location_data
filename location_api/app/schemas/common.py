from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class Pagination(BaseModel):
    limit: int = Field(20, ge=1, le=200)
    offset: int = Field(0, ge=0)

class Translations(BaseModel):
    __root__: Dict[str, Dict[str, Any]] = {}
