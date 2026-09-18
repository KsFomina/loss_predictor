VALID_PAYLOAD = {
    "request_id": "req-1",
    "item_id": "ITEM-001",
    "item_price": 2500.0,
    "delivery_days": 4,
    "client_is_app": True,
    "type_prepayment": "card",
}

def test_predict_success(client, item_in_db):
    resp=client.post("/predictions", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["request_id"] =="req-1"
    assert body["prediction"] == 501.34
    assert body["model_version"] == "test-1.0.0"

def test_predict_validation_error(client):
    bad = {**VALID_PAYLOAD, "type_prepayment":"bitcoin"}
    resp= client.post("/predictions", json=bad)
    assert resp.status_code==422

def test_predict_item_not_found(client):
    bad={**VALID_PAYLOAD, "item_id":"NOPE-999"}
    resp=client.post("/predictions", json=bad)
    assert resp.status_code==404

def test_predict_idempotent(client, item_in_db):
    r1 = client.post("/predictions", json=VALID_PAYLOAD)
    assert r1.status_code == 200

    changed_payload={**VALID_PAYLOAD, "item_price": 9999.0}
    r2=client.post("/predictions", json = changed_payload)
    assert r2.status_code== 200
    assert r2.json() == r1.json()

    r3 = client.get("/predictions/req-1")
    assert r3.status_code==200
    assert r3.json() == r1.json()

def test_get_prediction(client, item_in_db):
    client.post("/predictions", json = VALID_PAYLOAD)
    resp= client.get("/predictions/req-1")
    assert resp.status_code == 200
    assert resp.json()["prediction"] == 501.34

def test_get_prediction_not_found(client):
    resp = client.get("/predictions/unknown")
    assert resp.status_code == 404


