"""Flask app for OpenClaw token usage report."""
import logging
import os
import traceback
from flask import Flask, render_template

from openclaw_token_monitor.scanner import ScanAgentsRoot
from openclaw_token_monitor.aggregator import Aggregate

logger = logging.getLogger(__name__)
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

# Data root: env OPENCLAW_AGENTS_ROOT or default
def GetAgentsRoot():
    return os.environ.get("OPENCLAW_AGENTS_ROOT") or os.path.expanduser("~/.openclaw/agents")


def BuildReport(agents_root=None):
    """Scan, aggregate, return dict for template (by_agent, by_session, totals)."""
    root = agents_root or GetAgentsRoot()
    records = ScanAgentsRoot(root)
    return Aggregate(records)


def _AgentsRoot():
    return app.config.get("OPENCLAW_AGENTS_ROOT") or GetAgentsRoot()


@app.errorhandler(Exception)
def HandleException(exc):
    if isinstance(exc, FileNotFoundError):
        return str(exc), 404
    logger.exception("Unhandled exception: %s", exc)
    return traceback.format_exc(), 500


@app.route("/")
def Index():
    data = BuildReport(_AgentsRoot())
    return render_template("index.html.j2", **data)


@app.route("/refresh", methods=["GET", "POST"])
def Refresh():
    data = BuildReport(_AgentsRoot())
    return render_template("index.html.j2", **data)


@app.route("/export")
def Export():
    data = BuildReport(_AgentsRoot())
    return render_template("index.html.j2", **data)


def CreateApp(agents_root=None):
    """Factory: optionally bind agents_root to config for this app instance."""
    if agents_root is not None:
        app.config["OPENCLAW_AGENTS_ROOT"] = agents_root
    return app
