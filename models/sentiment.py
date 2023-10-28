import os
import pandas as pd

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

def get_data():
    file1 = "company_sentiments_nlp.csv"
    file2 = "company_sentiments_time.csv"
    file1_path = os.path.join(ROOT_PATH, "data", file1)
    file2_path = os.path.join(ROOT_PATH, "data", file2)

    df1 = pd.read_csv(file1_path, names=['company', 'sentiment'])
    df2 = pd.read_csv(file2_path, names=['company', 'sentiment'])
    return df1, df2

def calculate_score():
    df1, df2 = get_data()

    # Convert the 'sentiment' column to numeric
    df1['sentiment'] = pd.to_numeric(df1['sentiment'], errors='coerce')
    df2['sentiment'] = pd.to_numeric(df2['sentiment'], errors='coerce')

    # Apply weights to sentiment scores
    df1['sentiment'] = df1['sentiment'] * 0.35  # 35% weight
    df2['sentiment'] = df2['sentiment'] * 0.65  # 65% weight

    # Merge the two DataFrames and group by 'company' to calculate the final score
    merged_df = pd.concat([df1, df2]).groupby('company', as_index=False).sum()

    return merged_df

final_scores = calculate_score()
print(final_scores)
