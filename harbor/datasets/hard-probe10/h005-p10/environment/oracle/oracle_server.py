"""Oracle sidecar: POST /probe {a,b} -> student's answer; GET /log -> probes so far.
Enforces the budget and refuses held-out test questions."""
import json, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path.insert(0, "/oracle")
import hard_probe as hp
CASE = json.load(open("/oracle/case.json"))
COMPS = [tuple(c) for c in CASE["rule"]["components"]]
FORBIDDEN = {tuple(x) for x in CASE["forbidden"]}
LOG, LOCK = [], threading.Lock()

class H(BaseHTTPRequestHandler):
    def send(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path == "/log":
            with LOCK:
                return self.send(200, {"budget": CASE["budget"], "probes": LOG})
        self.send(200, {"ok": True}) if self.path == "/health" else self.send(404, {"error": "not found"})
    def do_POST(self):
        if self.path != "/probe":
            return self.send(404, {"error": "not found"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            a, b = int(body["a"]), int(body["b"])
            if not (100 <= a <= 99999 and 0 <= b <= a):
                raise ValueError("Probe must use 3- to 5-digit A, with 0 <= B <= A")
            if (a, b) in FORBIDDEN:
                raise ValueError("Cannot probe a held-out test question")
            with LOCK:
                if len(LOG) >= CASE["budget"]:
                    raise ValueError("No probes remaining")
                ans = hp.simulate(a, b, COMPS)
                LOG.append({"a": a, "b": b, "student_answer": ans})
                left = CASE["budget"] - len(LOG)
            self.send(200, {"a": a, "b": b, "student_answer": ans, "remaining": left})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            self.send(400, {"error": str(e)})
    def log_message(self, *a):
        pass

ThreadingHTTPServer(("0.0.0.0", 8000), H).serve_forever()
