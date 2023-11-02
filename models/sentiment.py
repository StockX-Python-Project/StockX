import os
import pandas as pd
import json
import csv

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data(company):
    file1 = "company_sentiments_nlp.csv"
    file2 = "company_sentiments_time.csv"
    file1_path = os.path.join(ROOT_PATH, "data", file1)
    file2_path = os.path.join(ROOT_PATH, "data", file2)
    
    with open('static/assets/data.json', 'r') as json_file:
        data = json.load(json_file)
        
    index = -1
    for i, item in enumerate(data['ticker']):
        if item == company:
            index = i
            break 
    company_1 = data['nlpTicker'][index]
    
    score_1=0.0
    score_2=0.0
    
    with open(file1_path, mode='r') as csv_file:
        csv_reader_1 = csv.reader(csv_file)
        next(csv_reader_1)
        for row in csv_reader_1:
            if (row[0] == company_1):
                score_1=row[1]
    with open(file2_path, mode='r') as csv_file:
        csv_reader_2 = csv.reader(csv_file)
        next(csv_reader_2)
        for row in csv_reader_2:
            if (row[0] == company+".NS"):
                score_2=row[1]
        

    return ((float(score_1)+float(score_2))/2)