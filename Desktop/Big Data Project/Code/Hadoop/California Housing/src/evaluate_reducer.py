#!/usr/bin/env python3
"""
Job 4 Reducer: reads (row_id, actual, predicted), computes evaluation metrics.
"""
import sys, math

def main():
    actuals, predictions = [], []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        try:
            actuals.append(float(parts[1]))
            predictions.append(float(parts[2]))
        except ValueError:
            continue

    n = len(actuals)
    if n == 0:
        print("No predictions found.")
        return

    mse  = sum((a - p) ** 2 for a, p in zip(actuals, predictions)) / n
    rmse = math.sqrt(mse)
    mae  = sum(abs(a - p) for a, p in zip(actuals, predictions)) / n
    y_mean = sum(actuals) / n
    ss_tot = sum((a - y_mean) ** 2 for a in actuals)
    ss_res = sum((a - p) ** 2 for a, p in zip(actuals, predictions))
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    print("=" * 55)
    print("  California House Price Prediction — Evaluation")
    print("=" * 55)
    print(f"  Samples   : {n}")
    print(f"  MSE       : {mse:,.2f}")
    print(f"  RMSE      : ${rmse:,.2f}")
    print(f"  MAE       : ${mae:,.2f}")
    print(f"  R² Score  : {r2:.4f}")
    print("=" * 55)
    print("\nSample predictions (first 10):")
    print(f"  {'Actual':>14}  {'Predicted':>14}  {'Error':>14}")
    for a, p in zip(actuals[:10], predictions[:10]):
        print(f"  ${a:>12,.0f}  ${p:>12,.0f}  ${abs(a-p):>12,.0f}")

if __name__ == "__main__":
    main()
