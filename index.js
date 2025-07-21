//London Coords
let ldn_coords = [51.485, -0.09];
//Birmingham Coords
let bir_coords = [52.45, -1.85];
//Bristol Coords
let brist_coord = [51.4701862, -2.5957059];
//Leeds Coords
let leeds_coords = [53.7789516, -1.5475212];
//Manchester Coords
let man_coords = [53.4655819, -2.2480237];
//Sheffield Coords
let shef_coords = [53.3839402, -1.4542744];
//liverpool Coords
let liver_coords = [53.4072995, -2.9907975];

// ===== Edit
let region = 'London';
// =====

let coords;

let developerActive = false;

//Check if dev
const urlParams = new URLSearchParams(window.location.search);
developerActive = urlParams.has('dev') ? true : false;

let scoreDesc = {
    "CQIScoreThresh": "(Z Score) The percentage of total streets within the MSOA with a CQI Score over 55",
    "CrashRate": "(Z Score) The Number of Cycling Incidents (slight/serious/fatal) that have occurred within the MSOA",
    "CommuteRate": "(Z Score) The percentage of people who cycle to work",
    "Overall": "(Z Score) A combination of the Space Index Score + The commute rate score + the crash rate score ",
    "MeanCQIScore": "(Z Score) The average Cycling Quality Index Score of all ways in an MSOA ",
    "IndexLength": "(Z Score) The average Cycling Quality Index Score of all ways in an MSOA weighted by road length",
    "IndexSpaceSyntax": "(Z Score) The Cycling Quality Index Score of all ways weighted by the roads edge harmonic and betweenness centrality",
    "SpaceSyntaxLength": "(Z Score) The Cycling Quality Index Score of all ways weighted by the roads edge harmonic and betweenness centrality and weighted by road length",
    "CommutePath": "(Z Score) The average Space Index Length, crash rate and commute rate along the most popular commute route from the selected MSOA.",
    "diabetes": "(Z Score) The prescription rate of diabetes in the MSOA",
    "OME": "(Z Score) The prescription rate of OME medication in the MSOA",
    "asthma": "(Z Score) The prescription rate of asthma in the MSOA",
    "anxiety": "(Z Score) The prescription rate of anxiety disorders in the MSOA",
    "depression": "(Z Score) The prescription rate of depression in the MSOA",
    "hypertension": "(Z Score) The prescription rate of hypertension in the MSOA",
    "opioids": "(Z Score) The prescription rate of opioid use in the MSOA",
    "total": "(Z Score) The total health prescription rate in the MSOA"
};

//Used for zColour - Optional, currently not being used
let scoreColours = {
    "CQIScoreThresh": "#FF5733", // Red
    "CrashRate": "#C70039",      // Dark Red
    "CommuteRate": "#FFC300",    // Yellow
    "Overall": "#DAF7A6",        // Light Green
    "MeanCQIScore": "#33FF57",   // Green
    "IndexLength": "#33C1FF",    // Light Blue
    "IndexSpaceSyntax": "#3375FF", // Blue
    "SpaceSyntaxLength": "#335BFF", // Dark Blue
    "CommutePath": "#8E44AD",    // Purple
    "diabetes": "#E74C3C",       // Red
    "OME": "#F1C40F",            // Yellow
    "asthma": "#2ECC71",         // Green
    "anxiety": "#3498DB",        // Blue
    "depression": "#9B59B6",     // Purple
    "hypertension": "#E67E22",   // Orange
    "opioids": "#D35400",        // Dark Orange
    "total": "#34495E"           // Dark Gray
};

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
    case 'Sheffield':
        coords = shef_coords;
        break;
    case 'Liverpool':
        coords = liver_coords;
        break;
    default:
        coords = ldn_coords;
}

let map = L.map('map').setView(coords, 11); // Set to city loc and zoom

msoa_scores = {};
selectedMSOA = null;
selectedScore = 'Overall';

let msoa_scores_path = `Score Scripts/${region}Datasets/${region}_msoa_scores_zscaled.csv`;
let medsat_msoa_scores_path = `MedSat/${region}/msoa_medsat_scores_zscaled.csv`;
let polygon_path = `Datasets/Filtered_${region}_Polygon.geojson`;
let cqiRegion = `${region}_cqi_jsons_msoa_REDUCED`;

