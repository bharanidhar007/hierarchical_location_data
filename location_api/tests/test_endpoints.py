import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_countries_ok():
    r = client.get("/api/v1/countries")
    assert r.status_code == 200
    assert "items" in r.json()

def test_pagination_params():
    r = client.get("/api/v1/countries?limit=5&offset=0")
    assert r.status_code == 200
    assert r.json()["count"] <= 5
