# Clinical Trial Challenge

## Project Overview

This project implements an end-to-end ETL pipeline for clinical trial data using Python, PostgreSQL, Docker, and SQLAlchemy. The pipeline ingests raw clinical trial data, validates and transforms it, loads it into a relational database, and supports analytical SQL queries for reporting.

The implementation focuses on producing a modular, reproducible, and production-inspired pipeline while handling common real-world data quality issues such as duplicate records, missing values, inconsistent formats, and redacted data.

For the scope of this challenge, ingestion was implemented for CSV data only. The pipeline was intentionally designed with modular Extract, Transform and Load components to allow additional sources such as REST APIs or SQL databases to be incorporated in future.

---

# Current Functionality

The project currently includes:

* Configuration-driven CSV ingestion
* Modular Extract → Transform → Load pipeline
* PostgreSQL relational database
* Docker Compose deployment
* SQLAlchemy database loading
* Automated data validation
* Duplicate detection and removal
* Preservation of withheld (redacted) studies
* Surrogate primary key generation
* Automated unit tests
* Analytical SQL queries

---

# Project Structure

```text
clinical-trial-challenge/
├── config/         # Pipeline configuration
├── data/           # Raw datasets
├── notebooks/      # Data profiling and exploration
├── sql/            # Database schema and analytics queries
├── src/            # ETL source code
└── tests/          # Automated tests
```

---

# Architecture

```text
                 config/settings.yaml
                          │
                          ▼
                +-------------------+
                |     Extract       |
                |-------------------|
                | Read CSV dataset  |
                +-------------------+
                          │
                          ▼
                +-------------------+
                |    Transform      |
                |-------------------|
                | Validate columns  |
                | Clean data        |
                | Remove duplicates |
                | Preserve withheld |
                | Cast data types   |
                | Generate study_id |
                +-------------------+
                          │
                          ▼
                +-------------------+
                |       Load        |
                |-------------------|
                | SQLAlchemy        |
                | PostgreSQL        |
                +-------------------+
                          │
                          ▼
                  PostgreSQL Database
                          │
                          ▼
                      studies table
```

---

# Dependency Management

The project uses Python's built-in `venv` together with `requirements.txt`.

This approach keeps the project lightweight, reproducible, Docker-friendly, and appropriate for the scope of the challenge.

---

# ETL Pipeline

## Extract

* Reads pipeline configuration from `config/settings.yaml`
* Loads the selected clinical trial CSV dataset into a pandas DataFrame

## Transform

The transformation pipeline:

* Validates required input columns
* Removes CSV export index columns
* Casts columns to appropriate data types
* Separates withheld (`[Redacted]`) studies from non-withheld studies
* Removes duplicate non-withheld studies
* Preserves all withheld studies
* Adds an `is_withheld` flag
* Renames columns to match the database schema
* Generates a surrogate primary key (`study_id`)
* Validates the transformed dataset before loading

## Load

* Connects to PostgreSQL using SQLAlchemy
* Reads connection settings from `.env`
* Loads transformed data into PostgreSQL
* Validates against the predefined database schema

---

# Database Design

The project uses PostgreSQL running in a Docker container.

The current MVP database schema consists of a single `studies` table designed for analytical querying.

The schema includes:

* Surrogate primary key (`study_id`)
* Typed clinical trial attributes
* Boolean flag identifying withheld studies (`is_withheld`)

A surrogate primary key was chosen because the source dataset does not contain a reliable natural identifier. Study titles, organizations, and other attributes cannot uniquely identify every study, particularly for withheld records where many fields have been redacted.

---

## Indexing Strategy

To support the expected analytical workload, indexes were added to columns frequently used in filtering and grouping operations, including study_type, phases, overall_status, start_date, and organization_full_name.

Index performance was validated using PostgreSQL's EXPLAIN ANALYZE. Selective queries filtering by study_type and phases used an Index Only Scan, while full-table aggregation queries appropriately used a Sequential Scan, demonstrating PostgreSQL's cost-based query planner selecting the most efficient execution strategy.


# Docker

The application is fully containerized using Docker Compose.

Two services are orchestrated:

* PostgreSQL database
* Python ETL application

The database initializes automatically using `sql/schema.sql`, after which the ETL container executes the complete pipeline.

