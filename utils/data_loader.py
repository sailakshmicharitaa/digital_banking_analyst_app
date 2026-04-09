from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "digital_banking_data.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df["application_date"] = pd.to_datetime(df["application_date"])
    df["activated_date"] = pd.to_datetime(df["activated_date"], errors="coerce")
    return df


@st.cache_data
def filtered_data(
    df: pd.DataFrame,
    selected_regions: list[str],
    selected_channels: list[str],
    selected_products: list[str],
) -> pd.DataFrame:
    filtered = df.copy()

    if selected_regions:
        filtered = filtered[filtered["region"].isin(selected_regions)]

    if selected_channels:
        filtered = filtered[filtered["acquisition_channel"].isin(selected_channels)]

    if selected_products:
        filtered = filtered[filtered["product_type"].isin(selected_products)]

    return filtered.reset_index(drop=True)
