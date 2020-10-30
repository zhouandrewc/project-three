// Chart template and starter code from:
// https://www.d3-graph-gallery.com/graph/density_double.html

function createKDE(feat, svg_sel) {
  d3.csv("static/data.csv").then(function(data) {

    var feat_values = data.map(d => +d[feat])
    var feat_min = Math.min(...feat_values)
    var feat_max = Math.max(...feat_values)
    var feat_range = feat_max - feat_min


    var left = feat_min-feat_range*0.15
    var right = feat_max+feat_range*0.15

    if (feat == "wealth") {
      left = -100000
      right = 1000000
    }
    // add the x Axis
    var x = d3.scaleLinear()
        .domain([left, right])
        .range([0, width]);


    svg_sel.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-20)")
            .style("text-anchor", "end")

  svg_sel.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - 30)
        .attr("text-anchor", "middle")
        .attr("class", "axis")
        .style("font-size", "35px")
        .text("Density of " + var_names_kde[feat] + " by Degree");

  svg_sel.append("text")
        .attr("x", (width / 2))
        .attr("y", height + 80)
        .attr("class", "axis")
        .attr("text-anchor", "middle")
        .style("font-size", "30px")
        .text(var_names_kde[feat]);

  svg_sel.append("text")
        .attr("x", -height/2)
        .attr("y", -70)
        .attr("text-anchor", "middle")
        .attr("class", "axis")
        .style("font-size", "28px")
        .attr("transform", "translate(-15,-10)rotate(-90)")
        .text("Density");

    // Compute kernel density estimation
    var kde = kernelDensityEstimator(kernelEpanechnikov(12), x.ticks(60))
    var density1 =  kde( data
        .filter( function(d){return d["grad_bach"] == 0} )
        .map(function(d){  return d[feat]; }) )
    var density2 =  kde( data
        .filter( function(d){return d["grad_bach"] == 1} )
        .map(function(d){  return d[feat]; }) )

    // Hardcode some of the normalization
    var d_vals = density1.map(d => +d[1]*2*1455.0/2605)
    var d_max = Math.max(...d_vals)
    var d_vals2 = density1.map(d => +d[1]*2*610.0/2065)
    var d_max = Math.max(...d_vals2, d_max)

    // Hardcode wealth y-domain
    if (feat == "wealth") {
      d_max = 0.006/1.3
    }

    // add the y Axis
    var y = d3.scaleLinear()
              .range([height, 0])
              .domain([0, d_max*1.3]);
    svg_sel.append("g")
        .attr("class", "axis")
        .call(d3.axisLeft(y));

    // Plot the area
    svg_sel.append("path")
        .attr("class", "mypath")
        .datum(density1)
        .attr("fill", "#69b3a2")
        .attr("opacity", ".6")
        .attr("stroke", "#000")
        .attr("stroke-width", 1)
        .attr("stroke-linejoin", "round")
        .attr("d",  d3.line()
          .curve(d3.curveBasis)
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return y(d[1]*2*1455.0/2065); })
        );

    // Plot the area
    svg_sel.append("path")
        .attr("class", "mypath")
        .datum(density2)
        .attr("fill", "#404080")
        .attr("opacity", ".6")
        .attr("stroke", "#000")
        .attr("stroke-width", 1)
        .attr("stroke-linejoin", "round")
        .attr("d",  d3.line()
          .curve(d3.curveBasis)
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return y(d[1]*2*610.0/2065); })
        );

  });

  // Handmade legend
  svg_sel.append("circle").attr("cx",width*0.6).attr("cy",20).attr("r", 6).style("fill", "#69b3a2")
  svg_sel.append("circle").attr("cx",width*0.6).attr("cy",50).attr("r", 6).style("fill", "#404080")
  svg_sel.append("text").attr("x", width*0.6+10).attr("y", 20).text("No Bachelor's Degree").style("font-size", "18px").attr("alignment-baseline","middle").attr("class", "axis")
  svg_sel.append("text").attr("x", width*0.6+10).attr("y", 50).text("Bachelor's Degree").style("font-size", "18px").attr("alignment-baseline","middle").attr("class", "axis")

  // Function to compute density
  function kernelDensityEstimator(kernel, X) {
    return function(V) {
      return X.map(function(x) {
        return [x, d3.mean(V, function(v) { return kernel(x - v); })];
      });
    };
  }
  function kernelEpanechnikov(k) {
    return function(v) {
      return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
    };
  }
}

var var_names_kde = {
  "math_score": "Math Score",
  "reading_score": "Reading Score",
  "age": "Age",
  "wealth": "Wealth ($)",
  "environment_type_urb_met": "Metro City",
  "environment_type_rural": "Rural",
  "white_only": "White",
  "black": "Black",
  "asian": "Asian",
  "live_w_both_parents": "Both Parents",
  "income": "Income ($)",
  "hispanic": "Hispanic",
  "food_security": "Food Security",
  "environment_type_met_fringe": "Metro Fringe",
  "environment_type_met_central": "Large Metro",
  "environment_type_met_small": "Small Metro",
  "environment_type_urb_nonmet": "Non-Metro City"
}

