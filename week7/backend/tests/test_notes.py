def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_get_note(client):
    r = client.post("/notes/", json={"title": "Get me", "content": "content"})
    note_id = r.json()["id"]
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["id"] == note_id


def test_get_note_not_found(client):
    r = client.get("/notes/99999")
    assert r.status_code == 404


def test_delete_note(client):
    r = client.post("/notes/", json={"title": "Delete me", "content": "bye"})
    note_id = r.json()["id"]
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_create_note_validation(client):
    r = client.post("/notes/", json={"title": "", "content": "valid"})
    assert r.status_code == 422
    r = client.post("/notes/", json={"title": "valid", "content": ""})
    assert r.status_code == 422


def test_notes_pagination_skip_limit(client):
    ids = [
        client.post("/notes/", json={"title": f"Note {i}", "content": "x"}).json()["id"]
        for i in range(4)
    ]
    r = client.get("/notes/", params={"sort": "id", "skip": 1, "limit": 2})
    assert r.status_code == 200
    returned_ids = [n["id"] for n in r.json()]
    assert returned_ids == ids[1:3]


def test_notes_limit_one(client):
    for i in range(3):
        client.post("/notes/", json={"title": f"N{i}", "content": "x"})
    r = client.get("/notes/", params={"limit": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_notes_sort_ascending_vs_descending(client):
    ids = [
        client.post("/notes/", json={"title": f"Sort {i}", "content": "x"}).json()["id"]
        for i in range(3)
    ]
    asc_ids = [n["id"] for n in client.get("/notes/", params={"sort": "id"}).json()]
    desc_ids = [n["id"] for n in client.get("/notes/", params={"sort": "-id"}).json()]
    assert asc_ids == sorted(asc_ids)
    assert desc_ids == sorted(desc_ids, reverse=True)


def test_notes_invalid_sort_field_no_500(client):
    client.post("/notes/", json={"title": "Fallback", "content": "x"})
    r = client.get("/notes/", params={"sort": "nonexistent_field"})
    assert r.status_code == 200
