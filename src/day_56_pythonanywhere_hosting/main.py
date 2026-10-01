"""Day 56 – Hosting Python Code Online with PythonAnywhere.

Scenario: deploy a tiny *"Quote of the Day" web app* – a standard-library WSGI
application that runs locally with ``wsgiref`` and on PythonAnywhere unchanged.

Deliverables (syllabus):
* Cloud deployment basics (WSGI entry point, config via environment, checklist)
* Live app hosting (PythonAnywhere WSGI file, health endpoint, local preview)
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Iterable
from datetime import date
from typing import Any

DELIVERABLES: dict[str, str] = {
    "WSGI application (the hosting contract)": "application",
    "routing and status codes": "application",
    "health check endpoint for monitoring": "application",
    "PythonAnywhere WSGI configuration file": "pythonanywhere_wsgi_file",
    "deployment checklist": "DEPLOY_STEPS",
    "local preview server": "serve_locally",
}

QUOTES = [
    "Simple is better than complex.",
    "Readability counts.",
    "Errors should never pass silently.",
    "Now is better than never.",
]

DEPLOY_STEPS = (
    "Create a free account at pythonanywhere.com",
    "Open a Bash console: git clone https://github.com/<you>/pro-python-mastery.git",
    "python3.12 -m venv ~/.venvs/ppm && source ~/.venvs/ppm/bin/activate && pip install -r requirements.txt",
    "Web tab → Add a new web app → Manual configuration → Python 3.12",
    "Set the virtualenv path to ~/.venvs/ppm",
    "Edit the WSGI file: paste the output of pythonanywhere_wsgi_file()",
    "Add environment variables (APP_NAME) in the WSGI file or a .env – never commit secrets",
    "Reload the web app and open https://<you>.pythonanywhere.com/health",
)

StartResponse = Callable[[str, list[tuple[str, str]]], Any]


def quote_for(day: date) -> str:
    return QUOTES[day.toordinal() % len(QUOTES)]


def _respond(start_response: StartResponse, status: str, body: str, content_type: str) -> list[bytes]:
    data = body.encode("utf-8")
    start_response(status, [("Content-Type", f"{content_type}; charset=utf-8"),
                            ("Content-Length", str(len(data)))])
    return [data]


def application(environ: dict[str, Any], start_response: StartResponse) -> Iterable[bytes]:
    """The WSGI callable every Python host (PythonAnywhere, gunicorn, uWSGI) looks for."""
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    app_name = os.environ.get("APP_NAME", "Quote of the Day")
    if method != "GET":
        return _respond(start_response, "405 Method Not Allowed", "Only GET is supported", "text/plain")
    if path == "/":
        quote = quote_for(date.today())
        html = f"<!doctype html><title>{app_name}</title><h1>{app_name}</h1><blockquote>{quote}</blockquote>"
        return _respond(start_response, "200 OK", html, "text/html")
    if path == "/api/quote":
        return _respond(start_response, "200 OK", json.dumps({"date": date.today().isoformat(),
                                                              "quote": quote_for(date.today())}), "application/json")
    if path == "/health":
        return _respond(start_response, "200 OK", json.dumps({"status": "ok"}), "application/json")
    return _respond(start_response, "404 Not Found", f"No page at {path}", "text/plain")


def pythonanywhere_wsgi_file(username: str, project_dir: str = "pro-python-mastery") -> str:
    """Contents for /var/www/<username>_pythonanywhere_com_wsgi.py."""
    if not username.isidentifier():
        raise ValueError("PythonAnywhere usernames are letters, digits and underscores")
    home = f"/home/{username}/{project_dir}"
    return (
        "import os\n"
        "import sys\n\n"
        f"path = {home!r}\n"
        "if path not in sys.path:\n"
        "    sys.path.insert(0, path)\n\n"
        'os.environ.setdefault("APP_NAME", "Quote of the Day")\n\n'
        "from src.day_56_pythonanywhere_hosting.main import application  # noqa: E402,F401\n"
    )


def serve_locally(port: int = 8000) -> None:  # pragma: no cover – blocking server
    from wsgiref.simple_server import make_server

    with make_server("127.0.0.1", port, application) as server:
        print(f"Preview at http://127.0.0.1:{port}/  (Ctrl-C to stop)")
        server.serve_forever()


def main() -> None:
    print("Day 56 – Deploying to PythonAnywhere\n")
    for number, step in enumerate(DEPLOY_STEPS, start=1):
        print(f"{number}. {step}")
    print("\nWSGI file for user 'asha':\n" + pythonanywhere_wsgi_file("asha"))
    print("Run `python -m src.day_56_pythonanywhere_hosting.main --serve` to preview locally.")


if __name__ == "__main__":  # pragma: no cover
    import sys

    serve_locally() if "--serve" in sys.argv else main()
