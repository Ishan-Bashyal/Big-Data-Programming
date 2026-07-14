#!/usr/bin/env python3
"""
Job 2 Reducer: aggregates partial gradients, updates and saves new weights.
Writes weights_new.txt locally (then promoted to weights.txt between epochs).
"""
import sys, os, json

FEATURE_COUNT = 8
LEARNING_RATE = 0.01

def load_weights():
    weights, bias = [0.0] * FEATURE_COUNT, 0.0
    if os.path.exists("weights.txt"):
        with open("weights.txt") as f:
            d = json.load(f)
            weights = d.get("weights", weights)
            bias    = d.get("bias", bias)
    return weights, bias

def main():
    weights, bias = load_weights()
    sum_dW  = [0.0] * FEATURE_COUNT
    sum_db  = 0.0
    total_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 4:
            continue
        key, idx, grad_val, count = parts[0], int(parts[1]), float(parts[2]), int(parts[3])
        if key == "grad":
            sum_dW[idx] += grad_val
            total_count = max(total_count, count)
        elif key == "grad_b":
            sum_db += grad_val

    if total_count == 0:
        total_count = 1

    for i in range(FEATURE_COUNT):
        weights[i] -= LEARNING_RATE * (sum_dW[i] / total_count)
    bias -= LEARNING_RATE * (sum_db / total_count)

    with open("weights_new.txt", "w") as f:
        json.dump({"weights": weights, "bias": bias}, f, indent=2)

    for i, w in enumerate(weights):
        print(f"weight_{i}\t{w:.8f}")
    print(f"bias\t{bias:.8f}")
    print(f"total_samples\t{total_count}")

if __name__ == "__main__":
    main()
