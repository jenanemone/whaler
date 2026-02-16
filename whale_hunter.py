#! user/bin/env Python3
import pandas as pd

INPUT_CSV = "pools_target_cities_feb26/normalized_master_residential.csv"
FINAL_TARGETS = "pools_target_cities_feb26/maricopa_master_whale_leads_auidted.csv"

def generate_whale_targets_final():
    print("🎯 Initializing Final Whale Hunter...")
    
    # Load data
    df = pd.read_csv(INPUT_CSV, dtype=str, encoding='latin1')
    
    # 1. Qualify for Pools
    # We do this first to shrink the dataset size for faster processing
    df['pool_sqft_num'] = pd.to_numeric(df['pool_sqft'], errors='coerce').fillna(0)
    pools = df[df['pool_sqft_num'] > 0].copy()

    # 2. THE CLEANING & GHOST PURGE
    # Create a clean version for grouping, but keep the original for the final CSV
    pools['owner_name_clean'] = pools['owner_name'].fillna('').str.strip().str.upper()
    
    # Identify junk: actual nulls, the string 'NAN', or empty strings
    junk_values = ['NAN', 'N/A', '', 'NONE', 'NULL', 'UNKNOWN']
    ghost_mask = (pools['owner_name_clean'].isin(junk_values)) | (pools['owner_name'].isna())
    
    print(f"👻 Ghost Audit: Removing {ghost_mask.sum():,} nameless/junk pool properties.")
    pools = pools[~ghost_mask].copy()

    # 3. Create the Mail Key (Grouping by physical location to find stealth whales)
    pools['mail_key'] = (
        pools['mail_street'].fillna('') + "|" + 
        pools['mail_city'].fillna('') + "|" + 
        pools['mail_state'].fillna('')
    ).str.upper().str.strip()

    # 4. Calculate Strength (The Portfolio Count)
    print("📊 Calculating Portfolio Strength...")
    # This counts how many times each NAME and each ADDRESS appears
    name_counts = pools.groupby('owner_name_clean')['parcel_id'].transform('count')
    addr_counts = pools.groupby('mail_key')['parcel_id'].transform('count')
    
    # We take the max. If an LLC name has 1 house, but the address has 50, the LLC gets a score of 50.
    pools['portfolio_strength'] = pd.concat([name_counts, addr_counts], axis=1).max(axis=1)

    # 5. Filter for Whales (2 or more properties)
    whales = pools[pools['portfolio_strength'] >= 2].copy()

    # 6. Labeling the Tiers
    def get_tier(count):
        if count >= 50: return 'Tier 1: Institutional'
        if count >= 10: return 'Tier 2: Mid-Size Investor'
        return 'Tier 3: Local Multi-Owner'

    whales['target_tier'] = whales['portfolio_strength'].apply(get_tier)

    # 7. Sorting: Biggest Portfolios at the top
    whales = whales.sort_values(by=['portfolio_strength', 'owner_name'], ascending=[False, True])

    # 8. Final Export - Using your exact verified column list
    final_cols = [
        'owner_name', 'portfolio_strength', 'target_tier', 
        'mail_street', 'mail_city', 'mail_state', 'mail_zip', 
        'parcel_id', 'site_city', 'site_zip', 'pool_sqft'
    ]
    
    # Check to make sure we don't try to export anything missing
    existing_cols = [c for c in final_cols if c in whales.columns]
    
    whales[existing_cols].to_csv(FINAL_TARGETS, index=False)
    
    print(f"🏁 Success!")
    print(f"Total Unique Whale Entities: {whales['owner_name_clean'].nunique():,}")
    print(f"Lead list saved to: {FINAL_TARGETS}")

if __name__ == "__main__":
    generate_whale_targets_final()