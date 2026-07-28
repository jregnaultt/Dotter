import os
from fastapi.testclient import TestClient
from app.main import app
from app.models.sprite import SpriteState

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_supported_states():
    response = client.get("/api/v1/sprites/states")
    assert response.status_code == 200
    states = response.json()["supported_states"]
    assert "idle" in states
    assert "punch" in states
    assert "kick" in states
    assert "damage" in states
    assert "projectile" in states
    assert "character_select" in states
    assert "mega_evolution_1" in states
    assert "mega_evolution_2" in states
    assert "fatality" in states

def test_generate_character_sprites():
    payload = {
        "character_name": "TestFighter",
        "description": "Luchador con aura azul y guayabera",
        "states": ["idle", "punch", "fatality"],
        "pollinations_model": "zimage"
    }
    response = client.post("/api/v1/sprites/generate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["character_name"] == "TestFighter"
    assert data["total_generated"] == 3
    assert os.path.exists(data["vertical_sheet_path"])
