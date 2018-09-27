#!/usr/bin/env python3

import matplotlib; matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import math

def lineGraph(output, series, bounds, ylabel, title):
  """Plot line chart with the given values and output to the given file."""
  plt.figure(figsize = [16, 4])
  # Plot line series
  for s in series:
    plt.plot(s.xaxis, s.yaxis, '--', label = s.label)
    plt.legend(bbox_to_anchor = (1, 1), loc = 'upper left', borderaxespad = 0.)
  # Specify chart labels
  plt.xticks(np.arange(math.floor(bounds.xmin), math.ceil(bounds.xmax)))
  plt.yticks(np.arange(math.floor(bounds.ymin), math.ceil(bounds.ymax), (bounds.ymax - bounds.ymin) / 10))
  plt.ylabel(ylabel)
  plt.title(title)
  plt.savefig(output)
