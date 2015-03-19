
function plot_circus(selector,names,matrix){

  var width = 300;
  var height = 300;
  var innerRadius = Math.min(width, height) * .37;
  var outerRadius = innerRadius * 1.1;

  var svg = d3.select(selector).append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
      
  var chord = d3.layout.chord()
      .padding(.05)
      .matrix(matrix);
      //.sortSubgroups(d3.descending)      

  var fill = d3.scale.ordinal()
      .domain(d3.range(10))
      .range(['#FF0000','#800000','#FFFF00','#808000','#00FF00','#008000','#00FFFF','#008080','#0000FF','#000080']);


  svg.append("g").selectAll("path")
      .data(chord.groups)
    .enter().append("path")
      .style("fill", function(d) { return fill(d.index); })
      .style("stroke", function(d) { return fill(d.index); })
      .attr("d", d3.svg.arc().innerRadius(innerRadius).outerRadius(outerRadius))
      .on("mouseover", fade(.1))
      .on("mouseout", fade(1));

  var ticks = svg.append("g").selectAll("g")
      .data(chord.groups)
    .enter().append("g").selectAll("g")
      .data(groupTicks)
    .enter().append("g")
      .attr("transform", function(d) {
        return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
            + "translate(" + outerRadius + ",0)";
      });

  ticks.append("line")
      .attr("x1", 1)
      .attr("y1", 0)
      .attr("x2", 5)
      .attr("y2", 0)
      .style("stroke", "#000");

  ticks.append("text")
      .attr("x", 8)
      .attr("dy", ".35em")
      .attr("transform", function(d) { return d.angle > Math.PI ? "rotate(180)translate(-16)" : null; })
      .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
      .text(function(d) { return d.label; });

  // Returns an array of tick angles and labels, given a group.
  function groupTicks(d) {
    var k = (d.endAngle - d.startAngle) / d.value;
    return d3.range(d.value/2, d.value, d.value/2).map(function(v, i) {
      return {
        angle: v * k + d.startAngle,
        label: names[d.index]
      };
    });
  } 

  svg.append("g")
      .attr("class", "chord")
    .selectAll("path")
      .data(chord.chords)
    .enter().append("path")
      .attr("d", d3.svg.chord().radius(innerRadius))
      .style("fill", function(d) { return fill(d.target.index); })
      .style("opacity", 1);

  // Returns an event handler for fading a given chord group.
  function fade(opacity) {
    return function(g, i) {
      svg.selectAll(".chord path")
          .filter(function(d) { return d.source.index != i && d.target.index != i; })
        .transition()
          .style("opacity", opacity);
    };
  }
}

function plot_multiseries(selector,url){
  // creamos los elementos gráficos para dibujar:
  // valores en px:
  var margin = {top: 20, right: 40, bottom: 30, left: 40};
  var width = 800 - margin.left - margin.right;
  var height = 300 - margin.top - margin.bottom;
  
  var parseDate = d3.time.format("%Y-%m-%d").parse;
  
  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);
  
  var color = d3.scale.category10();
  var xAxis = d3.svg.axis().scale(x).orient("bottom");
  var yAxis = d3.svg.axis().scale(y).orient("left");
  function make_x_line() { return d3.svg.axis().scale(x).orient("bottom"); };
  function make_y_line() { return d3.svg.axis().scale(y).orient("left"); };
  var line = d3.svg.line().interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });
  
  var svg = d3.select(selector).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("class", "svg-canvas")
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // cargamos los datos enviados como csv desde el backend, solicitando la url:
  d3.csv(url, function(error, data) {
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));
    data.forEach(function(d) { d.date = parseDate(d.date); });
    var stocks = color.domain().map(function(name) {
      return {
        name: name,
        values: data.map(function(d) {
          return {date: d.date, close: +d[name]};
        })
      };
    });
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([
      d3.min(stocks, function(c) { return d3.min(c.values, function(v) { return v.close; }); }),
      d3.max(stocks, function(c) { return d3.max(c.values, function(v) { return v.close; }); })
    ]);
    //formateamos los ticks de los ejes:
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Close");
    svg.append("g")         
        .attr("class", "grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_line().tickSize(-height, 0, 0).tickFormat(""))
    svg.append("g")         
        .attr("class", "grid")
        .call(make_y_line().tickSize(-width, 0, 0).tickFormat(""))
    // asignamos a cada linea la clase .stock
    var stock = svg.selectAll(".stock")
        .data(stocks)
      .enter().append("g")
        .attr("class", "stock")
        .attr("id", function(d){ return "stock-"+d.name.split('.')[0]; });
    // pintamos y coloreamos la linea
    stock.append("path")
        .attr("class", "line")
        .attr("d", function(d) { return line(d.values); })
        .style("stroke", function(d) { return color(d.name); });
    // le añadimos el texto a cada serie
    stock.append("text")
        .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.close) + ")"; })
        .attr("x", 3)
        .attr("dy", ".1em")
        .text(function(d) { return d.name; });
  });
};

