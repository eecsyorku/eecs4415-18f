#!/usr/bin/env python3

import os
import mimetypes
import collections
import csv
import plot

from os import path
from collections import OrderedDict, namedtuple
from datetime import datetime

__dirpath__ = path.dirname(__file__)

class GreatLakesData:
  """
    Great Lakes Water Quality Monitoring and Surveillance Data.

    Water quality and ecosystem health data collected in the Great Lakes and
    priority tributaries to determine baseline water quality status, long term
    trends and spatial distributions, the effectiveness of management actions,
    determine compliance with water quality objectives and identify emerging
    issues are included in this dataset.

    Source: http://data.ec.gc.ca/data/substances/monitor/
            great-lakes-water-quality-monitoring-and-aquatic-ecosystem-health-data/
            great-lakes-water-quality-monitoring-and-surveillance-data/
  """

  def __init__(self, downloadsroot):
    """
      Initialize GreatLakesData class with an array of dataset labels (lakes),
      a dictionary of measurement codes and asssociated descriptions and attributes,
      and a dictionary of column names in the dataset and associated descriptions
      and metadata attributes.
    """
    self.downloadsroot = path.join(__dirpath__, downloadsroot)
    self.dataroot = path.join(self.downloadsroot, 'data')
    self.lakes = self._getLakes(self.dataroot)
    self.codes = self._getCodes(path.join(self.downloadsroot, 'codes.csv'))
    self.columns = self._getColumns(path.join(self.downloadsroot, 'columns.csv'))

  def _getLakes(self, dataroot):
    """
      Returns a list of dataset labels (lakes) found within the dataroot.

      For each file / directory in the given dataroot path, test if
      the path f is a file and is of type CSV. If the file is a CSV,
      append its basename, without .csv extension to list to be returned.
    """
    lakes = []
    for f in os.listdir(dataroot):
      f = path.join(dataroot, f)
      if path.isfile(f) and mimetypes.guess_type(f)[0] == 'text/csv':
        lakes.append(path.splitext(path.basename(f))[0])
    return lakes

  def _getCodes(self, filepath):
    """
      Returns an ordered dictionary of measurement codes and
      asssociated descriptions and attributes in CSV at given filepath.
      Reads CSV and adds the row to the ordered dictionary mapped to the
      associated code if code is not empty string.
    """
    codes = OrderedDict()
    with open(filepath, 'r', encoding = 'windows-1250') as csvfile:
      for row in csv.DictReader(csvfile):
        if not row['CODE']: continue
        codes[row['CODE']] = row
    return codes

  def _getColumns(self, filepath):
    """
      Returns an ordered dictionary of column names in the dataset and
      associated descriptions and metadata attributes in CSV at given filepath.
      Reads CSV and adds the row to the ordered dictionary mapped to the
      associated column if column header is not empty string.
    """
    columns = OrderedDict()
    with open(filepath, 'r', encoding = 'windows-1250') as csvfile:
      for row in csv.DictReader(csvfile):
        if not row['Header']: continue
        columns[row['Header']] = row
    return columns

  def aggregateByCode(self, code):
    """
      Returns the aggregate for each lake dataset, for the specific given
      measurement method code, grouped by month and year as a new
      GreatLakesAggregate instance.
    """
    return GreatLakesAggregate(self, code)

  def aggregateByMethodName(self, method):
    """
      Returns the aggregate for each lake dataset, for a specific given
      measurement method name, grouped by month and year as a new
      GreatLakesAggregate instance. If the method does not match any known
      measurement method name, returns None.
    """
    for code, codeobj in self.codes.items():
      if codeobj['FULL_NAME'] == method: return self.aggregateByCode(code)
    return None

  def __str__(self):
    """Serializes this GreatLakesData object as a string."""
    return "Lakes: %s\n" % (str(self.lakes)) \
         + "Codes: %s\n" % (str(list(self.codes.keys()))) \
         + "Columns: %s\n" % (str(list(self.columns.keys())))

