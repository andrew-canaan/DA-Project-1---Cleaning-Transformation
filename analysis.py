import pandas as pd
import numpy as np

pd.set_option('display.width', 160)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv("players_21.csv")

print("Number of null entries per column: \n")
print(df.isnull().sum())

# Useful insights gained from df.isnull().sum():

# # The columns gk_handling, gk_positioning etc seem
# # to be a duplicate column for the columns named 
# # goalkeeping_handling, goalkeeping_positiong. 
# # The shorthand columns have 16,861 NaN's in each column
# # Oppositely, the goalkeeping_ columns have no NaN's.
# # Additionally the column defending_marking should be removed
# # as it has n-1 NaN values.
# # Other high NaN count columns include:
# # player_tags: 17536
# # loaned_from: 18186
# # nation_position: 17817
# # nation_jersey_number: 17817
# # gk_diving/handling/kicking/reflexes/speed/positioning: 16861
# # player_traits: 10629
# # defending_marking: 18944

# df = df.dropna() will actually drop the entire
# dataframe as the column defending_marking is entirely
# null except for 1 entry, so it is not an effective means
# of NaN handling in this case.

# This means we need to be thoughtful about how we drop
# NaN's in each column. Additionally, simply imputing
# mean in-place should be done carefully because
# certain players may not have certain entries as those
# players do not play certain positions (i.e. goalkeeping?)

# The following code (doesnt work) should impute in-place the mean
# This code can likely be refactored to go through only columns
# which have entries that are shared by all positions. This is to
# avoid imputing values for traits which certain players don't have, for example
# do non goal-keepers need any values for goalkeeping traits?
# for i in df.columns[df.isnull().any(axis=0)]:
#     df[i].fillna(df[i].mean(),inplace=True)

# Drop rows/columns where all elements are missing
df = df.dropna(how='all')
df = df.drop(columns='defending_marking') # drop defending_marking because it is 99.9% NaN






print("After NaN handling: \n")
print(df.isnull().sum())

