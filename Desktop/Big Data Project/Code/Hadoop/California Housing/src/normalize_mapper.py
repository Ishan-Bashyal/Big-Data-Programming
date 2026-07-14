#!/usr/bin/env python3
"""
Job 1 Mapper: reads CSV rows, emits (feature_index, value) for each feature.
"""
import sys
import csv

FEATURE_COUNT = 8  # all columns except median_house_value

def main():
    reader = csv.reader(sys.stdin)
    header_skipped = False
    for row in reader:
        if not header_skipped:
            header_skipped = True
            continue
        if len(row) < 9:
            continue
        try:
            values = [float(v) for v in row[:9]]
        except ValueError:
            continue
        for i in range(FEATURE_COUNT):
            print(f"{i}\t{values[i]}")

if __name__ == "__main__":
    main()
