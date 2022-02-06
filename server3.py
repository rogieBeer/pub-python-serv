# Student Number: 14062696

import sys
from socket import *
import _thread
import pycurl
from io import BytesIO
import urllib3
import requests
from base64 import b64encode
import json


# Hold the values for adding to portfolio.json
stockValues = []
# Basic authentication variables
username = '14062696'
password = '14062696'
encoded_credentials = b64encode(
    bytes(f'{username}:{password}', encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'
# Server variables
serverSocket = socket(AF_INET, SOCK_STREAM)
# serverPort = 8080
serverPort = int(sys.argv[1])
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print('The server is running')
# Server should be up and running and listening to the incoming connections


# Extract the given header value from the HTTP request message
def getHeader(message, header):

    if message.find(header) > -1:
        value = message.split(header)[1].split()[0]
    else:
        value = None

    return value


# service function to fetch the requested file, and send the contents back to the client in a HTTP response.
def getFile(filename):
    try:
        # open and read the file contents. This becomes the body of the HTTP response
        f = open(filename, "rb")
        body = f.read()
        header = status(200, "").encode()
    except IOError:
        # Send HTTP response message for resource not found
        header, body = status(404, "")
        header = header.encode()
        body = body.encode()
    return header, body


# returns a string with basic header text to reduce typing.
def status(code, redir):
    if code == 200:
        return "HTTP/1.1 200 OK\r\n\r\n"
    elif code == 301:
        return 'HTTP/1.1 301 Redirect\r\nLocation: ' + redir + '\r\n'
    elif code == 401:
        return 'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="Access to the staging site"\r\n\r\n'
    elif code == 404:
        return "HTTP/1.1 404 Not Found\r\n\r\n", "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
    else:
        return "HTTP/1.1 420 Unknown Error \r\n\r\n"


# Returns 401 code and header and body info.
def auth(message):
    header = status(401, "").encode()
    body = "<html><head></head><body><h1>401 Unauthorized</h1></body></html>\r\n".encode()
    return header, body


# redirects the browser if the user outs in /portfolio vs portfolio.html.
def portfolioHTML():
    header = status(301, "/portfolio.html").encode()
    body = "<html><head></head><body><h1>301 Redirect</h1></body></html>\r\n".encode()
    return header, body


# Gets the latest price from cloud.iexapis and returns that price.
def getStockIndex(stock):
    response_buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.SSL_VERIFYPEER, False)
    curl.setopt(curl.URL, 'https://cloud.iexapis.com/stable/stock/' +
                stock+'/quote?token=pk_a7f87019e6f24a32b7f321db47ce8826')
    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)
    curl.perform()
    curl.close()
    body = response_buffer.getvalue().decode('UTF-8')
    price = json.loads(body)
    price = price.get('latestPrice')
    return price


#  builds the stock to be insersted into the json file.
def newJSON(stock, qty, price, gl):
    obj = {
        "stock": stock,
        "quantity": qty,
        "price": price,
        "Gain/Loss": gl
    }
    return obj


# Opens the JSON file.
def openJSON():
    initiatFile = {"portfolio": [], "symbol": []}
    try:
        with open('portfolio.json') as json_file:
            obj = json.load(json_file)
            return obj
    except Exception:
        print("openJSON()")
        print(Exception)
        return initiatFile


# Adds stock info to portfolio.json, if not already in the portfolio, and its qty is <= 0
def addJSON(stock, qty, price):
    stockValues.clear()
    jsonFile = openJSON()
    print(stock, qty, price)
    if updateJSON(jsonFile, stock, qty, price) != True:
        jsonFile = openJSON()
        latestPrice = getStockIndex(stock)
        newStock = newJSON(stock, qty, price, gainLoss(price, latestPrice))
        jsonFile["portfolio"].append(newStock)
        jsonFile["portfolio"]
        if qty <= 0:
            return
        else:
            wrtieJSON(jsonFile)


# if stock is currently in the list updates it with new details returns true for addJSON() to compare.
def updateJSON(jsonFile, stock, qty, price):
    for item in jsonFile["portfolio"]:
        if item["stock"] == stock:
            nQTY = quantityJSON(item["quantity"], qty)
            latestPrice = getStockIndex(stock)
            print("latestPrice = ", latestPrice)
            nPrice = priceJSON(item["quantity"], qty, item["price"], price)
            item.update({'quantity': nQTY})
            item.update({'price': nPrice})
            item.update({'Gain/Loss': gainLoss(nPrice, latestPrice)})
            if nQTY <= 0:
                jsonFile["portfolio"].remove(item)
            wrtieJSON(jsonFile)
            return True


