def test_response_includes_request_id(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "x-request-id" in r.headers
    assert len(r.headers["x-request-id"]) > 0
