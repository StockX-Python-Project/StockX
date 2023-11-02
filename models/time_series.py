import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from datetime import date, timedelta

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error

def train_and_predict(ticker):
    today = date.today() - timedelta(days=5)
    d1 = today.strftime("%Y-%m-%d")
    end_date = d1
    d2 = date.today() - timedelta(days=3655)
    d2 = d2.strftime("%Y-%m-%d")
    start_date = d2

    df = yf.download(ticker, start=start_date, end=end_date, progress=False)

    df = df.asfreq('D', method='ffill')

    df.insert(0, 'Date', df.index, True)
    df.reset_index(drop=True, inplace=True)

    df = df[['Date','Close']]

    def check_stationarity(df):
        result = adfuller(df)
        if result[1] <= 0.05:
            return True
        else:
            return False

    check_stationarity(df['Close'])

    decompose = seasonal_decompose(df['Close'], model='multiplicative', period=30)

    p = 2
    d = 1
    q = 2

    model = SARIMAX(df.Close, order=(p,d,q), seasonal_order=(p,d,q,12))

    model = model.fit()

    predictions = model.predict(start=len(df), end=len(df)+5).rename('SARIMA Predictions')

    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    end_date = d1
    d2 = date.today() - timedelta(days=9)
    d2 = d2.strftime("%Y-%m-%d")
    start_date = d2

    test = yf.download(ticker, start=start_date, end=end_date, progress=False)
    test.insert(0, 'Date', test.index, True)
    test.reset_index(drop=True, inplace=True)
    test = test[['Date','Close']]

    test.set_index(predictions.index, inplace=True)

    mape = mean_absolute_percentage_error(test['Close'], predictions)
    accuracy = 100 - mape

    # Predict the stock price for the next five days
    predictions = model.predict(start=len(df), end=len(df)+5).rename('SARIMA Predictions')

    # Calculate the percentage change in the predicted stock price
    pct_change = ((predictions.iloc[-1] - test.iloc[0]['Close']) / predictions.iloc[0])*100

    # Calculate the score
    score = np.tanh(pct_change)

    # Get the actual price for the last 5 days
    end_date = pd.to_datetime('today')
    start_date = end_date - pd.DateOffset(days=5)
    actual = yf.download(ticker, start=start_date, end=end_date, progress=False)['Close']

    # Append the ticker and score to a CSV file
    df = pd.DataFrame({'Ticker': [ticker], 'Score': [score]})
    df.to_csv('/Users/apple/Desktop/Stock Market Bot/ARIMA/final/scores.csv', mode='a', header=False, index=False)

    print(f'Predicted stock prices for the next five days: {predictions}')
    print(f'Score: {score}')
    print(f'Actual stock prices for the last five days: {actual}')
    print(f'Accuracy: {accuracy}')

    return predictions, score, actual, accuracy

company_tickers = ['TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'WIPRO.NS''ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ITC.NS', 'INDUSINDBK.NS', 'INFY.NS', 'JSWSTEEL.NS', 'JIOFIN.NS', 'KOTAKBANK.NS', 'LTIM.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'NESTLEIND.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', ]
for ticker in company_tickers:
    train_and_predict(ticker)
