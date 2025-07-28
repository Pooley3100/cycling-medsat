# Pedal-Powered Insights: Localized Cycling Usage and Infrastructure Correlations with Public Health

# About
Urban planners and public health officials are increasingly investing in cycling infrastructure to promote
sustainable transportation and improve population health.
However, the uneven distribution of biking amenities - such as varying quality bike lanes, shared-use
paths, and bike-share stations - is problematic as it may exacerbate existing health disparities.
This project examines the local relationship between cycling infrastructure and usage and their
impact on health outcomes, aiming to understand how access to cycling resources influences community
well-being.

![What the dashboard looks like](OverallExample.png)

# Todo's to run
To use run.py, this should run the user through the steps required to creat a cycling & health map for the region

## Steps user will need to take

1) Running Overpass turbo on desired region, potentiall in sub boxes if big (i.e London) and adding path name to config.py with overpass geojson boxes in.
2) Requires manually running OSM-Cycling-Quality-Index (UK edited script)(REMOVE MPH) in QGIS, also remove all mph mentions manually in geojson <---
3) Creating MSOA region file for desired region, this file is created but need to be filled in by the user

# Result msoa_scores csv file, medsat_msoa_scores.csv file. AND boundary output_jsons_msoa file with msoa each way CQI scores

Seven cities currently included are Bristol, London, Birmingham, Manchester, Liverpool, Sheffield, Leeds

## Cycling Score Metrics by MSOA:

All scores are stored in msoa_scores.csv and then Z-based normalized are stored in msoa_scores_zscaled.csv for each dataset:
1) Overall - Necessary?
2) Commuter Rate
3) Crash Rate
4) CQI Threshold - % over 55 score
5) CQI Mean Score
6) CQI Mean and weighted by road length
7) CQI Mean weighted by space syntax
8) CQI Mean weighted by space syntax and road length
9) Combine with Origin Destination Data for Commute Rate.


## Health Metrics by MSOA:
OME,anxiety,asthma,depression,diabetes,hypertension,opioids,total

## Cities currently included
London, Birmingham, Leeds, Liverpool, Sheffield, Manchester, Bristol

