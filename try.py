import pandas as pd

data = pd.read_csv('./data/ind_nifty50list.csv')

symbols = data['Symbol'].tolist()

print(symbols)

for x in symbols:

    print(f"<h4><a href='{{ url_for('stock', stock='{x}') }}' target='_blank' class='scroll'>{x}</a></h4>")