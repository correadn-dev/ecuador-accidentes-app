import streamlit as st
from utils import load_all
from views import resumen, hotspots, pronostico, exploracion

st.set_page_config(
    page_title="Ecuador Vial · Dashboard",
    page_icon=":material/traffic:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Bootstrap Icons CDN + estilos ─────────────────────────────────────────────
st.markdown("""
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
/* sidebar oscuro */
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    padding: 1.5rem 1rem;
}
/* botones nav: base inactivo */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    transition: background 0.15s !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}
/* boton activo */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #1d4ed8 !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #2563eb !important;
    color: #ffffff !important;
}
/* Bootstrap Icons font cascade: PUA chars (icons) → bootstrap-icons, ASCII → system-ui */
section[data-testid="stSidebar"] .stButton button,
section[data-testid="stSidebar"] .stButton button p {
    font-family: "bootstrap-icons", system-ui, -apple-system, sans-serif !important;
}
/* metricas */
[data-testid="stMetric"] {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 14px 18px;
}
[data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: 700; }
[data-testid="stMetricLabel"] { font-size: 0.76rem !important; color: #64748b; }
.block-container { padding-top: 2rem; }
section[data-testid="stSidebar"] .stCaption { color: #475569 !important; }
section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# ── datos (cacheados) ──────────────────────────────────────────────────────────
(summary, monthly, metrics, preds, forecast,
 by_hour, by_day, clusters, by_prov, by_type, top_cant) = load_all()

# ── navegacion via session_state (sin reload de pagina) ───────────────────────
# \uF... = Bootstrap Icons PUA unicode (rendered via font-family cascade in CSS)
NAV_ITEMS = [
    ("resumen",     "  Resumen"),
    ("hotspots",    "  Hotspots"),
    ("pronostico",  "  Pronostico"),
    ("exploracion", "  Exploracion"),
]

if "page" not in st.session_state:
    st.session_state.page = "resumen"

with st.sidebar:
    st.markdown(
        '<h3><i class="bi bi-car-front-fill" style="color:#3b82f6"></i>'
        ' Ecuador Vial</h3>',
        unsafe_allow_html=True,
    )
    st.caption("Analisis Espaciotemporal - ANT 2017-2024")
    st.markdown("<br>", unsafe_allow_html=True)

    for key, label in NAV_ITEMS:
        active = st.session_state.page == key
        if st.button(
            label,
            key="nav_" + key,
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = key
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("UDLA - ISWZ3402 AI-II")
    st.caption("Gonzalez et al., Urban Science 2026")

page = st.session_state.page

# ── render pagina activa ───────────────────────────────────────────────────────
if page == "resumen":
    resumen.render(monthly, metrics, forecast)
elif page == "hotspots":
    hotspots.render(clusters, top_cant)
elif page == "pronostico":
    pronostico.render(monthly, metrics, preds, forecast)
elif page == "exploracion":
    exploracion.render(monthly, by_hour, by_day, by_prov, by_type)
