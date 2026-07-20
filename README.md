# Clinical Trial Challenge

Data pipeline for a life sciences consultancy use case.

## Project Overview

This project builds a data pipeline to ingest, validate, transform, and analyze clinical trial data.

## Current Status

- MVP development in progress using a CSV source as the initial data input
- Project structure established
- Initial data exploration and profiling completed

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