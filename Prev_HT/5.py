import pandas as pd

df = pd.read_csv('daily_data.csv')
pd.set_option("display.max.columns", None)
df.drop(['Unnamed: 0.1', 'Unnamed: 0'], inplace=True, axis=1)

# print(df.head())

new = df.T
print(new.head())

# new["date_played"] = pd.to_datetime(nba["date_game"])

new.to_csv('daily_data_new.csv')
