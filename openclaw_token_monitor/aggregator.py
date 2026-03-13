"""Aggregate scanner usage records by agent and session."""
from collections import defaultdict


def Aggregate(records):
    """
    Input: list of dicts with agent_id, session_id, input_tokens, output_tokens, cost (optional).
    Output: by_agent, by_session, totals per design doc.
    """
    session_sums = defaultdict(lambda: {"input": 0, "output": 0, "cost": None})
    session_has_cost = defaultdict(bool)

    for r in records:
        key = (r["agent_id"], r["session_id"])
        session_sums[key]["input"] += r.get("input_tokens", 0)
        session_sums[key]["output"] += r.get("output_tokens", 0)
        c = r.get("cost")
        if c is not None:
            if session_sums[key]["cost"] is None:
                session_sums[key]["cost"] = 0
            session_sums[key]["cost"] += c
            session_has_cost[key] = True

    by_session = []
    for (agent_id, session_id), s in session_sums.items():
        total_cost = s["cost"] if session_has_cost[(agent_id, session_id)] else None
        by_session.append({
            "agent_id": agent_id,
            "session_id": session_id,
            "total_input": s["input"],
            "total_output": s["output"],
            "total_cost": total_cost,
            "last_activity": None,
        })

    agent_sums = defaultdict(lambda: {"input": 0, "output": 0, "cost": None, "sessions": set()})
    for (agent_id, session_id), s in session_sums.items():
        agent_sums[agent_id]["input"] += s["input"]
        agent_sums[agent_id]["output"] += s["output"]
        agent_sums[agent_id]["sessions"].add(session_id)
        if s["cost"] is not None:
            if agent_sums[agent_id]["cost"] is None:
                agent_sums[agent_id]["cost"] = 0
            agent_sums[agent_id]["cost"] += s["cost"]

    by_agent = []
    for agent_id, a in agent_sums.items():
        by_agent.append({
            "agent_id": agent_id,
            "session_count": len(a["sessions"]),
            "total_input": a["input"],
            "total_output": a["output"],
            "total_cost": a["cost"],
        })

    total_input = sum(a["input"] for a in agent_sums.values())
    total_output = sum(a["output"] for a in agent_sums.values())
    total_cost = None
    for a in agent_sums.values():
        if a["cost"] is not None:
            total_cost = (total_cost or 0) + a["cost"]

    return {
        "by_agent": by_agent,
        "by_session": by_session,
        "totals": {
            "total_input": total_input,
            "total_output": total_output,
            "total_cost": total_cost,
        },
    }