The ETL container mounts the local `data/` directory at runtime rather than embedding datasets inside the Docker image. This keeps the image lightweight, separates application code from input data, and allows datasets to be updated without rebuilding the image.

---

# Running the Pipeline

Ensure Docker and Docker Compose are installed before running the project.

### 1. Configure environment variables

Create a local `.env` file containing the PostgreSQL connection settings.
An example configuration is provided in `.env.example`.

### 2. Start the application

```bash
docker compose up --build
```

Running the command will automatically:

* Create the PostgreSQL database
* Execute `sql/schema.sql`
* Run the ETL pipeline
* Load the transformed dataset into PostgreSQL

---

# Testing

Run the automated test suite with:

```bash
pytest
```

Current test coverage includes:

* Duplicate study removal
* Preservation of withheld studies
* Nullable field handling
* Required column validation
* Data type conversion
* Surrogate key generation
* End-to-end transformation behaviour

---

# Data Quality Decisions

Several real-world data quality issues were identified during exploratory analysis, including:

* Duplicate studies
* Missing values
* Mixed date formats
* Nullable clinical attributes
* Redacted organisations

A key design decision was preserving every withheld (`[Redacted]`) study.

Although many withheld records appear identical after redaction, there is no evidence that they represent duplicate studies. Removing them could incorrectly discard legitimate clinical trials. Instead, duplicates are removed only for non-withheld studies while all withheld records are retained and explicitly flagged using `is_withheld`.

---

# Design Decisions and Limitations

The challenge encouraged consideration of relational modelling.

The `Conditions` column was investigated for normalization. During data profiling, it was found that the dataset stores multiple medical concepts within a single free-text field where commas are used both:

* as separators between conditions
* within individual medical terminology

Examples include:

* `Kidney Failure, Chronic`
* `Arthroplasty, Replacement, Knee`

Because no reliable delimiter exists, automatic normalization would incorrectly split valid medical terms into separate conditions.

To preserve data integrity, the project intentionally retains the original representation supplied by the source dataset rather than introducing potentially incorrect normalized records.

This reflects a deliberate engineering trade-off that prioritizes data integrity over aggressive normalization when the source data is ambiguous.

---

# Analytics

Example analytical SQL queries are provided in:

```text
sql/analytics_queries.sql
```

The queries answer questions such as:

* Trials by study type and phase
* Most common conditions
* Intervention completion rates
* Trial status distribution
* Timeline analysis
* Geographic distribution (not possible with the available dataset due to the absence of location information)

---

# Time Allocation

Approximate effort:

- Project setup, Python environment and Docker configuration: ~45 minutes
- Exploratory data analysis and data profiling: ~45 minutes
- ETL implementation (Extract, Transform, Load): ~90 minutes
- Database schema design and analytical SQL queries: ~30 minutes
- Testing and validation: ~30 minutes
- Investigation of relational modelling and normalization feasibility (ultimately not implemented after data profiling identified ambiguous source formatting): ~60 minutes
- Documentation and final refinement: ~45 minutes

**Total:** approximately **5.5 hours**.

---

# Future Improvements

Potential production enhancements include:

* Support for additional data sources (REST APIs and databases)
* Incremental loading instead of full refreshes
* Additional normalization once reliable domain rules are available
* Database partitioning and query optimization for larger datasets
* Structured logging and monitoring
* Data lineage and audit logging
* CI/CD pipeline with automated testing and deployment

---

## Bonus Discussion

### Security

In production, sensitive data would be protected using role-based access control (RBAC), encrypted database connections, secret management for credentials, and audit logging to restrict and monitor access.

### Data Quality

Production data quality would be managed through automated validation rules, schema enforcement, completeness checks, duplicate detection, and monitoring dashboards to identify anomalies during ingestion.

### Scalability

For larger datasets, the pipeline could support incremental loading, table partitioning, parallel processing, and orchestration using workflow tools such as Airflow.

### Cloud Deployment

A production deployment could utilise cloud-managed PostgreSQL, object storage for raw data, container orchestration (e.g. Kubernetes or ECS), and CI/CD pipelines for automated deployment.

### AI Assistance

AI was used to assist with brainstorming, documentation refinement, and code review. All implementation, debugging, testing, and validation were completed and verified manually before submission.