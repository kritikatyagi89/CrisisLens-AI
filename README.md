# CrisisLens AI

## AI-Powered Disaster Response System

CrisisLens AI is an academic major project focused on using earthquake data, population exposure, and machine learning to support disaster impact assessment and emergency response planning.

## Project Objective

The goal is to help emergency teams understand potential earthquake impacts and support decisions related to emergency resources and response planning.

**Note:** The current ML task focuses on event-level fatality-risk classification after an earthquake. It does not predict earthquakes.

## My Contribution: Data Acquisition and Processing

My responsibilities include:
- Collecting earthquake data from USGS and AtlasCat.
- Matching earthquake records across datasets.
- Cleaning and validating integrated data.
- Preparing labeled data for machine learning.
- Auditing target quality and potential data leakage.
- Documenting candidate feature columns.

## Preliminary Dataset Summary

Based on the reported target-quality audit:

- Matched earthquake events: 2,224
- Labeled events: 499
- Positive class (reported deaths greater than zero): 263
- Negative class (explicitly reported zero deaths): 236
- Events with missing death values: 1,725

Missing death values are not treated as zero.

## Data Sources

- USGS Earthquake Catalogue
- AtlasCat Constraints
- AtlasCat Exposure
- AtlasCat Losses

## Current Status

- Data collection and matching: Reported complete
- Data cleaning and validation: Reported complete
- Preliminary target-quality audit: Reported complete
- Feature selection and leakage review: Pending final approval
- Baseline ML model and evaluation: Upcoming

## Important Limitation

The current labeled target represents event-level reported fatality risk. It should not be interpreted as a prediction of earthquake occurrence or as a district-level death estimate.

## Technologies and Tools

- Python
- CSV datasets
- Data processing and validation
- Machine learning (planned)

This project is under development as part of an academic major project.
