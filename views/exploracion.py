import plotly.express as px
import streamlit as st
from utils import PLOT_CFG


def render(monthly, by_hour, by_day, by_prov, by_type):
    st.title("Exploración de Datos")
    st.markdown("**166,682 accidentes** · ANT Ecuador · Enero 2017 – Abril 2024")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        peak = int(by_hour.loc[by_hour["accidentes"].idxmax(), "HORA"])
        st.subheader(f"Por hora — pico: {peak}h")
        fh = px.bar(by_hour, x="HORA", y="accidentes",
                    color="accidentes", color_continuous_scale="Reds")
        fh.add_vline(x=peak, line_dash="dash", line_color="#ef4444")
        fh.update_layout(height=260, coloraxis_showscale=False, **PLOT_CFG)
        st.plotly_chart(fh, use_container_width=True)

    with c2:
        st.subheader("Por día de la semana")
        order = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        bds   = by_day.set_index("dia_es").reindex(order).reset_index()
        fd = px.bar(bds, x="dia_es", y="accidentes",
                    color="accidentes", color_continuous_scale="Blues")
        fd.update_layout(height=260, coloraxis_showscale=False, **PLOT_CFG)
        st.plotly_chart(fd, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Top 15 provincias")
        fp = px.bar(by_prov.head(15).sort_values("accidentes"),
                    x="accidentes", y="provincia", orientation="h",
                    color="accidentes", color_continuous_scale="OrRd")
        fp.update_layout(height=340, coloraxis_showscale=False, **PLOT_CFG)
        st.plotly_chart(fp, use_container_width=True)

    with c4:
        st.subheader("Tipo de accidente")
        ft = px.pie(by_type.head(8), values="accidentes", names="TIPO_ACCIDENTE",
                    hole=0.42, color_discrete_sequence=px.colors.qualitative.Set2)
        ft.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(ft, use_container_width=True)

    st.subheader("Evolución anual")
    monthly["anio"] = monthly["fecha"].dt.year
    by_year = monthly.groupby("anio")["accidentes"].sum().reset_index()
    fy = px.bar(by_year, x="anio", y="accidentes", text="accidentes",
                color="accidentes", color_continuous_scale="RdYlGn_r")
    fy.update_traces(texttemplate="%{text:,}", textposition="outside")
    fy.update_layout(height=280, coloraxis_showscale=False, **PLOT_CFG)
    st.plotly_chart(fy, use_container_width=True)
    st.caption("2020: confinamiento COVID-19  ·  2024: solo enero–abril")
