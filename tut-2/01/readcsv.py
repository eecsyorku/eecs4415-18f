#!/usr/bin/env python

import csv
import sys

# open and read text from 'input.txt'
with open('inputs/input.csv', 'r') as csvfile:
  # parse into rows, input comes from CSV file
  rows = csv.DictReader(csvfile)
  # configure output CSV writer
  writer = csv.DictWriter(sys.stdout, fieldnames = ['First Name', 'Last Name', 'Email'])
  writer.writeheader()
  # for each row in the CSV
  for row in rows:
    # write the results to STDOUT (standard output)
    writer.writerow({ 'First Name': row['first_name'],
                      'Last Name': row['last_name'],
                      'Email': row['email'] })
