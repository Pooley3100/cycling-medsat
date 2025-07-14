//London Coords
let ldn_coords = [51.485, -0.09];
//Birmingham Coords
let bir_coords = [52.45,-1.85];
//Bristol Coords
let brist_coord = [51.4701862,-2.5957059];
//Leeds Coords
let leeds_coords = [53.7789516,-1.5475212];
//Manchester Coords
let man_coords = [53.4655819,-2.2480237];

// ===== Edit
let region = 'London';
// =====

let coords;

switch (region) {
    case 'London':
        coords = ldn_coords;
        break;
    case 'Birmingham':
        coords = bir_coords;
        break;
    case 'Bristol':
        coords = brist_coord;
        break;
    case 'Leeds':
        coords = leeds_coords;
        break;
    case 'Manchester':
        coords = man_coords;
        break;
    default:
        coords = ldn_coords;
}

let map = L.map('map').setView(coords, 11); // Set initial view (latitude, longitude, zoom)

msoa_scores = {};
selectedMSOA = null;
selectedScore = 'Overall';

let github_append = ''

let msoa_scores_path = github_append+`Score Scripts/${region}Datasets/${region}_msoa_scores_zscaled.csv`;
let medsat_msoa_scores_path = github_append+`MedSat/${region}/msoa_medsat_scores_zscaled.csv`;
let polygon_path = github_append+`Datasets/Filtered_${region}_Polygon.geojson`;
let cqiRegion = `${region}_cqi_jsons_msoa_REDUCED`;

// Load the CSV file containing MSOA scores
function initialise_scores_and_map(){
    fetch(msoa_scores_path)
        .then(response => response.text())
        .then(data => {
            const rows = data.split('\n').slice(1); // Skip header row

            rows.forEach(row => {
                const columns = row.split(',');

                // Ensure the row has at least 5 columns
                if (columns.length < 5) {
                    console.warn('Skipping invalid row:', row);
                    return;
                }

                const msoaCode = columns[0].trim();
                const overall = parseFloat(columns[1].trim());
                const CQIscore = parseFloat(columns[2].trim()); // Convert to number !!!!
                const mean_CQIscore = parseFloat(columns[3].trim());
                const commute_path = parseFloat(columns[4].trim());
                const commute_rate = parseFloat(columns[5].trim());
                const crash_rate = parseFloat(columns[6].trim());
                const index_length = parseFloat(columns[7].trim());
                const index_space_syntax = parseFloat(columns[8].trim());
                const index_space_syntax_length = parseFloat(columns[9].trim());

                const cycle_scores = { "CQIScoreThresh": CQIscore, "CrashRate": crash_rate, "CommuteRate": commute_rate, "Overall": overall, "MeanCQIScore": mean_CQIscore, "IndexLength":index_length, "IndexSpaceSyntax":index_space_syntax, "SpaceSyntaxLength":index_space_syntax_length, "CommutePath":commute_path };
                if (msoaCode in msoa_scores) {
                    Object.assign(msoa_scores[msoaCode], cycle_scores);
                } else {
                    msoa_scores[msoaCode] = cycle_scores;
                }
            });
        })
        .then(get_medsat_scores())
        .then(initmap())
        .catch(error => console.error('Error loading CQI CSV:', error));
}


function get_medsat_scores(){
    fetch(medsat_msoa_scores_path)
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n').slice(1); // Skip header row

        rows.forEach(row => {
            const columns = row.split(',');

            // Ensure the row has at least 5 columns
            if (columns.length < 5) {
                console.warn('Skipping invalid row:', row);
                return;
            }
            const msoaCode = columns[0].trim();
            const healthScores = {
                OME: parseFloat(columns[1].trim()),
                anxiety: parseFloat(columns[2].trim()),
                asthma: parseFloat(columns[3].trim()),
                depression: parseFloat(columns[4].trim()),
                diabetes: parseFloat(columns[5].trim()),
                hypertension: parseFloat(columns[6].trim()),
                opioids: parseFloat(columns[7].trim()),
                total: parseFloat(columns[8].trim())
            };

            if (msoaCode in msoa_scores) {
                Object.assign(msoa_scores[msoaCode], healthScores);
            } else {
                msoa_scores[msoaCode] = healthScores;
            }

        });
    })
    .catch(error => console.error('Error loading MedSat CSV:', error))
}


