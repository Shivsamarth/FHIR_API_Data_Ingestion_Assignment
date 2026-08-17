   # Patient Details Data Pipeline

## Overview

This project implements an end-to-end FHIR patient data pipeline using Databricks, Apache Spark, and Delta Lake. It extracts Patient, Encounter, Observation, and Condition resources from a FHIR API and processes them through Raw, Bronze, Silver, and Gold layers.

The pipeline supports date-based processing, metadata tracking, SCD Type 2 versioning, notebook orchestration, and Databricks job notifications.

## Architecture

```text
FHIR API
   ↓
Raw JSON Files
   ↓
Bronze Delta Tables
   ↓
Silver Delta Tables
   ↓
Gold Delta Tables
```

The master notebook orchestrates the processing notebooks in sequence:

```text
Configuration → Raw → Bronze → Silver → Gold
```

## Notebooks

### Configuration Notebook

The configuration notebook centralizes reusable settings such as API endpoints, resource names, storage paths, and table mappings. This avoids hardcoding values across notebooks and makes the pipeline easier to maintain and extend.

### One-Time Detail Notebook

The one-time notebook contains environment setup, schema initialization, path configuration, and reference DDL logic.

Patient Bronze and Silver DDL examples are included for reference. The equivalent DDLs for Encounter, Observation, and Condition were not manually defined because their nested FHIR structures are extensive; their schemas can be inferred or created when required. All Gold tables have been physically created and populated.

### Raw Layer

The Raw notebook extracts paginated FHIR API responses and stores the original JSON files in date-based folders:


<raw_path>/<resource_name>/extraction_date=<load_date>/


Each page is saved as a separate JSON file, preserving the source response for replay, auditing, and troubleshooting.

### Bronze Layer

The Bronze notebook reads the Raw JSON files, expands FHIR bundle entries, and stores resource-level records in Delta tables. It also retains source metadata such as:

- Source file path.
- Extraction timestamp.
- API URL or request parameters.

### Silver Layer

The Silver notebook deduplicates records by resource ID and selects the latest version using `meta.lastUpdated`. It adds processing and record-validity metadata, including:

- `silver_processed_timestamp`.
- `is_current`.
- `effective_start_date`.
- `effective_end_date`.

SCD Type 2 versioning is implemented. When a newer version arrives, the previous current record is expired and the new version is inserted as the current record. This preserves historical changes while making the latest record easy to identify.

### Gold Layer

The Gold notebook creates curated analytical tables from current Silver records:

| Table                      |                      Purpose |
|---                         |---                                         |
| `gold_patient_observation` | Stores current patient observation details. |
| `gold_patient_condition` | Stores current patient condition details. |
| `gold_patient_encounter` | Stores current patient encounter details. |
| `gold_patient_summary` | Stores patient demographics and clinical record counts. |
| `gold_condition_summary` | Stores condition-level occurrence and patient counts. |

All Gold tables include a processing timestamp for auditability.

## Date Parameterization

The Databricks job passes a pipeline date as a job parameter. The master notebook captures this value as `load_date` and passes it through the pipeline.

The date is used to:

- Select the relevant extraction window.
- Create date-based Raw folders.
- Track extraction and processing metadata.
- Maintain the extraction date through the downstream layers.

## Job Orchestration

The master notebook calls the Raw, Bronze, Silver, and Gold notebooks in the required order. The Databricks job also uses the platform's default notification feature to notify users when the pipeline succeeds or fails.

Screenshots in Job Screenshots.zip of the configured Patient Details job is provided as supporting evidence for the notebook tasks, parameters, and notifications.

## Key Requirements Completed

- FHIR API extraction for Patient, Encounter, Observation, and Condition resources.
- Pagination handling for API responses.
- Date-based Raw file organization.
- Bronze ingestion into Delta tables.
- Silver deduplication and current-record management.
- SCD Type 2 historical versioning.
- Gold table creation and data loading.
- Patient and condition summary datasets.
- Parameter-driven Databricks execution.
- Master notebook orchestration.
- Databricks success and failure notifications.
- Reusable configuration notebook.
- GitHub-based source control.

## Repository

The complete project code is committed to the GitHub repository.

Repository: https://github.com/Shivsamarth/FHIR_API_Data_Ingestion_Assignment
