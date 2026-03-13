"""Tests for openclaw_token_monitor.aggregator."""
import pytest

try:
    from openclaw_token_monitor.aggregator import Aggregate
except ImportError:
    Aggregate = None


@pytest.fixture
def SampleRecords():
    return [
        {"agent_id": "a1", "session_id": "s1", "input_tokens": 100, "output_tokens": 50, "cost": 0.01},
        {"agent_id": "a1", "session_id": "s1", "input_tokens": 200, "output_tokens": 80, "cost": 0.02},
        {"agent_id": "a1", "session_id": "s2", "input_tokens": 300, "output_tokens": 100, "cost": None},
    ]


def test_aggregate_by_agent_and_session(SampleRecords):
    if Aggregate is None:
        pytest.skip("aggregator not implemented")
    out = Aggregate(SampleRecords)
    assert "by_agent" in out
    assert "by_session" in out
    assert "totals" in out
    by_agent = {r["agent_id"]: r for r in out["by_agent"]}
    assert by_agent["a1"]["total_input"] == 600
    assert by_agent["a1"]["total_output"] == 230
    assert by_agent["a1"]["session_count"] == 2
    by_session_list = out["by_session"]
    session_totals = {(r["agent_id"], r["session_id"]): (r["total_input"], r["total_output"]) for r in by_session_list}
    assert session_totals[("a1", "s1")] == (300, 130)
    assert session_totals[("a1", "s2")] == (300, 100)
    assert out["totals"]["total_input"] == 600
    assert out["totals"]["total_output"] == 230
