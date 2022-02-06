var xmlhttp = new XMLHttpRequest();
var url = "https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_a7f87019e6f24a32b7f321db47ce8826";
// var url = "valid.json";
var compare = []


xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var myArr = JSON.parse(this.responseText);
    getJSON(myArr);
  }
};
xmlhttp.open("GET", url, true);
xmlhttp.send();

// Gets the icons and adds them to a array.
function getJSON(myObj){
     for (x in myObj) {     
        compare.push(myObj[x].symbol)
    }
}


// Validates the form and returns a alert if not in found.
function formValidation(){
    var name = document.forms["stockInput"]["stock"];
    if (compare.includes(name.value.toUpperCase())) {
        
        return true;
      }  
    window.alert("Please enter a valid stock ID.");
    name.focus();
    return false;
  
  }