//Openstreetmap add layer to leaflet
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


function setupColourmap(min = -3, max = 3, scheme = d3.interpolateRdBu) {
    /* Diverging scale centred on 0, Flips depending on value, goal is Blue GOOD, Red=BAD */
    if (['diabetes', 'CrashRate', 'OME', 'asthma', 'anxiety', 'depression', 'hypertension', 'opioids', 'total'].includes(selectedScore)) {
        [min, max] = [max, min];
    }
    return d3.scaleDiverging(scheme)
        .domain([min, 0, max])  
        .clamp(true);            // clip out‑of‑range scores to the ends
}

function resetScores(){
    //Check if city changed
    switch (region) {
        case 'London':
            coords = ldn_coords;
            break;
        case 'Birmingham':
            coords = bir_coords;
            break;
        case 'Bristol':
            coords = brist_coord;
            break;
        case 'Leeds':
            coords = leeds_coords;
            break;
        case 'Manchester':
            coords = man_coords;
            break;
        default:
            coords = ldn_coords;
    }
    
    map.setView(coords, 11); // Update the view to the new coordinates
    
    msoa_scores = {};
    selectedMSOA = null;
    selectedScore = 'Overall';
    
    msoa_scores_path = `../Score Scripts/${region}Datasets/${region}_msoa_scores_zscaled.csv`;
    medsat_msoa_scores_path = `../MedSat/${region}/msoa_medsat_scores_zscaled.csv`;
    polygon_path = `../Datasets/Filtered_${region}_Polygon.geojson`;
    cqiRegion = `${region}_cqi_jsons_msoa`;
    
    // Reset the map by removing all layers
    map.eachLayer((layer) => {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });
    
    //WIll also run initmap
    initialise_scores_and_map();
}

function resetMap() {
    // Reset the map by removing all layers
    map.eachLayer((layer) => {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });
    
    //WIll also run initmap
    initmap();
}

// Load the GeoJSON file and add it as polygons to map
function initmap() {
    if(region != 'London'){
        fetch(polygon_path)
            .then(response => response.json())
            .then(data => {
                //Setup zColour
                const zColour = setupColourmap();
                // Add GeoJSON data to the map
                L.geoJSON(data, {

                    style: (feature) => {
                        if (feature.properties.MSOA21CD != selectedMSOA) {

                            if (!(feature.properties.MSOA21CD in msoa_scores)) {
                                return {}
                            }
                            //console.log("Colour is: ", zColour(msoa_scores[feature.properties.MSOA21CD][selectedScore]))
                            return {
                                color: 'blue', // Polygon border color
                                weight: 2,     // Border thickness
                                // fillColor: 'lightblue', // Fill color
                                fillColor: zColour(msoa_scores[feature.properties.MSOA21CD][selectedScore]),
                                fillOpacity: 0.7 // Fill opacity
                            }
                        } else {
                            return {};
                        }
                    },
                    onEachFeature: (feature, layer) => {
                        // Add a click event to each polygon
                        layer.on('click', () => {
                            selectedMSOA = feature.properties.MSOA21CD;
                            resetMap();
                            updateMSOAOverlay();
                            loadCycleQuality();
                            // Highlight the selected polygon
                            layer.setStyle({
                                color: '',
                                weight: 3,
                                fillOpacity: 0
                            });
                        });
                    }
                }).addTo(map);
            })
            .catch(error => console.error('Error loading GeoJSON:', error));
    } else{
        const polygonPaths = [
            `Datasets/Filtered_London_Polygon_ONE.geojson`,
            `Datasets/Filtered_London_Polygon_TWO.geojson`
        ];

        Promise.all(polygonPaths.map(path => 
            fetch(path)
            .then(response => response.json())
            .then(data => {
                //Setup zColour
                const zColour = setupColourmap();
                // Add GeoJSON data to the map
                L.geoJSON(data, {
                style: (feature) => {
                    if (feature.properties.MSOA21CD != selectedMSOA) {
                    if (!(feature.properties.MSOA21CD in msoa_scores)) {
                        return {}
                    }
                    return {
                        color: 'blue', // Polygon border color
                        weight: 2,     // Border thickness
                        fillColor: zColour(msoa_scores[feature.properties.MSOA21CD][selectedScore]),
                        fillOpacity: 0.7 // Fill opacity
                    }
                    } else {
                    return {};
                    }
                },
                onEachFeature: (feature, layer) => {
                    // Add a click event to each polygon
                    layer.on('click', () => {
                    selectedMSOA = feature.properties.MSOA21CD;
                    resetMap();
                    updateMSOAOverlay();
                    loadCycleQuality();
                    // Highlight the selected polygon
                    layer.setStyle({
                        color: '',
                        weight: 3,
                        fillOpacity: 0
                    });
                    });
                }
                }).addTo(map);
            })
            .catch(error => console.error('Error loading GeoJSON:', error))
        ));
    }

}

