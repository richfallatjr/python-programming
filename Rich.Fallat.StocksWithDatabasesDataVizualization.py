"""
Author: Rich 
email:     
Date:       
Version:    1.0
Code Purpose:

"""
from datetime import datetime
import json
import matplotlib.pyplot as plt
import sqlite3

# dictionary setup
filename = "AllStocks.json"
with open(filename) as f:
    data = json.load(f)

# Create entries for stock value based on number of shares
def getStockVal(symbol, close):
    """Calculate the stock value at closing price"""
    num_shares = {
        "GOOG": 25,
        "MSFT": 85,
        "RDS-A": 400,
        "AIG": 235,
        "FB": 150,
        "M": 425,
        "F": 85,
        "IBM": 80
    }
    return num_shares[symbol] * close


# Transform the data so it is ready for graphing
def getSubplot(symbol, symbolList, dateList, closeList):
    """Parse lists to create subplot"""

    date, close = [], []

    for i in range(len(symbolList)):
        if symbolList[i] == symbol:
            date.append(dateList[i])
            close.append(closeList[i])

    return date, close

# Transform JSON data to lists
symbol, date, close = [], [], []

for i in data:
    symbol.append(i["Symbol"])
    # convert json data to datetime object
    date.append(datetime.strptime(i["Date"], "%d-%b-%y"))
    # calculate stock value based on number of shares
    close.append(round(getStockVal(i["Symbol"], i["Close"]), 2))

# Get subplots
goog_date, goog_close = getSubplot("GOOG", symbol, date, close)
msft_date, msft_close = getSubplot("MSFT", symbol, date, close)
rdsa_date, rdsa_close = getSubplot("RDS-A", symbol, date, close)
aig_date, aig_close = getSubplot("AIG", symbol, date, close)
fb_date, fb_close = getSubplot("FB", symbol, date, close)
m_date, m_close = getSubplot("M", symbol, date, close)
f_date, f_close = getSubplot("F", symbol, date, close)
ibm_date, ibm_close = getSubplot("IBM", symbol, date, close)

# Run the graph
plt.style.use("seaborn")
fig, ax = plt.subplots()

ax.plot(goog_date, goog_close, c="#66D9EF", label="GOOG")
ax.plot(msft_date, msft_close, c="#E6DB74", label="MSFT")
ax.plot(rdsa_date, rdsa_close, c="#A6E22E", label="RDS-A")
ax.plot(aig_date, aig_close, c="#F92672", label="AIG")
ax.plot(fb_date, fb_close, c="#AE81FF", label="FB")
ax.plot(m_date, m_close, c="#FD971F", label="M")
ax.plot(f_date, f_close, c="#272822", label="F")
ax.plot(ibm_date, ibm_close, c="#7C806C", label="IBM")

# Format plot
ax.set_title("All Stock Values", fontsize=18)
ax.set_ylabel("Stock Value", fontsize=12)
fig.autofmt_xdate()
plt.legend()

# Save the image
plt.savefig("AllStocks.png")

# Save transformed JSON Data to a database
conn = sqlite3.connect("AllStocks.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS allStocks (
            symbol text,
            date text,
            close float
        )""")

# Transform data to tuples for database
many_stocks = []

for i in range(len(symbol)):
    many_stocks.append((symbol[i], date[i], close[i]))

c.executemany("INSERT INTO allStocks VALUES (?, ?, ?)", many_stocks)

# Validate that tables are available
rows = c.execute("SELECT * FROM allStocks").fetchall()
counter = 0
for i in rows:
    print(i)
    counter += 1

print(f"All Stocks DB contains {counter} rows.")

conn.commit()
conn.close()


