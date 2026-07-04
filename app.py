import json
from pathlib import Path

import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Accidentes Ecuador",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── minimal CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 1.4rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; }
.block-container { padding-top: 1.5rem; }
section[data-testid="stSidebar"] { background-color: #1a1f2e; }
section[data-testid="stSidebar"] * { color: #e8ecf4 !important; }
</style>
""", unsafe_allow_html=True)

# ── data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    d = Path("data")
    summary  = json.loads((d / "summary.json").read_text(encoding="utf-8"))
    monthly  = pd.read_csv(d / "monthly_series.csv",    parse_dates=["fecha"])
    metrics  = pd.read_csv(d / "model_metrics.csv")
    preds    = pd.read_csv(d / "model_predictions.csv", parse_dates=["fecha"])
    forecast = pd.read_csv(d / "forecast.csv",          parse_dates=["fecha"])
    by_hour  = pd.read_csv(d / "by_hour.csv")
    by_day   = pd.read_csv(d / "by_day.csv")
    clusters = pd.read_csv(d / "cluster_centroids.csv")
    by_prov  = pd.read_csv(d / "by_province.csv")
    by_type  = pd.read_csv(d / "by_type.csv")
    top_cant = pd.read_csv(d / "top_cantons.csv")
    return summary, monthly, metrics, preds, forecast, by_hour, by_day, clusters, by_prov, by_type, top_cant

summary, monthly, metrics, preds, forecast, by_hour, by_day, clusters, by_prov, by_type, top_cant = load_all()

MODEL_COLORS = {
    "Random Forest": "#2196F3",
    "XGBoost":       "#4CAF50",
    "LSTM":          "#FF9800",
    "SARIMA":        "#9C27B0",
    "Prophet":       "#F44336",
}

# ── sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🚦 Ecuador Vial")
    st.caption("Análisis Espaciotemporal · ANT 2017–2024")
    st.divider()
    page = option_menu(
        menu_title=None,
        options=["Resumen", "Hotspots", "Pronóstico", "Exploración"],
        icons=["bar-chart-fill", "geo-alt-fill", "graph-up-arrow", "search"],
        default_index=0,
        styles={
            "container":       {"background-color": "transparent", "padding": "0"},
            "icon":            {"color": "#7eb3ff", "font-size": "15px"},
            "nav-link":        {"font-size": "14px", "color": "#cdd8f0",
                                "border-radius": "8px", "margin": "2px 0"},
            "nav-link-selected": {"background-color": "#2d3a5c", "color": "#ffffff",
                                  "font-weight": "600"},
        },
    )
    st.divider()
    st.caption("UDLA · ISWZ3402 AI-II  \nGonzález et al., *Urban Science* 2026")


# ══════════════════════════════════════════════════════════════════════════════
# RESUMEN
# ══════════════════════════════════════════════════════════════════════════════
if page == "Resumen":
    st.title("Análisis Espaciotemporal de Accidentes de Tránsito")
    st.markdown("Reproducción de **González-Rodríguez et al. (2026)** — *Urban Science 10(5), 280*")
    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total accidentes", "166,682")
    c2.metric("Período", "Ene 2017 – Abr 2024")
    c3.metric("Hotspots DBSCAN", "457 zonas")
    c4.metric("Cobertura", "92.0 % del dataset")
    c5.metric("Mejor modelo", "RF · RMSE 132.2")
    st.divider()

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.subheader("Accidentes mensuales 2017–2024")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["fecha"], y=monthly["accidentes"],
            fill="tozeroy", line=dict(color="#E53935", width=2),
            name="Accidentes/mes",
        ))
        fig.add_vrect(x0="2020-03-01", x1="2020-09-01",
                      fillcolor="rgba(0,0,0,0.07)", line_width=0,
                      annotation_text="COVID-19", annotation_position="top left")
        fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0),
                          hovermode="x unified",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("RMSE por modelo")
        fig2 = px.bar(
            metrics.sort_values("RMSE"), x="RMSE", y="Modelo", orientation="h",
            color="Tipo", text="RMSE",
            color_discrete_map={"ML":"#2196F3","DL":"#FF9800","Estadístico":"#9C27B0"},
        )
        fig2.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig2.update_layout(height=300, margin=dict(l=0,r=30,t=0,b=0),
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Pronóstico mayo 2024 – abril 2025 (Random Forest)")
    forecast["mes"] = forecast["fecha"].dt.strftime("%b %Y")
    fig3 = px.bar(forecast, x="mes", y="accidentes", color="nivel", text="accidentes",
                  color_discrete_map={"Medio":"#4CAF50","Alto":"#FF9800","Crítico":"#E53935"})
    fig3.update_traces(textposition="outside")
    fig3.update_layout(height=270, margin=dict(l=0,r=0,t=0,b=0),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                       legend_title="Riesgo")
    st.plotly_chart(fig3, use_container_width=True)
    st.error("**Enero 2025 — mayor riesgo proyectado (~1,700 accidentes).** "
             "Se recomienda reforzar operativos en los 457 hotspots identificados.")


# ══════════════════════════════════════════════════════════════════════════════
# HOTSPOTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Hotspots":
    st.title("Hotspots Espaciales — DBSCAN")
    st.markdown("**ε = 750 m · MinPts = 10 · Métrica: Haversine** sobre 166,682 registros ANT")
    st.divider()

    col_ctrl, col_map = st.columns([1, 3])
    with col_ctrl:
        top_n   = st.slider("Top N clusters", 10, 457, 150)
        min_acc = st.number_input("Mín. accidentes", 10, 2000, 30)
        st.divider()
        st.metric("Clusters totales", "457")
        st.metric("Silhouette Score", "−0.059")
        st.metric("Davies-Bouldin", "0.481")
        st.metric("En clusters", "92.0 %")
        st.divider()
        st.caption("**Top 10 hotspots**")
        st.dataframe(
            clusters.head(10)[["rank","accidentes"]].rename(
                columns={"rank":"#","accidentes":"Accidentes"}),
            hide_index=True, use_container_width=True,
        )

    with col_map:
        filt = clusters[clusters["accidentes"] >= min_acc].head(top_n)
        m = folium.Map(location=[-1.8, -78.2], zoom_start=7, tiles="CartoDB positron")
        mx = filt["accidentes"].max()
        for _, r in filt.iterrows():
            ratio  = r["accidentes"] / mx
            radius = 4 + ratio * 14
            red    = int(220 * ratio + 35)
            grn    = int(60 * (1 - ratio))
            col    = f"#{red:02x}{grn:02x}32"
            folium.CircleMarker(
                [r["lat"], r["lon"]], radius=radius,
                color=col, fill=True, fill_color=col, fill_opacity=0.72,
                popup=folium.Popup(
                    f"<b>Cluster #{int(r['rank'])}</b><br>"
                    f"Accidentes: <b>{int(r['accidentes'])}</b><br>"
                    f"{r['lat']:.4f}, {r['lon']:.4f}", max_width=200),
                tooltip=f"#{int(r['rank'])} — {int(r['accidentes'])} acc.",
            ).add_to(m)
        st_folium(m, height=500, use_container_width=True)

    st.divider()
    st.subheader("Top cantones por concentración en hotspots")
    fig_c = px.bar(top_cant.head(15).sort_values("accidentes"),
                   x="accidentes", y="canton", orientation="h",
                   color="accidentes", color_continuous_scale="Reds",
                   labels={"canton":"Cantón","accidentes":"Accidentes"})
    fig_c.update_layout(height=360, coloraxis_showscale=False,
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_c, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PRONÓSTICO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Pronóstico":
    st.title("Pronóstico Temporal")
    st.markdown("**88 meses** (Ene 2017 – Abr 2024) · Train: 76 meses · Test: últimos 12 meses")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["Serie", "Predicciones vs Real", "Métricas", "Pronóstico futuro"])

    with tab1:
        train = monthly.iloc[:-12]
        test_ = monthly.iloc[-12:]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=train["fecha"], y=train["accidentes"],
                                 name="Entrenamiento", line=dict(color="#546E7A", width=1.5)))
        fig.add_trace(go.Scatter(x=test_["fecha"], y=test_["accidentes"],
                                 name="Test (real)", line=dict(color="#E53935", width=2.5)))
        fig.add_vrect(x0=str(test_["fecha"].iloc[0])[:10],
                      x1=str(monthly["fecha"].iloc[-1])[:10],
                      fillcolor="rgba(33,150,243,0.07)", line_width=0)
        fig.add_vrect(x0="2020-03-01", x1="2020-09-01",
                      fillcolor="rgba(0,0,0,0.06)", line_width=0,
                      annotation_text="COVID-19", annotation_position="top left")
        fig.update_layout(height=400, hovermode="x unified",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=0,r=0,t=0,b=0),
                          legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)
        a, b, c = st.columns(3)
        a.metric("Media mensual",     "1,893.8", help="Paper: 1,894.11 ✓")
        b.metric("Máximo histórico",  "2,676",   help="Dic 2017")
        c.metric("Mínimo histórico",  "520",     help="Abr 2020 — COVID")

    with tab2:
        sel = st.multiselect("Modelos", list(MODEL_COLORS),
                             default=["Random Forest","SARIMA","Prophet"])
        col_map = {"Random Forest":"RF","XGBoost":"XGBoost",
                   "LSTM":"LSTM","SARIMA":"SARIMA","Prophet":"Prophet"}
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=preds["fecha"], y=preds["real"],
                                  name="Real", line=dict(color="#37474F", width=3)))
        for mdl in sel:
            col = col_map[mdl]
            if col in preds.columns:
                rmse = metrics.loc[metrics["Modelo"]==mdl,"RMSE"].values[0]
                fig2.add_trace(go.Scatter(x=preds["fecha"], y=preds[col],
                                          name=f"{mdl} (RMSE={rmse:.1f})",
                                          line=dict(color=MODEL_COLORS[mdl], width=1.8, dash="dot")))
        fig2.update_layout(height=400, hovermode="x unified",
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           margin=dict(l=0,r=0,t=0,b=0),
                           legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        ca, cb = st.columns(2)
        for ax, col_name, title in [(ca,"RMSE","RMSE — menor es mejor"),
                                     (cb,"MAE", "MAE — menor es mejor")]:
            with ax:
                fig_ = px.bar(metrics.sort_values(col_name), x=col_name, y="Modelo",
                              orientation="h", color="Tipo", text=col_name, title=title,
                              color_discrete_map={"ML":"#2196F3","DL":"#FF9800","Estadístico":"#9C27B0"})
                fig_.update_traces(texttemplate="%{text:.2f}", textposition="outside")
                fig_.update_layout(height=300, plot_bgcolor="rgba(0,0,0,0)",
                                   paper_bgcolor="rgba(0,0,0,0)",
                                   margin=dict(l=0,r=30,t=40,b=0))
                st.plotly_chart(fig_, use_container_width=True)
        st.dataframe(metrics.sort_values("RMSE")
                     .style.format({"RMSE":"{:.2f}","MAE":"{:.2f}"}),
                     hide_index=True, use_container_width=True)
        st.caption("**RF** RMSE=132.20 supera LSTM-Direct del paper (137.47)  |  "
                   "**SARIMA** 157.59 ≈ paper 157.94 ✓  |  "
                   "**Prophet** 382 vs paper 175 — falta corrección outliers COVID")

    with tab4:
        forecast["mes"] = forecast["fecha"].dt.strftime("%b %Y")
        figf = px.bar(forecast, x="mes", y="accidentes", color="nivel", text="accidentes",
                      color_discrete_map={"Medio":"#4CAF50","Alto":"#FF9800","Crítico":"#E53935"},
                      labels={"mes":"Mes","accidentes":"Accidentes proyectados","nivel":"Riesgo"})
        figf.update_traces(textposition="outside")
        figf.update_layout(height=360, plot_bgcolor="rgba(0,0,0,0)",
                           paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(figf, use_container_width=True)
        st.error("**Enero 2025** — pico proyectado (~1,700 acc.). "
                 "Reforzar operativos en los 457 hotspots identificados.")


# ══════════════════════════════════════════════════════════════════════════════
# EXPLORACIÓN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Exploración":
    st.title("Exploración de Datos")
    st.markdown("**166,682 accidentes** · ANT Ecuador · Enero 2017 – Abril 2024")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Por hora del día")
        peak = int(by_hour.loc[by_hour["accidentes"].idxmax(), "HORA"])
        fh = px.bar(by_hour, x="HORA", y="accidentes",
                    color="accidentes", color_continuous_scale="Reds",
                    labels={"HORA":"Hora","accidentes":"Accidentes"})
        fh.add_vline(x=peak, line_dash="dash", line_color="#E53935",
                     annotation_text=f"Pico: {peak}h")
        fh.update_layout(height=280, coloraxis_showscale=False,
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fh, use_container_width=True)

    with c2:
        st.subheader("Por día de la semana")
        order = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        bds   = by_day.set_index("dia_es").reindex(order).reset_index()
        fd = px.bar(bds, x="dia_es", y="accidentes",
                    color="accidentes", color_continuous_scale="Blues",
                    labels={"dia_es":"Día","accidentes":"Accidentes"})
        fd.update_layout(height=280, coloraxis_showscale=False,
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fd, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Top 15 provincias")
        fp = px.bar(by_prov.head(15).sort_values("accidentes"),
                    x="accidentes", y="provincia", orientation="h",
                    color="accidentes", color_continuous_scale="OrRd",
                    labels={"provincia":"Provincia","accidentes":"Accidentes"})
        fp.update_layout(height=360, coloraxis_showscale=False,
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fp, use_container_width=True)

    with c4:
        st.subheader("Tipo de accidente")
        ft = px.pie(by_type.head(8), values="accidentes", names="TIPO_ACCIDENTE",
                    hole=0.42, color_discrete_sequence=px.colors.qualitative.Set2)
        ft.update_layout(height=360, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(ft, use_container_width=True)

    st.subheader("Evolución anual")
    monthly["anio"] = monthly["fecha"].dt.year
    by_year = monthly.groupby("anio")["accidentes"].sum().reset_index()
    fy = px.bar(by_year, x="anio", y="accidentes", text="accidentes",
                color="accidentes", color_continuous_scale="RdYlGn_r",
                labels={"anio":"Año","accidentes":"Total accidentes"})
    fy.update_traces(texttemplate="%{text:,}", textposition="outside")
    fy.update_layout(height=300, coloraxis_showscale=False,
                     plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                     margin=dict(l=0,r=0,t=0,b=30))
    st.plotly_chart(fy, use_container_width=True)
    st.caption("2020: efecto COVID-19 · 2024: solo enero–abril")
