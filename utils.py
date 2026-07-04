import json
from pathlib import Path
import pandas as pd
import streamlit as st

MODEL_COLORS = {
    "Random Forest": "#3b82f6",
    "XGBoost":       "#22c55e",
    "LSTM":          "#f59e0b",
    "SARIMA":        "#a855f7",
    "Prophet":       "#ef4444",
}

PLOT_CFG = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=10, t=10, b=0),
)

@st.cache_data
def load_all():
    d = Path("data")
    return (
        json.loads((d / "summary.json").read_text(encoding="utf-8")),
        pd.read_csv(d / "monthly_series.csv",    parse_dates=["fecha"]),
        pd.read_csv(d / "model_metrics.csv"),
        pd.read_csv(d / "model_predictions.csv", parse_dates=["fecha"]),
        pd.read_csv(d / "forecast.csv",          parse_dates=["fecha"]),
        pd.read_csv(d / "by_hour.csv"),
        pd.read_csv(d / "by_day.csv"),
        pd.read_csv(d / "cluster_centroids.csv"),
        pd.read_csv(d / "by_province.csv"),
        pd.read_csv(d / "by_type.csv"),
        pd.read_csv(d / "top_cantons.csv"),
    )
