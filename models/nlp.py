import pandas as pd
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data(task):
    output_file = "cleaned_news.csv"
    output_csv_file = os.path.join(ROOT_PATH, "data", output_file)
    
    if task == "predict":
        df = pd.read_csv(output_csv_file, names=['company', 'body', 'sentiment'])
    elif task == "group":
        df = pd.read_csv(output_csv_file, names=['company', 'body', 'sentiment'])
        df = df[df['sentiment'].str.replace(".", "", 1).str.isnumeric()]
        df['sentiment'] = df['sentiment'].astype(float)
    return df

def predict():
    df = get_data("predict")
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    sentiment_scores = []

    for i in range(len(df)):
        encoded_text = tokenizer(df['body'][i], return_tensors='pt', truncation=True, padding=True, max_length=512)
        output = model(**encoded_text)
        scores = output.logits.detach().numpy()
        scores = softmax(scores, axis=1)
        sentiment_score = scores[0][1]
        sentiment_scores.append(sentiment_score)
    
    df['sentiment'] = sentiment_scores
    df.to_csv(ROOT_PATH + "./data/cleaned_news.csv", index=False)

def group_company(df):
    df = get_data("group")
    company_sentiments = df.groupby('company')['sentiment'].mean().reset_index()
    company_sentiments.to_csv(os.path.join(ROOT_PATH, "data", "company_sentiments_nlp.csv"), index=False)
