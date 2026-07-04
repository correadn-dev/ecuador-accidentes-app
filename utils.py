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

@st.cache_data(show_spinner="Cargando datos…")
def load_all():
    d = Path("data")
    clusters = pd.read_csv(d / "cluster_centroids.csv")
    # Garantiza columnas canton/fallecidos/heridos aunque el cache sea viejo
    for col in ("canton", "fallecidos", "heridos"):
        if col not in clusters.columns:
            clusters[col] = 0 if col != "canton" else "–"
    if "rank" not in clusters.columns:
        clusters = clusters.sort_values("accidentes", ascending=False).reset_index(drop=True)
        clusters["rank"] = clusters.index + 1
    return (
        json.loads((d / "summary.json").read_text(encoding="utf-8")),
        pd.read_csv(d / "monthly_series.csv",    parse_dates=["fecha"]),
        pd.read_csv(d / "model_metrics.csv"),
        pd.read_csv(d / "model_predictions.csv", parse_dates=["fecha"]),
        pd.read_csv(d / "forecast.csv",          parse_dates=["fecha"]),
        pd.read_csv(d / "by_hour.csv"),
        pd.read_csv(d / "by_day.csv"),
        clusters,
        pd.read_csv(d / "by_province.csv"),
        pd.read_csv(d / "by_type.csv"),
        pd.read_csv(d / "top_cantons.csv"),
    )
