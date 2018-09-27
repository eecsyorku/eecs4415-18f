#!/usr/bin/env python3

import sys
import lakes

from os import path

__dirpath__ = path.dirname(__file__)

def main():
  codes = sys.argv[1:]
  outputpath = path.join(__dirpath__, '../outputs')
  dataobj = lakes.GreatLakesData('../downloads')
  for code, codeobj in dataobj.codes.items():
    if code not in codes: continue
    print("Generating (%s) %s..." % (code, codeobj['FULL_NAME']))
    aggregate = dataobj.aggregateByCode(code)
    aggregate.plot(path.join(outputpath, "%s %s.png" % (code, codeobj['FULL_NAME'])), codeobj['UNITS'], codeobj['FULL_NAME'])

if __name__ == "__main__":
  main()
