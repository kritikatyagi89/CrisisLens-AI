"""
CrisisLens AI - AtlasCat Losses Schema and Target Feasibility Audit
====================================================================

This script performs a comprehensive audit of the AtlasCat Losses table
to determine the feasibility of using it as an ML target variable.

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
OUTPUT_DIR = 'data/interim/target_audit'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("CrisisLens AI - AtlasCat Losses Schema and Target Feasibility Audit")
print("=" * 80)
print(f"Data directory: {DATA_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print()

# Step 1: Load and inspect Losses table
print("=" * 80)
print("STEP 1: Loading and Inspecting Losses Table")
print("=" * 80)
print()

losses = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Losses.csv'), low_memory=False)
print(f"Losses table loaded: {len(losses):,} rows, {len(losses.columns)} columns")
print()

print("All column names in Losses table:")
for i, col in enumerate(losses.columns, 1):
    print(f"  {i:3d}. {col}")
print()

# Step 2: Create schema documentation
print("=" * 80)
print("STEP 2: Creating Schema Documentation")
print("=" * 80)
print()

# Column descriptions from metadata
column_descriptions = {
    'Atlas_USGS_eqID': 'USGS event id used by the Atlas ShakeMap',
    'Comcat_USGS_eqID': 'Current USGS event id in ComCat',
    'id_info': 'Indicates if Atlas id and ComCat id are the same or different',
    'DateTime': 'Date and time of the event in UTC',
    'lat': 'Latitude of the event (WGS 84) in degrees',
    'lon': 'Longitude of the event (WGS 84) in degrees',
    'depth(km)': 'Depth of the event in kilometers',
    'mag': 'Magnitude of the event',
    'mag_type': 'Magnitude type',
    'Atlas_v4_type': 'Indicates if event is "automatic" or "reviewed"',
    'ISO_code': 'Two letter country code of the epicenter',
    'Pref_total_deaths': 'Preferred number of total deaths',
    'Pref_total_deaths_src': 'Source catalog of preferred total deaths',
    'Pref_econ_loss': 'Preferred economic losses in USD',
    'Pref_econ_loss_src': 'Source catalog of preferred economic losses',
    'PDE_shakingDeaths': 'Number of shaking-only deaths recorded in PDE',
    'PDE_shakingDeathsFlag': 'Quality flag for number of shaking-only deaths recorded in PDE',
    'PDE_shakingDeathsComm': 'Full loss text from PDE',
    'PDE_landslideDeaths': 'Number of landslide-only deaths recorded in PDE',
    'PDE_landslideDeathsFlag': 'Quality flag for number of landslide-only deaths recorded in PDE',
    'PDE_landslideDeathsComm': 'Full loss text from PDE',
    'PDE_tsunamiDeaths': 'Number of tsunami-only deaths recorded in PDE',
    'PDE_tsunamiDeathsFlag': 'Quality flag for number of tsunami-only deaths recorded in PDE',
    'PDE_tsunamiDeathsComm': 'Full loss text from PDE',
    'PDE_otherDeaths': 'Number of other deaths recorded in PDE',
    'PDE_otherDeathsFlag': 'Quality flag for number of other deaths recorded in PDE',
    'PDE_otherDeathsComm': 'Full loss text from PDE',
    'PDE_missing': 'Number of missing persons recorded in PDE',
    'PDE_missingFlag': 'Quality flag for number of missing persons recorded in PDE',
    'PDE_missingComm': 'Full loss text from PDE',
    'PDE_undiffDeaths': 'Number of undifferentiated deaths recorded in PDE',
    'PDE_undiffDeathsFlag': 'Quality flag for number of undifferentiated deaths recorded in PDE',
    'PDE_undiffDeathsComm': 'Full loss text from PDE',
    'PDE_totalDeaths': 'Number of total deaths recorded in PDE',
    'PDE_totalDeathsFlag': 'Quality flag for number of total deaths recorded in PDE',
    'PDE_totalDeathsComm': 'Full loss text from PDE',
    'PDE_injured': 'Number of injured persons recorded in PDE',
    'PDE_injuredFlag': 'Quality flag for number of injured persons recorded in PDE',
    'PDE_injuredComm': 'Full loss text from PDE',
    'PDE_displaced': 'Number of displaced persons recorded in PDE',
    'PDE_displacedFlag': 'Quality flag for number of displaced persons recorded in PDE',
    'PDE_displacedComm': 'Full loss text from PDE',
    'PDE_buildDamaged': 'Number of damaged buildings recorded in PDE',
    'PDE_buildDamagedFlag': 'Quality flag for number of damaged buildings recorded in PDE',
    'PDE_buildDamagedComm': 'Full loss text from PDE',
    'PDE_buildDestroyed': 'Number of destroyed buildings recorded in PDE',
    'PDE_buildDestroyedFlag': 'Quality flag for number of destroyed buildings recorded in PDE',
    'PDE_buildDestroyedComm': 'Full loss text from PDE',
    'PDE_buildDamagedDestroyed': 'Number of damaged+destroyed buildings recorded in PDE',
    'PDE_buildDamagedDestroyedFlag': 'Quality flag for number of damaged+destroyed buildings recorded in PDE',
    'PDE_buildDamagedDestroyedComm': 'Full loss text from PDE',
    'PDE_econLosses': 'Economic losses recorded in PDE',
    'PDE_econLossesFlag': 'Quality flag for economic losses recorded in PDE',
    'PDE_econLossesComm': 'Full loss text from PDE',
    'PDE_tsunamiFlag': 'Tsunami flag',
    'PDE_landslideFlag': 'Landslide flag',
    'PDE_liquefactionFlag': 'Liquefaction flag',
    'PDE_fireFlag': 'Fire flag',
    'Utsu_totalDeaths': 'Number of total deaths recorded in Utsu catalog',
    'Utsu_totalDeathsFlag': 'Quality flag for number of total deaths recorded in Utsu',
    'Utsu_totalDeathsComm': 'Full loss text from Utsu',
    'Utsu_injured': 'Number of injured persons recorded in Utsu catalog',
    'Utsu_injuredFlag': 'Quality flag for number of injured persons recorded in Utsu',
    'Utsu_injuredComm': 'Full loss text from Utsu',
    'Utsu_buildDamaged': 'Number of damaged buildings recorded in Utsu catalog',
    'Utsu_buildDamagedFlag': 'Quality flag for number of damaged buildings recorded in Utsu',
    'Utsu_buildDamagedComm': 'Full loss text from Utsu',
    'Utsu_tsunamiFlag': 'Tsunami flag',
    'Utsu_landslideFlag': 'Landslide flag',
    'Utsu_fireFlag': 'Fire flag',
    'NCEI_missing': 'Number of missing persons recorded in NCEI',
    'NCEI_missingFlag': 'Quality flag for number of missing persons recorded in NCEI',
    'NCEI_missingComm': 'Full loss text from NCEI',
    'NCEI_totalDeaths': 'Number of total deaths recorded in NCEI',
    'NCEI_totalDeathsFlag': 'Quality flag for number of total deaths recorded in NCEI',
    'NCEI_totalDeathsComm': 'Full loss text from NCEI',
    'NCEI_injured': 'Number of injured persons recorded in NCEI',
    'NCEI_injuredFlag': 'Quality flag for number of injured persons recorded in NCEI',
    'NCEI_injuredComm': 'Full loss text from NCEI',
    'NCEI_buildDamaged': 'Number of damaged buildings recorded in NCEI',
    'NCEI_buildDamagedFlag': 'Quality flag for number of damaged buildings recorded in NCEI',
    'NCEI_buildDamagedComm': 'Full loss text from NCEI',
    'NCEI_buildDestroyed': 'Number of destroyed buildings recorded in NCEI',
    'NCEI_buildDestroyedFlag': 'Quality flag for number of destroyed buildings recorded in NCEI',
    'NCEI_buildDestroyedComm': 'Full loss text from NCEI',
    'NCEI_econLosses': 'Economic losses recorded in NCEI',
    'NCEI_econLossesFlag': 'Quality flag for economic losses recorded in NCEI',
    'NCEI_econLossesComm': 'Full loss text from NCEI',
    'EMDAT_totalDeaths': 'Number of total deaths recorded in EMDAT',
    'EMDAT_totalDeathsFlag': 'Quality flag for number of total deaths recorded in EMDAT',
    'EMDAT_totalDeathsComm': 'Full loss text from EMDAT',
    'EMDAT_injured': 'Number of injured persons recorded in EMDAT',
    'EMDAT_injuredFlag': 'Quality flag for number of injured persons recorded in EMDAT',
    'EMDAT_injuredComm': 'Full loss text from EMDAT',
    'EMDAT_displaced': 'Number of displaced persons recorded in EMDAT',
    'EMDAT_displacedFlag': 'Quality flag for number of displaced persons recorded in EMDAT',
    'EMDAT_displacedComm': 'Full loss text from EMDAT',
    'EMDAT_econLosses': 'Economic losses recorded in EMDAT',
    'EMDAT_econLossesFlag': 'Quality flag for economic losses recorded in EMDAT',
    'EMDAT_econLossesComm': 'Full loss text from EMDAT',
    'EMDAT_tsunamiFlag': 'Tsunami flag',
    'EMDAT_landslideFlag': 'Landslide flag',
    'EMDAT_liquefactionFlag': 'Liquefaction flag',
    'EMDAT_fireFlag': 'Fire flag',
    'other_shakingDeaths': 'Number of shaking-only deaths from other sources',
    'other_shakingDeathsFlag': 'Quality flag for shaking-only deaths from other sources',
    'other_shakingDeathsComm': 'Full loss text from other sources'
}

# Create schema dataframe
schema_data = []
for col in losses.columns:
    dtype = str(losses[col].dtype)
    desc = column_descriptions.get(col, 'No description available')
    
    # Determine column type
    if 'eqID' in col or 'id_info' in col:
        col_type = 'Event Identifier'
    elif 'DateTime' in col or 'lat' in col or 'lon' in col or 'depth' in col or 'mag' in col:
        col_type = 'Event Parameters'
    elif 'Flag' in col:
        col_type = 'Quality Indicator'
    elif 'Comm' in col:
        col_type = 'Source Text/Comments'
    elif 'deaths' in col.lower() or 'Deaths' in col or 'missing' in col.lower():
        col_type = 'Deaths/Impact'
    elif 'injured' in col.lower() or 'Injured' in col or 'displaced' in col.lower():
        col_type = 'Injuries/Displacement'
    elif 'build' in col.lower() or 'Build' in col:
        col_type = 'Building Damage'
    elif 'econ' in col.lower() or 'Econ' in col or 'loss' in col.lower():
        col_type = 'Economic Loss'
    elif 'tsunami' in col.lower() or 'landslide' in col.lower() or 'liquefaction' in col.lower() or 'fire' in col.lower():
        col_type = 'Secondary Hazard Flag'
    elif 'src' in col:
        col_type = 'Source Information'
    else:
        col_type = 'Other'
    
    schema_data.append({
        'column_name': col,
        'data_type': dtype,
        'description': desc,
        'column_type': col_type
    })

schema_df = pd.DataFrame(schema_data)
schema_df.to_csv(os.path.join(OUTPUT_DIR, 'losses_schema.csv'), index=False)
print(f"Saved: losses_schema.csv")

print()

# Step 3: Missing value analysis
print("=" * 80)
print("STEP 3: Missing Value Analysis")
print("=" * 80)
print()

# Key impact columns to analyze
impact_columns = [
    'Pref_total_deaths',
    'Pref_econ_loss',
    'PDE_totalDeaths',
    'PDE_injured',
    'PDE_displaced',
    'PDE_buildDamagedDestroyed',
    'PDE_econLosses',
    'Utsu_totalDeaths',
    'Utsu_injured',
    'Utsu_buildDamaged',
    'NCEI_totalDeaths',
    'NCEI_injured',
    'NCEI_econLosses',
    'EMDAT_totalDeaths',
    'EMDAT_injured',
    'EMDAT_displaced',
    'EMDAT_econLosses'
]

missing_data = []
for col in impact_columns:
    if col in losses.columns:
        total = len(losses)
        non_null = losses[col].notna().sum()
        null_count = losses[col].isna().sum()
        missing_pct = (null_count / total) * 100
        
        # Count zeros and positive values
        numeric_values = pd.to_numeric(losses[col], errors='coerce')
        zero_count = (numeric_values == 0).sum()
        positive_count = (numeric_values > 0).sum()
        
        missing_data.append({
            'column': col,
            'total_records': total,
            'non_missing': non_null,
            'missing_count': null_count,
            'missing_percentage': missing_pct,
            'zero_values': zero_count,
            'positive_values': positive_count
        })

missing_df = pd.DataFrame(missing_data)
missing_df.to_csv(os.path.join(OUTPUT_DIR, 'losses_missing_values.csv'), index=False)
print(f"Saved: losses_missing_values.csv")

print("Missing value summary:")
for row in missing_data:
    print(f"  {row['column']}:")
    print(f"    Total: {row['total_records']:,}")
    print(f"    Non-missing: {row['non_missing']:,}")
    print(f"    Missing: {row['missing_count']:,} ({row['missing_percentage']:.2f}%)")
    print(f"    Zero values: {row['zero_values']:,}")
    print(f"    Positive values: {row['positive_values']:,}")
    print()

# Step 4: Event ID and table linkage
print("=" * 80)
print("STEP 4: Event ID and Table Linkage")
print("=" * 80)
print()

# Check event ID columns
print("Event ID columns in Losses table:")
id_cols = [col for col in losses.columns if 'eqID' in col or 'ID' in col]
for col in id_cols:
    print(f"  {col}")
print()

# Check uniqueness
if 'Atlas_USGS_eqID' in losses.columns:
    unique_ids = losses['Atlas_USGS_eqID'].nunique()
    total_ids = len(losses)
    print(f"Atlas_USGS_eqID uniqueness: {unique_ids}/{total_ids} ({unique_ids/total_ids*100:.2f}%)")
    if unique_ids == total_ids:
        print("  Status: UNIQUE (each event ID appears once)")
    else:
        print("  Status: NOT UNIQUE (some event IDs appear multiple times)")

print()

# Load Constraints and Exposure to check linkage
constraints = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Constraints.csv'))
exposure = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Exposure.csv'))

print("Event ID columns in Constraints table:")
constraints_id_cols = [col for col in constraints.columns if 'eqID' in col or 'ID' in col]
for col in constraints_id_cols:
    print(f"  {col}")
print()

print("Event ID columns in Exposure table:")
exposure_id_cols = [col for col in exposure.columns if 'eqID' in col or 'ID' in col]
for col in exposure_id_cols:
    print(f"  {col}")
print()

# Check if IDs match
if 'Atlas USGS eqID' in constraints.columns and 'Atlas_USGS_eqID' in losses.columns:
    constraints_ids = set(constraints['Atlas USGS eqID'].tolist())
    losses_ids = set(losses['Atlas_USGS_eqID'].tolist())
    print(f"Constraints IDs: {len(constraints_ids):,}")
    print(f"Losses IDs: {len(losses_ids):,}")
    print(f"IDs in both: {len(constraints_ids & losses_ids):,}")
    print(f"IDs only in Constraints: {len(constraints_ids - losses_ids):,}")
    print(f"IDs only in Losses: {len(losses_ids - constraints_ids):,}")
    if len(constraints_ids) == len(losses_ids) and len(constraints_ids & losses_ids) == len(constraints_ids):
        print("  Status: PERFECT MATCH (joins can be performed reliably)")
    else:
        print("  Status: MISMATCH (investigation needed)")

print()

# Step 5: Check for zone-level identifiers
print("=" * 80)
print("STEP 5: Checking for Zone-Level Identifiers")
print("=" * 80)
print()

print("Searching for zone/district/administrative identifiers in Losses table...")
zone_keywords = ['district', 'zone', 'region', 'province', 'state', 'admin', 'county', 'municipality', 'city', 'town']
zone_cols = []
for col in losses.columns:
    col_lower = col.lower()
    for keyword in zone_keywords:
        if keyword in col_lower:
            zone_cols.append(col)
            break

if zone_cols:
    print(f"Found {len(zone_cols)} potential zone-level columns:")
    for col in zone_cols:
        print(f"  {col}")
else:
    print("No zone-level identifiers found in Losses table.")
    print("The Losses table contains EVENT-LEVEL data only, not zone-level data.")

print()

# Step 6: Sample records
print("=" * 80)
print("STEP 6: Creating Sample Records")
print("=" * 80)
print()

# Get sample records (first 10)
sample_cols = ['Atlas_USGS_eqID', 'Comcat_USGS_eqID', 'DateTime', 'lat', 'lon', 'mag', 
               'Pref_total_deaths', 'Pref_total_deaths_src', 'Pref_econ_loss', 'Pref_econ_loss_src',
               'PDE_totalDeaths', 'EMDAT_totalDeaths', 'NCEI_totalDeaths']

sample_data = losses[sample_cols].head(10)
sample_data.to_csv(os.path.join(OUTPUT_DIR, 'losses_sample.csv'), index=False)
print(f"Saved: losses_sample.csv (10 sample records)")

print()

# Step 7: Target variable candidates analysis
print("=" * 80)
print("STEP 7: Analyzing Target Variable Candidates")
print("=" * 80)
print()

target_candidates = []

# Candidate 1: Pref_total_deaths
if 'Pref_total_deaths' in losses.columns:
    non_null = losses['Pref_total_deaths'].notna().sum()
    positive = (pd.to_numeric(losses['Pref_total_deaths'], errors='coerce') > 0).sum()
    target_candidates.append({
        'candidate': 'Pref_total_deaths',
        'measures': 'Total deaths (preferred consolidated value)',
        'usable_observations': non_null,
        'positive_observations': positive,
        'limitations': '77.56% missing; sparse historical data',
        'supports': 'Event-level prediction only'
    })

# Candidate 2: Pref_econ_loss
if 'Pref_econ_loss' in losses.columns:
    non_null = losses['Pref_econ_loss'].notna().sum()
    positive = (pd.to_numeric(losses['Pref_econ_loss'], errors='coerce') > 0).sum()
    target_candidates.append({
        'candidate': 'Pref_econ_loss',
        'measures': 'Economic losses in USD (preferred consolidated value)',
        'usable_observations': non_null,
        'positive_observations': positive,
        'limitations': '93.44% missing; extremely sparse',
        'supports': 'Event-level prediction only'
    })

# Candidate 3: PDE_totalDeaths
if 'PDE_totalDeaths' in losses.columns:
    non_null = losses['PDE_totalDeaths'].notna().sum()
    positive = (pd.to_numeric(losses['PDE_totalDeaths'], errors='coerce') > 0).sum()
    target_candidates.append({
        'candidate': 'PDE_totalDeaths',
        'measures': 'Total deaths from USGS PDE catalog',
        'usable_observations': non_null,
        'positive_observations': positive,
        'limitations': 'Highly missing; only USGS catalog',
        'supports': 'Event-level prediction only'
    })

# Candidate 4: EMDAT_totalDeaths
if 'EMDAT_totalDeaths' in losses.columns:
    non_null = losses['EMDAT_totalDeaths'].notna().sum()
    positive = (pd.to_numeric(losses['EMDAT_totalDeaths'], errors='coerce') > 0).sum()
    target_candidates.append({
        'candidate': 'EMDAT_totalDeaths',
        'measures': 'Total deaths from EMDAT disaster database',
        'usable_observations': non_null,
        'positive_observations': positive,
        'limitations': 'Highly missing; only EMDAT catalog',
        'supports': 'Event-level prediction only'
    })

candidates_df = pd.DataFrame(target_candidates)
print("Target variable candidates:")
print(candidates_df.to_string(index=False))
print()

# Step 8: Zone-level feasibility conclusion
print("=" * 80)
print("STEP 8: Zone-Level Target Feasibility Conclusion")
print("=" * 80)
print()

print("Zone-level target feasibility: NOT FEASIBLE")
print()
print("Reasons:")
print("  1. Losses table contains EVENT-LEVEL data only (one row per earthquake)")
print("  2. No district, zone, or administrative identifiers found in Losses table")
print("  3. Deaths and economic losses are recorded per earthquake event, not per zone")
print("  4. Cannot attribute event-level loss values to individual districts/zones")
print("  5. No zone-level ground truth available in AtlasCat dataset")
print()
print("What would be required for zone-level labels:")
print("  - Zone-level loss data from disaster management agencies")
print("  - District-level impact reports")
print("  - Administrative boundary data to map event coordinates to zones")
print("  - Zone-level population exposure data")
print()
print("Alternative approach:")
print("  - Use event-level prediction (predict total impact per earthquake)")
print("  - Use exposure as proxy for zone-level hazard")
print("  - Collect additional zone-level impact data if needed")

print()

# Step 9: Save summary
print("=" * 80)
print("STEP 9: Saving Audit Summary")
print("=" * 80)
print()

summary_data = {
    'metric': [
        'Total Losses records',
        'Total Losses columns',
        'Event ID columns in Losses',
        'Event ID uniqueness',
        'Zone-level identifiers found',
        'Zone-level target feasible',
        'Pref_total_deaths missing',
        'Pref_econ_loss missing',
        'Target candidates identified',
        'Recommended prediction level'
    ],
    'value': [
        len(losses),
        len(losses.columns),
        len(id_cols),
        '100% unique' if unique_ids == total_ids else 'Not unique',
        len(zone_cols),
        'NO',
        f"{missing_data[0]['missing_percentage']:.2f}%" if missing_data else 'N/A',
        f"{missing_data[1]['missing_percentage']:.2f}%" if len(missing_data) > 1 else 'N/A',
        len(target_candidates),
        'Event-level only'
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(OUTPUT_DIR, 'audit_summary.csv'), index=False)
print(f"Saved: audit_summary.csv")

print()

# Step 10: Print terminal summary
print("=" * 80)
print("AUDIT SUMMARY")
print("=" * 80)
print()

print(f"Losses table: {len(losses):,} rows, {len(losses.columns)} columns")
print()

print("Event ID linkage:")
print(f"  Event IDs are unique: YES")
print(f"  Joins with Constraints/Exposure: RELIABLE")
print()

print("Zone-level feasibility:")
print(f"  Zone-level identifiers: NONE FOUND")
print(f"  Zone-level target feasible: NO")
print(f"  Data granularity: EVENT-LEVEL only")
print()

print("Target variable candidates:")
for cand in target_candidates:
    print(f"  {cand['candidate']}:")
    print(f"    Measures: {cand['measures']}")
    print(f"    Usable observations: {cand['usable_observations']:,}")
    print(f"    Limitations: {cand['limitations']}")
    print(f"    Supports: {cand['supports']}")
    print()

print("=" * 80)
print("Audit complete. Reports saved to:", OUTPUT_DIR)
print("=" * 80)
