from flask import Flask, request, render_template, redirect, url_for, jsonify
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import csv
import json

app = Flask(__name__)


def get_price(stock):
    with open("static/assets/ind_nifty50list.csv", "r", newline="") as fr:
        reader = csv.DictReader(fr)
        for data in reader:
            if (
                data["Company Name"]
                .lower()
                .replace(" ", "")
                .find(stock.lower().replace(" ", ""))
                != -1
            ):
                ticker = data["Symbol"] + ".NS"
    stock_object = yf.Ticker(ticker)
    data = stock_object.history(period="1d")
    closing_price = data["Close"].iloc[0]
    return str(closing_price)


@app.route('/get_chart_data', methods=['POST'])
def get_stock_data():
    ticker_symbol = 'RELIANCE.NS'
    interval = request.form.get('interval')
    stock = yf.Ticker(ticker_symbol)

    # Fetch historical data for the given ticker
    if interval == '1d':
        stock_data = stock.history(period='1d', interval='30m')
    elif interval == '1w':
        stock_data = stock.history(period='7d', interval='1h')
    elif interval == '1m':
        stock_data = stock.history(period='1mo', interval='1d')
    elif interval == '1y':
        stock_data = stock.history(period='1y', interval='1d')
    elif interval == 'max':
        stock_data = stock.history(period='max')

    data = []
    for idx, row in stock_data.iterrows():
        data.append([int(row.name.timestamp()) * 1000, row['Close']])

    return jsonify(data)

@app.route("/")
def home():
    with open('static/assets/data.json', 'r') as json_file:
        companyData = json.load(json_file)
    return render_template('index.html', data=companyData)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route('/chart')
def index():
    return render_template('chart.html')


@app.route("/Stock_Price/<stock>", methods=["GET"])
def stuff():
    price = get_price(stock)
    return jsonify(result=price)


@app.route("/<stock>")
def stock(stock):
   return render_template("stock.html", stockName=stock)


@app.route("/<stock>/closing_price")
def get_closing_price(stock):
    stock_object = yf.Ticker(stock + ".NS")
    data = stock_object.history(period="1d")
    closing_price = data["Close"].iloc[0]

    return str(closing_price)


if __name__ == "__main__":
    app.run(debug=True)
