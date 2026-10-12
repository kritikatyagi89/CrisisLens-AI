# CrisisLens AI - Data Validation Report

**Date:** October 11, 2026
**Step:** Step 2 - Basic Data Verification
**Status:** Complete

---

## Executive Summary

All datasets have been successfully validated. The USGS historical files (2010-2019) and AtlasCat files (Constraints, Exposure, Losses) are properly formatted, readable, and contain consistent data.

**Key Findings:**
- **Total USGS records:** 181,695 earthquakes (2010-2019)
- **Total AtlasCat records:** 42,753 (14,251 events × 3 files)
- **Missing years:** None (all 10 years present)
- **Duplicate records:** 0 across all files
- **Invalid coordinates:** None detected
- **AtlasCat alignment:** Perfect (row counts and event IDs match across all 3 files)

**Overall Assessment:** Datasets passed basic validation and are ready for Step 3 (Data Integration).

---

## 1. USGS Yearly Files Validation

### 1.1 File Overview

| File Name | Rows | Columns | Date Range | Expected Year | Year Coverage |
|-----------|------|---------|------------|--------------|--------------|
| usgs_2010.csv | 17,096 | 22 | 2010-01-01 to 2010-12-31 | 2010 | ✓ Complete |
| usgs_2011.csv | 18,791 | 22 | 2011-01-01 to 2011-12-31 | 2011 | ✓ Complete |
| usgs_2012.csv | 15,609 | 22 | 2012-01-01 to 2012-12-31 | 2012 | ✓ Complete |
| usgs_2013.csv | 16,254 | 22 | 2013-01-01 to 2013-12-31 | 2013 | ✓ Complete |
| usgs_2014.csv | 19,632 | 22 | 2014-01-01 to 2014-11-25 | 2014 | ⚠ Partial (ends Nov 25) |
| usgs_2015.csv | 19,881 | 22 | 2015-01-01 to 2015-12-31 | 2015 | ✓ Complete |
| usgs_2016.csv | 19,204 | 22 | 2016-01-01 to 2016-12-31 | 2016 | ✓ Complete |
| usgs_2017.csv | 16,984 | 22 | 2017-01-01 to 2017-12-31 | 2017 | ✓ Complete |
| usgs_2018.csv | 19,902 | 22 | 2018-01-01 to 2018-11-01 | 2018 | ⚠ Partial (ends Nov 1) |
| usgs_2019.csv | 18,342 | 22 | 2019-01-01 to 2019-12-31 | 2019 | ✓ Complete |

**Total USGS Records:** 181,695

### 1.2 Column Structure

All USGS files have consistent column structure (22 columns):
- `time` - Event timestamp
- `latitude` - Epicenter latitude
- `longitude` - Epicenter longitude
- `depth` - Event depth (km)
- `mag` - Magnitude
- `magType` - Magnitude type
- `nst` - Number of seismic stations
- `gap` - Azimuthal gap
- `dmin` - Horizontal distance to nearest station
- `rms` - Root-mean-square travel time residual
- `net` - Network code
- `id` - Unique event identifier
- `updated` - Last update timestamp
- `place` - Textual location description
- `type` - Event type
- `horizontalError` - Horizontal location uncertainty
- `depthError` - Depth uncertainty
- `magError` - Magnitude uncertainty
- `magNst` - Number of stations for magnitude
- `status` - Review status
- `locationSource` - Source of location data
- `magSource` - Source of magnitude data

### 1.3 Data Quality

**Missing Values:**
- 2010: 66,658 missing values across all columns
- 2011: 75,219 missing values
- 2012: 63,958 missing values
- 2013: 57,017 missing values
- 2014: 41,970 missing values
- 2015: 28,743 missing values
- 2016: 27,247 missing values
- 2017: 21,643 missing values
- 2018: 23,125 missing values
- 2019: 20,786 missing values

**Note:** Missing values are expected in optional fields (e.g., `horizontalError`, `depthError`, `magError` for events with limited station coverage).

**Duplicate Records:** 0 across all USGS files

**Duplicate Event IDs:** 0 across all USGS files

**Coordinate Validity:** All latitude and longitude values are within valid ranges (latitude: -90 to 90, longitude: -180 to 180)

**Magnitude Validity:** All magnitude values are present and valid

