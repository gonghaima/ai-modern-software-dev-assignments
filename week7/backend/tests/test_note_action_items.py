def test_create_and_list_note_action_items(client):
    note = client.post("/notes/", json={"title": "Meeting", "content": "Discuss roadmap"}).json()
    note_id = note["id"]

    r = client.post(f"/notes/{note_id}/action-items", json={"description": "Send recap email"})
    assert r.status_code == 201
    item = r.json()
    assert item["description"] == "Send recap email"
    assert item["note_id"] == note_id
    assert item["completed"] is False

    r = client.get(f"/notes/{note_id}/action-items")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["note_id"] == note_id


def test_list_note_action_items_empty(client):
    note = client.post("/notes/", json={"title": "Empty", "content": "No actions"}).json()
    r = client.get(f"/notes/{note['id']}/action-items")
    assert r.status_code == 200
    assert r.json() == []


def test_create_note_action_item_note_not_found(client):
    r = client.post("/notes/99999/action-items", json={"description": "Ghost item"})
    assert r.status_code == 404


def test_list_note_action_items_note_not_found(client):
    r = client.get("/notes/99999/action-items")
    assert r.status_code == 404


def test_delete_note_cascades_action_items(client):
    note = client.post("/notes/", json={"title": "Cascade", "content": "Will be deleted"}).json()
    note_id = note["id"]
    item = client.post(f"/notes/{note_id}/action-items", json={"description": "Linked item"}).json()

    client.delete(f"/notes/{note_id}")
    r = client.get(f"/action-items/{item['id']}")
    assert r.status_code == 404


def test_action_item_note_id_in_global_list(client):
    note = client.post("/notes/", json={"title": "Linked", "content": "content"}).json()
    client.post(f"/notes/{note['id']}/action-items", json={"description": "Linked action"})

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    linked = [i for i in items if i["note_id"] == note["id"]]
    assert len(linked) == 1
