import pytest
from fastapi.testclient import TestClient

from retail_api.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)
