#!/usr/bin/env python

# open and read text from 'input.txt'
with open('inputs/input.txt', 'r') as f:
  # input comes from file
  for line in f:
    # remove leading and trailing whitespace
    line = line.strip()
    # write the results to STDOUT (standard output)
    print(line)
