#!/usr/bin/env python3
"""
Job 2 Mapper: computes partial gradients for this data partition.
Reads weights.txt and stats.txt from the distributed cache.
Emits: grad  feature_index  delta_w  count
       grad_b  0  delta_b  count
"""
import sys, os, csv, json

FEATURE_COUNT = 8
LABEL_SCALE   = 100000.0

def load_weights():
    weights, bias = [0.0] * FEATURE_COUNT, 0.0
    if os.path.exists("weights.txt"):
        with open("weights.txt") as f:
            d = json.load(f)
            weights = d.get("weights", weights)
            bias    = d.get("bias", bias)
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
    dW = [0.0] * FEATURE_COUNT
    db = 0.0
    count = 0

    reader = csv.reader(sys.stdin)
    header_skipped = False
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

        X = [(raw[i] - means[i]) / stds[i] for i in range(FEATURE_COUNT)]
        y = raw[8] / LABEL_SCALE
        y_hat = sum(weights[i] * X[i] for i in range(FEATURE_COUNT)) + bias
        error = y_hat - y

        for i in range(FEATURE_COUNT):
            dW[i] += error * X[i]
        db += error
        count += 1

    if count > 0:
        for i in range(FEATURE_COUNT):
            print(f"grad\t{i}\t{dW[i]:.8f}\t{count}")
        print(f"grad_b\t0\t{db:.8f}\t{count}")

if __name__ == "__main__":
    main()
