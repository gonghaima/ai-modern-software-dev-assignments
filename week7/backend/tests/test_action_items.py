def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_get_action_item(client):
    r = client.post("/action-items/", json={"description": "Get me"})
    item_id = r.json()["id"]
    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 200
    assert r.json()["id"] == item_id


def test_get_action_item_not_found(client):
    r = client.get("/action-items/99999")
    assert r.status_code == 404


def test_delete_action_item(client):
    r = client.post("/action-items/", json={"description": "Delete me"})
    item_id = r.json()["id"]
    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204
    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 404


def test_delete_action_item_not_found(client):
    r = client.delete("/action-items/99999")
    assert r.status_code == 404


def test_create_action_item_validation(client):
    r = client.post("/action-items/", json={"description": ""})
    assert r.status_code == 422


def test_action_items_pagination_skip_limit(client):
    ids = [
        client.post("/action-items/", json={"description": f"Item {i}"}).json()["id"]
        for i in range(4)
    ]
    r = client.get("/action-items/", params={"sort": "id", "skip": 1, "limit": 2})
    assert r.status_code == 200
    returned_ids = [i["id"] for i in r.json()]
    assert returned_ids == ids[1:3]


def test_action_items_limit_one(client):
    for i in range(3):
        client.post("/action-items/", json={"description": f"A{i}"})
    r = client.get("/action-items/", params={"limit": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_action_items_sort_ascending_vs_descending(client):
    for i in range(3):
        client.post("/action-items/", json={"description": f"Sort {i}"})
    asc_ids = [i["id"] for i in client.get("/action-items/", params={"sort": "id"}).json()]
    desc_ids = [i["id"] for i in client.get("/action-items/", params={"sort": "-id"}).json()]
    assert asc_ids == sorted(asc_ids)
    assert desc_ids == sorted(desc_ids, reverse=True)


def test_action_items_completed_false_filter(client):
    r = client.post("/action-items/", json={"description": "incomplete"})
    incomplete_id = r.json()["id"]
    r = client.post("/action-items/", json={"description": "complete me"})
    client.put(f"/action-items/{r.json()['id']}/complete")

    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    items = r.json()
    assert all(not i["completed"] for i in items)
    assert any(i["id"] == incomplete_id for i in items)


def test_action_items_invalid_sort_field_no_500(client):
    client.post("/action-items/", json={"description": "Fallback"})
    r = client.get("/action-items/", params={"sort": "nonexistent_field"})
    assert r.status_code == 200
