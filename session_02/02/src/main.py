#!/usr/bin/env python

import os
import plot
import tokenizer

__dirpath__ = os.path.dirname(__file__)

def process_inputs(tk, stopwords, f_input):
  tk.add_stopwords(stopwords)
  tk.flush_words()
  with open(f_input, 'r') as f: tk.process_input(f)
  freq = tk.most_frequent()[:10]
  values = [tk.words[word] for word in freq]
  return (freq, values)

def main():
  tk = tokenizer.Tokenizer()
  stopwords = os.path.join(__dirpath__, '../inputs/stopwords.txt')
  f_input   = os.path.join(__dirpath__, '../inputs/book.txt')
  f_output  = os.path.join(__dirpath__, '../outputs/wordfreq.%s')
  freq, values = process_inputs(tk, stopwords, f_input)
  plot.plot_figure(f_output % 'png', freq, values, '#occurrence', 'Top 10 Words')
  tk.write_table(f_output % 'csv', freq)

if __name__ == "__main__":
  main()
