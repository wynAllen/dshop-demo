def test_not_found_returns_404_with_unified_body(client):
    r = client.get("/api/v1/notfound")
    assert r.status_code == 404
    body = r.json()
    assert "code" in body
    assert "message" in body


def test_validation_error_returns_422_with_unified_body(client):
    r = client.post("/api/v1/users/register", json={})
    assert r.status_code == 422
    body = r.json()
    assert "code" in body
    assert "message" in body
