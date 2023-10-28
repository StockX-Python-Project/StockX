import csv, yfinance as yf
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

stock = "Tata Consultancy Services"
with open("static/assets/ind_nifty50list.csv", "r", newline="") as fr:
    reader = csv.DictReader(fr)
    for data in reader:
        if data["Company Name"].lower().replace(" ", "").find(stock.lower().replace(" ", "")) != -1:
            print(data["Company Name"])
            ticker = data["Symbol"] + ".NS"
            print(ticker)

stock_object = yf.Ticker(ticker)
today = stock_object.history(period="1d")
week = stock_object.history(period="5d")
month = stock_object.history(period="1m")
year = stock_object.history(period="1y")
maximum = stock_object.history(period="max")

today_price = today["Close"]
week_price = week["Close"]
month_price = month["Close"]
year_price = year["Close"]
maximum_price = maximum["Close"]

today_dates = today.index.date
week_dates = week.index.date
month_dates = month.index.date
year_dates = year.index.date
maximum_dates = maximum.index.date

fig = px.line(x=week_dates, y=week_price)
fig.show()


# st.title(f"Price of {stock}")
# fig, ax = plt.subplots()
# ax = week_price.plot(figsize=(12, 8), title=stock+" Stock Price", fontsize=20, label="CLose Price")
# plt.legend()
# plt.grid()
# st.pyplot(fig)


# fig = go.Figure(data=go.Scatter(x=week_dates, y=week_price, mode="lines"))
# fig.show()

# print(today, week, month, year, maximum)
# closing_price = data["Close"][0]
# print(closing_price)
# price_data = yf.download(ticker , start = '2021-01-01', end = '2021-08-25')
# print(price_data)