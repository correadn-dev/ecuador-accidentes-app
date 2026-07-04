import folium
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
from utils import PLOT_CFG


def render(clusters, top_cant):
    st.title("Hotspots Espaciales — DBSCAN")
    st.markdown("**ε = 750 m · MinPts = 10 · Métrica: Haversine**")
    st.divider()

    col_ctrl, col_map = st.columns([1, 3])

    with col_ctrl:
        top_n   = st.slider("Top N clusters", 10, 457, 150)
        min_acc = st.number_input("Mín. accidentes", 10, 2000, 30)
        st.divider()
        for label, val in [("Clusters", "457"), ("Silhouette", "−0.059"),
                            ("Davies-Bouldin", "0.481"), ("En clusters", "92.0 %")]:
            st.metric(label, val)

    with col_map:
        filt = clusters[clusters["accidentes"] >= min_acc].head(top_n)
        m = folium.Map(location=[-1.8, -78.2], zoom_start=7, tiles="CartoDB positron")
        mx = filt["accidentes"].max()
        for _, r in filt.iterrows():
            ratio = r["accidentes"] / mx
            red   = int(220 * ratio + 35)
            grn   = int(60 * (1 - ratio))
            color = f"#{red:02x}{grn:02x}32"
            folium.CircleMarker(
                [r["lat"], r["lon"]], radius=4 + ratio * 14,
                color=color, fill=True, fill_color=color, fill_opacity=0.72,
                popup=folium.Popup(
                    f"<b>Cluster #{int(r['rank'])}</b><br>"
                    f"Accidentes: <b>{int(r['accidentes'])}</b>", max_width=180),
                tooltip=f"#{int(r['rank'])} — {int(r['accidentes'])} acc.",
            ).add_to(m)
        st_folium(m, height=500, use_container_width=True)

    st.subheader("Top 10 hotspots — zonas de mayor riesgo")
    top10_cols = ["rank", "canton", "accidentes", "fallecidos"]
    top10 = clusters.head(10)[top10_cols].rename(columns={
        "rank": "#", "canton": "Cantón",
        "accidentes": "Accidentes", "fallecidos": "Fallecidos",
    })
    st.dataframe(
        top10,
        hide_index=True,
        use_container_width=True,
        column_config={
            "#":           st.column_config.NumberColumn(width="small"),
            "Cantón":      st.column_config.TextColumn(width="medium"),
            "Accidentes":  st.column_config.NumberColumn(format="%d", width="medium"),
            "Fallecidos":  st.column_config.NumberColumn(format="%d", width="medium"),
        },
    )
    st.divider()
    st.subheader("Top cantones en hotspots")
    fig = px.bar(
        top_cant.head(15).sort_values("accidentes"),
        x="accidentes", y="canton", orientation="h",
        color="accidentes", color_continuous_scale="Reds",
    )
    fig.update_layout(height=340, coloraxis_showscale=False, **PLOT_CFG)
    st.plotly_chart(fig, use_container_width=True)
