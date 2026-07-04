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
/* radio → nav items */
section[data-testid="stSidebar"] .stRadio > label { display: none; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    display: flex; flex-direction: column; gap: 3px;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    padding: 10px 14px; border-radius: 8px;
    color: #94a3b8 !important; font-size: 14px; font-weight: 500;
    cursor: pointer; transition: background 0.15s;
    display: flex; align-items: center;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.07); color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked) {
    background: #1d4ed8 !important; color: #ffffff !important;
}
/* hide radio circle */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:first-child { display: none; }
/* Bootstrap Icons before each label text */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(1) > div:last-child::before { font-family:"bootstrap-icons"; content:"\f1b2"; margin-right:8px; font-style:normal; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(2) > div:last-child::before { font-family:"bootstrap-icons"; content:"\f3e0"; margin-right:8px; font-style:normal; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(3) > div:last-child::before { font-family:"bootstrap-icons"; content:"\f504"; margin-right:8px; font-style:normal; }
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:nth-child(4) > div:last-child::before { font-family:"bootstrap-icons"; content:"\f52a"; margin-right:8px; font-style:normal; }
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

# ── navegación via session_state (sin reload completo) ────────────────────────
NAV_LABELS = ["Resumen", "Hotspots", "Pronóstico", "Exploración"]
NAV_KEYS   = ["resumen", "hotspots", "pronostico", "exploracion"]

if "page" not in st.session_state:
    st.session_state.page = "resumen"

with st.sidebar:
    st.markdown('<h3 style="color:#f1f5f9"><i class="bi bi-car-front-fill" style="color:#3b82f6"></i> Ecuador Vial</h3>', unsafe_allow_html=True)
    st.caption("Análisis Espaciotemporal · ANT 2017–2024")
    st.markdown("<br>", unsafe_allow_html=True)

    sel_label = st.radio(
        "nav", NAV_LABELS,
        index=NAV_KEYS.index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = NAV_KEYS[NAV_LABELS.index(sel_label)]

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("UDLA · ISWZ3402 AI-II")
    st.caption("González et al., *Urban Science* 2026")

page = st.session_state.page

# ── render página activa ──────────────────────────────────────────────────────
if page == "resumen":
    resumen.render(monthly, metrics, forecast)
elif page == "hotspots":
    hotspots.render(clusters, top_cant)
elif page == "pronostico":
    pronostico.render(monthly, metrics, preds, forecast)
elif page == "exploracion":
    exploracion.render(monthly, by_hour, by_day, by_prov, by_type)
