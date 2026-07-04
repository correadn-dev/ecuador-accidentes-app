import streamlit as st
from utils import load_all
from views import resumen, hotspots, pronostico, exploracion

st.set_page_config(
    page_title="Ecuador Vial · Dashboard",
    page_icon=":material/traffic:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Bootstrap Icons (CDN) + estilos globales ──────────────────────────────────
st.markdown("""
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
/* sidebar fondo oscuro */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    padding: 2rem 1rem 1.5rem;
}
/* nav links */
.bi-nav a {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 8px;
    color: #94a3b8; text-decoration: none;
    font-size: 14px; font-weight: 500;
    transition: background 0.15s, color 0.15s;
    margin-bottom: 3px;
}
.bi-nav a:hover  { background: rgba(255,255,255,0.07); color: #e2e8f0; }
.bi-nav a.active { background: #1d4ed8; color: #ffffff !important; }
.bi-nav i { font-size: 16px; min-width: 18px; }
/* metric cards */
[data-testid="stMetric"] {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 14px 18px;
}
[data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: 700; }
[data-testid="stMetricLabel"] { font-size: 0.76rem !important; color: #64748b; }
.block-container { padding-top: 2rem; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span { color: #64748b !important; }
section[data-testid="stSidebar"] h3   { color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

# ── datos ─────────────────────────────────────────────────────────────────────
(summary, monthly, metrics, preds, forecast,
 by_hour, by_day, clusters, by_prov, by_type, top_cant) = load_all()

# ── navegación via query params ───────────────────────────────────────────────
PAGES = {
    "resumen":    ("bar-chart-fill",  "Resumen"),
    "hotspots":   ("geo-alt-fill",    "Hotspots"),
    "pronostico": ("graph-up-arrow",  "Pronóstico"),
    "exploracion":("search",          "Exploración"),
}

page = st.query_params.get("page", "resumen")
if page not in PAGES:
    page = "resumen"

with st.sidebar:
    st.markdown('<h3 style="color:#f1f5f9"><i class="bi bi-car-front-fill" style="color:#3b82f6"></i> Ecuador Vial</h3>', unsafe_allow_html=True)
    st.caption("Análisis Espaciotemporal · ANT 2017–2024")
    st.markdown("<br>", unsafe_allow_html=True)

    links = ""
    for key, (icon, label) in PAGES.items():
        active = "active" if key == page else ""
        links += (
            f'<a href="?page={key}" class="{active}">'
            f'<i class="bi bi-{icon}"></i>{label}</a>'
        )
    st.markdown(f'<div class="bi-nav">{links}</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("UDLA · ISWZ3402 AI-II")
    st.caption("González et al., *Urban Science* 2026")

# ── render página activa ──────────────────────────────────────────────────────
if page == "resumen":
    resumen.render(monthly, metrics, forecast)
elif page == "hotspots":
    hotspots.render(clusters, top_cant)
elif page == "pronostico":
    pronostico.render(monthly, metrics, preds, forecast)
elif page == "exploracion":
    exploracion.render(monthly, by_hour, by_day, by_prov, by_type)
