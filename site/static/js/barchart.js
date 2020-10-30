// Chart template and starter code from:
// https://www.d3-graph-gallery.com/graph/barplot_basic.html


function createBarChart(svg, width, height, csv_link) {
  d3.csv(csv_link).then(function(data) {
    console.log(data[0])
    data.sort(function(a, b) {
      return d3.descending(Math.abs(a[1]), Math.abs(b[1]))
    })

    // X axis
    var x = d3.scaleBand()
      .range([ 0, width ])
      .domain(data.map(function(d) { return var_names[d[0]]; }))
      .padding(0.2);

    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .attr("class", "axis")
      .call(d3.axisBottom(x))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end")
        .on("click", function(d) {
          renderSelectChart(var_names_rev[d])
        });

  svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - 30)
        .attr("text-anchor", "middle")
        .attr("class", "axis")
        .style("font-size", "35px")
        .text("Feature Importances for Graduation Model");

  svg.append("text")
        .attr("x", -height/2)
        .attr("y", -35)
        .attr("text-anchor", "middle")
        .attr("class", "axis")
        .style("font-size", "28px")
        .attr("transform", "translate(-15,-10)rotate(-90)")
        .text("Logistic Regression Coefficient");

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, 1])
      .range([ height, 0]);
    svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y));
    // Bars
    svg.selectAll("mybar")
      .data(data)
      .enter()
      .append("rect")
        .attr("x", function(d) { return x(var_names[d[0]]); })
        .attr("y", function(d) { return y(Math.abs(d[1])); })
        .attr("width", x.bandwidth())
        .attr("height", function(d) { return height - y(Math.abs(d[1])); })
        .attr("fill", function(d) {
          if (d[1] > 0) {
            return "#5758a6";
          } else {
            return "#a70b44";
          }
        })
        .on("click", function(d) {
          renderSelectChart(d[0])
        });

    })
    function renderSelectChart(feat) {
      svg_sel.selectAll("*").remove();
      if (["math_score", "reading_score", "income", "wealth"].includes(feat)) {
        createKDE(feat, svg_sel)
      } else {
        createStackedBar(feat, svg_sel)
      }
    }
}


var var_names = {
  "math_score": "Math",
  "reading_score": "Reading",
  "age": "Age",
  "wealth": "Wealth",
  "environment_type_urb_met": "Metro City",
  "environment_type_rural": "Rural",
  "white_only": "White",
  "black": "Black",
  "asian": "Asian",
  "live_w_both_parents": "Both Parents",
  "income": "Income",
  "hispanic": "Hispanic",
  "food_security": "Food Security",
  "environment_type_met_fringe": "Metro Fringe",
  "environment_type_met_central": "Large Metro",
  "environment_type_met_small": "Small Metro",
  "environment_type_urb_nonmet": "Non-Metro City"
}

var var_names_rev = {
  "Math": "math_score",
  "Reading": "reading_score",
  "Age": "age",
  "Wealth": "wealth",
  "Metro City": "environment_type_urb_met",
  "Rural": "environment_type_rural",
  "White": "white_only",
  "Black": "black",
  "Asian": "Asian",
  "Both Parents": "live_w_both_parents",
  "Income": "income",
  "Hispanic": "hispanic",
  "Food Security": "food_security",
  "Metro Fringe": "environment_type_met_fringe",
  "Large Metro": "environment_type_met_central",
  "Small Metro": "environment_type_met_small",
  "Non-Metro City": "environment_type_urb_nonmet"
}
