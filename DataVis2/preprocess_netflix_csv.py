import pandas as pd

# === 1. Load and clean Netflix data ===
df = pd.read_csv("netflix_titles.csv")

# Drop missing countries
df = df.dropna(subset=["country"])

# Split multiple countries into separate rows
df = df.assign(country=df["country"].str.split(", ")).explode("country")

# Country name mapping for alignment with World Bank / TopoJSON
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

# === 2. Count titles per country ===
country_counts = df["country"].value_counts().reset_index()
country_counts.columns = ["country", "count"]

# === 3. Add 2021 population data (in people) ===
population_2021 = {
    "United States of America": 331002651,
    "India": 1393409038,
    "United Kingdom": 68207116,
    "Canada": 38005238,
    "France": 67391582,
    "Japan": 125836021,
    "Spain": 47351567,
    "Korea, Republic of": 51709098,
    "Germany": 83240525,
    "Mexico": 126014024,
    "China": 1411778724,
    "Australia": 25788216,
    "Egypt, Arab Republic of": 109262178,
    "Turkey": 85652000,
    "Hong Kong": 7474200,
    "Nigeria": 213401323,
    "Italy": 59554023,
    "Brazil": 213993437,
    "Argentina": 45605823,
    "Belgium": 11589623,
    "Indonesia": 273753191,
    "Taiwan": 23568378,
    "Philippines": 111046913,
    "Russian Federation": 143446060,
    "Iran, Islamic Republic of": 85028760,
    "Czechia": 10708981,
    "Viet Nam": 98168829,
    "Venezuela, Bolivarian Republic of": 28301498,
    "Lao People's Democratic Republic": 7447396,
    "Tanzania, United Republic of": 63588334,
    "Korea, Democratic People's Republic of": 25869218,
    "Syrian Arab Republic": 22125247,
    "Bolivia, Plurinational State of": 12079471
}

pop_df = pd.DataFrame(list(population_2021.items()), columns=["country", "population_2021"])

# === 4. Merge population data ===
country_counts = pd.merge(country_counts, pop_df, on="country", how="left")

# === 5. Compute titles per million people ===
country_counts["titles_per_million"] = (country_counts["count"] / country_counts["population_2021"]) * 1_000_000

# === 6. Save to CSV ===
country_counts.to_csv("netflix_country_counts.csv", index=False)

print(country_counts.head(10))
