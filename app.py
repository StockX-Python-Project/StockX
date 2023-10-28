from flask import Flask, request, render_template, redirect, url_for, jsonify
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import csv

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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/Stock_Price/<stock>", methods=["GET"])
def stuff():
    price = get_price(stock)
    return jsonify(result=price)


@app.route("/<stock>")
def stock(stock):
    # with open("static/assets/ind_nifty50list.csv", "r", newline="") as fr:
    #     reader = csv.DictReader(fr)
    #     for data in reader:
    #         if data["Company Name"].lower().replace(" ", "").find(stock.lower().replace(" ", "")) != -1:
    #             ticker = data["Symbol"] + ".NS"

    # stock_object = yf.Ticker(ticker)
    # data = stock_object.history(period="1d")
    # closing_price = data["Close"].iloc[0]

    # today = stock_object.history(period="1d")
    # week = stock_object.history(period="5d")
    # month = stock_object.history(period="1m")
    # year = stock_object.history(period="1y")
    # maximum = stock_object.history(period="max")

    # today_price = today["Close"]
    # week_price = week["Close"]
    # month_price = month["Close"]
    # year_price = year["Close"]
    # maximum_price = maximum["Close"]

    # today_dates = today.index.date
    # week_dates = week.index.date
    # month_dates = month.index.date
    # year_dates = year.index.date
    # maximum_dates = maximum.index.date

    return render_template("stock.html", stockName=stock)


@app.route("/<stock>/closing_price")
def get_closing_price(stock):
    stock_object = yf.Ticker(stock + ".NS")
    data = stock_object.history(period="1d")
    closing_price = data["Close"].iloc[0]

    return str(closing_price)


if __name__ == "__main__":
    app.run(debug=True)