// Load the CSV file containing MSOA scores and then map (Starter Location)
function initialise_scores_and_map() {
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

                const cycle_scores = { "CQIScoreThresh": CQIscore, "CrashRate": crash_rate, "CommuteRate": commute_rate, "Overall": overall, "MeanCQIScore": mean_CQIscore, "IndexLength": index_length, "IndexSpaceSyntax": index_space_syntax, "SpaceSyntaxLength": index_space_syntax_length, "CommutePath": commute_path };
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


function get_medsat_scores() {
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
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

//CARTO basemap with positron (dark_all OR rastertiles/voyager OR ligh_all)
const cartoBasemap = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20,
    minZoom: 0
  }).addTo(map);


function setupColourmap(min = -3, max = 3, scheme = d3.interpolateRdBu) {
    /* Diverging scale centred on 0, Flips depending on value, goal is Blue GOOD, Red=BAD */
    if (['diabetes', 'CrashRate', 'OME', 'asthma', 'anxiety', 'depression', 'hypertension', 'opioids', 'total'].includes(selectedScore)) {
        [min, max] = [max, min];
        flipLegend(true);
    } else {
        //Catch DOM load test
        let test = document.getElementById('legendBox');
        if (test != null) {
            flipLegend(false);
        }
    }
    return d3.scaleDiverging(scheme)
        .domain([min, 0, max])
        .clamp(true);            // clip out‑of‑range scores to the ends
}

/* Alternative function for having one colour per score: */

// function setupColourmap(min = -4, max = 4) {
//     const baseColour = scoreColours[selectedScore] || "#888"; //Colour to interpolate
//     let [low, high] = [d3.color("black"), d3.color(baseColour)];

//     if (['diabetes', 'CrashRate', 'OME', 'asthma', 'anxiety', 'depression', 'hypertension', 'opioids', 'total'].includes(selectedScore)) {
//         [low, high] = [d3.color(baseColour), d3.color("white")];
//     }

//     return d3.scaleLinear()
//         .domain([min, max])
//         .range([low, high])
//         .interpolate(d3.interpolateRgb)
//         .clamp(true);
// }

function resetScores() {
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
        case 'Sheffield':
            coords = shef_coords;
            break;
        case 'Liverpool':
            coords = liver_coords;
            break;
        default:
            coords = ldn_coords;
    }

    map.setView(coords, 11); // Update the view to the new coordinates

    msoa_scores = {};
    selectedMSOA = null;
    //selectedScore = 'Overall';

    msoa_scores_path = `Score Scripts/${region}Datasets/${region}_msoa_scores_zscaled.csv`;
    medsat_msoa_scores_path = `MedSat/${region}/msoa_medsat_scores_zscaled.csv`;
    polygon_path = `Datasets/Filtered_${region}_Polygon.geojson`;
    cqiRegion = `${region}_cqi_jsons_msoa_REDUCED`;

    // Reset the map by removing all layers
    map.eachLayer((layer) => {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });

    //WIll also run initmap
    initialise_scores_and_map();
}

function resetDescBox() {
    const pBox = document.getElementById("descP");
    pBox.innerHTML = scoreDesc[selectedScore];
}

function resetMap() {
    // Reset the map by removing all layers
    map.eachLayer((layer) => {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });

    //Change description box
    resetDescBox();
    //WIll also run initmap
    initmap();
}

