{
  "api": {
    "base_url": "https://hapi.fhir.org/baseR4",
    "response_format": "json",
    "timeout_seconds": 60
  },
  "resources": [
    {
      "name": "Patient",
      "endpoint": "/Patient"
    },
    {
      "name": "Encounter",
      "endpoint": "/Encounter"
    },
    {
      "name": "Observation",
      "endpoint": "/Observation"
    },
    {
      "name": "Condition",
      "endpoint": "/Condition"
    }
  ],
  "ingestion": {
    "days_to_ingest": 3,
    "page_size": 100,
    "pagination_mode": "next_link",
    "sort_by": "_lastUpdated"
  },
  "paths": {
    "raw_base_path": "/tmp/fhir_assignment/raw",
    "bronze_database": "fhir_bronze",
    "silver_database": "fhir_silver",
    "gold_database": "fhir_gold"
  },
  "metadata_columns": [
    "extraction_timestamp",
    "api_url_or_params",
    "api_call_timestamp",
    "data_saved_timestamp",
    "source_file_name"
  ],
  "scd_type_2": {
    "enabled": true,
    "effective_from_column": "effective_from",
    "effective_to_column": "effective_to",
    "is_current_column": "is_current",
    "record_hash_column": "record_hash"
  }
}