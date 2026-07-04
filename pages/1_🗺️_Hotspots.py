import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Hotspots Espaciales", page_icon="🗺️", layout="wide")

@st.cache_data
def load():
    clusters = pd.read_csv("data/cluster_centroids.csv")
    top_cant = pd.read_csv("data/top_cantons.csv")
    return clusters, top_cant

clusters, top_cant = load()

st.title("🗺️ Hotspots Espaciales — DBSCAN")
st.markdown("**Parámetros:** ε = 750 m · MinPts = 10 · Métrica: Haversine · Dataset: 166,682 accidentes")
st.divider()

col_map, col_ctrl = st.columns([3, 1])

with col_ctrl:
    st.subheader("Filtros")
    top_n   = st.slider("Top N clusters", 10, 457, 150)
    min_acc = st.number_input("Mín. accidentes", 10, 2000, 30)
    st.divider()
    st.metric("Total clusters", 457)
    st.metric("Silhouette Score", "−0.059")
    st.metric("Davies-Bouldin", "0.481")
    st.metric("En clusters", "92.0%")
    st.metric("Ruido (aislados)", "8.0%")
    st.divider()
    st.subheader("Top 10")
    st.dataframe(
        clusters.head(10)[["rank", "accidentes"]].rename(columns={"rank": "Rank", "accidentes": "Accidentes"}),
        hide_index=True, use_container_width=True,
    )

with col_map:
    filtered = clusters[clusters["accidentes"] >= min_acc].head(top_n)
    m = folium.Map(location=[-1.8, -78.2], zoom_start=7, tiles="CartoDB positron")
    max_acc = filtered["accidentes"].max()

    for _, row in filtered.iterrows():
        ratio  = row["accidentes"] / max_acc
        radius = 4 + ratio * 14
        r = int(220 * ratio + 35)
        g = int(60 * (1 - ratio))
        color = f"#{r:02x}{g:02x}32"
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radius,
            color=color, fill=True, fill_color=color, fill_opacity=0.72,
            popup=folium.Popup(
                f"<b>Cluster #{int(row['rank'])}</b><br>"
                f"Accidentes: <b>{int(row['accidentes'])}</b><br>"
                f"Lat: {row['lat']:.4f} | Lon: {row['lon']:.4f}",
                max_width=220,
            ),
            tooltip=f"#{int(row['rank'])} — {int(row['accidentes'])} acc.",
        ).add_to(m)

    st_folium(m, height=520, use_container_width=True)

st.divider()
st.subheader("Top cantones por concentración en hotspots")
fig = px.bar(
    top_cant.head(15).sort_values("accidentes"),
    x="accidentes", y="canton", orientation="h",
    color="accidentes", color_continuous_scale="Reds",
    labels={"canton": "Cantón", "accidentes": "Accidentes"},
)
fig.update_layout(
    height=380, coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
)
st.plotly_chart(fig, use_container_width=True)
