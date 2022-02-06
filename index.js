var xmlhttp = new XMLHttpRequest();
var url = "portfolio.json";


xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var myArr = JSON.parse(this.responseText);
    sortData(myArr);
  }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();

// gets the data from the json file and adds it to the tables
function sortData(myObj){
    var stocks = [];
    for (x in myObj['portfolio']) {        
        stocks.push(myObj['portfolio'][x])
    }
    stocks.sort();
    let table = document.querySelector("table");
    let data = Object.keys(stocks[0]);
    generateTableHead(table, data);
    generateTable(table, stocks);
}


// Creates table headers
function generateTableHead(table, data) {
  let thead = table.createTHead();
  let row = thead.insertRow();
  for (let key of data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key.toUpperCase());
      th.appendChild(text);
      row.appendChild(th);
  }
}
  

// generates table information
function generateTable(table, data) {
  for (let element of data) {
    let row = table.insertRow();
    for (key in element) {
      let cell = row.insertCell();
      let text = document.createTextNode(element[key]);
      cell.appendChild(text);
    }
  }
}

