from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.extract import load_config, extract_csv
from src.transform import transform

# Project root (clinical-trial-challenge/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")


def get_engine():
    """
    Create a SQLAlchemy engine using the DATABASE_URL
    defined in the .env file.
    """
    database_url = os.environ.get("DATABASE_URL")

    if database_url is None:
        raise ValueError(
            "DATABASE_URL not found in .env"
        )

    return create_engine(database_url)


def load_studies(df: pd.DataFrame, engine):
    """
    Load study records into the PostgreSQL studies table.
    """
    if df.empty:
        raise ValueError(
            "Cannot load an empty DataFrame."
        )

    df.to_sql(
        name="studies",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(df):,} rows into studies.")

def main():
    config = load_config()

    df = extract_csv(
        PROJECT_ROOT / config["data"]["raw_path"]
    )

    df = transform(df)

    engine = get_engine()

    load_studies(df, engine)


if __name__ == "__main__":
    main()