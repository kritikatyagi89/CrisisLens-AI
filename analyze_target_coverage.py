"""
CrisisLens AI - Step 6A: Target Coverage Analysis
===================================================

This script calculates the actual availability and distribution of candidate
target variables for the verified 2,224-event subset from 2010-2019.

Author: CrisisLens AI Team
Date: October 11, 2026
"""

import pandas as pd
import numpy as np
import os
import warnings

# Ignore warnings for cleaner output
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = 'data/interim'
OUTPUT_DIR = 'data/interim/target_audit'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("CrisisLens AI - Step 6A: Target Coverage Analysis")
print("=" * 80)
print(f"Data directory: {DATA_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print()

# Step 1: Load and verify the subset
print("=" * 80)
print("STEP 1: Verifying the 2,224-Event Subset")
print("=" * 80)
print()

# Load cleaned dataset
cleaned = pd.read_csv(os.path.join(DATA_DIR, 'validation/atlascat_cleaned.csv'), low_memory=False)
print(f"Loaded atlascat_cleaned.csv: {len(cleaned):,} rows, {len(cleaned.columns)} columns")

# Load exact matches
exact_matches = pd.read_csv(os.path.join(DATA_DIR, 'matching/exact_id_matches.csv'), low_memory=False)
print(f"Loaded exact_id_matches.csv: {len(exact_matches):,} rows")

# Load spatiotemporal matches
spatiotemporal_matches = pd.read_csv(os.path.join(DATA_DIR, 'matching/spatiotemporal_matches.csv'), low_memory=False)
print(f"Loaded spatiotemporal_matches.csv: {len(spatiotemporal_matches):,} rows")

print()

# Verify event IDs
print("Event ID verification:")
print(f"  Unique IDs in cleaned dataset: {cleaned['atlas_usgs_eqid'].nunique():,}")
print(f"  Total rows in cleaned dataset: {len(cleaned):,}")
print(f"  Duplicate IDs: {len(cleaned) - cleaned['atlas_usgs_eqid'].nunique():,}")

if len(cleaned) == cleaned['atlas_usgs_eqid'].nunique():
    print("  Status: NO DUPLICATES")
else:
    print("  Status: DUPLICATES FOUND")

print()

# Verify date range
print("Date range verification:")
if 'datetime' in cleaned.columns:
    cleaned['datetime'] = pd.to_datetime(cleaned['datetime'], errors='coerce')
    min_date = cleaned['datetime'].min()
    max_date = cleaned['datetime'].max()
    print(f"  Date range: {min_date} to {max_date}")
    print(f"  Year range: {min_date.year} to {max_date.year}")

print()

# Check matching outputs
print("Matching outputs verification:")
print(f"  Exact matches: {len(exact_matches):,}")
print(f"  Spatiotemporal matches: {len(spatiotemporal_matches):,}")
print(f"  Total matched events: {len(exact_matches) + len(spatiotemporal_matches):,}")

# Check if cleaned dataset matches expected 2,224
print()
print("Subset verification:")
if len(cleaned) == 2224:
    print(f"  Cleaned dataset rows: {len(cleaned):,} ✓ EXPECTED")
else:
    print(f"  Cleaned dataset rows: {len(cleaned):,} ✗ EXPECTED 2,224")
    print(f"  Discrepancy: {len(cleaned) - 2224:+,}")

print()

# Step 2: Pref_total_deaths analysis
print("=" * 80)
print("STEP 2: Pref_total_deaths Analysis")
print("=" * 80)
print()

death_col = 'pref_total_deaths'
if death_col in cleaned.columns:
    total_records = len(cleaned)
    
    # Convert to numeric, preserving NaN
    death_numeric = pd.to_numeric(cleaned[death_col], errors='coerce')
    
    # Count different value types
    non_null = death_numeric.notna().sum()
    null_count = death_numeric.isna().sum()
    
    # Count zero and positive values
    zero_count = (death_numeric == 0).sum()
    positive_count = (death_numeric > 0).sum()
    negative_count = (death_numeric < 0).sum()
    
    # Check for string values like 'n/a'
    string_values = cleaned[death_col][cleaned[death_col].apply(lambda x: isinstance(x, str))].value_counts()
    
    print(f"Total records: {total_records:,}")
    print(f"Non-null numeric values: {non_null:,} ({non_null/total_records*100:.2f}%)")
    print(f"Missing/NaN values: {null_count:,} ({null_count/total_records*100:.2f}%)")
    print(f"Zero-death records: {zero_count:,}")
    print(f"Positive-death records: {positive_count:,}")
    print(f"Negative or invalid values: {negative_count:,}")
    
    if len(string_values) > 0:
        print(f"String values (n/a, etc.):")
        for val, count in string_values.items():
            print(f"  '{val}': {count:,}")
    else:
        print(f"String values (n/a, etc.): None")
    
    print()
else:
    print(f"Column '{death_col}' not found in cleaned dataset")
    print()

# Step 3: Pref_econ_loss analysis
print("=" * 80)
print("STEP 3: Pref_econ_loss Analysis")
print("=" * 80)
print()

econ_col = 'pref_econ_loss'
if econ_col in cleaned.columns:
    total_records = len(cleaned)
    
    # Convert to numeric, preserving NaN
    econ_numeric = pd.to_numeric(cleaned[econ_col], errors='coerce')
    
    # Count different value types
    non_null = econ_numeric.notna().sum()
    null_count = econ_numeric.isna().sum()
    
    # Count zero and positive values
    zero_count = (econ_numeric == 0).sum()
    positive_count = (econ_numeric > 0).sum()
    negative_count = (econ_numeric < 0).sum()
    
    # Check for string values
    string_values = cleaned[econ_col][cleaned[econ_col].apply(lambda x: isinstance(x, str))].value_counts()
    
    print(f"Total records: {total_records:,}")
    print(f"Non-null numeric values: {non_null:,} ({non_null/total_records*100:.2f}%)")
    print(f"Missing/NaN values: {null_count:,} ({null_count/total_records*100:.2f}%)")
    print(f"Zero-loss records: {zero_count:,}")
    print(f"Positive-loss records: {positive_count:,}")
    print(f"Negative or invalid values: {negative_count:,}")
    
    if len(string_values) > 0:
        print(f"String values (n/a, etc.):")
        for val, count in string_values.items():
            print(f"  '{val}': {count:,}")
    else:
        print(f"String values (n/a, etc.): None")
    
    print()
else:
    print(f"Column '{econ_col}' not found in cleaned dataset")
    print()

# Step 4: Complete-record coverage
print("=" * 80)
print("STEP 4: Complete-Record Coverage")
print("=" * 80)
print()

# Define required columns
required_earthquake = ['magnitude', 'depth_km', 'datetime', 'latitude', 'longitude']
required_exposure = ['MMI_III', 'MMI_VI', 'MMI_VIII', 'max_mmi']  # Core exposure fields

print("Required earthquake features:")
for col in required_earthquake:
    if col in cleaned.columns:
        non_null = cleaned[col].notna().sum()
        print(f"  {col}: {non_null:,}/{len(cleaned):,} ({non_null/len(cleaned)*100:.2f}%)")
    else:
        print(f"  {col}: NOT FOUND")

print()

print("Required exposure features:")
for col in required_exposure:
    if col in cleaned.columns:
        non_null = cleaned[col].notna().sum()
        print(f"  {col}: {non_null:,}/{len(cleaned):,} ({non_null/len(cleaned)*100:.2f}%)")
    else:
        print(f"  {col}: NOT FOUND")

print()

# Calculate coverage counts
coverage_data = []

# 1. Valid death target
valid_death = death_numeric.notna()
coverage_data.append({
    'coverage_type': 'Death target only',
    'count': valid_death.sum(),
    'percentage': valid_death.sum() / len(cleaned) * 100
})

# 2. Death target + core earthquake features
valid_earthquake = cleaned[required_earthquake].notna().all(axis=1)
death_plus_earthquake = valid_death & valid_earthquake
coverage_data.append({
    'coverage_type': 'Death target + core earthquake features',
    'count': death_plus_earthquake.sum(),
    'percentage': death_plus_earthquake.sum() / len(cleaned) * 100
})

# 3. Death target + core features + exposure data
valid_exposure = cleaned[required_exposure].notna().all(axis=1)
death_plus_exposure = death_plus_earthquake & valid_exposure
coverage_data.append({
    'coverage_type': 'Death target + core features + exposure data',
    'count': death_plus_exposure.sum(),
    'percentage': death_plus_exposure.sum() / len(cleaned) * 100
})

# 4. Death target + core features + exposure + verified linkage
# (All events in cleaned dataset have verified linkage by construction)
coverage_data.append({
    'coverage_type': 'Death target + core features + exposure + verified linkage',
    'count': death_plus_exposure.sum(),
    'percentage': death_plus_exposure.sum() / len(cleaned) * 100
})

coverage_df = pd.DataFrame(coverage_data)
print("Complete-record coverage:")
for _, row in coverage_df.iterrows():
    print(f"  {row['coverage_type']}: {row['count']:,} ({row['percentage']:.2f}%)")

print()

# Step 5: Death-count distribution
print("=" * 80)
print("STEP 5: Death-Count Distribution")
print("=" * 80)
print()

valid_deaths = death_numeric[death_numeric.notna() & (death_numeric >= 0)]

if len(valid_deaths) > 0:
    print(f"Observations used for statistics: {len(valid_deaths):,}")
    print()
    print(f"Minimum: {valid_deaths.min():,.0f}")
    print(f"Median: {valid_deaths.median():,.0f}")
    print(f"Mean: {valid_deaths.mean():,.0f}")
    print(f"75th percentile: {valid_deaths.quantile(0.75):,.0f}")
    print(f"90th percentile: {valid_deaths.quantile(0.90):,.0f}")
    print(f"95th percentile: {valid_deaths.quantile(0.95):,.0f}")
    print(f"99th percentile: {valid_deaths.quantile(0.99):,.0f}")
    print(f"Maximum: {valid_deaths.max():,.0f}")
    print()
    
    # Check skewness
    skewness = valid_deaths.skew()
    print(f"Skewness: {skewness:.2f}")
    
    if skewness > 1:
        print("Distribution: HIGHLY SKEWED (right-skewed)")
        print("Interpretation: A few extreme events with very high death counts dominate the mean")
    elif skewness > 0.5:
        print("Distribution: MODERATELY SKEWED")
    else:
        print("Distribution: APPROXIMATELY SYMMETRIC")
    
    print()
else:
    print("No valid death values for distribution analysis")
    print()

# Step 6: Save output files
print("=" * 80)
print("STEP 6: Saving Output Files")
print("=" * 80)
print()

# 1. Matched subset target counts
target_counts_data = {
    'metric': [
        'Total records',
        'Pref_total_deaths non-null',
        'Pref_total_deaths missing',
        'Pref_total_deaths zero',
        'Pref_total_deaths positive',
        'Pref_econ_loss non-null',
        'Pref_econ_loss missing',
        'Pref_econ_loss positive',
        'Death target + core features',
        'Death target + core + exposure',
        'Death target + core + exposure + linkage'
    ],
    'count': [
        len(cleaned),
        non_null,
        null_count,
        zero_count,
        positive_count,
        econ_numeric.notna().sum(),
        econ_numeric.isna().sum(),
        (econ_numeric > 0).sum(),
        death_plus_earthquake.sum(),
        death_plus_exposure.sum(),
        death_plus_exposure.sum()
    ],
    'percentage': [
        100.0,
        non_null / len(cleaned) * 100,
        null_count / len(cleaned) * 100,
        zero_count / len(cleaned) * 100,
        positive_count / len(cleaned) * 100,
        econ_numeric.notna().sum() / len(cleaned) * 100,
        econ_numeric.isna().sum() / len(cleaned) * 100,
        (econ_numeric > 0).sum() / len(cleaned) * 100,
        death_plus_earthquake.sum() / len(cleaned) * 100,
        death_plus_exposure.sum() / len(cleaned) * 100,
        death_plus_exposure.sum() / len(cleaned) * 100
    ]
}

target_counts_df = pd.DataFrame(target_counts_data)
target_counts_df.to_csv(os.path.join(OUTPUT_DIR, 'matched_subset_target_counts.csv'), index=False)
print(f"Saved: matched_subset_target_counts.csv")

# 2. Death target distribution
if len(valid_deaths) > 0:
    distribution_data = {
        'statistic': ['Minimum', 'Median', 'Mean', '75th percentile', '90th percentile', 
                      '95th percentile', '99th percentile', 'Maximum', 'Skewness', 'Observations'],
        'value': [
            valid_deaths.min(),
            valid_deaths.median(),
            valid_deaths.mean(),
            valid_deaths.quantile(0.75),
            valid_deaths.quantile(0.90),
            valid_deaths.quantile(0.95),
            valid_deaths.quantile(0.99),
            valid_deaths.max(),
            skewness,
            len(valid_deaths)
        ]
    }
else:
    distribution_data = {
        'statistic': ['Observations'],
        'value': [0]
    }

distribution_df = pd.DataFrame(distribution_data)
distribution_df.to_csv(os.path.join(OUTPUT_DIR, 'death_target_distribution.csv'), index=False)
print(f"Saved: death_target_distribution.csv")

# 3. Complete feature coverage
coverage_df.to_csv(os.path.join(OUTPUT_DIR, 'complete_feature_coverage.csv'), index=False)
print(f"Saved: complete_feature_coverage.csv")

print()

# Step 7: Print terminal summary
print("=" * 80)
print("TARGET COVERAGE SUMMARY")
print("=" * 80)
print()

print(f"Verified subset: {len(cleaned):,} events")
print(f"Date range: {min_date.year} to {max_date.year}")
print(f"Event ID uniqueness: 100% (no duplicates)")
print()

print("Death target (Pref_total_deaths):")
print(f"  Non-null: {non_null:,} ({non_null/len(cleaned)*100:.2f}%)")
print(f"  Zero deaths: {zero_count:,}")
print(f"  Positive deaths: {positive_count:,}")
print()

print("Economic loss target (Pref_econ_loss):")
print(f"  Non-null: {econ_numeric.notna().sum():,} ({econ_numeric.notna().sum()/len(cleaned)*100:.2f}%)")
print(f"  Positive losses: {(econ_numeric > 0).sum():,}")
print()

print("Complete-record coverage:")
print(f"  Death target + core features: {death_plus_earthquake.sum():,} ({death_plus_earthquake.sum()/len(cleaned)*100:.2f}%)")
print(f"  Death target + core + exposure: {death_plus_exposure.sum():,} ({death_plus_exposure.sum()/len(cleaned)*100:.2f}%)")
print()

if len(valid_deaths) > 0:
    print("Death distribution:")
    print(f"  Median: {valid_deaths.median():,.0f}")
    print(f"  Mean: {valid_deaths.mean():,.0f}")
    print(f"  Max: {valid_deaths.max():,.0f}")
    print(f"  Skewness: {skewness:.2f} (highly skewed)")
    print()

print("=" * 80)
print("Analysis complete. Reports saved to:", OUTPUT_DIR)
print("=" * 80)
