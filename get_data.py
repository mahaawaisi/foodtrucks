import pandas as pd
from sqlalchemy import create_engine, text

# Read data from spreadsheet into a DataFrame
db_name = "foodtrucktest"
df = pd.read_csv('food-truck-data.csv')

# Prepare data (if needed)
columns = ['locationid', 'Applicant', 'FacilityType', 'LocationDescription', 'Address', 'Status', 'FoodItems',
           'X', 'Y', 'Latitude', 'Longitude', 'Location']

df_filtered = df[columns]

# Set up SQLite database
engine = create_engine(f"sqlite:///{db_name}.db")

# Define database schema (if needed)
# For simplicity, let's assume a single table called 'data'
# Adjust the schema according to your spreadsheet structure
schema = """
CREATE TABLE data (
    locationId INTEGER PRIMARY KEY,
    Applicant TEXT,
    FacilityType TEXT,
    LocationDescription TEXT, 
    Address TEXT, 
    Status TEXT,
    FoodItems TEXT,
    X REAL,
    Y REAL, 
    Latitude REAL, 
    Longitude REAL, 
    Location TEXT

)
"""

with engine.connect() as conn:
    conn.execute(text(schema))

# Populate database
df_filtered.to_sql('data', con=engine, if_exists='append', index=False)

print("Data inserted into SQLite database.")
