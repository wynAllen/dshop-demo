"""Tests for openclaw_token_monitor.scanner."""
import os
import pytest

# Import after implementation exists
try:
    from openclaw_token_monitor.scanner import ScanAgentsRoot
except ImportError:
    ScanAgentsRoot = None


@pytest.fixture
def FixtureSessionsRoot():
    return os.path.join(os.path.dirname(__file__), "fixtures", "sessions")


def test_scan_fixture_returns_records(FixtureSessionsRoot):
    """Scan fixture dir and assert we get usage records with input_tokens, output_tokens."""
    if ScanAgentsRoot is None:
        pytest.skip("scanner not implemented")
    records = ScanAgentsRoot(FixtureSessionsRoot)
    assert len(records) >= 1
    one = records[0]
    assert "input_tokens" in one
    assert "output_tokens" in one
    assert one["input_tokens"] >= 0
    assert one["output_tokens"] >= 0
