from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/get_stock_data', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
