import pandas as pd
import numpy as np

pd.set_option('display.width', 160)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv("players_21.csv")

# Drop rows/columns where all elements are missing
# Drop gk_diving, gk_handling, gk_kicking, gk_reflexes, gk_positioning
df = df.dropna(how='all')
df = df.drop(columns=['defending_marking', 'gk_diving', 'gk_handling', 'gk_kicking', 'gk_reflexes', 'gk_positioning'], axis=1) 

# Insert and copy row for gk_speed before dropping it
df.insert(loc=74, column='goalkeeping_speed', value=['' for i in range(df.shape[0])])
df['goalkeeping_speed'] = df['gk_speed'].copy()
df.drop(columns=['gk_speed'], axis=1, inplace=True) 

# Drop entries that have an empty/NaN team position or team jersey number.
playersToPop = list()
for index in df.index:
    # if 'team_position' or 'team_jersey_number' or 'club_name'or 'league_name' or 'league_rank' entries are empty, remove player
    # rows that have a null entry in team_position also have null entries in the aforementioned columns
    if pd.isnull(df.loc[index, 'team_position']):
        playersToPop.append(index)

for player in playersToPop:
    df.drop(index=player, inplace=True)
    print(f"Removing bad element with index {player}")

print("After NaN handling: \n")
print(df.isnull().sum())

# writer = pd.ExcelWriter("results.xlsx")
# df.to_excel(writer, "Output")
# writer.save()

# x = 0
# for index, row in df.iterrows():
#     if x > 50:
#         break
#     print(row['goalkeeping_speed'])
#     x = x + 1


