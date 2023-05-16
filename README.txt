Dataset: FIFA 21 Players Dataset (https://www.kaggle.com/datasets/stefanoleone992/fifa-21-complete-player-dataset)

Guiding Questions:
a. Do the height and weight columns have the appropriate data types?
    - Yes, the columns have the appropriate data types as they are int64's. Scalar values such
    as heigh, or weight should be stored as ints/floats depending.
b. Can you separate the joined column into year, month, and day columns?
c. Can you clean and transform the value, wage, and release clause columns of the integers?
d. How can you remove the newline characters from the Hits column?
e. Should you separate the Teams & Contract column into separate team and contract columns?

Observations: 
- The columns gk_handling, gk_positioning etc seem to be a duplicate column for the columns named goalkeeping_handling, goalkeeping_positiong. 
The shorthand columns have 16,861 NaN's in each column Oppositely, the goalkeeping_ columns have no NaN's.
Additionally the column defending_marking should be removed as it has n-1 NaN values.
Other high NaN count columns include:
    player_tags: 17536
    loaned_from: 18186
    nation_position: 17817
    nation_jersey_number: 17817
    gk_diving/handling/kicking/reflexes/speed/positioning: 16861
    player_traits: 10629
    defending_marking: 18944

- This means we need to be thoughtful about how we drop NaN's in each column. Additionally, simply imputing mean in-place should be done carefully 
because certain players may not have certain entries as those players do not play certain positions.

- I chose to delete the columns gk_xyz as they are a duplicate column of goalkeeping_xyz traits. The former columns is only non-null when the player
is actually a goalkeepr. If the player is not a goalkeeper, the entry will be NaN. However the column goalkeeping_xyz does have values even if the
player is not a goalkeeper. This is very visible when you look at goalkeeping_xyz traits of goalkeeper vs non goalkeeper. The goalkeeper will
have significantly higher values. Therefore, we can also drop the gk_xyz columns with the EXCEPTION of gk_speed. gk_speed is missing from the other
goalkeeping columns, so instead what should be done is:
    add a columns goalkeeping_speed to match gk_speed after column goalkeeping_reflexes
    copy gk_speed column into goalkeeping_speed and replace any NaN's with zero

- Any players with blank positions should be dropped

- df.isnull() does not count empty strings as null