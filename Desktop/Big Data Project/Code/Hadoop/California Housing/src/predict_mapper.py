#!/usr/bin/env python3
"""
Job 3 Mapper: applies learned weights to each row, emits predictions.
Output: row_id  actual_price  predicted_price
"""
import sys, os, csv, json

FEATURE_COUNT = 8
LABEL_SCALE   = 100000.0

def load_weights():
    weights, bias = [0.0] * FEATURE_COUNT, 0.0
    for fname in ["weights.txt"]:
        if os.path.exists(fname):
            with open(fname) as f:
                d = json.load(f)
                weights = d.get("weights", weights)
                bias    = d.get("bias", bias)
            break
    return weights, bias

def load_stats():
    means = [0.0] * FEATURE_COUNT
    stds  = [1.0] * FEATURE_COUNT
    if os.path.exists("stats.txt"):
        with open("stats.txt") as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    idx = int(parts[0])
                    means[idx] = float(parts[1])
                    stds[idx]  = float(parts[2])
    return means, stds

def main():
    weights, bias = load_weights()
    means, stds   = load_stats()
    reader = csv.reader(sys.stdin)
    header_skipped = False
    row_id = 0

    for row in reader:
        if not header_skipped:
            header_skipped = True
            continue
        if len(row) < 9:
            continue
        try:
            raw = [float(v) for v in row[:9]]
        except ValueError:
            continue

        X     = [(raw[i] - means[i]) / stds[i] for i in range(FEATURE_COUNT)]
        y_act = raw[8]
        y_hat = (sum(weights[i] * X[i] for i in range(FEATURE_COUNT)) + bias) * LABEL_SCALE

        print(f"{row_id}\t{y_act:.2f}\t{y_hat:.2f}")
        row_id += 1

if __name__ == "__main__":
    main()
