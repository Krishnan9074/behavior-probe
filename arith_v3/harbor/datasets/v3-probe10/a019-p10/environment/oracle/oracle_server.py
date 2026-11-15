"""ARITH-PROBE v3 oracle sidecar: the only place the hidden student exists during the run.

POST /probe    {"op","a","b"} -> student's integer answer (budget, domain and held-out checks
               are the same as arithmetic_eval/server.py)
POST /snapshot {"predictions": [...]} -> stored with the current probe count; never scored here
GET  /log      -> probes + snapshots (read by the verifier after the agent finishes)
"""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, "/oracle")
from arithmetic_eval.grade import parse_predictions  # noqa: E402
from arithmetic_eval.student import OPS, answer  # noqa: E402

CASE = json.load(open("/oracle/case.json"))
QUESTIONS = CASE["test_questions"]
HELD_OUT = {(q["op"], q["a"], q["b"]) for q in QUESTIONS}
PROBES, SNAPSHOTS, LOCK = [], [], threading.Lock()


def probe(body):
    op, a, b = body.get("op"), body.get("a"), body.get("b")
    if (op not in OPS or type(a) is not int or type(b) is not int or
            not 0 <= a <= 1000000 or not 0 <= b <= 1000000 or (op == "div" and b == 0)):
        raise ValueError("Invalid operation or operands (op in add/sub/mul/div, 0 <= a,b <= 1000000)")
    if op == "sub" and a < b:
        raise ValueError("Subtraction requires a >= b")
    if op == "div" and a % b:
        raise ValueError("Division requires an exact integer quotient")
    if (op, a, b) in HELD_OUT:
        raise ValueError("Exact held-out question cannot be probed")
    with LOCK:
        if len(PROBES) >= CASE["budget"]:
            raise ValueError("Probe budget exhausted")
        y = answer(op, a, b, CASE["rules"][op])
        PROBES.append({"op": op, "a": a, "b": b, "student_answer": y})
        return {"op": op, "a": a, "b": b, "student_answer": y,
                "used": len(PROBES), "remaining": CASE["budget"] - len(PROBES)}


def snapshot(body):
    _, warning = parse_predictions(body, QUESTIONS)  # kept even if malformed: it scores 0
    with LOCK:
        SNAPSHOTS.append({"after_probes": len(PROBES), "submission": body})
        return {"saved": len(SNAPSHOTS), "after_probes": len(PROBES),
                "schema_warning": warning, "hidden_score_revealed": False}


class H(BaseHTTPRequestHandler):
    def send(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self.send(200, {"ok": True})
        if self.path == "/log":
            with LOCK:
                return self.send(200, {"budget": CASE["budget"], "probes": PROBES, "snapshots": SNAPSHOTS})
        self.send(404, {"error": "not found"})

    def do_POST(self):
        handler = {"/probe": probe, "/snapshot": snapshot}.get(self.path)
        if not handler:
            return self.send(404, {"error": "not found"})
        try:
            size = int(self.headers.get("Content-Length", 0))
            if not 0 < size <= 131072:
                raise ValueError("Invalid request size")
            body = json.loads(self.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError("JSON body must be an object")
            self.send(200, handler(body))
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            self.send(400, {"error": str(e)})

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()
