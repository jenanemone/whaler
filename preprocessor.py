#! user/bin/env Python3

import re
import csv

INPUT_FILE = 'pools_target_cities_feb26/maricopa_master_residential.txt'
OUTPUT_FILE = 'pools_target_cities_feb26/verified_pool_list.csv'

# Patterns based on your data sample
garage_pat = re.compile(r'^[GCR]\d-\d+') # Matches G2-380
patio_pat = re.compile(r'^(CV|UC)-')     # Matches CV-120

print("🎯 High-Precision Pool Extraction Starting...")

with open(INPUT_FILE, 'r', encoding='latin1') as f_in, \
     open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f_out:
    
    writer = csv.writer(f_out)
    writer.writerow(['parcel', 'pool_sqft', 'owner', 'mail_addr', 'city', 'zip'])

    pool_count = 0
    for line in f_in:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 25: continue

        # FIND THE GARAGE LANDMARK
        # In your data, Pool SqFt is exactly TWO columns after Garage
        # Garage (Index 16) -> Patio (Index 17) -> POOL (Index 18)
        
        garage_idx = -1
        for i, part in enumerate(parts):
            if garage_pat.match(part):
                garage_idx = i
                break
        
        if garage_idx != -1:
            try:
                # Based on your data: 10101028...|G2-400|CV-150|400|...
                # Pool is garage_idx + 2
                pool_sqft = float(parts[garage_idx + 2])
                
                if pool_sqft > 0:
                    # Anchor backward from the 'USA' field for stability
                    # USA is usually index -10 or -11 in your sample
                    usa_idx = -1
                    if "USA" in parts:
                        usa_idx = parts.index("USA")
                    
                    owner = parts[usa_idx - 6] if usa_idx != -1 else "Unknown"
                    addr = parts[usa_idx - 5] if usa_idx != -1 else "Unknown"
                    city = parts[usa_idx - 2] if usa_idx != -1 else "Unknown"
                    zip_code = parts[usa_idx - 1] if usa_idx != -1 else "Unknown"

                    writer.writerow([parts[0], pool_sqft, owner, addr, city, zip_code])
                    pool_count += 1
            except (ValueError, IndexError):
                continue

print(f"🏁 DONE! Found {pool_count} verified pools.")