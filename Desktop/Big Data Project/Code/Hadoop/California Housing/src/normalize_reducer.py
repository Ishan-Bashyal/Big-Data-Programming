#!/usr/bin/env python3
"""
Job 1 Reducer: receives sorted (feature_index, value) pairs.
Outputs: feature_index  mean  std  count
"""
import sys
import math

def emit_stats(feature_idx, values):
    n = len(values)
    if n == 0:
        return
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    std = math.sqrt(variance) if variance > 0 else 1.0
    print(f"{feature_idx}\t{mean:.6f}\t{std:.6f}\t{n}")

def main():
    current_feature = None
    values = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        feature_idx, value = int(parts[0]), float(parts[1])
        if current_feature is None:
            current_feature = feature_idx
        if feature_idx != current_feature:
            emit_stats(current_feature, values)
            current_feature = feature_idx
            values = []
        values.append(value)
    if current_feature is not None:
        emit_stats(current_feature, values)

if __name__ == "__main__":
    main()
