#!/usr/bin/env python3
import csv, random, os

random.seed(42)
ROWS = 5000
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "california_housing.csv")

COLUMNS = [
    "longitude", "latitude", "housing_median_age", "total_rooms",
    "total_bedrooms", "population", "households", "median_income",
    "median_house_value"
]

def generate_row():
    longitude      = round(random.uniform(-124.35, -114.31), 4)
    latitude       = round(random.uniform(32.54, 41.95), 4)
    housing_age    = random.randint(1, 52)
    households     = random.randint(50, 2000)
    total_rooms    = households * random.randint(3, 8)
    total_bedrooms = int(total_rooms * random.uniform(0.18, 0.35))
    population     = int(households * random.uniform(2.0, 3.5))
    median_income  = round(random.uniform(0.5, 15.0), 4)
    price = (
        median_income * 20000
        - (latitude - 34) * 15000
        - (longitude + 118) * 8000
        + housing_age * 500
        + random.gauss(0, 30000)
    )
    price = max(14999, min(500001, round(price, 2)))
    return [longitude, latitude, housing_age, total_rooms,
            total_bedrooms, population, households, median_income, price]

with open(OUTPUT, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(COLUMNS)
    for _ in range(ROWS):
        writer.writerow(generate_row())

print(f"Generated {ROWS} rows → {OUTPUT}")