// Load the GeoJSON file and add it as polygons to map
function initmap() {
    //London is two polygon files (it's big)
    if (region != 'London') {
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
                                color: 'blue',
                                weight: 1,
                                // fillColor: 'lightblue',
                                fillColor: zColour(msoa_scores[feature.properties.MSOA21CD][selectedScore]),
                                fillOpacity: 1
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
                            // Highlight the selected polygon -- such to get the CQI Way level scores
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
    } else {
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
                                    color: 'blue',
                                    weight: 1,     // Border thickness
                                    fillColor: zColour(msoa_scores[feature.properties.MSOA21CD][selectedScore]),
                                    fillOpacity: 1
                                }
                            } else {
                                return {};
                            }
                        },
                        onEachFeature: (feature, layer) => {
                            // Add a click event to each polygon -- such to get the CQI Way level scores
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
        const container = L.DomUtil.create('div', '');

        container.innerHTML = `
        <label for="cycleSelect">Choose Score:</label>
        <select id="mySelect" style="height: 40px;">
          <option value="Overall">Overall Score</option>
          
          <option value="CommuteRate">Commuter Rate</option>
          <option value="CrashRate">Crash Rate</option>
          <option value="MeanCQIScore">Mean CQI Scores</option>
          
          ${developerActive ? `<option value="SpaceSyntaxLength">SpaceSyntaxLength</option>` : ''}
          ${!developerActive ? `<option value="SpaceSyntaxLength">CQI Space Syntax</option>` : ''}
          <option value="CommutePath">CommutePath</option>
          
          <option value="diabetes">Diabetes</option>
          <option value="anxiety">anxiety</option>
          <option value="asthma">asthma</option>
          <option value="depression">depression</option>
          <option value="hypertension">hypertension</option>
          <option value="opioids">opioids</option>
          <option value="total">total</option>

          ${developerActive ? `<option value="OME">OME</option>` : ''}
          ${developerActive ? `<option value="IndexSpaceSyntax">IndexSpaceSyntax</option>` : ''}
          ${developerActive ? `<option value="CQIScoreThresh">Cycling Quality Index</option>` : ''}
          ${developerActive ? `<option value="IndexLength">IndexLength</option>` : ''}
          
        </select>
          `;

        container.style.backgroundColor = 'white';
        // Prevent map from reacting to events inside it
        L.DomEvent.disableClickPropagation(container);

        return container;
    },
});
const scoreOverlay = new L.Control.CustomOverlay({ position: 'topleft' });
map.addControl(scoreOverlay);


//Logic for cycle score option select

//Different score overlay
const selectElement = document.getElementById('mySelect');
selectElement.addEventListener('change', (event) => {
    const selectedValue = event.target.value;
    console.log('Selected option:', selectedValue);
    selectedScore = selectedValue;
    selectedMSOA = null;
    //Remove Legend box as well, necessary?
    const legendBox = document.getElementById('CQILegend');
    if (legendBox != null) {
        legendBox.remove();
    }
    resetMap();
});

