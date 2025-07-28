"""
Pipeline Flow to re-create for anywhere in UK (MedSat Limitation):

0) Change Config.py to required values
1) Get Location of City / Area and create BBOX
2) Divide BBox into sub area size (depends) - London is 8 Sub Boxes
3) Run QueryLondonOSM.txt script in Overpass turbo with each of these boxes and place in Datasets/{osm_query_boxes_path} as names in config.py
4) Run Combine Boxes in  MapPrep File.
5) Take file and run OSM Cycling Quality Index on in QGIS
6) Create {place}MSOA.csv File.
7) Get Boundary MSOA geojson data for region
8) Run ReduceRegion python file in MapPrep using previous MSOA file.
10) Add msoa_scores_{region}.csv file with headers = msoa,ScoreCQI,crash_rate,commute_rate,OverallCycleScore,ScoreCQIMean,index_length,index_space_syntax,index_space_syntax_length,commute_path
9) Run CQI/AddMSOAtoCQI.py -- WARNING this likely takes a while (ADDs THRESHOLD METRIC)
10) Run Divide LondonCQIBoxsMSOA.py to create geojson file for each MSOA way marks
11) Run MSOAAverageCQIScore.py For average CQI metric not threshold
12) Run CalculateCommuteMSOA.py
13) Run Calculate CrashMSOA.py crash rate
14) Space Syntax, Update extensions.py first
15) Space Syntax, spacesyntax.py
16) updateMSOA.py space syntax to get averages
17) Commute Route, path.py bit long
18) Overall (hmm not a fan of this one really)
17) Run Normalise.py in Score Rates
18) Run filter.py in MedSat to create corresponding health scores for the required MSOA's
19) Reduce, add space space syntax norm scores and reduced folder
20) Edit index.js to visualise

"""

from config import *
import os
import subprocess
import pandas as pd

def check_column_empty(df, col):
    return df[col].isnull().all()

# ======== Step 1 - Combine Query Boxes
# Check if folder for OSM query boxes exists
if not os.path.exists('Datasets/' + osm_query_boxes_path):
    print('Please create Overpass Query Boxes for the desired region')
    exit(0)

# ======== Step 2 - Run Combine Boxes in MapPrep
# Set the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create Folder for datasets in score scripts
if not os.path.exists(score_datasets_path):
    os.makedirs(score_datasets_path)
    print("Cycling Score Script Directory Created")

