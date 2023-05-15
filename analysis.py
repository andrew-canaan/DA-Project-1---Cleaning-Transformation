import pandas as pd
import numpy as np

pd.set_option('display.width', 160)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv("players_21.csv")

print("Number of null entries per column: \n")
print(df.isnull().sum())

# Drop rows/columns where all elements are missing
# Drop gk_diving, gk_handling, gk_kicking, gk_reflexes, gk_positioning
df = df.dropna(how='all')
df = df.drop(columns=['defending_marking', 'gk_diving', 'gk_handling', 'gk_kicking', 'gk_reflexes', 'gk_positioning'], axis=1) 

# Insert and copy row for gk_speed before dropping it
df.insert(loc=74, column='goalkeeping_speed', value=['' for i in range(df.shape[0])])
df['goalkeeping_speed'] = df['gk_speed'].copy()
df['goalkeeping_speed'] = df['goalkeeping_speed'].fillna(0)
df = df.drop(columns=['gk_speed'], axis=1) 

# Drop entries that have an empty/NaN team position or team jersey number.
for index, row in df.iterrows():
    if row['team_position'] == np.nan or row['team_position'] == '':
        df.drop(df.index)
        print("a")
        continue
    if row['team_jersey_number'] == np.nan or row['team_jersey_number'] == '':
        df.drop(df.index)
        print("a")
        continue

print("After NaN handling: \n")
print(df.isnull().sum())

# TODO IF STATEMENTES ON LINE 26, 30 ARE NOT EXECUTING

# x = 0
# for index, row in df.iterrows():
#     if x > 50:
#         break
#     print(row['goalkeeping_speed'])
#     x = x + 1