**Event Type:** The `type` column exists in all files but was not validated in this step (will be checked in Step 3)

### 1.4 Year Coverage Issues

**Partial Year Coverage:**
- **usgs_2014.csv:** Ends on 2014-11-25 (missing December 2014)
- **usgs_2018.csv:** Ends on 2018-11-01 (missing November-December 2018)

**Impact:** These files do not contain complete year coverage. This may affect time-series analysis or yearly comparisons.

**Recommendation:** Verify if these partial years are expected or if data needs to be re-downloaded for complete coverage.

---

## 2. AtlasCat Files Validation

### 2.1 File Overview

| File Name | Rows | Columns | Date Range |
|-----------|------|---------|------------|
| AtlasCat_Constraints.csv | 14,251 | 14 | 1900-07-29 to 2020-12-29 |
| AtlasCat_Exposure.csv | 14,251 | 22 | 1900-07-29 to 2020-12-29 |
| AtlasCat_Losses.csv | 14,251 | 127 | 1900-07-29 to 2020-12-29 |

**Total AtlasCat Records:** 42,753 (14,251 events × 3 files)

### 2.2 Column Structure

**AtlasCat_Constraints.csv (14 columns):**
- `Atlas USGS eqID` - USGS event ID
- `Comcat USGS eqID` - ComCat event ID
- `id_info` - ID compatibility indicator
- `DateTime` - Event timestamp
- `lat` - Latitude
- `lon` - Longitude
- `depth (km)` - Depth
- `mag` - Magnitude
- `mag type` - Magnitude type
- `Atlas v4 type` - ShakeMap production method
- `ISO_code` - Country code
- `Fault` - Fault model availability
- `Intensity Observations` - Count of intensity observations
- `Ground Motion Recordings` - Count of ground motion recordings

**AtlasCat_Exposure.csv (22 columns):**
- Core columns (same as Constraints with slight naming differences)
- `Atlas_USGS_eqID` (note: underscore vs space in Constraints)
- `Comcat_USGS_eqID`
- `DateTime`
- `lat`, `lon`, `depth(km)`
- `mag`, `mag_type`
- `Atlas_v4_type`
- `ISO_code`
- `Version_at_release`
- `location_string`
- `MMI_III` through `MMI_X` - Population exposure by intensity
- `Max_MMI` - Maximum intensity with exposure

**AtlasCat_Losses.csv (127 columns):**
- Core columns (same as Exposure)
- `Pref_total_deaths` - Preferred total deaths
- `Pref_total_deaths_src` - Death data source
- `Pref_econ_loss` - Preferred economic loss
- `Pref_econ_loss_src` - Economic loss source
- PDE (USGS) loss columns (deaths, injuries, displaced, buildings, economic loss)
- Utsu catalog loss columns
- NCEI/NOAA catalog loss columns
- EMDAT catalog loss columns
- Various quality flags and comments

### 2.3 Data Quality

**Missing Values:**
- Constraints: 18 missing values (minimal)
- Exposure: 28,719 missing values (mostly in MMI columns for events without exposure data)
- Losses: 1,425,569 missing values (expected - many loss fields are sparse)

**Duplicate Records:** 0 across all AtlasCat files

**Duplicate Event IDs:** 0 across all AtlasCat files

**Coordinate Validity:** All latitude and longitude values are valid

**Magnitude Validity:** All magnitude values are present and valid

### 2.4 File Alignment

**Row Count Alignment:**
- Constraints: 14,251 rows
- Exposure: 14,251 rows
- Losses: 14,251 rows
- **Status:** ✓ Perfect match

**Event ID Alignment:**
- Constraints ID column: `Atlas USGS eqID`
- Exposure ID column: `Atlas_USGS_eqID`
- Losses ID column: `Atlas_USGS_eqID`
- **Status:** ✓ All event IDs match across all three files

**Note:** There is a minor naming inconsistency (space vs underscore in ID column names), but the actual IDs match perfectly.

---

## 3. Data Quality Assessment

### 3.1 CSV File Format

**Status:** ✓ All files are valid CSV files and can be parsed correctly using pandas.

### 3.2 Coordinate Validation

**Status:** ✓ All latitude and longitude values are within valid geographic ranges.
- Latitude: -90 to 90 degrees
- Longitude: -180 to 180 degrees

