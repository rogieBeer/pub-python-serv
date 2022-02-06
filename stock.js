var xmlhttp = new XMLHttpRequest();
var url = "portfolio.json";


// Loads in the portfolio data which holds the current stock symbol.
// Loads the graph from canvasJS
window.onload = function () {
    xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        console.log(myArr)
        var sym = myArr["symbol"][0]
        console.log(sym["stock"])
        var dataPoints = [];
        var stockChart = new CanvasJS.StockChart("stockChartContainer", {
        exportEnabled: true,
        title: {
            text:"YTD Share Prices for "+sym["stock"]
        },
        subtitles: [{
            text:""
        }],
        charts: [{
            axisX: {
            crosshair: {
                enabled: true,
                snapToDataPoint: true,
                valueFormatString: "MMM YYYY"
            }
            },
            axisY: {
            title: "Dollars",
            prefix: "$",
            suffix: "",
            crosshair: {
                enabled: true,
                snapToDataPoint: true,
                valueFormatString: "$#,###.00",
            }
            },
            data: [{
            type: "line",
            xValueFormatString: "MMM YYYY",
            yValueFormatString: "$#,###.##",
            dataPoints : dataPoints
            }]
        }],
        navigator: {
            slider: {
            minimum: new Date(2010, 00, 01),
            maximum: new Date(2018, 00, 01)
            }
        }
        });
        $.getJSON("https://cloud.iexapis.com/stable/stock/"+sym["stock"]+"/chart/ytd?chartCloseOnly=true&token=pk_a7f87019e6f24a32b7f321db47ce8826", function(data) {
        for(var i = 0; i < data.length; i++){
            dataPoints.push({x: new Date(data[i].date), y: Number(data[i].close)});
        }
        stockChart.render();
        });
        }
        };
        xmlhttp.open("GET", url, true);
        xmlhttp.send();    
}