#Check if cycling quality index geojson file exists before combine
cycling_quality_index_file = os.path.join(score_datasets_path, 'cycling_quality_index.geojson')
if not os.path.exists(cycling_quality_index_file):
    combine_boxes_script = 'Score Scripts/MapPrep/CombineBoxes.py'
    result = subprocess.run(['python', combine_boxes_script, osm_query_boxes_path], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running CombineBoxes.py:", result.stderr)
    else:
        print("CombineBoxes.py executed successfully, Now Run OSM-Cyccling-Quality-Index - REMOVE MPH", result.stdout)
        exit(0)

#Check if cycling quality index geojson file exists
cycling_quality_index_file = os.path.join(score_datasets_path, 'cycling_quality_index.geojson')
if not os.path.exists(cycling_quality_index_file):
    print(f"cycling_quality_index.geojson does not exist within {score_datasets_path}. Please ensure it is generated before proceeding.")
    exit(0)

#Check if region_msoa_path exists in score_datasets_path
region_msoa_file = os.path.join(score_datasets_path, region_msoa_path)
if not os.path.exists(region_msoa_file):
    print(f"{region_msoa_path} does not exist within {score_datasets_path}. Please ensure it is generated before proceeding.")
    exit(0)
    

# Okay now we can get going
# ======== Step 3 score script and reduce region boundary

# Create Score Script
if not os.path.exists(score_datasets_path + '/' + msoa_score_path):
    with open(score_datasets_path + '/' + msoa_score_path, 'w') as f:
        f.write('msoa,ScoreCQI,crash_rate,commute_rate,OverallCycleScore,ScoreCQIMean,index_length,index_space_syntax,index_space_syntax_length,commute_path')

    # Load the existing score dataset
    score_df = pd.read_csv(os.path.join(score_datasets_path, msoa_score_path))

    # Copy the region MSOA dataset data in 'MSOA21CD' column into score_df column 'msoa'
    region_msoa_df = pd.read_csv(os.path.join(score_datasets_path, region_msoa_path))

    score_df['msoa'] = region_msoa_df['MSOA21CD']

    # Save the updated dataframe back to the CSV
    score_df.to_csv(os.path.join(score_datasets_path, msoa_score_path), index=False)

    print("New Score Dataset created and column msoa added to the score dataset.")

#Run Reduce region
script = 'Score Scripts/MapPrep/ReduceRegionPolygon.py'
polygon_path = f'Datasets/Filtered_{Region}_Polygon.geojson'
if not os.path.exists(polygon_path):
    result = subprocess.run(['python', script, region_msoa_path, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running reduce polygon:", result.stderr)
    else:
        print("Reduce executed successfully Filtered Polygon file created", result.stdout)
else:
    print(f'{polygon_path} Already Created')


#Step 4 ===== Run CQI Metrics
#Check if folder exists first with msoa's broken up
msoa_folder_path = f'Datasets/{Region}_cqi_jsons_msoa'
if not os.path.exists(msoa_folder_path):
    print('Creating CQI Metrics')
    # Input console type y to continue n to skip
    user_input = input("Do you want to continue with the CQI Metrics MSOA calculation (WARNING SLOW TO RUN)? (y/n): ")

    if user_input.lower() == 'y':
        cqi_script = 'Score Scripts/CQI/AddMSOAtoCQI.py'
        result = subprocess.run(['python', cqi_script, Region], capture_output=True, text=True)

        if result.returncode != 0:
            print("Error running AddMSOAtoCQI.py:", result.stderr)
        else:
            print("CQI Metrics calculation completed successfully:", result.stdout)
    else:
        print("CQI Metrics calculation skipped.")


#Step 4 ===== Break up CQI geojson into separate files for each msoa
if not os.path.exists(msoa_folder_path):
    script = 'Score Scripts/CQI/DivideCQIBoxesMSOA.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running AddMSOAtoCQI.py:", result.stderr)
    else:
        print("CQI Successfully broken up into MSOA regions:", result.stdout)
else:
    print(f"Folder already exists at {msoa_folder_path}")


# Step 5  ===== stage 11 in the pipeline process
df = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])
if check_column_empty(df, 'ScoreCQIMean'):
    script = 'Score Scripts/CQI/MSOAAverageCQIScore.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running AddMSOAtoCQI.py:", result.stderr)
    else:
        print("Average CQI Scores Added", result.stdout)
else:
    print('Average CQI Score already create, or incorrect formating in csv folder check')

# Threshold scores
if check_column_empty(df, 'ScoreCQI'):
    script = 'Score Scripts/CQI/AddThresholdScores.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running Add Threshold Score py:", result.stderr)
    else:
        print("Average CQI Scores Added", result.stdout)
else:
    print('Threshold scores already created, or incorrect formating in csv folder check')

# Step 6 ===== stage 12 and 13
if check_column_empty(df, 'crash_rate'):
    script = 'Score Scripts/CrashRate/CalculateCrashMSOA.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error calculating crash rate", result.stderr)
    else:
        print("Crash Rate Added", result.stdout)
else:
    print('Crash Rate Score already create, or incorrect formating in csv folder check')

if check_column_empty(df, 'commute_rate'):
    script = 'Score Scripts/CommuteRate/CalculateCommuteMSOA.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error calculating commute rate", result.stderr)
    else:
        print("Commute Rate added", result.stdout)
else:
    print('Commute Score already created, or incorrect formating in csv folder check')


# Step 7 Space Syntax ===== stage 14, 15, 16
if check_column_empty(df, 'index_space_syntax'):
    script = 'Score Scripts/SpaceSyntax and Length/updateExtensions.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error update extensions", result.stderr)
    else:
        print("Extensions updated", result.stdout)

    script = 'Score Scripts/SpaceSyntax and Length/spacesyntax.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Errors in space syntax calculation", result.stderr)
    else:
        print("Space Syntax Calculated", result.stdout)

    script = 'Score Scripts/SpaceSyntax and Length/updateMSOA.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error mean space syntax scores", result.stderr)
    else:
        print("Mean space syntax scores calculated", result.stdout)

# Step 8 Commute Path 
if check_column_empty(df, 'commute_path'):
    script = 'Score Scripts/Commute Route/path.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error in commute path calculation", result.stderr)
    else:
        print("Commute path scores added", result.stdout)

# Step 9 Overall score ?
if check_column_empty(df, 'OverallCycleScore'):
    script = 'Score Scripts/OverallCycleScore.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error in overall score", result.stderr)
    else:
        print("Overall scores added", result.stdout)

# Step 10 Normalize
if not os.path.exists(score_datasets_path + '/' + f"{Region}_msoa_scores_zscaled.csv"):
    script = 'Score Scripts/Normalize.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Error in normalization", result.stderr)
    else:
        print("Normalized scores created", result.stdout)

# Step 11 MedSat data
# Create folder
medsat_folder_path = f'MedSat/{Region}/'
if not os.path.exists(medsat_folder_path):
    os.makedirs(medsat_folder_path)
    print(f"Folder created at {medsat_folder_path}")

# Run filter.py
if not os.path.exists(medsat_folder_path + '/' + 'msoa_medsat_scores.csv'):
    script = 'MedSat/filter.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Medsat Score creation error", result.stderr)
    else:
        print("Medsat scores created!", result.stdout)

# Run normalize
if not os.path.exists(medsat_folder_path + '/' + 'msoa_medsat_scores_zscaled.csv'):
    script = 'MedSat/Normalize.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Medsat Score normalization error", result.stderr)
    else:
        print("Medsat scores normalized!", result.stdout)

# Run reduce norm and reduce file
if not os.path.exists(f'Datasets/{Region}_cqi_jsons_msoa_REDUCED'):
    script = 'Datasets/normalizeSpaceSyntax.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("Space Syntax Normalization error", result.stderr)
    else:
        print("Space Syntax scores normalized", result.stdout)

    script = 'Datasets/reduce.py'
    result = subprocess.run(['python', script, Region], capture_output=True, text=True)

    if result.returncode != 0:
        print("reduce file error", result.stderr)
    else:
        print("reduced file created", result.stdout)

print("Done")