"""
CrisisLens AI - Step 4: AtlasCat Table Integration and Validation
===================================================================

This script integrates the three AtlasCat tables (Constraints, Exposure, Losses)
using verified event IDs from the matching process.

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
DATA_DIR = 'data/raw'
MATCHING_DIR = 'data/interim/matching'
OUTPUT_DIR = 'data/interim/integration'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("CrisisLens AI - Step 4: AtlasCat Table Integration and Validation")
print("=" * 80)
print(f"Data directory: {DATA_DIR}")
print(f"Matching directory: {MATCHING_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print()

# Step 1: Inspect column names
print("=" * 80)
print("STEP 1: Inspecting Column Names")
print("=" * 80)
print()

# Load AtlasCat files to inspect column names
constraints = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Constraints.csv'))
exposure = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Exposure.csv'))
losses = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Losses.csv'), low_memory=False)

print("AtlasCat_Constraints.csv columns:")
print(f"  Total columns: {len(constraints.columns)}")
print(f"  ID columns: {[col for col in constraints.columns if 'eqID' in col or 'ID' in col]}")
print()

print("AtlasCat_Exposure.csv columns:")
print(f"  Total columns: {len(exposure.columns)}")
print(f"  ID columns: {[col for col in exposure.columns if 'eqID' in col or 'ID' in col]}")
print()

print("AtlasCat_Losses.csv columns:")
print(f"  Total columns: {len(losses.columns)}")
print(f"  ID columns: {[col for col in losses.columns if 'eqID' in col or 'ID' in col]}")
print()

# Load matching output to inspect
exact_matches = pd.read_csv(os.path.join(MATCHING_DIR, 'exact_id_matches.csv'))
print("exact_id_matches.csv columns:")
print(f"  Total columns: {len(exact_matches.columns)}")
print(f"  ID columns: {[col for col in exact_matches.columns if 'id' in col.lower()]}")
print()

# Step 2: Identify and standardize event keys
print("=" * 80)
print("STEP 2: Identifying and Standardizing Event Keys")
print("=" * 80)
print()

print("Column naming inconsistency detected:")
print("  Constraints: 'Atlas USGS eqID', 'Comcat USGS eqID' (spaces)")
print("  Exposure:   'Atlas_USGS_eqID', 'Comcat_USGS_eqID' (underscores)")
print("  Losses:     'Atlas_USGS_eqID', 'Comcat_USGS_eqID' (underscores)")
print()

# Standardize column names in working copies
print("Standardizing column names...")

# Standardize Constraints
constraints_std = constraints.rename(columns={
    'Atlas USGS eqID': 'atlas_usgs_eqid',
    'Comcat USGS eqID': 'comcat_usgs_eqid',
    'id_info': 'id_info',
    'DateTime': 'datetime',
    'lat': 'latitude',
    'lon': 'longitude',
    'depth (km)': 'depth_km',
    'mag': 'magnitude',
    'mag type': 'magnitude_type',
    'Atlas v4 type': 'atlas_v4_type',
    'ISO_code': 'iso_code',
    'Fault': 'fault',
    'Intensity Observations': 'intensity_observations',
    'Ground Motion Recordings': 'ground_motion_recordings'
})

# Standardize Exposure (already has underscores, just ensure consistency)
exposure_std = exposure.rename(columns={
    'Atlas_USGS_eqID': 'atlas_usgs_eqid',
    'Comcat_USGS_eqID': 'comcat_usgs_eqid',
    'id_info': 'id_info',
    'DateTime': 'datetime',
    'lat': 'latitude',
    'lon': 'longitude',
    'depth(km)': 'depth_km',
    'mag': 'magnitude',
    'mag_type': 'magnitude_type',
    'Atlas_v4_type': 'atlas_v4_type',
    'ISO_code': 'iso_code',
    'Version_at_release': 'version_at_release',
    'location_string': 'location_string',
    'Max_MMI': 'max_mmi'
})

# Standardize Losses (already has underscores, just ensure consistency)
losses_std = losses.rename(columns={
    'Atlas_USGS_eqID': 'atlas_usgs_eqid',
    'Comcat_USGS_eqID': 'comcat_usgs_eqid',
    'id_info': 'id_info',
    'DateTime': 'datetime',
    'lat': 'latitude',
    'lon': 'longitude',
    'depth(km)': 'depth_km',
    'mag': 'magnitude',
    'mag_type': 'magnitude_type',
    'Atlas_v4_type': 'atlas_v4_type',
    'ISO_code': 'iso_code',
    'Pref_total_deaths': 'pref_total_deaths',
    'Pref_total_deaths_src': 'pref_total_deaths_src',
    'Pref_econ_loss': 'pref_econ_loss',
    'Pref_econ_loss_src': 'pref_econ_loss_src'
})

print("Column names standardized to use underscores consistently.")
print()

# Step 3: Get verified event IDs from matching output
print("=" * 80)
print("STEP 3: Loading Verified Event IDs from Matching Output")
print("=" * 80)
print()

# Load exact matches to get verified event IDs
verified_ids = exact_matches['atlas_usgs_eqid'].unique().tolist()
print(f"Verified event IDs from matching: {len(verified_ids):,}")
print()

# Step 4: Filter AtlasCat tables to verified events
print("=" * 80)
print("STEP 4: Filtering AtlasCat Tables to Verified Events")
print("=" * 80)
print()

# Filter Constraints
constraints_filtered = constraints_std[constraints_std['atlas_usgs_eqid'].isin(verified_ids)]
print(f"Constraints before filter: {len(constraints_std):,}")
print(f"Constraints after filter: {len(constraints_filtered):,}")
print(f"Constraints filtered out: {len(constraints_std) - len(constraints_filtered):,}")
print()

# Filter Exposure
exposure_filtered = exposure_std[exposure_std['atlas_usgs_eqid'].isin(verified_ids)]
print(f"Exposure before filter: {len(exposure_std):,}")
print(f"Exposure after filter: {len(exposure_filtered):,}")
print(f"Exposure filtered out: {len(exposure_std) - len(exposure_filtered):,}")
print()

# Filter Losses
losses_filtered = losses_std[losses_std['atlas_usgs_eqid'].isin(verified_ids)]
print(f"Losses before filter: {len(losses_std):,}")
print(f"Losses after filter: {len(losses_filtered):,}")
print(f"Losses filtered out: {len(losses_std) - len(losses_filtered):,}")
print()

# Step 5: Check for duplicate keys
print("=" * 80)
print("STEP 5: Checking for Duplicate Keys")
print("=" * 80)
print()

# Check duplicate atlas_usgs_eqid in each table
constraints_duplicates = constraints_filtered['atlas_usgs_eqid'].duplicated().sum()
exposure_duplicates = exposure_filtered['atlas_usgs_eqid'].duplicated().sum()
losses_duplicates = losses_filtered['atlas_usgs_eqid'].duplicated().sum()

print(f"Duplicate atlas_usgs_eqid in Constraints: {constraints_duplicates}")
print(f"Duplicate atlas_usgs_eqid in Exposure: {exposure_duplicates}")
print(f"Duplicate atlas_usgs_eqid in Losses: {losses_duplicates}")
print()

if constraints_duplicates > 0 or exposure_duplicates > 0 or losses_duplicates > 0:
    print("WARNING: Duplicate event IDs detected. This may indicate one-to-many relationships.")
    print("Investigating...")
    print()
    
    # Find which IDs are duplicated
    if constraints_duplicates > 0:
        dup_constraints = constraints_filtered[constraints_filtered['atlas_usgs_eqid'].duplicated(keep=False)]['atlas_usgs_eqid'].unique()
        print(f"Constraints duplicated IDs: {len(dup_constraints)}")
        print(f"Sample: {dup_constraints[:5].tolist()}")
    
    if exposure_duplicates > 0:
        dup_exposure = exposure_filtered[exposure_filtered['atlas_usgs_eqid'].duplicated(keep=False)]['atlas_usgs_eqid'].unique()
        print(f"Exposure duplicated IDs: {len(dup_exposure)}")
        print(f"Sample: {dup_exposure[:5].tolist()}")
    
    if losses_duplicates > 0:
        dup_losses = losses_filtered[losses_filtered['atlas_usgs_eqid'].duplicated(keep=False)]['atlas_usgs_eqid'].unique()
        print(f"Losses duplicated IDs: {len(dup_losses)}")
        print(f"Sample: {dup_losses[:5].tolist()}")
else:
    print("No duplicate event IDs found. All tables have one-to-one relationship on atlas_usgs_eqid.")

print()

# Step 6: Join tables
print("=" * 80)
print("STEP 6: Joining AtlasCat Tables")
print("=" * 80)
print()

# First join: Constraints + Exposure
print("Joining Constraints + Exposure on atlas_usgs_eqid...")
constraints_exposure = pd.merge(
    constraints_filtered,
    exposure_filtered,
    on='atlas_usgs_eqid',
    how='inner',
    suffixes=('_constraints', '_exposure')
)
print(f"Constraints + Exposure: {len(constraints_exposure):,} rows")
print(f"Expected rows (if one-to-one): {len(constraints_filtered):,}")
print(f"Row multiplication: {len(constraints_exposure) - len(constraints_filtered):,}")
print()

# Check if join caused row multiplication
if len(constraints_exposure) != len(constraints_filtered):
    print("WARNING: Join caused row multiplication!")
    print("This indicates one-to-many relationship between Constraints and Exposure.")
    print("Investigating...")
    print()
    
    # Find which IDs caused multiplication
    id_counts_constraints = constraints_filtered['atlas_usgs_eqid'].value_counts()
    id_counts_exposure = exposure_filtered['atlas_usgs_eqid'].value_counts()
    
    multi_ids = []
    for eid in verified_ids:
        count_c = id_counts_constraints.get(eid, 0)
        count_e = id_counts_exposure.get(eid, 0)
        if count_c > 1 or count_e > 1:
            multi_ids.append((eid, count_c, count_e))
    
    if multi_ids:
        print(f"Events with multiple records: {len(multi_ids)}")
        print("Sample:")
        for eid, count_c, count_e in multi_ids[:5]:
            print(f"  {eid}: Constraints={count_c}, Exposure={count_e}")
else:
    print("Join maintained one-to-one relationship. No row multiplication.")

print()

# Second join: (Constraints + Exposure) + Losses
print("Joining (Constraints + Exposure) + Losses on atlas_usgs_eqid...")
integrated = pd.merge(
    constraints_exposure,
    losses_filtered,
    on='atlas_usgs_eqid',
    how='inner',
    suffixes=('', '_losses')
)
print(f"Integrated dataset: {len(integrated):,} rows")
print(f"Expected rows (if one-to-one): {len(constraints_exposure):,}")
print(f"Row multiplication: {len(integrated) - len(constraints_exposure):,}")
print()

# Check if join caused row multiplication
if len(integrated) != len(constraints_exposure):
    print("WARNING: Join caused row multiplication!")
    print("This indicates one-to-many relationship with Losses.")
    print("Investigating...")
    print()
    
    # Find which IDs caused multiplication
    id_counts_losses = losses_filtered['atlas_usgs_eqid'].value_counts()
    
    multi_ids = []
    for eid in verified_ids:
        count_l = id_counts_losses.get(eid, 0)
        if count_l > 1:
            multi_ids.append((eid, count_l))
    
    if multi_ids:
        print(f"Events with multiple Losses records: {len(multi_ids)}")
        print("Sample:")
        for eid, count_l in multi_ids[:5]:
            print(f"  {eid}: Losses={count_l}")
else:
    print("Join maintained one-to-one relationship. No row multiplication.")

print()

# Step 7: Check for unmatched keys
print("=" * 80)
print("STEP 7: Checking for Unmatched Keys")
print("=" * 80)
print()

# Check if all verified IDs are present in each table
constraints_ids = set(constraints_filtered['atlas_usgs_eqid'].tolist())
exposure_ids = set(exposure_filtered['atlas_usgs_eqid'].tolist())
losses_ids = set(losses_filtered['atlas_usgs_eqid'].tolist())
verified_ids_set = set(verified_ids)

print(f"Verified IDs: {len(verified_ids_set):,}")
print(f"IDs in Constraints: {len(constraints_ids):,}")
print(f"IDs in Exposure: {len(exposure_ids):,}")
print(f"IDs in Losses: {len(losses_ids):,}")
print()

# Check for missing IDs
missing_in_constraints = verified_ids_set - constraints_ids
missing_in_exposure = verified_ids_set - exposure_ids
missing_in_losses = verified_ids_set - losses_ids

print(f"Verified IDs missing in Constraints: {len(missing_in_constraints)}")
print(f"Verified IDs missing in Exposure: {len(missing_in_exposure)}")
print(f"Verified IDs missing in Losses: {len(missing_in_losses)}")
print()

if missing_in_constraints or missing_in_exposure or missing_in_losses:
    print("WARNING: Some verified IDs are missing from AtlasCat tables.")
    if missing_in_constraints:
        print(f"Missing in Constraints: {list(missing_in_constraints)[:5]}")
    if missing_in_exposure:
        print(f"Missing in Exposure: {list(missing_in_exposure)[:5]}")
    if missing_in_losses:
        print(f"Missing in Losses: {list(missing_in_losses)[:5]}")
else:
    print("All verified IDs are present in all three AtlasCat tables.")

print()

# Step 8: Check missing values in important fields
print("=" * 80)
print("STEP 8: Checking Missing Values in Important Fields")
print("=" * 80)
print()

# Important fields to check
important_fields = {
    'atlas_usgs_eqid': 'Event ID',
    'datetime': 'Event timestamp',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'magnitude': 'Magnitude',
    'iso_code': 'Country code'
}

print("Missing values in important fields:")
for field, description in important_fields.items():
    if field in integrated.columns:
        missing = integrated[field].isnull().sum()
        print(f"  {field} ({description}): {missing:,} ({missing/len(integrated)*100:.2f}%)")
    else:
        # Check for suffixed versions
        field_c = f"{field}_constraints"
        field_e = f"{field}_exposure"
        if field_c in integrated.columns:
            missing = integrated[field_c].isnull().sum()
            print(f"  {field_c} ({description}): {missing:,} ({missing/len(integrated)*100:.2f}%)")
        elif field_e in integrated.columns:
            missing = integrated[field_e].isnull().sum()
            print(f"  {field_e} ({description}): {missing:,} ({missing/len(integrated)*100:.2f}%)")

print()

# Check exposure-specific fields
exposure_fields = ['max_mmi', 'MMI_III', 'MMI_IV', 'MMI_V', 'MMI_VI', 'MMI_VII', 'MMI_VIII', 'MMI_IX', 'MMI_X']
print("Missing values in exposure fields:")
for field in exposure_fields:
    if field in integrated.columns:
        missing = integrated[field].isnull().sum()
        print(f"  {field}: {missing:,} ({missing/len(integrated)*100:.2f}%)")

print()

# Check loss-specific fields
loss_fields = ['pref_total_deaths', 'pref_total_deaths_src', 'pref_econ_loss', 'pref_econ_loss_src']
print("Missing values in loss fields:")
for field in loss_fields:
    if field in integrated.columns:
        missing = integrated[field].isnull().sum()
        print(f"  {field}: {missing:,} ({missing/len(integrated)*100:.2f}%)")

print()

# Step 9: Save integrated dataset
print("=" * 80)
print("STEP 9: Saving Integrated Dataset")
print("=" * 80)
print()

# Save integrated dataset
integrated.to_csv(os.path.join(OUTPUT_DIR, 'atlascat_integrated.csv'), index=False)
print(f"Saved: atlascat_integrated.csv ({len(integrated):,} rows, {len(integrated.columns)} columns)")

# Also save individual filtered tables
constraints_filtered.to_csv(os.path.join(OUTPUT_DIR, 'constraints_filtered.csv'), index=False)
exposure_filtered.to_csv(os.path.join(OUTPUT_DIR, 'exposure_filtered.csv'), index=False)
losses_filtered.to_csv(os.path.join(OUTPUT_DIR, 'losses_filtered.csv'), index=False)
print(f"Saved: constraints_filtered.csv")
print(f"Saved: exposure_filtered.csv")
print(f"Saved: losses_filtered.csv")

print()

# Step 10: Generate summary
print("=" * 80)
print("STEP 10: Generating Integration Summary")
print("=" * 80)
print()

summary_data = {
    'metric': [
        'Original Constraints rows',
        'Original Exposure rows',
        'Original Losses rows',
        'Verified event IDs',
        'Constraints after filter',
        'Exposure after filter',
        'Losses after filter',
        'Integrated dataset rows',
        'Integrated dataset columns',
        'Duplicate keys in Constraints',
        'Duplicate keys in Exposure',
        'Duplicate keys in Losses',
        'Row multiplication in join',
        'Missing IDs in Constraints',
        'Missing IDs in Exposure',
        'Missing IDs in Losses'
    ],
    'value': [
        len(constraints_std),
        len(exposure_std),
        len(losses_std),
        len(verified_ids),
        len(constraints_filtered),
        len(exposure_filtered),
        len(losses_filtered),
        len(integrated),
        len(integrated.columns),
        constraints_duplicates,
        exposure_duplicates,
        losses_duplicates,
        len(integrated) - len(constraints_filtered),
        len(missing_in_constraints),
        len(missing_in_exposure),
        len(missing_in_losses)
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(OUTPUT_DIR, 'integration_summary.csv'), index=False)
print(f"Saved: integration_summary.csv")

print()

# Step 11: Print terminal summary
print("=" * 80)
print("INTEGRATION SUMMARY")
print("=" * 80)
print()

print(f"Original AtlasCat rows:")
print(f"  Constraints: {len(constraints_std):,}")
print(f"  Exposure: {len(exposure_std):,}")
print(f"  Losses: {len(losses_std):,}")
print()

print(f"Verified event IDs from matching: {len(verified_ids):,}")
print()

print(f"After filtering to verified IDs:")
print(f"  Constraints: {len(constraints_filtered):,}")
print(f"  Exposure: {len(exposure_filtered):,}")
print(f"  Losses: {len(losses_filtered):,}")
print()

print(f"Integrated dataset: {len(integrated):,} rows, {len(integrated.columns)} columns")
print()

print(f"Duplicate keys check:")
print(f"  Constraints: {constraints_duplicates}")
print(f"  Exposure: {exposure_duplicates}")
print(f"  Losses: {losses_duplicates}")
print()

print(f"Row multiplication: {len(integrated) - len(constraints_filtered):,}")
print(f"  (0 means one-to-one relationship maintained)")
print()

print(f"Unmatched keys:")
print(f"  Missing in Constraints: {len(missing_in_constraints)}")
print(f"  Missing in Exposure: {len(missing_in_exposure)}")
print(f"  Missing in Losses: {len(missing_in_losses)}")
print()

print("=" * 80)
print("Integration complete. Reports saved to:", OUTPUT_DIR)
print("=" * 80)
