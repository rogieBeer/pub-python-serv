<!DOCTYPE html>

<html lang="en">
<head> 
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Portfolio</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <ul>
        <li><a href="index.html">Home</a></li>
        <li><a class="active" href="portfolio.html">Portfolio</a></li>
        <li><a href="stock.html">Stock</a></li>
    </ul>
    <h2 id="testJS">Your Stocks</h2>
    <div id="demo"></div>
    <p id="display"></p>
    <div id="id01"></div>
    <table></table>
    <br>
    <br>
    <form action="" name = "stockInput" onsubmit="return formValidation()">
        <label for="stock">Stock ID:</label><br>
        <input type="text" id="stock" name="stock"  required><br>
        <label for="quantity">Quantitiy:</label><br>
        <input type="number" id="quantity" name="quantity" step=".01" required><br>
        <label for="price">Price:</label><br>
        <input type="" id="price" name="price" step=".01" required><br><br>
        <input type="submit" value="Submit">
        <input type="reset" value="Reset">
    </form>
    <script src="index.js"></script>
    <script src="valid.js"></script>  
</body>
</html>