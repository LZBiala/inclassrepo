// from data.js
var tableData = data;

// YOUR CODE HERE!
console.log(tableData);
var tbody = d3.select("tbody");
console.log(data);

 data.forEach(function(Reports) {
  console.log(Reports);
  var row = tbody.append("tr");
   Object.entries(Reports).forEach(function([key, value]) {
     console.log(key, value);
     var cell = tbody.append("td");
     cell.text(value);
   });
 });


 var submit = d3.select("#submit");


 submit.on("click", function() {

   d3.event.preventDefault();
   d3.select(".summary").html("");
 

   var inputElement = d3.select("#datetime");
   var inputValue = inputElement.property("value");
 
   var filteredData = tableData.filter(tableData => tableData.datetime === inputValue);
 

   filteredData.forEach((dateData) => {
     var row = tbody.append("tr");
     Object.entries(dateData).forEach(([key, value]) => {
       var cell = tbody.append("td");
       cell.text(value);
     });
   });
 });
