import pandas as pd
import os

DATA_PATH = "data/coupures.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

def save_data(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

def add_signalement(new_row):
    df = load_data()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    save_data(df)
    return df

def clean_data(df):
    if df.empty:
        return df

    df["duree_heures"] = pd.to_numeric(df["duree_heures"], errors="coerce")
    df["impact_numerique"] = pd.to_numeric(df["impact_numerique"], errors="coerce")
    df["frequence_numerique"] = pd.to_numeric(df["frequence_numerique"], errors="coerce")

    return df.dropna()