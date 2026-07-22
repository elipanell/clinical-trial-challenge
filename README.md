# Clinical Trial Challenge

Data pipeline for a life sciences consultancy use case.

## Project Overview

This project builds a data pipeline to ingest, validate, transform, and analyze clinical trial data.

## Current Status

Current MVP functionality includes:

- CSV extraction driven by configuration
- Data validation and transformation pipeline
- PostgreSQL schema for storing clinical trial data
- Data loading into PostgreSQL using SQLAlchemy
- Automated unit tests for the transformation pipeline

## Project Structure


clinical-trial-challenge/
├── config/ # Pipeline configuration
├── data/ # Raw and processed data locations
├── notebooks/ # Data exploration and profiling notebooks
├── sql/ # Database schemas
├── src/ # Pipeline source code
└── tests/ # Test suite

## Dependency Management

Chose Python's built-in `venv` and `requirements.txt` over Poetry/Conda to keep the project simple, reproducible, and Docker-friendly for the scope of this challenge.

### Extract

- Reads pipeline configuration from `config/settings.yaml`
- Loads the raw clinical trial CSV into a pandas DataFrame

### Transform

The transformation pipeline performs the following steps:

- Validates required input columns
- Removes CSV index columns created during export
- Casts columns to appropriate data types
- Separates withheld (`[Redacted]`) studies from non-withheld studies
- Removes duplicate non-withheld studies
- Preserves all withheld studies
- Adds an `is_withheld` flag
- Renames columns to match the PostgreSQL schema
- Validates the transformed output before loading

### Load

- Loads the transformed dataset into PostgreSQL using SQLAlchemy
- Reads database configuration from a local `.env` file
- Appends records into the `studies` table
- Validates against an existing SQL schema

## Database

The project uses PostgreSQL running locally in a Docker container.

The database schema is defined in `sql/schema.sql` and includes:

- Auto-generated primary key (`study_id`)
- Typed columns for clinical trial attributes
- Boolean flag identifying withheld studies (`is_withheld`)

The application connects to PostgreSQL using SQLAlchemy and environment variables stored in a local .env file.

## Running the Pipeline
1. Start PostgreSQL

Start a PostgreSQL Docker container.

2. Create the database schema

Execute the SQL schema contained in:

sql/schema.sql
3. Configure environment variables

Create a local .env file containing the PostgreSQL connection settings.

4. Run the pipeline
python -m src.load

This executes the complete ETL workflow:

Extract → Transform → Load
Testing

Run the automated test suite with:

pytest

The current tests validate:

- Duplicate study removal
- Withheld study handling
- Nullable field handling
- Required column validation
- End-to-end transformation behaviour