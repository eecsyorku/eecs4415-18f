# Example 3: Great Lakes Water Quality (Tutorial 2)

Great Lakes Water Quality Monitoring and Surveillance Data

Water quality and ecosystem health data collected in the Great Lakes and
priority tributaries to determine baseline water quality status, long term
trends and spatial distributions, the effectiveness of management actions,
determine compliance with water quality objectives and identify emerging
issues are included in this dataset.

**Source**: [Government of Canada][1]
**Datasets**: 5 (Lake Ontario, Lake Erie, Lake Huron, Lake Superior, and Georgian Bay)
**Note"": Contains 2106 different measurement methods (codes) for assessing water quality
**Format**: CSV

## Objective

Select a few methods, and output a line graph of the daily averages of
the measurement over time. Visualize the change in the measurements.

## Demonstrates

- Handling command line arguments
- Working with multiple dataset files
- Reading and parsing multiple CSV files
- Multiple classes
- Plotting line graphs with `matplotlib`

## Usage

- Start Python Docker container with volume mounted
- Run `./start.sh` to download the datasets and install the python library dependencies
- Run `python src/main.py` with method codes as arguments. For instance:
  - **245** -- `OXYGEN,CONCENTRATION DISSOLVED`
  - **247** -- `OXYGEN,% SAT. DISSOLVED`
  - **270** -- `AMMONIA NITROGEN,SOLUBLE`
- Output graphs should be found in the `outputs/` directory.

```
$ docker run -it –v $PWD:/usr/src/app –w /usr/src/app python bash
root:/usr/src/app# ls -la
root:/usr/src/app# ./start.sh
root:/usr/src/app# python src/main.py 245 247 270
root:/usr/src/app# ls -la outputs/
```

[1]: http://data.ec.gc.ca/data/substances/monitor/great-lakes-water-quality-monitoring-and-aquatic-ecosystem-health-data/great-lakes-water-quality-monitoring-and-surveillance-data/
