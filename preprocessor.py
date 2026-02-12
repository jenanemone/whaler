#! user/bin/env Python3

# check validity of parse structure pipe against provided instructions
import pandas as pd

# validate pandas is within venv
print(f"Pandas location: {pd.__file__}")

# for file work
import sys

# Verification step: Does Pandas see what we see? Does it follow the provided columnar shape?
test_df = pd.read_csv('pools_target_cities_feb26/maricopa_master_residential.txt', sep='|', header=None, nrows=1, encoding='latin1')
actual_col_count = test_df.shape[1]

if actual_col_count != 35:
    print(f"⚠️ Warning: Detected {actual_col_count} columns, but expected 35.")

# Load just the very first row of the real file
df_audit = pd.read_csv('pools_target_cities_feb26/maricopa_master_residential.txt', sep='|', header=None, nrows=1, encoding='latin1')

print("--- 🗺️ THE ACTUAL 39-COLUMN MAP ---")
for i, value in enumerate(df_audit.iloc[0]):
    print(f"Index {i}: {value}")

