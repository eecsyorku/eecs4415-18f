#!/bin/bash

WEBROOT="http://data.ec.gc.ca/data/substances/monitor/great-lakes-water-quality-monitoring-and-aquatic-ecosystem-health-data/great-lakes-water-quality-monitoring-and-surveillance-data"
LAKES="LAKE_ONTARIO,LAKE_ERIE,LAKE_HURON,LAKE_SUPERIOR,GEORGIAN_BAY"

if [[ ! -d ./downloads ]]; then
  curl --create-dirs \
       -o ./downloads/data/#1.csv "$WEBROOT/{$LAKES}_Water_Quality_2000-present.csv" \
       -o ./downloads/columns.csv "$WEBROOT/Great_Lakes_Offshore_Header_Column_Descriptions.csv" \
       -o ./downloads/codes.csv   "$WEBROOT/Great_Lakes_Offshore_Water_Quality_Method_Codes.csv"
fi
