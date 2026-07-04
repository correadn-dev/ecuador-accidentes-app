import streamlit as st
import json

st.set_page_config(
    page_title="Accidentes de Tránsito Ecuador",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_summary():
    return json.loads(open("data/summary.json", encoding="utf-8").read())

summary = load_summary()

st.title("🚦 Análisis Espaciotemporal de Accidentes de Tránsito — Ecuador")
st.markdown("**Reproducción de:** González-Rodríguez et al. (2026) — *Urban Science, 10(5), 280*  \n"
            "Universidad de las Américas | Proyecto Final AI-II (ISWZ3402)")
st.divider()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total accidentes", f"{summary['total_accidentes']:,}", help="Ene 2017 – Abr 2024")
k2.metric("Período", summary["periodo"])
k3.metric("Hotspots DBSCAN", str(summary["n_clusters"]), help="ε=750m, MinPts=10")
k4.metric("Cobertura hotspots", f"{summary['pct_en_clusters']}%")
k5.metric("Mejor modelo (RMSE)", f"{summary['best_rmse']} — {summary['best_model']}")

st.divider()
st.markdown("""
### Navegación
Usa el menú lateral para explorar cada sección del análisis:

| Página | Contenido |
|--------|-----------|
| 🗺️ **Hotspots Espaciales** | Mapa interactivo de los 457 clusters DBSCAN en Ecuador |
| 📈 **Pronóstico Temporal** | Comparativa de 5 modelos + proyección de accidentes futuros |
| 🔍 **Exploración de Datos** | Análisis por hora, día, provincia y tipo de accidente |

### Metodología
- **Parte 1 — Espacial:** DBSCAN con métrica Haversine (ε=750m, MinPts=10) sobre 166,682 registros de la ANT
- **Parte 2 — Temporal:** SARIMA · Prophet · Random Forest · XGBoost · LSTM sobre serie de 88 meses (2017–2024)
""")

st.info("📄 Análisis completo disponible en el notebook del proyecto (ISWZ3402).")
