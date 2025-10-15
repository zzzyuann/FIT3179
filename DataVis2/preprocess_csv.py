import pandas as pd

df = pd.read_csv("netflix_titles.csv")

df = df.dropna(subset=["country"])

df = df.assign(country=df["country"].str.split(", ")).explode("country")

country_mapping = {
    "United States": "United States of America",
    "Russia": "Russian Federation",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Democratic People's Republic of",
    "Iran": "Iran, Islamic Republic of",
    "Egypt": "Egypt, Arab Republic of",
    "Vietnam": "Viet Nam",
    "Syria": "Syrian Arab Republic",
    "Bolivia": "Bolivia, Plurinational State of",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "Laos": "Lao People's Democratic Republic",
    "Tanzania": "Tanzania, United Republic of",
    "Czech Republic": "Czechia"
}

df["country"] = df["country"].replace(country_mapping)

country_counts = df["country"].value_counts().reset_index()
country_counts.columns = ["country", "count"]

country_counts.to_csv("netflix_country_counts.csv", index=False)
