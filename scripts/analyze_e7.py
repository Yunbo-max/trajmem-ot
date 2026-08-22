#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def summarize(rows):
    result = []
    for k in range(1, len(rows[0]["sweep"])):
        values = [row["sweep"][k] for row in rows]
        q0 = np.asarray([row["q0"] for row in rows])
        qp = np.asarray([value["q_plus"] for value in values])
        qm = np.asarray([value["q_minus"] for value in values])
        random_pairs = [qp[i] > q for i, value in enumerate(values) for q in value["q_random"]]
        result.append({
            "rho": values[0]["rho"],
            "n_states": len(rows),
            "p_plus_gt_base": float(np.mean(qp > q0)),
            "p_plus_gt_minus": float(np.mean(qp > qm)),
            "p_plus_gt_random": float(np.mean(random_pairs)),
            "mean_delta_q": float(np.mean(qp - q0)),
            "median_delta_q": float(np.median(qp - q0)),
        })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = []
    for name in args.inputs:
        rows.extend(json.loads(line) for line in Path(name).read_text().splitlines() if line.strip())
    rows.sort(key=lambda row: row["index"])
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["task"]].append(row)
    losses = np.asarray([-row["q0"] for row in rows])
    threshold = float(np.median(losses))
    report = {
        "metric": "negative demonstration action MSE (offline geometry; not environment return)",
        "n_states": len(rows),
        "random_controls_per_state_radius": len(rows[0]["sweep"][1]["q_random"]),
        "overall": summarize(rows),
        "by_task": {name: summarize(part) for name, part in sorted(grouped.items())},
        "baseline_mse_median": threshold,
        "higher_mse_half": summarize([row for row in rows if -row["q0"] >= threshold]),
        "lower_mse_half": summarize([row for row in rows if -row["q0"] < threshold]),
    }
    # Deterministic descriptive selection: maximize plus-vs-minus, then
    # plus-vs-random, then choose the smaller radius on exact ties.  This is a
    # diagnostic choice, not a claim that the selected radius passed the gate.
    selected = max(report["overall"], key=lambda x: (x["p_plus_gt_minus"], x["p_plus_gt_random"], -x["rho"]))
    report["selected_rho"] = selected["rho"]
    report["gate_pass"] = bool(
        selected["p_plus_gt_base"] >= 0.65
        and selected["p_plus_gt_minus"] >= 0.65
        and selected["p_plus_gt_random"] >= 0.65
    )
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
