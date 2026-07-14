#!/usr/bin/env python3
"""
Mapper Script for Word Count
This script reads text from standard input, splits it into words,
and emits each word with a count of 1.
Output format: word\t1
"""

import sys

MIN_WORD_LENGTH = 3

# Read from standard input
for line in sys.stdin:
    # Remove leading/trailing whitespace
    line = line.strip()
    
    # Split line into words
    words = line.split()
    
    # Emit each word with count 1
    # Output format: word<TAB>1
    for word in words:
        # Convert to lowercase for case-insensitive counting
        word = word.lower()
        # Remove punctuation if needed (optional)
        # word = ''.join(c for c in word if c.isalnum())
        #print(f"{word}\t1")
        
        #Filter condition
        if len(word) >= MIN_WORD_LENGTH:
            print(f"{word}\t1")
        
