def test_metrics_returns_200_and_contains_http_requests(client):
    client.get("/health")
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"http_requests_total" in r.content
