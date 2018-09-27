#!/usr/bin/env python

import csv
import sys
import re

class Tokenizer:

  def __init__(self):
    """Initialize tokenizer with empty stopwords and words tables."""
    self.words = {}
    self.stopwords = []

  def add_stopwords(self, stopwords):
    """Read from stopwords.txt and add stop words to list of words to ignore."""
    with open(stopwords, 'r') as stream:
      for line in stream:
        self.stopwords.append(line.strip())

  def iterate_input(self, iterable):
    """Word generator given an input iterable."""
    for line in iter(iterable):
      line = line.strip()
      words = filter(None, re.split('[\W+_]', line))
      for word in words:
        word = word.lower()
        yield word

  def iterate_word(self, ordering):
    """Iterate over word-frequency pairs given an ordering."""
    for word in ordering:
      yield (word, self.words[word])

  def process_input(self, stream = sys.stdin):
    """Read input and count the number of words, excluding stop words."""
    for word in self.iterate_input(stream):
      if word not in self.stopwords and len(word) > 1:
        if word in self.words.keys():
          self.words[word] += 1
        else:
          self.words[word] = 1

  def most_frequent(self):
    """Sort the words by the most frequent first."""
    return sorted(self.words, key = self.words.get, reverse = True)

  def output_table(self, words, output = sys.stdout):
    """
      Outputs a comma-separated table of words and corresponding counts to the
      given output stream. Outputs ordering specified by the given words list.
    """
    fieldnames = ['Word', 'Frequency']
    writer = csv.DictWriter(output, fieldnames = fieldnames)
    writer.writeheader()
    for word, frequency in self.iterate_word(words):
      writer.writerow({'Word': word, 'Frequency': frequency})

  def print_table(self, words):
    """
      Print a comma-separated table of words and corresponding counts.
      Print ordering specified by the given words list.
    """
    self.output_table(words)

  def write_table(self, output, words):
    """
      Write a comma-separated table of words and corresponding counts to the given output file.
      Write words in ordering specified by the given words list.
    """
    with open(output, 'w') as f:
      self.output_table(words, f)

  def flush_words(self):
    """Clear dictionary of words-frequencies."""
    self.words = {}
