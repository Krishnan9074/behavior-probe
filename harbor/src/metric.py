# /// script
# requires-python = ">=3.10"
# ///
"""Dataset score: mean accuracy on the questions where the student errs (missing task = 0)."""
import argparse, json
ap = argparse.ArgumentParser(); ap.add_argument("-i"); ap.add_argument("-o")
args = ap.parse_args()
rows = [json.loads(l) for l in open(args.i) if l.strip()]
vals = [r or {} for r in rows]
def mean(k, keep_missing=True):
    xs = [v.get(k) for v in vals if keep_missing or v.get(k) is not None]
    xs = [x if x is not None else 0.0 for x in xs]
    return sum(xs) / len(xs) if xs else 0.0
out = {
    "score": 100 * mean("reward"),
    "overall_accuracy": 100 * mean("overall_accuracy", False),
    "familiar_error_accuracy": 100 * mean("familiar_error_accuracy", False),
    "transfer_error_accuracy": 100 * mean("transfer_error_accuracy", False),
    "brier": mean("brier", False),
    "probes_used": mean("probes_used", False),
    "valid_submissions": sum(1 for v in vals if v.get("valid")),
    "tasks": len(vals),
}
json.dump(out, open(args.o, "w"))
