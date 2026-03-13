"""CLI: serve | export for OpenClaw token usage monitor."""
import argparse
import os
import sys

# Ensure package is importable when run as __main__
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openclaw_token_monitor.scanner import ScanAgentsRoot
from openclaw_token_monitor.aggregator import Aggregate
from openclaw_token_monitor.server import CreateApp


def RenderStatic(agents_root, output_path):
    """Scan, aggregate, render to HTML and write to output_path."""
    import jinja2
    records = ScanAgentsRoot(agents_root)
    data = Aggregate(records)
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template("index.html.j2")
    html = template.render(**data)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def Main():
    parser = argparse.ArgumentParser(description="OpenClaw token usage monitor")
    parser.add_argument(
        "--openclaw-data-dir",
        default=os.environ.get("OPENCLAW_AGENTS_ROOT", os.path.expanduser("~/.openclaw/agents")),
        help="OpenClaw agents root (default: ~/.openclaw/agents)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    serve_parser = sub.add_parser("serve", help="Start Flask server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    serve_parser.add_argument("--port", type=int, default=5050, help="Bind port")

    export_parser = sub.add_parser("export", help="Export static HTML report")
    export_parser.add_argument("--output", "-o", default="openclaw_usage.html", help="Output HTML file")

    args = parser.parse_args()
    agents_root = os.path.expanduser(args.openclaw_data_dir)

    if args.command == "serve":
        app = CreateApp(agents_root=agents_root)
        app.run(host=args.host, port=args.port, debug=False)

    elif args.command == "export":
        try:
            RenderStatic(agents_root, args.output)
            print(f"Exported to {args.output}")
        except FileNotFoundError as e:
            print(e, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    Main()
