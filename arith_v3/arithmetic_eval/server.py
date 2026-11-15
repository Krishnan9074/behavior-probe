"""Local trusted-side JSON probe service; stdlib only.

Intended for pilots with separate isolated agent runners. Not production hardened.
It must run OUTSIDE the agent sandbox with cases/private/ inaccessible to agents.
"""
from __future__ import annotations

import hmac
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .generate import read_json, write_json
from .grade import parse_predictions
from .student import OPS, answer


def _load(root: Path, session_name: str):
    if not isinstance(session_name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", session_name):
        raise ValueError("Invalid session identifier")
    path = root / "private" / "sessions" / f"{session_name}.json"
    if not path.exists():
        raise ValueError("Unknown session")
    s = read_json(path)
    pub = read_json(root / "public" / f"{s['case']}.json")
    pri = read_json(root / "private" / f"{s['case']}.json")
    return path, s, pub, pri


def process(root: Path, session: str, token: str, action: str, body: dict | None = None) -> dict:
    path, s, public, private = _load(root, session)
    expected = s.get("api_token", "")
    if not expected or not isinstance(token, str) or not hmac.compare_digest(expected, token):
        raise PermissionError("Unauthorized")
    if action == "task":
        return {"task": public, "budget": s["budget"],
                "used": len(s["probes"]), "remaining": s["budget"] - len(s["probes"])}
    if s.get("closed"):
        raise ValueError("Session is closed")
    if action == "probe":
        if not isinstance(body, dict):
            raise ValueError("JSON body must be an object")
        op, a, b = body.get("op"), body.get("a"), body.get("b")
        if (op not in OPS or type(a) is not int or type(b) is not int or
                not 0 <= a <= 1000000 or not 0 <= b <= 1000000 or (op == "div" and b == 0)):
            raise ValueError("Invalid operation or operands")
        if op == "sub" and a < b:
            raise ValueError("Subtraction requires a >= b")
        if op == "div" and a % b != 0:
            raise ValueError("Division requires exact integer quotient")
        if len(s["probes"]) >= s["budget"]:
            raise ValueError("Probe budget exhausted")
        if (op, a, b) in {(q["op"], q["a"], q["b"]) for q in public["test_questions"]}:
            raise ValueError("Exact held-out question cannot be probed")
        y = answer(op, a, b, private["rules"][op])
        s["probes"].append({"op": op, "a": a, "b": b, "student_answer": y})
        write_json(path, s)
        return {"op": op, "a": a, "b": b, "student_answer": y,
                "used": len(s["probes"]), "remaining": s["budget"] - len(s["probes"])}
    if action == "snapshot":
        if not isinstance(body, dict):
            raise ValueError("Snapshot must be a JSON object")
        _, error = parse_predictions(body, public["test_questions"])
        # A malformed snapshot is still retained and scores 0, per benchmark policy.
        s["submissions"].append({"after_probes": len(s["probes"]), "submission": body})
        write_json(path, s)
        return {"saved": len(s["submissions"]), "after_probes": len(s["probes"]),
                "schema_warning": error, "hidden_score_revealed": False}
    raise ValueError("Unknown endpoint")


def serve(root: Path, host: str = "127.0.0.1", port: int = 8787) -> None:
    class Handler(BaseHTTPRequestHandler):
        def _json(self, status: int, obj: dict) -> None:
            data = json.dumps(obj).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _execute(self):
            path = urlparse(self.path)
            action = path.path.strip("/")
            if action not in {"task", "probe", "snapshot"}:
                return self._json(404, {"error": "Not found"})
            session = parse_qs(path.query).get("session", [None])[0]
            if not session:
                return self._json(400, {"error": "Missing session query parameter"})
            token_header = self.headers.get("Authorization", "")
            token = token_header[7:] if token_header.startswith("Bearer ") else ""
            if action == "task" and self.command != "GET":
                return self._json(405, {"error": "Use GET"})
            if action != "task" and self.command != "POST":
                return self._json(405, {"error": "Use POST"})
            body = None
            if self.command == "POST":
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 131072:
                    return self._json(413, {"error": "Invalid request size"})
                try:
                    body = json.loads(self.rfile.read(size).decode("utf-8"))
                except (ValueError, UnicodeError):
                    return self._json(400, {"error": "Malformed JSON"})
            try:
                result = process(root, session, token, action, body)
                self._json(200, result)
            except PermissionError as e:
                self._json(401, {"error": str(e)})
            except (ValueError, KeyError) as e:
                self._json(400, {"error": str(e)})

        def do_GET(self):
            self._execute()

        def do_POST(self):
            self._execute()

        def log_message(self, fmt, *args):
            return

    server = HTTPServer((host, port), Handler)
    print(f"Trusted probe server listening at http://{host}:{port}", flush=True)
    print("Never expose this server or its private/ directory to untrusted networks.", flush=True)
    try:
        server.serve_forever(poll_interval=.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
