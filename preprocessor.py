#! user/bin/env Python3
#!/usr/bin/env python3
import pandas as pd

# The 39-column schema confirmed by line counter for pipe counting as legend belies data form
columns = [
    "parcel_id", "completion", "class", "stories", "cooling_type",
    "heating", "bath_fixtures", "ext_walls", "roof_material", "roof_style",
    "year_built", "sqft_total", "sqft_1", "sqft_2", "sqft_3", "sqft_4",
    "garage_code", "patio_code", "pool_sqft", "sale_price", "sale_date",
    "added_sqft", "detach_sqft", "puc", "owner_name", "mail_street", 
    "mail_unit", "mail_city", "mail_state", "mail_zip", "mail_country",
    "site_number", "site_dir", "site_name", "site_type", "site_unit1", 
    "site_unit2", "site_city", "site_zip"
]

input_path = "pools_target_cities_feb26/maricopa_master_residential.txt"
output_path = "pools_target_cities_feb26/normalized_master_residential.csv"

print("Loading 1.4M records with Pandas...")

# Use 'low_memory=False' or 'dtype=str' to prevent DtypeWarnings, quoting=3 so quotes don't trip up Pandas
df = pd.read_csv(input_path, sep="|", names=columns, header=None, dtype=str, engine="c", quoting=3, encoding="latin1")

print(f"📊 Shape detected: {df.shape}")

# Select the specific columns for the "Square Check"
normalized = df[[
    "parcel_id", 
    "year_built", 
    "garage_code", 
    "patio_code", 
    "pool_sqft", 
    "sale_price", 
    "sale_date", 
    "owner_name", 
    "mail_street", 
    "mail_city", 
    "mail_state", 
    "mail_zip", 
    "mail_country",
    "site_number", 
    "site_dir", 
    "site_name", 
    "site_type", 
    "site_city", 
    "site_zip"
]].copy()

print("💾 Saving normalized audit file...")
normalized.to_csv(output_path, index=False)

print(f"🏁 Done! Review {output_path} to verify alignment.")