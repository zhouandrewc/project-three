
// set the dimensions and margins of the graph
var margin = {top: 75, right: 30, bottom: 120, left: 120},
    width = 800 - margin.left - margin.right,
    height = 680 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg_bar = d3.select("#bar-chart")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// set the dimensions and margins of the graph
var margin_sel = {top: 75, right: 30, bottom: 120, left: 120},
    width_sel = 800 - margin_sel.left - margin_sel.right,
    height_sel = 680 - margin_sel.top - margin_sel.bottom;

// append the svg object to the body of the page
var svg_sel = d3.select("#select-chart")
  .append("svg")
    .attr("width", width_sel + margin_sel.left + margin_sel.right)
    .attr("height", height_sel + margin_sel.top + margin_sel.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin_sel.left + "," + margin_sel.top + ")");

createBarChart(svg_bar, width, height, "static/feature_importances.csv")
createKDE("math_score", svg_sel)