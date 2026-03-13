"""Scan OpenClaw agents/sessions JSONL and extract usage records."""
import json
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_AGENTS_ROOT = os.path.expanduser("~/.openclaw/agents")


def _ParseUsage(obj):
    """Extract input_tokens, output_tokens, cost from message.usage or responseUsage."""
    usage = obj.get("message", {}).get("usage") or obj.get("responseUsage") or {}
    if isinstance(usage, dict):
        inp = usage.get("input_tokens") or usage.get("input") or 0
        out = usage.get("output_tokens") or usage.get("output") or 0
        cost = usage.get("cost")
        if cost is None and isinstance(usage.get("cost"), (int, float)):
            cost = usage["cost"]
        return int(inp), int(out), cost
    return 0, 0, None


def _ScanOneSessionFile(filepath, agent_id, session_id):
    """Read one .jsonl file and yield usage records (agent_id, session_id, input_tokens, output_tokens, cost)."""
    records = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as e:
                    logger.warning("Skip invalid JSON line in %s: %s", filepath, e)
                    continue
                usage = obj.get("message", {}).get("usage") or obj.get("responseUsage")
                if not usage:
                    continue
                inp, out, cost = _ParseUsage(obj)
                records.append({
                    "agent_id": agent_id,
                    "session_id": session_id,
                    "input_tokens": inp,
                    "output_tokens": out,
                    "cost": cost,
                })
    except OSError as e:
        logger.warning("Skip file %s: %s", filepath, e)
    return records


def ScanAgentsRoot(agents_root=None):
    """
    Scan agents_root/<agentId>/sessions/*.jsonl and return list of usage records.
    Each record: agent_id, session_id, input_tokens, output_tokens, cost (optional).
    """
    root = os.path.expanduser(agents_root or DEFAULT_AGENTS_ROOT)
    if not os.path.isdir(root):
        raise FileNotFoundError(f"Agents root not found or not a directory: {root}")

    all_records = []
    try:
        for agent_id in os.listdir(root):
            agent_path = os.path.join(root, agent_id)
            if not os.path.isdir(agent_path):
                continue
            sessions_dir = os.path.join(agent_path, "sessions")
            if not os.path.isdir(sessions_dir):
                continue
            try:
                for name in os.listdir(sessions_dir):
                    if ".deleted." in name or not name.endswith(".jsonl"):
                        continue
                    session_id = os.path.splitext(name)[0]
                    filepath = os.path.join(sessions_dir, name)
                    if not os.path.isfile(filepath):
                        continue
                    all_records.extend(
                        _ScanOneSessionFile(filepath, agent_id, session_id)
                    )
            except PermissionError as e:
                logger.warning("Skip sessions dir %s: %s", sessions_dir, e)
    except PermissionError as e:
        logger.warning("Skip agents root %s: %s", root, e)

    return all_records
