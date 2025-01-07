import pandas as pd

query = "SELECT * FROM books;"
dataframe = pd.read_sql(query, con=engine)
print(dataframe.head())