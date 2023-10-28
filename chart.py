import csv
import json
import yfinance

def get_data(name, time):
    with open('./data/ind_nifty50list.csv') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        column_index = 2 
        nifty50 = tuple(row[column_index] for row in reader)

    if name in nifty50 and (time == "1y" or time == "3y" or time == "5y" or time == "max"):
        stock = yfinance.Ticker(name + ".NS")
        hist = stock.history(period = time)
        json_data = hist.to_json(orient="records", indent=4)
        print(json_data)
    return json_data
