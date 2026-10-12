"""
CrisisLens AI - Step 2: Basic Data Validation
=============================================

This script validates the downloaded earthquake datasets:
- 10 USGS yearly files (2010-2019)
- 3 AtlasCat CSV files (Constraints, Exposure, Losses)

It checks for:
- File structure (rows, columns, column names)
- Date ranges and year coverage
- Missing values
- Duplicate rows and IDs
- Valid coordinates and magnitudes
- Event type verification
- AtlasCat file alignment

Author: CrisisLens AI Team
Date: October 11, 2026
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings

# Ignore warnings for cleaner output
warnings.filterwarnings('ignore')

# Configuration
DATA_DIR = 'data/raw'
USGS_DIR = os.path.join(DATA_DIR, 'usgs_historical')
REPORT_DIR = 'reports/data_validation'

# Create reports directory if it doesn't exist
os.makedirs(REPORT_DIR, exist_ok=True)

print("=" * 80)
print("CrisisLens AI - Basic Data Validation")
print("=" * 80)
print(f"Data directory: {DATA_DIR}")
print(f"Report directory: {REPORT_DIR}")
print()

# Lists to store validation results for all files
validation_results = []
missing_values_results = []
duplicate_results = []
date_range_results = []

def validate_csv_file(file_path, file_type, expected_year=None):
    """
    Validate a single CSV file and return validation results.
    
    Parameters:
    - file_path: Path to the CSV file
    - file_type: 'usgs' or 'atlascat'
    - expected_year: Expected year for USGS files (e.g., 2010)
    
    Returns:
    - Dictionary with validation results
    """
    print(f"Validating: {file_path}")
    
    result = {
        'file_name': os.path.basename(file_path),
        'file_type': file_type,
        'expected_year': expected_year if expected_year else 'N/A',
        'file_readable': False,
        'rows': 0,
        'columns': 0,
        'column_names': '',
        'min_date': 'N/A',
        'max_date': 'N/A',
        'date_column': 'N/A',
        'id_column': 'N/A',
        'missing_values_count': 0,
        'duplicate_rows': 0,
        'duplicate_ids': 0,
        'has_latitude': False,
        'has_longitude': False,
        'has_magnitude': False,
        'has_date': False,
        'latitude_valid': False,
        'longitude_valid': False,
        'magnitude_valid': False,
        'date_valid': False,
        'event_type_check': 'N/A',
        'event_type_valid': False,
        'error_message': ''
    }
    
    try:
        # Try to read the CSV file
        df = pd.read_csv(file_path)
        
        result['file_readable'] = True
        result['rows'] = len(df)
        result['columns'] = len(df.columns)
        result['column_names'] = ', '.join(df.columns.tolist())
        
        # Check for duplicate rows
        result['duplicate_rows'] = df.duplicated().sum()
        
        # Identify date column based on file type
        if file_type == 'usgs':
            date_col = 'time' if 'time' in df.columns else None
            id_col = 'id' if 'id' in df.columns else None
            type_col = 'type' if 'type' in df.columns else None
        else:  # atlascat
            date_col = 'DateTime' if 'DateTime' in df.columns else None
            id_col = 'Atlas_USGS_eqID' if 'Atlas_USGS_eqID' in df.columns else 'Atlas USGS eqID' if 'Atlas USGS eqID' in df.columns else None
            type_col = None  # AtlasCat doesn't have event type column
        
        result['date_column'] = date_col if date_col else 'Not found'
        result['id_column'] = id_col if id_col else 'Not found'
        
        # Check for presence of key columns
        result['has_latitude'] = 'latitude' in df.columns or 'lat' in df.columns
        result['has_longitude'] = 'longitude' in df.columns or 'lon' in df.columns
        result['has_magnitude'] = 'mag' in df.columns
        result['has_date'] = date_col is not None
        
        # Parse dates and check date range
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                result['min_date'] = df[date_col].min()
                result['max_date'] = df[date_col].max()
                result['date_valid'] = True
            except Exception as e:
                result['date_valid'] = False
                result['error_message'] = f"Date parsing error: {str(e)}"
        
        # Check for duplicate IDs
        if id_col:
            result['duplicate_ids'] = df[id_col].duplicated().sum()
        
        # Check latitude validity
        lat_col = 'latitude' if 'latitude' in df.columns else 'lat' if 'lat' in df.columns else None
        if lat_col:
            try:
                lat_values = pd.to_numeric(df[lat_col], errors='coerce')
                valid_lat = lat_values.between(-90, 90).sum()
                result['latitude_valid'] = valid_lat == len(df)
            except:
                result['latitude_valid'] = False
        
        # Check longitude validity
        lon_col = 'longitude' if 'longitude' in df.columns else 'lon' if 'lon' in df.columns else None
        if lon_col:
            try:
                lon_values = pd.to_numeric(df[lon_col], errors='coerce')
                valid_lon = lon_values.between(-180, 180).sum()
                result['longitude_valid'] = valid_lon == len(df)
            except:
                result['longitude_valid'] = False
        
        # Check magnitude validity
        mag_col = 'mag' if 'mag' in df.columns else None
        if mag_col:
            try:
                mag_values = pd.to_numeric(df[mag_col], errors='coerce')
                valid_mag = mag_values.notna().sum()
                result['magnitude_valid'] = valid_mag > 0
            except:
                result['magnitude_valid'] = False
        
        # Check event type for USGS files
        if file_type == 'usgs' and type_col:
            result['event_type_check'] = type_col
            if df[type_col].notna().any():
                all_earthquake = (df[type_col] == 'earthquake').all()
                result['event_type_valid'] = all_earthquake
            else:
                result['event_type_valid'] = True  # No type column means assume valid
        
        # Count missing values
        missing_count = df.isnull().sum().sum()
        result['missing_values_count'] = missing_count
        
        # Store missing values by column
        missing_by_col = df.isnull().sum()
        for col, count in missing_by_col.items():
            missing_values_results.append({
                'file_name': result['file_name'],
                'column': col,
                'missing_count': count,
                'missing_percentage': (count / len(df)) * 100
            })
        
        # Store duplicate information
        duplicate_results.append({
            'file_name': result['file_name'],
            'duplicate_rows': result['duplicate_rows'],
            'duplicate_ids': result['duplicate_ids'],
            'total_rows': result['rows']
        })
        
        # Store date range information
        date_range_results.append({
            'file_name': result['file_name'],
            'expected_year': expected_year if expected_year else 'N/A',
            'date_column': result['date_column'],
            'min_date': str(result['min_date']),
            'max_date': str(result['max_date']),
            'year_coverage': str(result['min_date'].year) if result['min_date'] != 'N/A' else 'N/A'
        })
        
    except Exception as e:
        result['error_message'] = f"File reading error: {str(e)}"
        print(f"  ERROR: {result['error_message']}")
    
    print(f"  Rows: {result['rows']:,}, Columns: {result['columns']}")
    print(f"  Date range: {result['min_date']} to {result['max_date']}")
    print(f"  Missing values: {result['missing_values_count']:,}")
    print(f"  Duplicate rows: {result['duplicate_rows']:,}")
    print()
    
    return result

# Step 1: Validate USGS yearly files
print("=" * 80)
print("STEP 1: Validating USGS Yearly Files (2010-2019)")
print("=" * 80)
print()

usgs_files = []
for year in range(2010, 2020):
    file_path = os.path.join(USGS_DIR, f'usgs_{year}.csv')
    if os.path.exists(file_path):
        usgs_files.append((file_path, year))
        result = validate_csv_file(file_path, 'usgs', expected_year=year)
        validation_results.append(result)
    else:
        print(f"WARNING: File not found: {file_path}")
        validation_results.append({
            'file_name': f'usgs_{year}.csv',
            'file_type': 'usgs',
            'expected_year': year,
            'file_readable': False,
            'error_message': 'File not found'
        })

# Step 2: Validate AtlasCat files
print("=" * 80)
print("STEP 2: Validating AtlasCat Files")
print("=" * 80)
print()

atlascat_files = [
    ('AtlasCat_Constraints.csv', 'atlascat'),
    ('AtlasCat_Exposure.csv', 'atlascat'),
    ('AtlasCat_Losses.csv', 'atlascat')
]

for file_name, file_type in atlascat_files:
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        result = validate_csv_file(file_path, file_type)
        validation_results.append(result)
    else:
        print(f"WARNING: File not found: {file_path}")
        validation_results.append({
            'file_name': file_name,
            'file_type': file_type,
            'expected_year': 'N/A',
            'file_readable': False,
            'error_message': 'File not found'
        })

# Step 3: Check AtlasCat file alignment
print("=" * 80)
print("STEP 3: Checking AtlasCat File Alignment")
print("=" * 80)
print()

try:
    constraints = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Constraints.csv'))
    exposure = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Exposure.csv'))
    losses = pd.read_csv(os.path.join(DATA_DIR, 'AtlasCat_Losses.csv'))
    
    # Check row counts
    print(f"Constraints rows: {len(constraints):,}")
    print(f"Exposure rows: {len(exposure):,}")
    print(f"Losses rows: {len(losses):,}")
    
    # Check if row counts match
    rows_match = (len(constraints) == len(exposure) == len(losses))
    print(f"Row counts match: {rows_match}")
    
    # Check ID column alignment
    constraints_id_col = 'Atlas USGS eqID' if 'Atlas USGS eqID' in constraints.columns else 'Atlas_USGS_eqID'
    exposure_id_col = 'Atlas_USGS_eqID' if 'Atlas_USGS_eqID' in exposure.columns else 'Atlas USGS eqID'
    losses_id_col = 'Atlas_USGS_eqID' if 'Atlas_USGS_eqID' in losses.columns else 'Atlas USGS eqID'
    
    print(f"Constraints ID column: {constraints_id_col}")
    print(f"Exposure ID column: {exposure_id_col}")
    print(f"Losses ID column: {losses_id_col}")
    
    # Check if IDs match across files
    if constraints_id_col in constraints.columns and exposure_id_col in exposure.columns:
        constraints_ids = set(constraints[constraints_id_col].tolist())
        exposure_ids = set(exposure[exposure_id_col].tolist())
        losses_ids = set(losses[losses_id_col].tolist())
        
        ids_match = (constraints_ids == exposure_ids == losses_ids)
        print(f"Event IDs match across all files: {ids_match}")
        
        if not ids_match:
            print(f"Constraints IDs: {len(constraints_ids):,}")
            print(f"Exposure IDs: {len(exposure_ids):,}")
            print(f"Losses IDs: {len(losses_ids):,}")
            print(f"IDs in Constraints but not in Exposure: {len(constraints_ids - exposure_ids):,}")
            print(f"IDs in Exposure but not in Constraints: {len(exposure_ids - constraints_ids):,}")
    
except Exception as e:
    print(f"ERROR checking AtlasCat alignment: {str(e)}")

print()

# Step 4: Generate reports
print("=" * 80)
print("STEP 4: Generating Validation Reports")
print("=" * 80)
print()

# Validation summary CSV
validation_df = pd.DataFrame(validation_results)
validation_df.to_csv(os.path.join(REPORT_DIR, 'validation_summary.csv'), index=False)
print(f"Saved: validation_summary.csv")

# Missing values report CSV
missing_df = pd.DataFrame(missing_values_results)
missing_df.to_csv(os.path.join(REPORT_DIR, 'missing_values_report.csv'), index=False)
print(f"Saved: missing_values_report.csv")

# Duplicate records report CSV
duplicate_df = pd.DataFrame(duplicate_results)
duplicate_df.to_csv(os.path.join(REPORT_DIR, 'duplicate_records_report.csv'), index=False)
print(f"Saved: duplicate_records_report.csv")

# Date range report CSV
date_df = pd.DataFrame(date_range_results)
date_df.to_csv(os.path.join(REPORT_DIR, 'date_range_report.csv'), index=False)
print(f"Saved: date_range_report.csv")

print()

# Step 5: Print terminal summary
print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print()

# Total USGS records
usgs_results = [r for r in validation_results if r['file_type'] == 'usgs' and r['file_readable']]
total_usgs_records = sum(r['rows'] for r in usgs_results)
print(f"Total USGS records (2010-2019): {total_usgs_records:,}")

# Total AtlasCat records
atlascat_results = [r for r in validation_results if r['file_type'] == 'atlascat' and r['file_readable']]
total_atlascat_records = sum(r['rows'] for r in atlascat_results)
print(f"Total AtlasCat records: {total_atlascat_records:,}")

# Missing years
missing_years = []
for year in range(2010, 2020):
    year_result = next((r for r in usgs_results if r['expected_year'] == year), None)
    if not year_result or not year_result['file_readable']:
        missing_years.append(year)

if missing_years:
    print(f"Missing years: {missing_years}")
else:
    print(f"Missing years: None")

# Duplicate IDs
total_duplicate_ids = sum(r['duplicate_ids'] for r in validation_results if r['file_readable'])
print(f"Total duplicate event IDs: {total_duplicate_ids:,}")

# Invalid coordinates
invalid_lat = sum(1 for r in validation_results if r['file_readable'] and not r['latitude_valid'])
invalid_lon = sum(1 for r in validation_results if r['file_readable'] and not r['longitude_valid'])
print(f"Files with invalid latitude: {invalid_lat}")
print(f"Files with invalid longitude: {invalid_lon}")

# Event type check
usgs_type_valid = sum(1 for r in usgs_results if r['event_type_valid'])
print(f"USGS files with valid event type (earthquake): {usgs_type_valid}/{len(usgs_results)}")

# Data quality issues
issues = []
for r in validation_results:
    if r['file_readable']:
        if r['duplicate_rows'] > 0:
            issues.append(f"{r['file_name']}: {r['duplicate_rows']} duplicate rows")
        if r['duplicate_ids'] > 0:
            issues.append(f"{r['file_name']}: {r['duplicate_ids']} duplicate IDs")
        if not r['latitude_valid']:
            issues.append(f"{r['file_name']}: Invalid latitude values")
        if not r['longitude_valid']:
            issues.append(f"{r['file_name']}: Invalid longitude values")
        if not r['magnitude_valid']:
            issues.append(f"{r['file_name']}: Invalid magnitude values")

if issues:
    print(f"\nData quality issues found:")
    for issue in issues[:10]:  # Show first 10 issues
        print(f"  - {issue}")
    if len(issues) > 10:
        print(f"  ... and {len(issues) - 10} more issues (see reports for details)")
else:
    print(f"\nNo major data quality issues found.")

print()
print("=" * 80)
print("Validation complete. Reports saved to:", REPORT_DIR)
print("=" * 80)
