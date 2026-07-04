import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Exploración de Datos", page_icon="🔍", layout="wide")

@st.cache_data
def load():
    by_hour  = pd.read_csv("data/by_hour.csv")
    by_day   = pd.read_csv("data/by_day.csv")
    monthly  = pd.read_csv("data/monthly_series.csv", parse_dates=["fecha"])
    by_prov  = pd.read_csv("data/by_province.csv") if Path("data/by_province.csv").exists() else pd.DataFrame()
    by_type  = pd.read_csv("data/by_type.csv")    if Path("data/by_type.csv").exists()    else pd.DataFrame()
    return by_hour, by_day, monthly, by_prov, by_type

by_hour, by_day, monthly, by_prov, by_type = load()

st.title("🔍 Exploración de Datos")
st.markdown("**Dataset:** ANT Ecuador · 166,682 accidentes · Enero 2017 – Abril 2024")
st.divider()

# ── HORA Y DÍA ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Accidentes por hora del día")
    peak = int(by_hour.loc[by_hour["accidentes"].idxmax(), "HORA"])
    fig_h = px.bar(
        by_hour, x="HORA", y="accidentes",
        color="accidentes", color_continuous_scale="Reds",
        labels={"HORA": "Hora", "accidentes": "Accidentes"},
    )
    fig_h.add_vline(x=peak, line_dash="dash", line_color="#E53935",
                    annotation_text=f"Pico: {peak}h")
    fig_h.update_layout(
        height=300, coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_h, use_container_width=True)

with col2:
    st.subheader("Accidentes por día de la semana")
    day_order = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    by_day_s  = by_day.set_index("dia_es").reindex(day_order).reset_index()
    fig_d = px.bar(
        by_day_s, x="dia_es", y="accidentes",
        color="accidentes", color_continuous_scale="Blues",
        labels={"dia_es": "Día", "accidentes": "Accidentes"},
    )
    fig_d.update_layout(
        height=300, coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_d, use_container_width=True)

# ── PROVINCIA Y TIPO ──────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    if not by_prov.empty:
        st.subheader("Top 15 provincias")
        fig_p = px.bar(
            by_prov.head(15).sort_values("accidentes"),
            x="accidentes", y="provincia", orientation="h",
            color="accidentes", color_continuous_scale="OrRd",
            labels={"provincia": "Provincia", "accidentes": "Accidentes"},
        )
        fig_p.update_layout(
            height=380, coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_p, use_container_width=True)

with col4:
    if not by_type.empty:
        st.subheader("Tipos de accidente")
        fig_t = px.pie(
            by_type.head(8), values="accidentes", names="TIPO_ACCIDENTE",
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_t.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_t, use_container_width=True)

# ── EVOLUCIÓN ANUAL ───────────────────────────────────────────────────────────
st.subheader("Evolución anual de accidentes")
monthly["anio"] = monthly["fecha"].dt.year
by_year = monthly.groupby("anio")["accidentes"].sum().reset_index()
fig_y = px.bar(
    by_year, x="anio", y="accidentes", text="accidentes",
    color="accidentes", color_continuous_scale="RdYlGn_r",
    labels={"anio": "Año", "accidentes": "Total accidentes"},
)
fig_y.update_traces(texttemplate="%{text:,}", textposition="outside")
fig_y.update_layout(
    height=340, coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=30),
)
st.plotly_chart(fig_y, use_container_width=True)
st.caption("2020 refleja el efecto COVID-19 (confinamiento mar–ago). 2024 solo incluye ene–abr.")
