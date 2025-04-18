# Inspect Python objects with type , help , dir , and vars
- type : shows the class of an object.
- help : shows documentation for an object.
- dir : shows all attributes and methods that the object supports.
- vars : shows attributes which live directly on that object.

PANDAS

- df.describe() : gets a summary of statistics for numeric columns in the dataframe
- df.info() : analogue for the glimpse() command in tidyverse 
- df.sort_values(by='time') : sort a dataframe by a specific column
- df.sort_values(by='time', ascending=True, inplace=True) : sort a dataframe by a specific column in place
- df[df['column'] == value] : filter rows in a DataFrame where a column equals a specific value

PICKLE

- pd.to_pickle('filename.pkl') : save a DataFrame to a pickle file
- pd.read_pickle('filename.pkl') : load a DataFrame from a pickle file