from flask import Flask, request, render_template, jsonify
import yfinance as yf
import json
import os
import importlib.util

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Define the path
path = ROOT_PATH + "\\models\\sentiment.py"

# Use importlib to load the module
spec = importlib.util.spec_from_file_location("get_data", path)
get_data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(get_data_module)


app = Flask(__name__)


def get_price(stock):
    ticker = stock + ".NS"
    stock_object = yf.Ticker(ticker)
    data = stock_object.history(period="1d")
    closing_price = data["Close"].iloc[0]
    return str(closing_price)


@app.route('/get_chart_data/<ticker>', methods=['POST'])
def get_stock_data(ticker):
    ticker_symbol = ticker+'.NS'
    interval = request.form.get('interval')
    stock = yf.Ticker(ticker_symbol)

    # Fetch historical data for the given ticker
    if interval == '1d':
        stock_data = stock.history(period='1d', interval='5m')
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
        close_price = round(row['Close'], 2)
        data.append([int(row.name.timestamp()) * 1000, close_price])

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

@app.route("/<stock>")
def stock(stock):
    sentiment = get_data_module.get_data(stock)
    stock_object = yf.Ticker(stock + ".NS")
    data = stock_object.history(period="1d")
    closing_price = round(data["Close"].iloc[0], 2)
    font_color = "#021324"
    decision = ""
    
    with open('static/assets/data.json', 'r') as json_file:
        data = json.load(json_file)
    
    ticker_list = data.get("ticker", [])
    company_list = data.get("company", [])
    company = ""
    
    if stock in ticker_list:
        index = ticker_list.index(stock)
        if index < len(company_list):
            company =  company_list[index]
        else:
            company = stock
        
        if sentiment < -0.2 :
            font_color = "red"
            decision = "Sell"
        elif sentiment >= -0.2 and sentiment <= 0.2 :
            font_color = "#021324"
            decision="Hold"
        elif sentiment > 0.2 :
            font_color = "green"
            decision = "Buy"
    return render_template("stock.html", stockName=stock, companyName=company, price=closing_price, sentiment=round(sentiment, 2), font_color=font_color, decision=decision)


@app.route("/<stock>/closing_price")
def get_closing_price(stock):
    stock_object = yf.Ticker(stock + ".NS")
    data = stock_object.history(period="1d")
    closing_price = data["Close"].iloc[0]

    return str(closing_price)


if __name__ == "__main__":
    app.run(debug=True)
    