//Option box overlay here

L.Control.CustomOverlay = L.Control.extend({
    onAdd: function (map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');

        container.innerHTML = `
        <label for="cycleSelect">Choose Score:</label>
        <select id="mySelect" style="height: 40px;">
          <option value="Overall">Overall Score</option>
          <option value="CQIScoreThresh">Cycling Quality Index</option>
          <option value="CommuteRate">Commuter Rate</option>
          <option value="CrashRate">Crash Rate</option>
          <option value="MeanCQIScore">Mean CQI Scores</option>
          <option value="IndexSpaceSyntax">IndexSpaceSyntax</option>
          <option value="SpaceSyntaxLength">SpaceSyntaxLength</option>
          <option value="CommutePath">CommutePath</option>
          <option value="IndexLength">IndexLength</option>
          <option value="diabetes">Diabetes</option>
          <option value="OME">OME</option>
          <option value="anxiety">anxiety</option>
          <option value="asthma">asthma</option>
          <option value="depression">depression</option>
          <option value="hypertension">hypertension</option>
          <option value="opioids">opioids</option>
          <option value="total">total</option>
        </select>
          `;

        container.style.backgroundColor = 'white'; // Set background to white

        // Prevent map from reacting to events inside the control
        L.DomEvent.disableClickPropagation(container);

        return container;
    },
});
const scoreOverlay = new L.Control.CustomOverlay({ position: 'topleft' });
map.addControl(scoreOverlay);


//Logic for cycle score option select

const selectElement = document.getElementById('mySelect');
selectElement.addEventListener('change', (event) => {
    const selectedValue = event.target.value;
    console.log('Selected option:', selectedValue);
    selectedScore = selectedValue;
    resetMap();
});

const selectCity = document.getElementById('citySelector');
selectCity.addEventListener('change', (event) => {
    const selectedValue = event.target.value;
    console.log('Selected city:', selectedValue);
    region = selectedValue;

    resetScores();
});

// Selected MSOA Box Info
L.Control.CustomOverlay = L.Control.extend({
    onAdd: function (map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');

        container.innerHTML = `
        <div class="MSOA-Overlay">
            <p>Please click on a MSOA for more info</p>
        </div>
        <div class="Additional-Overlay">
            <p>Health Information</p>
        </div>
        `;

        container.style.backgroundColor = 'transparent'; 

        // Prevent map from reacting to events inside the control
        L.DomEvent.disableClickPropagation(container);

        return container;
    },
});
const msoaOverlay = new L.Control.CustomOverlay({ position: 'topright' });
map.addControl(msoaOverlay);


