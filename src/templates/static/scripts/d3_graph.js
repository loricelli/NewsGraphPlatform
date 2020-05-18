const ed = JSON.parse(document.getElementById('edges').textContent);
  const nd = JSON.parse(document.getElementById('nodes').textContent);
  s_t_ed = ed.replace(/tail/g,"source");
  s_t_ed = s_t_ed.replace(/head/g,"target");

  fin_ed = JSON.parse(s_t_ed);
  console.log(fin_ed);
  fin_nd = JSON.parse(nd);

  width = 1200;
  height = 800;

  var svg = d3.select("#chart").attr("width",width).attr("height",height);
  const simulation = d3.forceSimulation(fin_nd)
    .force("link", d3.forceLink(fin_ed).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width/ 3, height/ 3));

  var link = svg.append("g")
    .selectAll("line")
    .data(fin_ed)
    .join("line")
    .attr("stroke", d => d.color )
    .attr("stroke-width", d => 0.5);


  var node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(fin_nd)
    .join("circle")
    .attr("r", 4)
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended))
    .attr("fill", d => d.color );
  node.append("title")
    .text(d => d.id);



  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  });


  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

