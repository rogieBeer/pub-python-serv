<!DOCTYPE html>

<html lang="en">
<head> 
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="portfolio.html">Portfolio</a></li>
      <li><a class="active" href="stock.html">Stock</a></li>
    </ul>
    <h1 id="YTD">YTD Stock</h1>
    <form action="action_page.php" name = "stockInput" onsubmit="return formValidation()">
        <label for="stock">Stock ID:</label><br>
        <input id = "stockID" type="text" name="stock" required><br>
        <input type="submit" value="Submit">
    </form>
    <div id="stockChartContainer" style="height: 400px; width: 100%;"></div>
    <script src="valid.js"></script> 
    <script type="text/javascript" src="https://canvasjs.com/assets/script/jquery-1.11.1.min.js"></script>
    <script type="text/javascript" src="https://canvasjs.com/assets/script/canvasjs.stock.min.js"></script>
    <script src="stock.js"></script> 
        
</body>
</html>