function updateMSOAOverlay() {
    const overlayContainer = document.querySelector('.MSOA-Overlay');
    const overlayHealthContainer = document.querySelector('.Additional-Overlay');
    if (overlayContainer) {
        overlayContainer.innerHTML = `
            <p><strong>Selected MSOA:</strong> ${selectedMSOA || 'None'}</p>
            <p><strong>Cycling Quality Index Threshold: ${msoa_scores[selectedMSOA].CQIScoreThresh.toFixed(3)}</strong></p>
            <p><strong>Commuter Rate: ${msoa_scores[selectedMSOA].CommuteRate.toFixed(3)}</strong></p>
            <p><strong>Crash Rate: ${msoa_scores[selectedMSOA].CrashRate.toFixed(3)}</strong></p>
            <p><strong>Overall Score: ${msoa_scores[selectedMSOA].Overall.toFixed(3)}</strong></p>
            <p><strong>Mean CQI Score: ${msoa_scores[selectedMSOA].MeanCQIScore.toFixed(3)}</strong></p>
            <p><strong>IndexSpaceSyntax: ${msoa_scores[selectedMSOA].IndexSpaceSyntax.toFixed(3)}</strong></p>
            <p><strong>IndexLength: ${msoa_scores[selectedMSOA].IndexLength.toFixed(3)}</strong></p>
            <p><strong>Commute Path: ${msoa_scores[selectedMSOA].CommutePath.toFixed(3)}</strong></p>
            
        `;
        overlayHealthContainer.innerHTML = `
            <p>Health Information</p>
            <p><strong>OME: ${msoa_scores[selectedMSOA].OME.toFixed(3)}</strong></p>
            <p><strong>asthma: ${msoa_scores[selectedMSOA].asthma.toFixed(3)}</strong></p>
            <p><strong>anxiety: ${msoa_scores[selectedMSOA].anxiety.toFixed(3)}</strong></p>
            <p><strong>depression: ${msoa_scores[selectedMSOA].depression.toFixed(3)}</strong></p>
            <p><strong>diabetes: ${msoa_scores[selectedMSOA].diabetes.toFixed(3)}</strong></p>
            <p><strong>hypertension: ${msoa_scores[selectedMSOA].hypertension.toFixed(3)}</strong></p>
            <p><strong>opioids: ${msoa_scores[selectedMSOA].opioids.toFixed(3)}</strong></p>
            <p><strong>total: ${msoa_scores[selectedMSOA].total.toFixed(3)}</strong></p>
        `;
    }
}

// Load the GeoJSON file with cycling quality info, needs filtering by MSOA, all of London is too slow
function loadCycleQuality() {
    fetch(`Datasets/${cqiRegion}/${selectedMSOA}.json`)
        .then(response => response.json())
        .then(data => {
            // Add theGeoJSON data to the map
            L.geoJSON(data, {
                style: feature => {
                    const index_level = feature.properties.index_10;
                    let colour;
                    switch (index_level) {
                        case 1: colour = 'red'; break;
                        case 2: colour = 'darkorange'; break;
                        case 3: colour = 'orange'; break;
                        case 4: colour = 'gold'; break;
                        case 5: colour = 'yellow'; break;
                        case 6: colour = 'lightyellow'; break;
                        case 7: colour = 'lightgreen'; break;
                        case 8: colour = 'mediumseagreen'; break;
                        case 9: colour = 'seagreen'; break;
                        case 10: colour = 'green'; break;
                        default: colour = 'gray';
                    }
                    return {
                        color: colour,
                        weight: 5,
                        opacity: 0.8
                    };
                },
            }).addTo(map);
        })
        .catch(error => console.error('Error loading GeoJSON:', error));

}

//I Box Logic
document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("popupIContainer");
    const popupButton = document.getElementById("iButton");
    document.addEventListener("click", () => {
        if (popup.style.display === "block") {
            popup.style.display = "none";
        }
    });
    popupButton.addEventListener("click", (event) => {
        event.stopPropagation();
        if (popup.style.display === "block") {
            popup.style.display = "none";
        } else {
            popup.style.display = "block";
        }
    });
});

document.addEventListener("click", (event) => {
    const popup = document.getElementById("popupIContainer");
    if (popup.style.display === "block") {
        popup.style.display = "none";
    }
});



initialise_scores_and_map();
