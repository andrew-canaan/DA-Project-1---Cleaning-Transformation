import pandas as pd
import numpy as np
import re

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

df = pd.read_csv("players_21.csv")

# Drop rows/columns where all/99% of elements are missing
df = df.dropna(how="all")
df = df.drop(
    columns=[
        "defending_marking",
        "gk_diving",
        "gk_handling",
        "gk_kicking",
        "gk_reflexes",
        "gk_positioning",
    ],
    axis=1,
)

# Insert and copy row for gk_speed before dropping it
df.insert(loc=30, column="year_joined", value=["" for i in range(df.shape[0])])
df.insert(loc=31, column="month_joined", value=["" for i in range(df.shape[0])])
df.insert(loc=32, column="day_joined", value=["" for i in range(df.shape[0])])
df.insert(loc=74, column="goalkeeping_speed", value=["" for i in range(df.shape[0])])

df["goalkeeping_speed"] = df["gk_speed"].copy()
df["goalkeeping_speed"] = df["goalkeeping_speed"].fillna(0)

df.drop(columns=["gk_speed"], axis=1, inplace=True)

# Checking if stored types are valid types for the data they store
height_entry = df.iloc[1]["height_cm"]
weight_entry = df.iloc[1]["weight_kg"]
print(f"Height value type: {type(height_entry)}")
print(f"Weight value type: {type(weight_entry)}")

playersToPop = list()
for index in df.index:
    # if 'team_position' or 'team_jersey_number' or 'club_name'or 'league_name' or 'league_rank' entries are empty, remove player
    # rows that have a null entry in team_position also have null entries in the aforementioned columns
    # additionally remove any players who don't have a valid "joined" entry
    if pd.isnull(df.loc[index, "team_position"]) or pd.isnull(df.loc[index, "joined"]):
        playersToPop.append(index)

    if pd.isnull(df.loc[index, "player_tags"]):
        df.loc[index, "player_tags"] = "#None"

    # Give goalkeepers zeroes for pace, shooting, passing, dribbling, defending, physic
    if pd.isnull(df.loc[index, "pace"]):
        df.loc[index, "pace"] = 0
        df.loc[index, "shooting"] = 0
        df.loc[index, "passing"] = 0
        df.loc[index, "dribbling"] = 0
        df.loc[index, "defending"] = 0
        df.loc[index, "physic"] = 0

    if not pd.isnull(df.loc[index, "joined"]):
        joined_entry = df.loc[index, "joined"]
        fields = re.split("-", joined_entry)
        df.loc[index, "year_joined"] = int(fields[0])
        df.loc[index, "month_joined"] = int(fields[1])
        df.loc[index, "day_joined"] = int(fields[2])

for player in playersToPop:
    df.drop(index=player, inplace=True)

df.drop(
    columns=["joined"], axis=1, inplace=True
)  # The joined columns has now been split into separate int fields and stores in their respective columns.


print(df.isnull().sum())

# writer = pd.ExcelWriter("results.xlsx")
# df.to_excel(writer, "Output")
# writer.save()
