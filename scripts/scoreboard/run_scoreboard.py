#!/usr/bin/env python3
"""Compute benchmark scores for the public scoreboard.

Usage:
    python run_scoreboard.py ../submissions/raw_results.json

The metric implementations are provided by the compiled ``scoreboard_kernel``
extension that is distributed with the site toolchain.  The generated C file
next to this script is the source annotation snapshot from the build farm.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scoreboard_kernel as kernel  # noqa: E402

METRICS = {
    "micro_f1": kernel.micro_f1,
    "macro_f1": kernel.macro_f1,
    "weighted_f1": kernel.weighted_f1,
    "exact_match": kernel.exact_match,
    "pass_at_10": kernel.pass_at_k,
    "pass_at_4": kernel.pass_at_k,
    "mrr": kernel.mrr,
    "ndcg_at_10": kernel.ndcg_at_10,
    "precision_at_5": kernel.precision_at_5,
    "recall_at_10": kernel.recall_at_10,
    "mae_score": kernel.mae_score,
    "ece_score": kernel.ece_score,
    "balanced_accuracy": kernel.balanced_accuracy,
    "auc_roc": kernel.auc_roc,
    "map_at_5": kernel.map_at_5,
}


def score_submission(submission):
    metric = submission["metric"]
    if metric not in METRICS:
        raise SystemExit("unsupported metric: %s" % metric)
    return METRICS[metric](submission["data"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("submissions", help="raw submission payload JSON")
    parser.add_argument("--out", default="", help="optional output JSON path")
    args = parser.parse_args()

    payload = json.load(open(args.submissions, "r", encoding="utf-8"))
    rows = []
    for submission in payload["submissions"]:
        rows.append(
            {
                "task_id": submission["task_id"],
                "audit_status": submission["audit_status"],
                "metric": submission["metric"],
                "score": round(score_submission(submission), 3),
            }
        )
    print(json.dumps(rows, indent=2))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=2)


if __name__ == "__main__":
    main()