//City Selector
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
        const container = L.DomUtil.create('div', '');

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
            <p><strong>Commuter Rate: ${msoa_scores[selectedMSOA].CommuteRate.toFixed(3)}</strong></p>
            <p><strong>Crash Rate: ${msoa_scores[selectedMSOA].CrashRate.toFixed(3)}</strong></p>
            <p><strong>Overall Score: ${msoa_scores[selectedMSOA].Overall.toFixed(3)}</strong></p>
            <p><strong>Mean CQI Score: ${msoa_scores[selectedMSOA].MeanCQIScore.toFixed(3)}</strong></p>
            ${developerActive ? `<p><strong>SpaceSyntaxLength: ${msoa_scores[selectedMSOA].SpaceSyntaxLength.toFixed(3)}</strong></p>` : ''}
            ${!developerActive ? `<p><strong>CQI Space Syntax: ${msoa_scores[selectedMSOA].SpaceSyntaxLength.toFixed(3)}</strong></p>` : ''}
            
            <p><strong>Commute Path: ${msoa_scores[selectedMSOA].CommutePath.toFixed(3)}</strong></p>
            
            ${developerActive ? `<p><strong>IndexSpaceSyntax: ${msoa_scores[selectedMSOA].IndexSpaceSyntax.toFixed(3)}</strong></p>` : ''}
            ${developerActive ? `<p><strong>Cycling Quality Index Threshold: ${msoa_scores[selectedMSOA].CQIScoreThresh.toFixed(3)}</strong></p>` : ''}
            ${developerActive ? `<p><strong>IndexLength: ${msoa_scores[selectedMSOA].IndexLength.toFixed(3)}</strong></p>` : ''}
            
        `;
        overlayHealthContainer.innerHTML = `
            <p>Health Information</p>
            <p><strong>asthma: ${msoa_scores[selectedMSOA].asthma.toFixed(3)}</strong></p>
            <p><strong>anxiety: ${msoa_scores[selectedMSOA].anxiety.toFixed(3)}</strong></p>
            <p><strong>depression: ${msoa_scores[selectedMSOA].depression.toFixed(3)}</strong></p>
            <p><strong>diabetes: ${msoa_scores[selectedMSOA].diabetes.toFixed(3)}</strong></p>
            <p><strong>hypertension: ${msoa_scores[selectedMSOA].hypertension.toFixed(3)}</strong></p>
            <p><strong>opioids: ${msoa_scores[selectedMSOA].opioids.toFixed(3)}</strong></p>
            <p><strong>total: ${msoa_scores[selectedMSOA].total.toFixed(3)}</strong></p>
            ${developerActive ? `<p><strong>OME: ${msoa_scores[selectedMSOA].OME.toFixed(3)}</strong></p>` : ''}
        `;
    }
}

// Load the GeoJSON file with cycling quality info, needs filtering by MSOA, all of London is too slow
function loadCycleQuality() {
    fetch(`Datasets/${cqiRegion}/${selectedMSOA}.json`)
        .then(response => response.json())
        .then(data => {
            // Add theGeoJSON data to the map
            if (selectedScore != 'SpaceSyntaxLength') {
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
            } else {
                const zColour = setupColourmap();
                L.geoJSON(data, {
                    style: feature => {
                        const index_level = feature.properties.index_space_syntax_length_norm;
                        const colour = zColour(index_level)
                        return {
                            color: colour,
                            weight: 5,
                            opacity: 0.8
                        };
                    },
                }).addTo(map);
            }
        })
        .then(loadCQILegend())
        .catch(error => console.error('Error loading GeoJSON:', error));

}

function flipLegend(reversed) {
    const legend = document.getElementById("legendBox")
    if (reversed) {
        legend.innerHTML = `
        <span>3</span>
        <span>0</span>
        <span>-3</span>`
    } else {
        legend.innerHTML = `
        <span>-3</span>
        <span>0</span>
        <span>3</span>`
    }
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

//Colour Legend for Z Scale
function setupLegend() {
    let legend = L.control({ position: 'bottomleft' });

    legend.onAdd = function () {
        let div = L.DomUtil.create('div', 'colourlegend');

        let width = 150, height = 15;
        let svg = d3.create("svg")
            .attr("width", width)
            .attr("height", height);

        // Create a horizontal gradient aided by: https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient/
        let defs = svg.append("defs");
        let linearGradient = defs.append("linearGradient")
            .attr("id", "linear-gradient");

        //Append multiple colours (100 with d3.range), offset distance from left, stop-colour just use the colourmap for that position
        linearGradient.selectAll("stop")
            .data(d3.range(0, 1.00, 0.01))
            .enter().append("stop")
            .attr("offset", d => `${d * 100}%`)
            .attr("stop-color", d => setupColourmap(-3, 3)(-3 + d * 6));

        svg.append("rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "url(#linear-gradient)");

        //Need to be able to flip later
        let labelHTML = `
            <div style="display: flex; justify-content: space-between; font-size: 14px;" id="legendBox">
                <span>-3</span>
                <span>0</span>
                <span>3</span>
            </div>
        `;

        // Attach SVG and labels to the div
        div.innerHTML = svg.node().outerHTML + labelHTML;
        return div;
    };

    legend.addTo(map);
}

function loadCQILegend() {
    const legendBox = document.getElementById('CQILegend');
    if (legendBox != null && selectedScore == 'SpaceSyntaxLength') {
        legendBox.remove();
        return
    } else if (legendBox != null) {
        return
    } else if (selectedScore == 'SpaceSyntaxLength') {
        return
    }

    L.Control.CQILegendOverlay = L.Control.extend({
        onAdd: function (map) {
            const container = L.DomUtil.create('div', '');

            container.innerHTML = `
            <div id="CQILegend">
                CQI Score
                <ul class="CQILegendList">
                    <li><span class="CQILegendBox" style="background-color: red;"></span> 1</li>
                    <li><span class="CQILegendBox" style="background-color: darkorange;"></span> 2</li>
                    <li><span class="CQILegendBox" style="background-color: orange;"></span> 3</li>
                    <li><span class="CQILegendBox" style="background-color: gold;"></span> 4</li>
                    <li><span class="CQILegendBox" style="background-color: yellow;"></span> 5</li>
                    <li><span class="CQILegendBox" style="background-color: lightyellow;"></span> 6</li>
                    <li><span class="CQILegendBox" style="background-color: lightgreen;"></span> 7</li>
                    <li><span class="CQILegendBox" style="background-color: mediumseagreen;"></span> 8</li>
                    <li><span class="CQILegendBox" style="background-color: seagreen;"></span> 9</li>
                    <li><span class="CQILegendBox" style="background-color: green;"></span> 10</li>
                </ul>
            </div>
            `;

            container.style.backgroundColor = 'transparent';

            // Prevent map from reacting to events inside the control
            L.DomEvent.disableClickPropagation(container);

            return container;
        },
    });
    const legendOverlay = new L.Control.CQILegendOverlay({ position: 'bottomleft' });
    map.addControl(legendOverlay);
}

//Startup
initialise_scores_and_map();
setupLegend();

