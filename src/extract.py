import pandas as pd
import yaml


def load_config(path: str = "config/settings.yaml") -> dict:
    """
    Load project configuration from a YAML file.

    Args:
        path: Path to the configuration file.

    Returns:
        Dictionary containing the project configuration.

    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        yaml.YAMLError: If the YAML file contains invalid syntax.
    """
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML in configuration file: {e}")


def extract_csv(path: str) -> pd.DataFrame:
    """
    Read the raw clinical trials CSV into a pandas DataFrame.

    Args:
        path: Path to the raw CSV file.

    Returns:
        DataFrame containing the raw clinical trial data.

    Raises:
        FileNotFoundError: If the CSV file cannot be found.
        pd.errors.ParserError: If the CSV file cannot be parsed.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {path}")
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error parsing CSV file: {e}")


if __name__ == "__main__":
    config = load_config()
    df = extract_csv(config["data"]["raw_path"])

    print(f"Successfully extracted {df.shape[0]:,} rows and {df.shape[1]} columns.")