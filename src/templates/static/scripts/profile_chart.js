

const j_data = JSON.parse(document.getElementById('data').textContent);
var data = JSON.parse(j_data);
var margin = {top: 10, right: 30, bottom: 30, left: 60},
  width = 600- margin.left - margin.right,
  height = 300- margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#line")
  .attr("preserveAspectRatio", "xMinYMin meet")
  .attr("viewBox", "0 0 600 500")
  .append("g")
  .attr("transform",
    "translate(" + margin.left + "," + margin.top + ")");


var x = d3.scaleLinear()
  .domain(d3.extent(data, function(d) { return Number(d.date__date.split("-")[2]); }))
  .range([ 1, width ]);
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x));


var y = d3.scaleLinear()
  .domain([0, d3.max(data, function(d) { return d.dcount; })])
  .range([ height, 0 ]);
svg.append("g")
  .call(d3.axisLeft(y).ticks(5));

svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 1.5)
  .attr("d", d3.line()
    .x(function(d) { return x(d.date__date.split("-")[2]) })
    .y(function(d) { return y(d.dcount) })
  );

