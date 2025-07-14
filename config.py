# Configuration settings for Cycling Quality Index

#   ======> Edit <========
#Region = 'Birmingham'
# Region = 'Bristol'
# Region = 'Leeds'
Region = 'Manchester'

#Add path here for geojson's from Overpass Turbo
osm_query_boxes_path = f'{Region}-Overpass-Query-Boxes'
#   =======================

#Score Scripts File Path
score_datasets_path = f'Score Scripts/{Region}Datasets'

#Overall json file with CQI
cqi_scores_path = f'{Region}_cycling_quality_index_with_scores.geojson'

# Path for list of MSOA's to include
region_msoa_path = f"{Region}MSOA.csv"

# Path for msoa_scores
msoa_score_path = f"{Region}_msoa_scores.csv"  

