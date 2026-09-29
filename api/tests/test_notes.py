import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.skipif(not __import__('os').getenv('MONGO_URI'), reason='MONGO_URI not set')
def test_create_update_delete_note():
    create_resp = client.post("/notes/", json={"title": "Test", "content": "Body"})
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert "id" in created
    note_id = created["id"]
    assert created["title"] == "Test"

    update_resp = client.put(f"/notes/{note_id}", json={"title": "Updated"})
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["id"] == note_id
    assert updated["title"] == "Updated"

    del_resp = client.delete(f"/notes/{note_id}")
    assert del_resp.status_code == 204

    not_found = client.put(f"/notes/{note_id}", json={"title": "x"})
    assert not_found.status_code == 404
