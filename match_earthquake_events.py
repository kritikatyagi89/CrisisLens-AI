"""
CrisisLens AI - Step 3: Earthquake Event Matching
==================================================

This script performs earthquake event matching between USGS historical data (2010-2019)
and AtlasCat datasets using:
1. Exact ID matching
2. Spatiotemporal matching for unmatched events

Author: CrisisLens AI Team
Date: October 11, 2026
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings

# Ignore warnings for cleaner output
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = 'data/raw'
USGS_DIR = os.path.join(DATA_DIR, 'usgs_historical')
OUTPUT_DIR = 'data/interim/matching'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("CrisisLens AI - Step 3: Earthquake Event Matching")
print("=" * 80)
print(f"Data directory: {DATA_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print()

# Step 1: Combine USGS yearly files into working catalogue
print("=" * 80)
print("STEP 1: Combining USGS Yearly Files (2010-2019)")
print("=" * 80)
print()

usgs_files = []
for year in range(2010, 2020):
    file_path = os.path.join(USGS_DIR, f'usgs_{year}.csv')
    if os.path.exists(file_path):
        usgs_files.append(file_path)
        print(f"Found: {file_path}")
    else:
        print(f"WARNING: File not found: {file_path}")

print(f"\nLoading {len(usgs_files)} USGS files...")

usgs_dfs = []
for file_path in usgs_files:
    df = pd.read_csv(file_path)
    # Add source filename for tracking
    df['source_file'] = os.path.basename(file_path)
    usgs_dfs.append(df)
    print(f"  Loaded {len(df):,} rows from {os.path.basename(file_path)}")

# Combine all USGS files
usgs_combined = pd.concat(usgs_dfs, ignore_index=True)
print(f"\nTotal USGS records combined: {len(usgs_combined):,}")

# Filter to 2010-2019 period (already filtered by file selection, but verify)
usgs_combined['time_parsed'] = pd.to_datetime(usgs_combined['time'])
usgs_2010_2019 = usgs_combined[
    (usgs_combined['time_parsed'] >= '2010-01-01') &
    (usgs_combined['time_parsed'] <= '2019-12-31')
]
print(f"USGS records in 2010-2019 period: {len(usgs_2010_2019):,}")

print()

# Step 2: Load and standardize AtlasCat files
print("=" * 80)
print("STEP 2: Loading and Standardizing AtlasCat Files")
print("=" * 80)
print()

# Load AtlasCat files
constraints = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Constraints.csv'))
exposure = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Exposure.csv'))
losses = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Losses.csv'), low_memory=False)

print(f"Loaded AtlasCat Constraints: {len(constraints):,} rows")
print(f"Loaded AtlasCat Exposure: {len(exposure):,} rows")
print(f"Loaded AtlasCat Losses: {len(losses):,} rows")

# Standardize column names in working copies
print("\nStandardizing column names...")

# Standardize Constraints column names
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

# Standardize Exposure column names
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

# Standardize Losses column names
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

print("Column names standardized.")

# Filter AtlasCat to 2010-2019 period for matching
constraints_std['datetime_parsed'] = pd.to_datetime(constraints_std['datetime'])
atlas_2010_2019 = constraints_std[
    (constraints_std['datetime_parsed'] >= '2010-01-01') &
    (constraints_std['datetime_parsed'] <= '2019-12-31')
]
print(f"\nAtlasCat events in 2010-2019 period: {len(atlas_2010_2019):,}")
print(f"AtlasCat events outside 2010-2019: {len(constraints_std) - len(atlas_2010_2019):,} (cannot be matched with current USGS data)")

print()

# Step 3: Exact ID matching
print("=" * 80)
print("STEP 3: Exact ID Matching")
print("=" * 80)
print()

# Normalize IDs (lowercase, strip whitespace)
usgs_2010_2019['usgs_id_normalized'] = usgs_2010_2019['id'].str.lower().str.strip()
atlas_2010_2019['comcat_id_normalized'] = atlas_2010_2019['comcat_usgs_eqid'].str.lower().str.strip()
atlas_2010_2019['atlas_id_normalized'] = atlas_2010_2019['atlas_usgs_eqid'].str.lower().str.strip()

# Get unique IDs
usgs_ids = set(usgs_2010_2019['usgs_id_normalized'].tolist())
atlas_comcat_ids = set(atlas_2010_2019['comcat_id_normalized'].tolist())
atlas_atlas_ids = set(atlas_2010_2019['atlas_id_normalized'].tolist())

print(f"USGS unique IDs (2010-2019): {len(usgs_ids):,}")
print(f"AtlasCat Comcat IDs (2010-2019): {len(atlas_comcat_ids):,}")
print(f"AtlasCat Atlas IDs (2010-2019): {len(atlas_atlas_ids):,}")

# Exact matches with Comcat IDs
exact_matches_comcat = usgs_ids.intersection(atlas_comcat_ids)
print(f"\nExact matches with Comcat IDs: {len(exact_matches_comcat):,}")

# Exact matches with Atlas IDs
exact_matches_atlas = usgs_ids.intersection(atlas_atlas_ids)
print(f"Exact matches with Atlas IDs: {len(exact_matches_atlas):,}")

# Combined exact matches
exact_matches_all = exact_matches_comcat.union(exact_matches_atlas)
print(f"Total exact matches: {len(exact_matches_all):,}")

# Create exact matches dataframe
exact_matches_list = []
for match_id in exact_matches_all:
    usgs_row = usgs_2010_2019[usgs_2010_2019['usgs_id_normalized'] == match_id].iloc[0]
    atlas_row = atlas_2010_2019[
        (atlas_2010_2019['comcat_id_normalized'] == match_id) |
        (atlas_2010_2019['atlas_id_normalized'] == match_id)
    ].iloc[0]
    
    exact_matches_list.append({
        'usgs_id': usgs_row['id'],
        'atlas_usgs_eqid': atlas_row['atlas_usgs_eqid'],
        'comcat_usgs_eqid': atlas_row['comcat_usgs_eqid'],
        'match_type': 'exact_id',
        'usgs_time': usgs_row['time'],
        'atlas_time': atlas_row['datetime'],
        'usgs_latitude': usgs_row['latitude'],
        'atlas_latitude': atlas_row['latitude'],
        'usgs_longitude': usgs_row['longitude'],
        'atlas_longitude': atlas_row['longitude'],
        'usgs_magnitude': usgs_row['mag'],
        'atlas_magnitude': atlas_row['magnitude'],
        'time_diff_hours': abs((usgs_row['time_parsed'] - atlas_row['datetime_parsed']).total_seconds() / 3600),
        'lat_diff_deg': abs(usgs_row['latitude'] - atlas_row['latitude']),
        'lon_diff_deg': abs(usgs_row['longitude'] - atlas_row['longitude']),
        'mag_diff': abs(usgs_row['mag'] - atlas_row['magnitude'])
    })

exact_matches_df = pd.DataFrame(exact_matches_list)
print(f"\nExact matches dataframe created: {len(exact_matches_df):,} rows")

# Save exact matches
exact_matches_df.to_csv(os.path.join(OUTPUT_DIR, 'exact_id_matches.csv'), index=False)
print(f"Saved: exact_id_matches.csv")

print()

# Step 4: Identify unmatched events for spatiotemporal matching
print("=" * 80)
print("STEP 4: Identifying Unmatched Events")
print("=" * 80)
print()

# USGS events not matched by exact ID
usgs_unmatched_ids = usgs_ids - exact_matches_all
usgs_unmatched = usgs_2010_2019[usgs_2010_2019['usgs_id_normalized'].isin(usgs_unmatched_ids)]
print(f"USGS events unmatched by exact ID: {len(usgs_unmatched):,}")

# AtlasCat events not matched by exact ID
atlas_unmatched_ids = atlas_comcat_ids - exact_matches_all
atlas_unmatched = atlas_2010_2019[atlas_2010_2019['comcat_id_normalized'].isin(atlas_unmatched_ids)]
print(f"AtlasCat events unmatched by exact ID: {len(atlas_unmatched):,}")

print()

# Step 5: Spatiotemporal matching
print("=" * 80)
print("STEP 5: Spatiotemporal Matching")
print("=" * 80)
print()

# Matching parameters
TIME_TOLERANCE_HOURS = 24  # ±24 hours
DIST_TOLERANCE_KM = 50  # ±50 km (approximately 0.5 degrees at equator)
MAG_TOLERANCE = 0.5  # ±0.5 magnitude

print(f"Matching parameters:")
print(f"  Time tolerance: ±{TIME_TOLERANCE_HOURS} hours")
print(f"  Distance tolerance: ±{DIST_TOLERANCE_KM} km")
print(f"  Magnitude tolerance: ±{MAG_TOLERANCE}")
print()

# Function to calculate Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate Haversine distance between two points in kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Earth radius in kilometers
    r = 6371
    return c * r

print("Performing spatiotemporal matching...")
print("This may take a few minutes...\n")

spatiotemporal_matches = []
ambiguous_matches = []
matched_usgs_ids = set()
matched_atlas_ids = set()

# For each unmatched USGS event, find candidate AtlasCat matches
for idx, usgs_row in usgs_unmatched.iterrows():
    # Skip if already matched
    if usgs_row['usgs_id_normalized'] in matched_usgs_ids:
        continue
    
    usgs_time = usgs_row['time_parsed']
    usgs_lat = usgs_row['latitude']
    usgs_lon = usgs_row['longitude']
    usgs_mag = usgs_row['mag']
    
    # Find candidates within time window
    time_min = usgs_time - timedelta(hours=TIME_TOLERANCE_HOURS)
    time_max = usgs_time + timedelta(hours=TIME_TOLERANCE_HOURS)
    
    candidates = atlas_unmatched[
        (atlas_unmatched['datetime_parsed'] >= time_min) &
        (atlas_unmatched['datetime_parsed'] <= time_max)
    ]
    
    if len(candidates) == 0:
        continue
    
    # Filter by distance
    candidates_with_dist = []
    for idx2, atlas_row in candidates.iterrows():
        # Skip if already matched
        if atlas_row['comcat_id_normalized'] in matched_atlas_ids:
            continue
        
        distance = haversine_distance(
            usgs_lat, usgs_lon,
            atlas_row['latitude'], atlas_row['longitude']
        )
        
        if distance <= DIST_TOLERANCE_KM:
            mag_diff = abs(usgs_mag - atlas_row['magnitude'])
            if mag_diff <= MAG_TOLERANCE:
                candidates_with_dist.append({
                    'atlas_row': atlas_row,
                    'distance_km': distance,
                    'mag_diff': mag_diff,
                    'time_diff_hours': abs((usgs_time - atlas_row['datetime_parsed']).total_seconds() / 3600)
                })
    
    # Handle matches
    if len(candidates_with_dist) == 1:
        # Single match - accept
        match = candidates_with_dist[0]
        atlas_row = match['atlas_row']
        
        spatiotemporal_matches.append({
            'usgs_id': usgs_row['id'],
            'atlas_usgs_eqid': atlas_row['atlas_usgs_eqid'],
            'comcat_usgs_eqid': atlas_row['comcat_usgs_eqid'],
            'match_type': 'spatiotemporal',
            'usgs_time': usgs_row['time'],
            'atlas_time': atlas_row['datetime'],
            'usgs_latitude': usgs_row['latitude'],
            'atlas_latitude': atlas_row['latitude'],
            'usgs_longitude': usgs_row['longitude'],
            'atlas_longitude': atlas_row['longitude'],
            'usgs_magnitude': usgs_row['mag'],
            'atlas_magnitude': atlas_row['magnitude'],
            'time_diff_hours': match['time_diff_hours'],
            'distance_km': match['distance_km'],
            'mag_diff': match['mag_diff'],
            'match_confidence': 'high' if match['distance_km'] < 10 and match['mag_diff'] < 0.2 else 'medium'
        })
        
        matched_usgs_ids.add(usgs_row['usgs_id_normalized'])
        matched_atlas_ids.add(atlas_row['comcat_id_normalized'])
        
    elif len(candidates_with_dist) > 1:
        # Multiple candidates - ambiguous
        for match in candidates_with_dist:
            atlas_row = match['atlas_row']
            ambiguous_matches.append({
                'usgs_id': usgs_row['id'],
                'atlas_usgs_eqid': atlas_row['atlas_usgs_eqid'],
                'comcat_usgs_eqid': atlas_row['comcat_usgs_eqid'],
                'match_type': 'ambiguous',
                'usgs_time': usgs_row['time'],
                'atlas_time': atlas_row['datetime'],
                'usgs_latitude': usgs_row['latitude'],
                'atlas_latitude': atlas_row['latitude'],
                'usgs_longitude': usgs_row['longitude'],
                'atlas_longitude': atlas_row['longitude'],
                'usgs_magnitude': usgs_row['mag'],
                'atlas_magnitude': atlas_row['magnitude'],
                'time_diff_hours': match['time_diff_hours'],
                'distance_km': match['distance_km'],
                'mag_diff': match['mag_diff'],
                'candidate_count': len(candidates_with_dist)
            })
    
    # Progress indicator
    if len(spatiotemporal_matches) % 100 == 0 and len(spatiotemporal_matches) > 0:
        print(f"  Processed {len(spatiotemporal_matches)} spatiotemporal matches...")

print(f"Spatiotemporal matches found: {len(spatiotemporal_matches):,}")
print(f"Ambiguous matches found: {len(ambiguous_matches):,}")

# Save spatiotemporal matches
if len(spatiotemporal_matches) > 0:
    spatiotemporal_df = pd.DataFrame(spatiotemporal_matches)
    spatiotemporal_df.to_csv(os.path.join(OUTPUT_DIR, 'spatiotemporal_matches.csv'), index=False)
    print(f"Saved: spatiotemporal_matches.csv")

# Save ambiguous matches
if len(ambiguous_matches) > 0:
    ambiguous_df = pd.DataFrame(ambiguous_matches)
    ambiguous_df.to_csv(os.path.join(OUTPUT_DIR, 'ambiguous_matches.csv'), index=False)
    print(f"Saved: ambiguous_matches.csv")

print()

# Step 6: Identify unmatched events
print("=" * 80)
print("STEP 6: Identifying Unmatched Events")
print("=" * 80)
print()

# USGS events still unmatched
final_unmatched_usgs_ids = usgs_unmatched_ids - matched_usgs_ids
final_unmatched_usgs = usgs_unmatched[usgs_unmatched['usgs_id_normalized'].isin(final_unmatched_usgs_ids)]
print(f"USGS events still unmatched: {len(final_unmatched_usgs):,}")

# AtlasCat events still unmatched
final_unmatched_atlas_ids = atlas_unmatched_ids - matched_atlas_ids
final_unmatched_atlas = atlas_unmatched[atlas_unmatched['comcat_id_normalized'].isin(final_unmatched_atlas_ids)]
print(f"AtlasCat events still unmatched: {len(final_unmatched_atlas):,}")

# Save unmatched events
final_unmatched_usgs[['id', 'time', 'latitude', 'longitude', 'mag', 'place', 'source_file']].to_csv(
    os.path.join(OUTPUT_DIR, 'unmatched_usgs_events.csv'), index=False
)
print(f"Saved: unmatched_usgs_events.csv")

final_unmatched_atlas[['atlas_usgs_eqid', 'comcat_usgs_eqid', 'datetime', 'latitude', 'longitude', 'magnitude', 'iso_code']].to_csv(
    os.path.join(OUTPUT_DIR, 'unmatched_atlascat_events.csv'), index=False
)
print(f"Saved: unmatched_atlascat_events.csv")

print()

# Step 7: Generate matching summary
print("=" * 80)
print("STEP 7: Generating Matching Summary")
print("=" * 80)
print()

total_usgs = len(usgs_2010_2019)
total_atlas = len(atlas_2010_2019)
total_exact = len(exact_matches_df)
total_spatiotemporal = len(spatiotemporal_matches)
total_ambiguous = len(ambiguous_matches)
total_matched = total_exact + total_spatiotemporal
total_unmatched_usgs = len(final_unmatched_usgs)
total_unmatched_atlas = len(final_unmatched_atlas)

summary_data = {
    'metric': [
        'Total USGS events (2010-2019)',
        'Total AtlasCat events (2010-2019)',
        'Exact ID matches',
        'Spatiotemporal matches',
        'Total matched events',
        'Ambiguous matches',
        'Unmatched USGS events',
        'Unmatched AtlasCat events',
        'USGS match rate',
        'AtlasCat match rate'
    ],
    'count': [
        total_usgs,
        total_atlas,
        total_exact,
        total_spatiotemporal,
        total_matched,
        total_ambiguous,
        total_unmatched_usgs,
        total_unmatched_atlas,
        f"{(total_matched/total_usgs)*100:.2f}%",
        f"{(total_matched/total_atlas)*100:.2f}%"
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(OUTPUT_DIR, 'matching_summary.csv'), index=False)
print(f"Saved: matching_summary.csv")

print()

# Step 8: Print terminal summary
print("=" * 80)
print("MATCHING SUMMARY")
print("=" * 80)
print()

print(f"Total USGS events (2010-2019): {total_usgs:,}")
print(f"Total AtlasCat events (2010-2019): {total_atlas:,}")
print()
print(f"Exact ID matches: {total_exact:,} ({(total_exact/total_usgs)*100:.2f}% of USGS)")
print(f"Spatiotemporal matches: {total_spatiotemporal:,} ({(total_spatiotemporal/total_usgs)*100:.2f}% of USGS)")
print(f"Total matched events: {total_matched:,} ({(total_matched/total_usgs)*100:.2f}% of USGS)")
print(f"Ambiguous matches: {total_ambiguous:,}")
print()
print(f"Unmatched USGS events: {total_unmatched_usgs:,} ({(total_unmatched_usgs/total_usgs)*100:.2f}% of USGS)")
print(f"Unmatched AtlasCat events: {total_unmatched_atlas:,} ({(total_unmatched_atlas/total_atlas)*100:.2f}% of AtlasCat)")
print()
print(f"AtlasCat events outside 2010-2019: {len(constraints_std) - len(atlas_2010_2019):,}")
print(f"  (These cannot be matched with current USGS data)")

print()
print("=" * 80)
print("Matching complete. Reports saved to:", OUTPUT_DIR)
print("=" * 80)
