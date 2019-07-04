function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  // Use d3 to select the panel with id of `#sample-metadata`

  // Use `.html("") to clear any existing metadata

  // Use `Object.entries` to add each key and value pair to the panel
  // Hint: Inside the loop, you will need to use d3 to append new
  // tags for each key-value in the metadata.

  // BONUS: Build the Gauge Chart
  // buildGauge(data.WFREQ);
}

function buildCharts(sample) {

  // Chart Params
  var svgWidth = 960;
  var svgHeight = 500;

  var margin = { top: 20, right: 40, bottom: 60, left: 50 };

  var width = svgWidth - margin.left - margin.right;
  var height = svgHeight - margin.top - margin.bottom;

  // Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
  var svg = d3
    .select("body")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Import data from an external CSV file
  d3.json("app.py", function (error, pop_mongo_doc) {
    if (error) throw error;

    console.log(pop_mongo_doc);

    // Create a function to parse date and time
    // var parseTime = d3.timeParse("%d-%b-%Y");

    // Format the data
    pop_mongo_doc.forEach(function (data) {
      data.date = parseTime(data.date);
      data.dow_index = +data.dow_index;
      data.smurf_sightings = +data.smurf_sightings;
    });

    // Create scaling functions
    var xTimeScale = d3.scaleTime()
      .domain(d3.extent(smurfData, d => d.date))
      .range([0, width]);

    var yLinearScale1 = d3.scaleLinear()
      .domain([0, d3.max(smurfData, d => d.dow_index)])
      .range([height, 0]);

    var yLinearScale2 = d3.scaleLinear()
      .domain([0, d3.max(smurfData, d => d.smurf_sightings)])
      .range([height, 0]);

    // Create axis functions
    var bottomAxis = d3.axisBottom(xTimeScale)
      .tickFormat(d3.timeFormat("%YYYY"));
    var leftAxis = d3.axisLeft(yLinearScale1);
    var rightAxis = d3.axisRight(yLinearScale2);

    // Add x-axis
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(bottomAxis);

    // Add y1-axis to the left side of the display
    chartGroup.append("g")
      // Define the color of the axis text
      .classed("green", true)
      .call(leftAxis);

    // Add y2-axis to the right side of the display
    chartGroup.append("g")
      // Define the color of the axis text
      .classed("blue", true)
      .attr("transform", `translate(${width}, 0)`)
      .call(rightAxis);

    // Line generators for each line
    var line1 = d3.line()
      .x(d => xTimeScale(d.date))
      .y(d => yLinearScale1(d.dow_index));

    var line2 = d3.line()
      .x(d => xTimeScale(d.date))
      .y(d => yLinearScale2(d.smurf_sightings));

    // Append a path for line1
    chartGroup.append("path")
      .data([smurfData])
      .attr("d", line1)
      .classed("line green", true);

    // Append a path for line2
    chartGroup.append("path")
      .data([smurfData])
      .attr("d", line2)
      .classed("line blue", true);

    // Append axes titles
    chartGroup.append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top + 20})`)
      .classed("dow-text text", true)
      .text("Dow Index");

    chartGroup.append("text")
      .attr("transform", `translate(${width / 2}, ${height + margin.top + 37})`)
      .classed("smurf-text text", true)
      .text("Smurf Sightings");
  });

}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();