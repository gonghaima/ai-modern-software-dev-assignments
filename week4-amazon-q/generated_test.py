def test_edit_note(client):
    r = client.post("/notes/", json={"title": "To Edit", "content": "Hello"})
    note_id = r.json()["id"]

    updated_note = {"title": "Edited", "content": "World"}
    r = client.put(f"/notes/{note_id}", json=updated_note)
    assert r.status_code == 200
    assert r.json()["title"] == updated_note["title"]
    assert r.json()["content"] == updated_note["content"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == updated_note["title"]
    assert r.json()["content"] == updated_note["content"]