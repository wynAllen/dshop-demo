def test_health_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()
