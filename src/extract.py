from pathlib import Path
import pandas as pd
import yaml

# Project root (clinical-trial-challenge/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config(config_path=None):
    """
    Load project configuration from the YAML file.
    """
    if config_path is None:
        config_path = PROJECT_ROOT / "config" / "settings.yaml"

    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")


def extract_csv(path):
    """
    Extract clinical trial data from a CSV file.
    """
    csv_path = PROJECT_ROOT / path

    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")


if __name__ == "__main__":
    config = load_config()
    df = extract_csv(config["data"]["raw_path"])

    print(f"Successfully extracted {df.shape[0]:,} rows and {df.shape[1]} columns.")