### 3.3 Magnitude Validation

**Status:** ✓ All magnitude values are present and numeric.

### 3.4 Date Validation

**Status:** ✓ All date columns can be parsed correctly.
- USGS: `time` column (ISO 8601 format)
- AtlasCat: `DateTime` column (ISO 8601 format)

### 3.5 Duplicate Detection

**Status:** ✓ No duplicate rows or event IDs detected in any file.

### 3.6 Event Type Check

**Status:** ⚠ Not validated in this step. The `type` column exists in USGS files but was not checked. This will be validated in Step 3.

---

## 4. Issues and Recommendations

### 4.1 Issues Found

**Minor Issues:**

1. **Partial Year Coverage (USGS):**
   - usgs_2014.csv ends on 2014-11-25 (missing December)
   - usgs_2018.csv ends on 2018-11-01 (missing November-December)
   - **Impact:** Incomplete yearly data for 2014 and 2018
   - **Severity:** Low
   - **Recommendation:** Verify if this is expected or re-download for complete coverage

2. **Column Naming Inconsistency (AtlasCat):**
   - Constraints uses `Atlas USGS eqID` (space)
   - Exposure/Losses use `Atlas_USGS_eqID` (underscore)
   - **Impact:** Minor inconvenience for data integration
   - **Severity:** Low
   - **Recommendation:** Standardize column names during Step 3 (Data Integration)

3. **Missing Values (Expected):**
   - USGS files have missing values in optional fields (error estimates)
   - AtlasCat Losses has many missing values (sparse loss data)
   - **Impact:** Expected behavior, not an error
   - **Severity:** None
   - **Recommendation:** Handle missing values appropriately during feature engineering

### 4.2 Recommendations for Step 3

1. **Standardize column names** across AtlasCat files (replace spaces with underscores)
2. **Verify event type** in USGS files (ensure all are "earthquake")
3. **Handle partial year coverage** in 2014 and 2018 (decide whether to use as-is or supplement)
4. **Implement missing value handling strategy** for feature engineering
5. **Validate date ranges** match expected years before merging

---

## 5. Validation Summary

### 5.1 Pass/Fail Status

| Check | Status | Notes |
|-------|--------|-------|
| File readability | ✓ PASS | All files readable |
| CSV format validity | ✓ PASS | All valid CSV files |
| Column presence | ✓ PASS | All required columns present |
| Date parsing | ✓ PASS | All dates parse correctly |
| Coordinate validity | ✓ PASS | All coordinates valid |
| Magnitude validity | ✓ PASS | All magnitudes valid |
| Duplicate rows | ✓ PASS | No duplicates found |
| Duplicate IDs | ✓ PASS | No duplicate IDs |
| Year coverage | ⚠ WARNING | 2014 and 2018 partial |
| AtlasCat alignment | ✓ PASS | Perfect alignment |
| Event type check | ⚠ PENDING | Will check in Step 3 |

### 5.2 Overall Assessment

**Status:** ✓ PASSED (with minor warnings)

The datasets have passed basic validation and are ready for Step 3 (Data Integration). The partial year coverage for 2014 and 2018 should be addressed, but this does not prevent proceeding to the next step.

### 5.3 Files Generated

All validation reports have been saved to `reports/data_validation/`:
- `validation_summary.csv` - Overall validation summary
- `missing_values_report.csv` - Missing values by column and file
- `duplicate_records_report.csv` - Duplicate record information
- `date_range_report.csv` - Date range and year coverage
- `data_validation_report.md` - This comprehensive report

---

## 6. Next Steps

**Step 3: Data Integration**
1. Standardize column names across AtlasCat files
2. Verify event type in USGS files
3. Merge USGS yearly files into single dataset
4. Merge AtlasCat files by event ID
5. Perform earthquake matching between USGS and AtlasCat
6. Handle missing values
7. Generate integrated dataset for feature engineering

**Step 4: Feature Engineering**
1. Extract temporal features (year, month, day, hour)
2. Calculate geographic features
3. Engineer exposure features
4. Create impact severity labels
5. Handle categorical variables

---

**Report prepared by:** CrisisLens AI Data Validation Script
**Date:** October 11, 2026
**Status:** Complete
