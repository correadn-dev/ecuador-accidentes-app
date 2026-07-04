import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import MODEL_COLORS, PLOT_CFG


def render(monthly, metrics, preds, forecast):
    st.title("Pronóstico Temporal")
    st.markdown("**88 meses** · Train: 76 · Test: 12 últimos meses")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["Serie", "Predicciones", "Métricas", "Futuro"])

    with tab1:
        train, test_ = monthly.iloc[:-12], monthly.iloc[-12:]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=train["fecha"], y=train["accidentes"],
                                 name="Entrenamiento", line=dict(color="#64748b", width=1.5)))
        fig.add_trace(go.Scatter(x=test_["fecha"], y=test_["accidentes"],
                                 name="Test", line=dict(color="#ef4444", width=2.5)))
        fig.add_vrect(x0=str(test_["fecha"].iloc[0])[:10],
                      x1=str(monthly["fecha"].iloc[-1])[:10],
                      fillcolor="rgba(59,130,246,0.06)", line_width=0)
        fig.add_vrect(x0="2020-03-01", x1="2020-09-01",
                      fillcolor="rgba(0,0,0,0.05)", line_width=0,
                      annotation_text="COVID-19", annotation_position="top left")
        fig.update_layout(height=380, hovermode="x unified",
                          legend=dict(orientation="h", y=-0.15), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)
        a, b, c = st.columns(3)
        a.metric("Media mensual", "1,893.8", help="Paper: 1,894.11 ✓")
        b.metric("Máximo", "2,676", help="Dic 2017")
        c.metric("Mínimo", "520",   help="Abr 2020 — COVID")

    with tab2:
        col_map = {"Random Forest": "RF", "XGBoost": "XGBoost",
                   "LSTM": "LSTM", "SARIMA": "SARIMA", "Prophet": "Prophet"}
        sel = st.multiselect("Modelos", list(MODEL_COLORS),
                             default=["Random Forest", "SARIMA", "Prophet"])
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=preds["fecha"], y=preds["real"],
                                  name="Real", line=dict(color="#1e293b", width=3)))
        for mdl in sel:
            col = col_map[mdl]
            if col in preds.columns:
                rmse = metrics.loc[metrics["Modelo"] == mdl, "RMSE"].values[0]
                fig2.add_trace(go.Scatter(
                    x=preds["fecha"], y=preds[col],
                    name=f"{mdl} ({rmse:.1f})",
                    line=dict(color=MODEL_COLORS[mdl], width=1.8, dash="dot"),
                ))
        fig2.update_layout(height=380, hovermode="x unified",
                           legend=dict(orientation="h", y=-0.2), **PLOT_CFG)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        ca, cb = st.columns(2)
        for ax, col_name, title in [(ca, "RMSE", "RMSE"), (cb, "MAE", "MAE")]:
            with ax:
                fig_ = px.bar(
                    metrics.sort_values(col_name), x=col_name, y="Modelo",
                    orientation="h", color="Tipo", text=col_name, title=title,
                    color_discrete_map={"ML": "#3b82f6", "DL": "#f59e0b", "Estadístico": "#a855f7"},
                )
                fig_.update_traces(texttemplate="%{text:.2f}", textposition="outside")
                fig_.update_layout(height=280, showlegend=False,
                                   margin=dict(l=0, r=40, t=30, b=0),
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_, use_container_width=True)
        st.dataframe(
            metrics.sort_values("RMSE").style.format({"RMSE": "{:.2f}", "MAE": "{:.2f}"}),
            hide_index=True, use_container_width=True,
        )
        st.info("**RF** 132.20 < LSTM-Direct paper 137.47  ·  "
                "**SARIMA** 157.59 ≈ paper 157.94 ✓  ·  "
                "**Prophet** 382 vs paper 175 — sin corrección outliers COVID")

    with tab4:
        forecast["mes"] = forecast["fecha"].dt.strftime("%b %Y")
        figf = px.bar(
            forecast, x="mes", y="accidentes", color="nivel", text="accidentes",
            color_discrete_map={"Medio": "#22c55e", "Alto": "#f59e0b", "Crítico": "#ef4444"},
        )
        figf.update_traces(textposition="outside")
        figf.update_layout(height=340, legend_title="Riesgo", **PLOT_CFG)
        st.plotly_chart(figf, use_container_width=True)
        st.error("**Enero 2025** — pico proyectado (~1,700 acc.).")
