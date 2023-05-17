import pandas as pd
import numpy as np
import re

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
df['goalkeeping_speed'] = df['goalkeeping_speed'].fillna(0)
df.drop(columns=['gk_speed'], axis=1, inplace=True)

# Drop entries that have an empty/NaN team position or team jersey number.
playersToPop = list()
for index in df.index:
    # if 'team_position' or 'team_jersey_number' or 'club_name'or 'league_name' or 'league_rank' entries are empty, remove player
    # rows that have a null entry in team_position also have null entries in the aforementioned columns
    # additionally remove any players who don't have a valid "joined" entry 
    if pd.isnull(df.loc[index, 'team_position']) or pd.isnull(df.loc[index, 'joined']):
        playersToPop.append(index)

for player in playersToPop:
    df.drop(index=player, inplace=True)

# Guiding Question 1: Do the height and weight columns have the appropriate data types?
# Let's begin by examining the data in the columns.
# This can be done by visually inspecting the cesv file, or by pulling out the columns
# with python.
height_entry = df.iloc[1]['height_cm']
weight_entry = df.iloc[1]['weight_kg']
print(f'Height value type: {type(height_entry)}')
print(f'Weight value type: {type(weight_entry)}')

# Guiding Question 2: Can you separate the joined (dd/mm/yyyy) column into year, month, and day columns?
# Let's begin by adding three columns after the 'joined' column for year, month, and day
df.insert(loc=30, column='year_joined', value=['' for i in range(df.shape[0])])
df.insert(loc=31, column='month_joined', value=['' for i in range(df.shape[0])])
df.insert(loc=32, column='day_joined', value=['' for i in range(df.shape[0])])

for index in df.index:
    if not pd.isnull(df.loc[index, 'joined']):
        joined_entry = df.loc[index, 'joined']
        fields = re.split('-', joined_entry)
        df.loc[index, 'year_joined'] = int(fields[0])
        df.loc[index, 'month_joined'] = int(fields[1])
        df.loc[index, 'day_joined'] = int(fields[2])
    if pd.isnull(df.loc[index, 'player_tags']):
        df.loc[index, 'player_tags'] = '#None'

df.drop(columns=['joined'], axis=1, inplace=True) # The joined columns has now been split into separate int fields and stores in their respective columns.

# Guiding Question 3: Can you clean and transform the value, wage, and release clause columns of the integers?
print(df.isnull().sum())
# Inspection shows that wage and value are all non-null, but there are a few null entries in release_clause_eur.
# After doing research into the sport, not all playes have a release clause, so removing players without one
# may be unncecessary. Therefore, the wage, value, and release clause columns are clean as far as data integrity goes.

# Guiding Question 4: How can you remove the newline characters from the Hits column?
# There does not appear to be a hits column, so instead I will add a #None entry for any empty entries in the tags column.
# This code will be done in the loop on line 49 to reduce run time.

# Guiding Question 5: Should you separate the Teams & Contract column into separate team and contract columns?
# Again, this column doesn't seem to exist. Therefore I decided to join the club_name and contract valid until column into 
# a club_until column which displays the club followed by the year their contract expires.

# writer = pd.ExcelWriter("results.xlsx")
# df.to_excel(writer, "Output")
# writer.save()