# works out the weighted total as I was assumed this is an overveiw of the portfolio.
def priceJSON(oldQTY, newQTY, oldPrice, newPrice):
    try:
        total = ((oldPrice*oldQTY)+(newPrice*newQTY))/(oldQTY+newQTY)
        total = float("{:.2f}".format(total))
        return total
    except ZeroDivisionError:
        print(ZeroDivisionError)
        return 0


# Works out the total quantity of stocks added
def quantityJSON(old, new):
    total = old + new
    total = float("{:.2f}".format(total))
    return total


# Works out the gains and losses as per instructions
def gainLoss(final, start):
    try:
        total = ((final-start)/start)*100
        total = float("{:.2f}".format(total))
        return total
    except ZeroDivisionError:
        print(ZeroDivisionError)
        return 0


# Writes the object to a json file.
def wrtieJSON(portfolio):
    try:
        with open('portfolio.json', 'w') as json_file:
            json.dump(portfolio, json_file, indent=4)
            return
    except Exception:
        print("Failed to write to file")
        print(Exception)
        return


# gets the submitted data and splits it up into manageable pieces to be added later.
def getSubmit(resource):
    try:
        item = resource.split("?")
        item = item[1]
        item = item.split("&")
        for pos in item:
            stock = pos.split("=")
            stockValues.append(stock[1])
        stock = stockValues[0]
        qty = stockValues[1]
        qty = float(qty)
        price = stockValues[2]
        price = float(price)
        addJSON(stock.upper(), qty, price)
    except Exception:
        print(Exception)


# redirects to stock.html if user puts in /stock vs stock.html
def stockHTML():
    header = status(301, "/stock.html").encode()
    body = "<html><head></head><body><h1>301 Redirect</h1></body></html>\r\n".encode()
    return header, body


# actions the php file and allows the graph to get the correct stock symbol.
def actionPage(resource):
    sym = resource.split('=')
    jsonFile = openJSON()
    try:
        jsonFile["symbol"].pop(0)
    except Exception:
        print(Exception)
    obj = {"stock": sym[1]}
    jsonFile["symbol"].append(obj)
    wrtieJSON(jsonFile)
    header, body = getFile("action_page.php")
    return header, body


# redirects to the index.html if localhost:8080 is searched.
def homeHTML():
    header = status(301, "/index.html").encode()
    body = "<html><head></head><body><h1>301 Redirect</h1></body></html>\r\n".encode()
    return header, body


# We process client request here. The requested resource in the URL is mapped to a service function which generates the HTTP reponse
# that is eventually returned to the client.
def process(connectionSocket):
    # Receives the request message from the client
    message = connectionSocket.recv(1024).decode()

    if len(message) > 1:
        # Extract the path of the requested object from the message
        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character
        resource = message.split()[1][1:]
        # map requested resource (contained in the URL) to specific function which generates HTTP response
        if auth_header == auth_header in message:
            if resource == "portfolio":
                responseHeader, responseBody = portfolioHTML()
            elif "stock_return.php?" == "stock_return.php?" in resource:
                getSubmit(resource)
                responseHeader, responseBody = getFile("stock_return.php")
            elif resource == "stock":
                responseHeader, responseBody = stockHTML()
            elif "action_page.php?" == "action_page.php?" in resource:
                responseHeader, responseBody = actionPage(resource)
                # originally I was returning a html file for both submits but swapped to php on a mission to fix heroku stalling on post but then realised I didnt really understand php.
                # after a lot of research and better understanding of week 5/6 I think should of done it client side and updated it without the page needing to reload just the container updating dynamically.
            elif resource == "":
                responseHeader, responseBody = homeHTML()
            else:
                responseHeader, responseBody = getFile(resource)
        else:
            responseHeader, responseBody = auth(resource)

    # Send the HTTP response header line to the connection socket
    connectionSocket.send(responseHeader)
    # Send the content of the HTTP body (e.g. requested file) to the connection socket
    connectionSocket.send(responseBody)
    # Close the client connection socket
    connectionSocket.close()


# Main web server loop. It simply accepts TCP connections, and get the request processed in seperate threads.
while True:

    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()

    # Clients timeout after 60 seconds of inactivity and must reconnect.
    connectionSocket.settimeout(60)
    # start new thread to handle incoming request
    _thread.start_new_thread(process, (connectionSocket,))
