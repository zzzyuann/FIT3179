import pandas as pd

df = pd.read_csv("imdb_top_1000.csv")

df['GrossValue'] = df['Gross'].str.replace(',', '').astype(float)

director_gross = df.groupby('Director')['GrossValue'].sum().reset_index()

top_5_directors = director_gross.sort_values(by='GrossValue', ascending=False).head(5)

top_directors_movies = df[df['Director'].isin(top_5_directors['Director'])]

top_directors_movies.to_csv("top_5_directors.csv", index=False)

