#!/usr/bin/env python3
"""
Reducer Script for Word Count
This script reads key-value pairs from the mapper (sorted by Hadoop),
groups words together, and sums their counts.
Input format: word\t1 (one per line, sorted by word)
Output format: word\tcount
"""

import sys

current_word = None
current_count = 0

# Read from standard input (Hadoop sorts mapper output by key before sending to reducer)
for line in sys.stdin:
    # Remove leading/trailing whitespace
    line = line.strip()
    
    # Parse word and count from input
    # Format: word\t1
    try:
        word, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        # Skip malformed lines
        continue
    
    # Check if this is a new word
    if word != current_word:
        # Output the previous word and its total count
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        
        # Start counting the new word
        current_word = word
        current_count = 0
    
    # Add to the count for the current word
    current_count += count

# Output the last word and its total count
if current_word is not None:
    print(f"{current_word}\t{current_count}")
