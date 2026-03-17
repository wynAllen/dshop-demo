import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("RETAIL_DATABASE_URL", "sqlite:///:memory:")

from retail_api.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)
