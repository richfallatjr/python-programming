"""
Author: Rich Fallat
email:  rich.fallat@du.edu   
Date:       6/4/21
Version:    2.0
Code Purpose: To read json data, graph the data, and save the data to a database.

"""
from datetime import datetime
import json
import matplotlib.pyplot as plt
import sqlite3


class StockGraph:
    """Create a time series graph from a json file"""
    def __init__(self, jsonFile):
        try:
            self._jsonFile = str(jsonFile)
        except TypeError:
            print("TypeError: The given file is not a string.")

        self._stocks = {
            "GOOG": {
                "num_shares": 25,
                "color": "#66D9EF"
            },
            "MSFT": {
                "num_shares": 85,
                "color": "#E6DB74"
            },
            "RDS-A": {
                "num_shares": 400,
                "color": "#A6E22E"
            },
            "AIG": {
                "num_shares": 235,
                "color": "#F92672"
            },
            "FB": {
                "num_shares": 150,
                "color": "#AE81FF"
            },
            "M": {
                "num_shares": 425,
                "color": "#FD971F"
            },
            "F": {
                "num_shares": 85,
                "color": "#272822"
            },
            "IBM": {
                "num_shares": 80,
                "color": "#7C806C"
            }
        }

        self.symbol = []
        self.date = []
        self.close = []
        
    def getJsonFile(self):
        return self._jsonFile

    def getJsonData(self):
        # dictionary setup
        filename = self.getJsonFile()
        with open(filename) as f:
            data = json.load(f)
        return data

    def getStocks(self):
        return self._stocks

    def getStockVal(self, symbol, close):
        """Calculate the stock value at closing price"""
        try:
            return self.getStocks()[symbol]["num_shares"] * close
        except KeyError:
            return 0

    def xformJson(self):
        """Transform json data into lists"""
        self.symbol, self.date, self.close = [], [], []

        for i in self.getJsonData():
            self.symbol.append(i["Symbol"])
            # convert json data to datetime object
            self.date.append(datetime.strptime(i["Date"], "%d-%b-%y"))
            # calculate stock value based on number of shares
            try:
                self.close.append(round(self.getStockVal(i["Symbol"], i["Close"]), 2))
            except TypeError:
                print("TypeError: The number shares input is not a number.")
                self.close.append(0)

        return self.symbol, self.date, self.close

    def getSubplot(self, symbol):
        """Parse lists to create subplot"""
        symbolList, dateList, closeList = self.xformJson()

        date, close = [], []

        for i in range(len(symbolList)):
            if symbolList[i] == symbol:
                date.append(dateList[i])
                close.append(closeList[i])

        return date, close

    def makePlots(self):
        """Create subplots based on symbols"""
        plt.style.use("seaborn")
        fig, ax = plt.subplots()

        for i in self.getStocks().keys():
            date, close = self.getSubplot(i)
            ax.plot(date, close, c=self.getStocks()[i]["color"], label=i)

        # Format plot
        ax.set_title("All Stock Values", fontsize=18)
        ax.set_ylabel("Stock Value", fontsize=12)
        fig.autofmt_xdate()
        plt.legend()

        # Save the image
        plt.savefig("AllStocks.png")

    def putDB(self, dbFile):
        """Save data to database"""
        try:
            self.dbFile = str(dbFile)
        except TypeError:
            print("TypeError: The given file is not a string.")

        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS allStocks (
                    symbol text,
                    date text,
                    close float
                )""")

        # Transform data to tuples for database
        many_stocks = []

        for i in range(len(self.symbol)):
            many_stocks.append((self.symbol[i], self.date[i], self.close[i]))

        c.executemany("INSERT INTO allStocks VALUES (?, ?, ?)", many_stocks)

        # Validate that tables are available
        rows = c.execute("SELECT * FROM allStocks").fetchall()
        counter = 0
        for i in rows:
            print(i)
            counter += 1

        print(f"{self.dbFile} contains {counter} rows.")

        conn.commit()
        conn.close()

    def setStocks(self):
        """Set the stocks via user input."""
        active = "n"

        active = input("Would you like to input the stock data? y/n ")

        # reset init stocks dictionary
        if active == "y":
            self._stocks = {}

        while active == "y":
            symbol = input("Which symbol? ")
            num_shares = float(input("How many shares? "))
            color = input("What color? ")
            self._stocks[symbol] = {
                "num_shares": num_shares,
                "color": color
            }
            active = input("Would you like to add another stock? y/n ")

stocks = StockGraph("AllStocks.json")
stocks.setStocks()
stocks.makePlots()
#stocks.putDB("AllStocks.db")
