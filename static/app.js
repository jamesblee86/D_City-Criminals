console.log('app.js file loaded');
function buildPopulation() {
  console.log("in build population");

  // population by year ----------------------------
  d3.json("/population").then((data) => {
    console.log(data);

    var popChart = {
      x: data.year,
      y: data.population,
      type: "line"
    };

    var popData = [popChart];

    var layout = {
      title: "Population Growth in Denver"
    };
    // console.log(popData, layout)

    Plotly.newPlot("line", popData, layout);
  });
}

// murders and robberies by year ---------------------------------------

function buildCharts(crime_id) {

  d3
    .json(`/crimes/${crime_id}`)
    .then((data) => {
      var otu_ids = data.otu_ids;
      var otu_labels = data.otu_labels;
      var sample_values = data.sample_values;
      console.log(otu_ids, otu_labels, sample_values)
      console.log(data);

      var popChart = {
        // x: data.year_month.map(year=>`${year}-01-01`),
        x: data.year_month.map(year=>moment(year, "YYYY").toDate()),
        y: data.count_murders,
        type: "line"
      };

      var popData = [popChart];

      var layout = {
        title: `${crime_id} in Denver`
      };
      console.log(popData, layout)

      Plotly.newPlot("line2", popData, layout);
    });
}



function optionChanged(newSample) {
  console.log(newSample);
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);

}



buildPopulation();


buildCharts('murder');