import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import PLOT_CFG


def render(monthly, metrics, forecast):
    st.title("Accidentes de Tránsito — Ecuador")
    st.markdown("Reproducción de **González-Rodríguez et al. (2026)** · *Urban Science 10(5), 280*")
    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total accidentes", "166,682")
    c2.metric("Período", "Ene 2017 – Abr 2024")
    c3.metric("Hotspots DBSCAN", "457")
    c4.metric("Cobertura", "92.0 %")
    c5.metric("Mejor modelo", "RF · RMSE 132.2")
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.subheader("Accidentes mensuales")
        fig = go.Figure(go.Scatter(
            x=monthly["fecha"], y=monthly["accidentes"],
            fill="tozeroy", line=dict(color="#ef4444", width=2), name="Acc/mes",
        ))
        fig.add_vrect(x0="2020-03-01", x1="2020-09-01",
                      fillcolor="rgba(0,0,0,0.06)", line_width=0,
                      annotation_text="COVID-19", annotation_position="top left")
        fig.update_layout(height=290, hovermode="x unified",
                          showlegend=False, **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("RMSE por modelo")
        fig2 = px.bar(
            metrics.sort_values("RMSE"), x="RMSE", y="Modelo",
            orientation="h", color="Tipo", text="RMSE",
            color_discrete_map={"ML":"#3b82f6","DL":"#f59e0b","Estadístico":"#a855f7"},
        )
        fig2.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig2.update_layout(height=290, showlegend=False,
                           margin=dict(l=0, r=40, t=10, b=0),
                           plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Pronóstico mayo 2024 – abril 2025")
    forecast["mes"] = forecast["fecha"].dt.strftime("%b %Y")
    fig3 = px.bar(forecast, x="mes", y="accidentes", color="nivel", text="accidentes",
                  color_discrete_map={"Medio":"#22c55e","Alto":"#f59e0b","Crítico":"#ef4444"})
    fig3.update_traces(textposition="outside")
    fig3.update_layout(height=260, legend_title="Riesgo", **PLOT_CFG)
    st.plotly_chart(fig3, use_container_width=True)
    st.error("**Enero 2025 — mayor riesgo proyectado (~1,700 acc.).**  "
             "Reforzar operativos en los 457 hotspots identificados.")
