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

1) Running Overpass turbo on desired region (creating a BBOX boundary), potentiall in sub boxes if big (i.e London) and adding the Region name to config.py with the path name to overpass geojson boxes in.
2) Run.py
2) Requires manually running OSM-Cycling-Quality-Index [https://www.osm-verkehrswende.org/cqi/] (UK edited script)(REMOVE MPH MANUALLY) in QGIS, read README within file, script modified for UK but ALL Accreditation goes to osm-verkehrswende. Essentially download [https://qgis.org/], load OSM-Cycling-Quality-Index folder, then load cycling_quality_index.py into the QGIS python scripts editor, make sure way_import.geojson, with mph removed, created by run.py is placed in data sub directory, then run the python file cycling_quality_index.py.
3) Creating MSOA.csv region file for desired region, this file is created but needs to be filled in by the user so the program know which MSOA boundaries to include, look at other Dataset files for an idea. (i.e. LondonMSOA.csv)
4) Scores should be created, to visualise edit top of index.js to include new location

Results = msoa_scores csv file, medsat_msoa_scores.csv file. AND boundary output_jsons_msoa file with msoa broken down into way scores.

## Cycling Score Metrics by MSOA:

All scores are stored in msoa_scores.csv and then Z-based normalized are stored in msoa_scores_zscaled.csv for each dataset:
1) Overall Cycle Score
2) Commuter Rate %
3) Crash Rate
4) CQI Threshold - % over 55 score
5) CQI Mean Score
6) CQI Mean and weighted by road length
7) CQI Mean weighted by space syntax
8) CQI Mean weighted by space syntax and road length (CQI Space Syntax)
9) Commute Path - Average CQI Space Syntax, Commute Rate, Crash Rate along most popular commute route


## Health Metrics by MSOA:
OME,anxiety,asthma,depression,diabetes,hypertension,opioids,total

## Cities currently included
London, Birmingham, Leeds, Liverpool, Sheffield, Manchester, Bristol

