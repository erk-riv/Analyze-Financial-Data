import pandas as pd
import numpy as np
import pandas_datareader.data as web
from matplotlib import pyplot as plt
from datetime import datetime


# =======================================================================================================================
# Graphs
def data(ticker, start, end):
    df = web.DataReader(ticker, 'yahoo', start, end)
    print("""

  ---------------------------------------------------------------------------
  """)
    print(ticker + ' Statistics\n')
    print(df.describe())

    # plt.figure(figsize=(20, 4))
    plt.subplot(2, 2, 1)
    df['Adj Close'].plot(legend=True, figsize=(10, 4))
    plt.title("Historical Closing Price")

    plt.subplot(2, 2, 2)
    df['Volume'].plot(legend=True, figsize=(10, 4))
    plt.title("Total Trading Volume")

    plt.subplot(2, 2, 3)
    df['Daily Return'] = df['Adj Close'].pct_change()
    # Then we'll plot the daily return percentage
    df['Daily Return'].plot(figsize=(12, 4), legend=True, linestyle='--', marker='o')
    plt.title("Daily Return")
    # df['Adj Close'].plot(legend=True, figsize=(10, 4))
    # df['Volume'].plot(legend=True, figsize=(10, 4))
    plt.tight_layout()
    plt.show()


# =======================================================================================================================

# grab ticker info
from yahoo_fin import stock_info as index

print('Grabbing Up to Date Stock Tickers...')
t1 = pd.DataFrame(index.tickers_sp500())
t2 = pd.DataFrame(index.tickers_nasdaq())
t3 = pd.DataFrame(index.tickers_dow())
t4 = pd.DataFrame(index.tickers_other())
s1 = set(symbol for symbol in t1[0].values.tolist())
s2 = set(symbol for symbol in t2[0].values.tolist())
s3 = set(symbol for symbol in t3[0].values.tolist())
s4 = set(symbol for symbol in t4[0].values.tolist())
tickers = set.union(s1, s2, s3, s4)
# W,R,P,Q are all extra suffixes that signify unwanted stocks, W = Outstanding Warrants, R = Rights Issues,
# P = Preferred Stocks, Q = Bankruptcy
unwanted_suffixes = ['W', 'R', 'P', 'Q']

# Look for symbols longer than 4 characters (have unwanted suffixes) and remove them
del_set = set()
sav_set = set()

for symbol in tickers:
    if len(symbol) > 4 and symbol[-1] in unwanted_suffixes:
        del_set.add(symbol)
    else:
        sav_set.add(symbol)
# =======================================================================================================================

# MAIN
print(f'There are {len(sav_set)} qualified stock symbols...\n')
while (True):
    print("Please Enter A Stock Ticker, EX: AAPL")
    inp = input("Stock: ").upper()
    if inp == 'DONE':
        exit()
    elif inp in sav_set and inp != '':
        while True:
            print("Enter a timeframe between 1 - 5 yrs")
            print("Or Enter 0 to Head Back to the Main Menu")
            while True:
                try:
                    time = int(input("Timeframe: "))
                    break
                except:
                    print("Enter an Integer!")
            if 1 <= time <= 5:
                end = datetime.now()
                start = datetime(end.year - time, end.month, end.day)
                data(inp, start, end)
            elif time == 0:
                print("Heading to Main Menu...")
                break
            else:
                print("Invalid Timeframe!")

    else:
        print("Invalid Stock - Please Try Again\n")