class GreatLakesAggregate:
  """
    Great Lakes Water Quality Monitoring and Surveillance Aggregated Data.
    This class aggregates the associated GreatLakesData for each lake dataset,
    for a specific given measurement method code, grouped by day.
  """

  def __init__(self, dataobj, code):
    """
      Initialize GreatLakesAggregate class with an associated GreatLakesData object,
      a measurement code to aggregate on, and a data structure (dict) of labels (lakes)
      each mapped to an ordered dictionary of daily to average values of the measurement
      duration that period.
    """
    self.dataobj = dataobj
    self.code = code
    self.aggregate = self._getAggregateAllDataset()
    self.series = self._getAllSeries(self.aggregate)
    self.bounds = self._computeBound(self.series)

  def _getAggregateAllDataset(self):
    """
      Returns a dictionary of labels (lakes) each mapped to an ordered
      dictionary of daily to average values of the measurement duration
      that period.
    """
    aggregate = {}
    for lake in self.dataobj.lakes:
      aggregate[lake] = self._getSortedAggregateSingleDataset(path.join(self.dataobj.dataroot, "%s.csv" % lake))
    return aggregate

  def _getSortedAggregateSingleDataset(self, filepath):
    """
      Returns a sorted, ordered dictionary of daily to average values of
      the measurement duration that period for the given dataset.
    """
    return OrderedDict(sorted(self._getAggregateSingleDataset(filepath).items(), key = lambda t: t[0]))

  def _getAggregateSingleDataset(self, filepath):
    """
      Returns an unsorted, ordered dictionary of daily to average values of
      the measurement duration that period for the given dataset.
    """
    states = {}
    aggregate = {}
    AggregateState = namedtuple('AggregateState', ['count', 'subtotal'])
    with open(filepath, 'r', encoding = 'windows-1250') as csvfile:
      for row in csv.DictReader(csvfile):
        if row['CODE'] != self.code: continue
        date = datetime.strptime(row['STN_DATE'], '%Y-%m-%d %H:%M:%S.%f')
        datekey = date.year + (float(date.month) + (float(date.day) / 30)) / 12
        if datekey not in states: states[datekey] = AggregateState(0, 0)
        count, subtotal = states[datekey]
        states[datekey] = AggregateState(count + 1, subtotal + float(row['VALUE']))
    for datekey, state in states.items():
      aggregate[datekey] = state.subtotal / state.count
    return aggregate

  def _getAllSeries(self, aggregate):
    """
      Returns a list of namedtuple of (label, xaxis, yaxis).
      Labels (lakes), xaxis is a list of x values and
      yaxis is a list of y values.
    """
    series = []
    for lake in self.dataobj.lakes:
      if not len(aggregate[lake].keys()): continue
      series.append(self._getSeries(aggregate[lake], lake))
    return series

  def _getSeries(self, aggregate, label):
    """
      Returns a namedtuple of (label, xaxis, yaxis) given a
      dictionary of daily to average values of the measurement duration
      that period and the label.
    """
    x = []
    y = []
    Series = namedtuple('Series', ['label', 'xaxis', 'yaxis'])
    for date, value in aggregate.items():
      x.append(date)
      y.append(value)
    return Series(label, x, y)

  def _computeBound(self, series):
    """
      Returns a namedtuple of the minimum and maximum values in the X- and
      Y-axes for all given series.
    """
    xmin = ymin = float('inf')
    xmax = ymax = float('-inf')
    Bound = namedtuple('Bound', ['xmin', 'xmax', 'ymin', 'ymax'])
    for s in series:
      xmin = min([xmin, min(s.xaxis)])
      xmax = max([xmax, max(s.xaxis)])
      ymin = min([ymin, min(s.yaxis)])
      ymax = max([ymax, max(s.yaxis)])
    return Bound(xmin, xmax, ymin, ymax)

  def plot(self, outputpath, ylabel, title):
    """
      Plot the values on a line graph. A line series for each dataset (lake).
      xaxis is the datetime interval and the y-axis is the values in
      the measurement code's specified units.
    """
    if len(self.series):
      plot.lineGraph(outputpath, self.series, self.bounds, ylabel, title)

  def __str__(self):
    """Serializes this GreatLakesAggregate object as a string."""
    return "Code: %s\n" % (str(self.code)) \
         + "Method: %s\n" % (str(self.dataobj.codes[self.code]['FULL_NAME'])) \
         + "Aggregate: %s\n" % (str(self.aggregate)) \
         + "Aggregate (Table): %s\n" % (str(self.table)) \
         + "Aggregate (Transposed): %s\n" % (str(self.transposed))
