import pandas as pd
import yaml

def load_config(path="config/settings.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def extract_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

if __name__ == "__main__":
    config = load_config()
    df = extract_csv(config["data"]["raw_path"])
    print(df.shape)
    print("csv extracted")