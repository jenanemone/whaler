#! user/bin/env Python3

import pandas as pd

FILE_TO_AUDIT = "pools_target_cities_feb26/normalized_master_residential.csv"

def run_interrogation():
    print(f"🕵️  Interrogating {FILE_TO_AUDIT}...")
    df = pd.read_csv(FILE_TO_AUDIT, dtype=str)

    # --- TEST 1: The "Squareness" Check ---
    # Zip codes should be 5 digits. If they are city names, the rows shifted.
    drifted = df[~df['site_zip'].str.contains(r'^\d{5}', na=False)]
    
    # --- TEST 2: The "Pivot" Check ---
    # Is 0131 hiding in the name field because of a missing pipe?
    pivot_leak = df[df['owner_name'].str.contains('0131', na=False)]

    # --- TEST 3: Pool Existence Audit ---
    # We treat pool_sqft as a binary flag. 
    # Anything > 0 means "Target Acquired."

    # 1. Convert to numeric for the check
    df['pool_sqft_num'] = pd.to_numeric(df['pool_sqft'], errors='coerce').fillna(0)

    # 2. Identify the target universe
    pool_targets = df[df['pool_sqft_num'] > 0]

    # 3. Validation: Look at the most common values
    # If your top 5 values are '300', '400', '450', etc., you've hit the pool field.
    # If your top values are '2023', '2024', etc., you've accidentally hit a Year column.
    common_values = pool_targets['pool_sqft_num'].value_counts().head(5)
        # --- REPORTING ---
    print(f"✅ Total Pool Properties Found: {len(pool_targets):,}")
    print("\n📋 Top 5 Pool Values (Verify these look like sqft):")
    print(common_values)

    print(f"\n📈 Audit Report:")
    print(f"Total Records: {len(df):,}")
    print(f"Drifted Rows Detected: {len(drifted)}")
    print(f"Pivot Leaks Detected: {len(pivot_leak)}")
    print(f"Pool Whales Found: {len(df[df['pool_sqft_num'] > 0])}")

    if len(drifted) > 0:
        print("\n❌ DRIFT SAMPLE (First 5):")
        print(drifted[['parcel_id', 'site_zip', 'site_city']].head())

if __name__ == "__main__":
    run_interrogation()