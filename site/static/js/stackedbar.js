// Chart template and starter code from:
// http://bl.ocks.org/mstanaland/6100713

function createStackedBar(feat, svg_sel) {

  // Parse the Data
  d3.csv("static/data.csv").then(function(data) {

  // List of subgroups = header of the csv files = soil condition here
  var subgroups = ["grad", "nongrad"]

  var groups = null
  var grads = []
  var nongrads = []

  // Hardcode some of the features
  if (feat == "age") {
    groups = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]

    for (var i = 0; i < groups.length; i++) {
      g = data.filter(function(d){return d["grad_bach"] == 1 && d["age"] == groups[i]})
      ng = data.filter( function(d){return d["grad_bach"] == 0 && d["age"] == groups[i]})
      grads.push(g.length)
      nongrads.push(ng.length)
    }
    feat_name = "Age"

  } else if (feat.substr(0, 3) == "env") {
    groups = ["met_central", "met_fringe", "met_small", "urb_met", "urb_nonmet", "rural"]

    for (var i = 0; i < groups.length; i++) {
      g = data.filter(function(d){return d["grad_bach"] == 1 && d["environment_type"] == groups[i]})
      ng = data.filter( function(d){return d["grad_bach"] == 0 && d["environment_type"] == groups[i]})
      grads.push(g.length)
      nongrads.push(ng.length)
    }
    groups = ["Large Metro", "Metro Fringe", "Small Metro", "Metro City", "Non-Metro City", "Rural"]
    feat_name = "Environment"
  } else if (["asian", "white_only", "black", "hispanic"].includes(feat)) {
    groups = ["asian", "white_only", "black", "hispanic"]

    for (var i = 0; i < groups.length; i++) {
      g = data.filter(function(d){return d["grad_bach"] == 1 && d[groups[i]] == 1})
      ng = data.filter( function(d){return d["grad_bach"] == 0 && d[groups[i]] == 1})
      grads.push(g.length)
      nongrads.push(ng.length)
    }
    groups = ["Asian", "White", "Black", "Hispanic"]
    feat_name = "Race"
  } else if (feat == "live_w_both_parents") {
    groups = [1, 0]
    for (var i = 0; i < groups.length; i++) {
      g = data.filter(function(d){return d["grad_bach"] == 1 && d["live_w_both_parents"] == groups[i]})
      ng = data.filter( function(d){return d["grad_bach"] == 0 && d["live_w_both_parents"] == groups[i]})
      grads.push(g.length)
      nongrads.push(ng.length)
    }
    groups = ["Both", "One or None"]
    feat_name = "Parental Cohabitation"
  } else if (feat == "food_security") {
    groups = [[6.5,10], [2.5, 5.5], [0.5, 2.5], [0, 0.5]]
    for (var i = 0; i < groups.length; i++) {
      g = data.filter(function(d){return d["grad_bach"] == 1 && d["food_security"] >= groups[i][0] && d["food_security"] <= groups[i][1]})
      ng = data.filter( function(d){return d["grad_bach"] == 0 && d["food_security"] >= groups[i][0] && d["food_security"] <= groups[i][1]})
      grads.push(g.length)
      nongrads.push(ng.length)
    }
    groups = ["Very Low", "Low", "Marginal", "High"]
    feat_name = "Food Security"
  }

  var newData = []

  percents = []
  max = 0
  for (var i = 0; i < groups.length; i++) {

    gr = grads[i]*100.0/(grads[i]+nongrads[i])
    percents.push(gr)

    newData.push({"group": groups[i], "grad": grads[i], "nongrad": nongrads[i]});
    max = Math.max(max, grads[i]+nongrads[i])
  }


  // Add X axis
  var x = d3.scaleBand()
      .domain(groups)
      .range([0, width])
      .padding([0.2])
  svg_sel.append("g")
  .attr("class", "axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSizeOuter(0));

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([0, max*1.1])
    .range([ height, 0 ]);

  svg_sel.append("g")
  .attr("class", "axis y-axis")
    .call(d3.axisLeft(y));

  svg_sel.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - 30)
        .attr("text-anchor", "middle")
        .attr("class", "axis")
        .style("font-size", "35px")
        .text("Graduation Status by " + feat_name);

  // color palette = one color per subgroup
  var color = d3.scaleOrdinal()
    .domain(subgroups)
    .range(["#2d6b1a", "#970559"])

  //stack the data? --> stack per subgroup
  var stackedData = d3.stack()
    .keys(subgroups)
    (newData)
// Prep the tooltip bits, initial display is hidden

  // Show the bars
  svg_sel.append("g")
    .attr("class", "g-elem")
    .selectAll("g")

    .attr("class", "stack-chart")
    // Enter in the stack data = loop key per key = group per group
    .data(stackedData)
    .enter().append("g")
      .attr("fill", function(d) { return color(d.key); })
      .selectAll("rect")
      .attr("class", "stack-bar-1")
      // enter a second time = loop subgroup per subgroup to add all rectangles
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("class", "stack-bar-2")
        .attr("x", function(d) { return x(d.data.group); })
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { return y(d[0]) - y(d[1]); })
        .attr("width",x.bandwidth())
          .on("mouseover", function() { tooltip.style("display", null); })
          .on("mouseout", function() { tooltip.style("display", "none"); })
          .on("mousemove", function(d) {
            var xPosition = d3.mouse(this)[0] - 35;
            var yPosition = d3.mouse(this)[1] - 55;
            tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
            var perc = 100.*d.data.grad/(d.data.nongrad+d.data.grad)
            tooltip.select("text").html(perc.toFixed(1) + "%");

          }).on("click", function(d) {
            updateChart();
          });

var tooltip = svg_sel.append("g")
  .attr("class", "tooltip")
  .style("display", "none");

tooltip.append("rect")
  .attr("width", 70)
  .attr("height", 40)
  .attr("fill", "white")
  .style("opacity", 0.85);

tooltip.append("text")
  .attr("x", 13)
  .attr("dy", "1.2em")
  .attr("data-html", "true")

tooltip.append("text")
  .attr("x", 13)
  .attr("dy", "2.4em")
  .text("Grads")
//  .style("text-anchor", "middle")
  svg_sel.append("text")
        .attr("x", (width / 2))
        .attr("y", height + 55)
        .attr("class", "axis")
        .attr("text-anchor", "middle")
        .style("font-size", "30px")
        .text(feat_name);

  svg_sel.append("text")
        .attr("x", -height/2)
        .attr("y", -55)
        .attr("text-anchor", "middle")
        .attr("class", "axis")
        .style("font-size", "28px")
        .attr("transform", "translate(-15,-10)rotate(-90)")
        .text("Count");
  svg_sel.append("circle").attr("class", "legend").attr("cx",width*0.05).attr("cy",0).attr("r", 6).style("fill", "#2d6b1a").attr("class", "legend")
  svg_sel.append("circle").attr("class", "legend").attr("cx",width*0.05).attr("cy",20).attr("r", 6).style("fill", "#970559").attr("class", "legend")
  svg_sel.append("text").attr("class", "legend").attr("x", width*0.05+10).attr("y", 0).text("Bachelor's").style("font-size", "18px").attr("alignment-baseline","middle").attr("class", "axis legend")
  svg_sel.append("text").attr("class", "legend").attr("x", width*0.05+10).attr("y", 20).text("No Bachelor's").style("font-size", "18px").attr("alignment-baseline","middle").attr("class", "axis legend")


  // Needs refactoring
  function updateChart() {

  svg_sel.selectAll(".stack-bar-1").remove();
  svg_sel.selectAll(".stack-bar-2").remove();
  svg_sel.selectAll(".g-elem").remove();
  svg_sel.selectAll(".y-axis").remove();
  svg_sel.selectAll(".legend").remove();

  y = d3.scaleLinear()
    .domain([0, 100])
    .range([ height, 0 ]);

  svg_sel.append("g")
  .attr("class", "y-axis axis")
    .call(d3.axisLeft(y));

  svg_sel.append("g")
    .attr("class", "g-elem")
    .selectAll("g")
    .attr("class", "stack-chart")
    // Enter in the stack data = loop key per key = group per group
    .data(stackedData)
    .enter().append("g")
      .attr("fill", function(d) { return color(d.key); })
      .selectAll("rect")
      .attr("class", "stack-bar-1")
      // enter a second time = loop subgroup per subgroup to add all rectangles
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("class", "stack-bar-2")
        .attr("x", function(d) { return x(d.data.group); })
        .attr("y", function(d) {
          var perc = 100.*d.data.grad/(d.data.nongrad+d.data.grad)

          if (d[0] == 0) {
            return y(0) - y(100.0*d.data.nongrad/(d.data.grad+d.data.nongrad));

          } else {
            return 0;
          }
        })
        .attr("height", function(d) {
          if (d[1] == d[1] + d[0]) {
            return y(100.0*d.data.nongrad/(d.data.grad+d.data.nongrad))
          } else {
            return y(100.0*d.data.grad/(d.data.grad+d.data.nongrad));
          }
        })
        .attr("width",x.bandwidth())
          .on("mouseover", function() { tooltip.style("display", null); })
          .on("mouseout", function() { tooltip.style("display", "none"); })
          .on("mousemove", function(d) {
            var xPosition = d3.mouse(this)[0] - 35;
            var yPosition = d3.mouse(this)[1] - 55;
            tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
            var perc = 100.*d.data.grad/(d.data.nongrad+d.data.grad)
            tooltip.select("text").html(perc.toFixed(1) + "%");

          }).on("click", function(d) {
            svg_sel.selectAll("*").remove();
            createStackedBar(feat, svg_sel);
          });

  svg_sel.append("circle").attr("cx",-20).attr("cy",-35).attr("r", 6).style("fill", "#2d6b1a")
  svg_sel.append("circle").attr("cx",-20).attr("cy",-15).attr("r", 6).style("fill", "#970559")
  svg_sel.append("text").attr("x", -10).attr("y", -35).text("Bachelor's").style("font-size", "18px").attr("alignment-baseline","middle").attr("class", "axis")
  svg_sel.append("text").attr("x", -10).attr("y", -15).text("No Bachelor's").style("font-size", "18px").attr("alignment-baseline","middle").attr("class", "axis")


var tooltip = svg_sel.append("g")
  .attr("class", "tooltip")
  .style("display", "none");



tooltip.append("rect")
  .attr("width", 70)
  .attr("height", 40)
  .attr("fill", "white")
  .style("opacity", 0.85);

tooltip.append("text")
  .attr("x", 13)
  .attr("dy", "1.2em")
  .attr("data-html", "true")

tooltip.append("text")
  .attr("x", 13)
  .attr("dy", "2.4em")
  .text("Grads")
  }

})}

