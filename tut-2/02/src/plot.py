#!/usr/bin/env python

import matplotlib; matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

def plot_figure(output, keys, values, ylabel, title):
  """Plot bar chart with the given values and output to the given file."""
  ypos = np.arange(len(keys))
  plt.figure()
  plt.bar(ypos, values, align = 'center', alpha = 0.5)
  plt.xticks(ypos, keys, rotation = 45)
  plt.ylabel(ylabel)
  plt.title(title)
  plt.subplots_adjust(bottom = 0.2)
  plt.savefig(output)
