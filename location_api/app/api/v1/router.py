from fastapi import APIRouter
from .endpoints import countries, states, cities, towns

api_router = APIRouter()
api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(states.router, prefix="/states", tags=["states"])
api_router.include_router(cities.router, prefix="/cities", tags=["cities"])
api_router.include_router(towns.router, prefix="/towns", tags=["towns"])
