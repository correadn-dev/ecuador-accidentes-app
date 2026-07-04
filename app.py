import streamlit as st
import streamlit.components.v1 as components
from utils import load_all
from views import resumen, hotspots, pronostico, exploracion

st.set_page_config(
    page_title="Ecuador Vial · Dashboard",
    page_icon=":material/traffic:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
section[data-testid="stSidebar"] {
    width: 200px !important;
    min-width: 200px !important;
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
}
section[data-testid="stSidebar"] > div {
    background: transparent !important;
    width: 200px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem;
}
/* Toggle button CSS fallback */
[data-testid="stSidebarCollapseButton"] {
    background: rgba(255,255,255,0.18) !important;
    background-color: rgba(255,255,255,0.18) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}
[data-testid="stSidebarCollapseButton"] button {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stSidebarCollapseButton"] svg,
button[kind="headerNoPadding"] svg {
    fill: #ffffff !important;
}
/* nav buttons */
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
    box-shadow: none !important; outline: none !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #1d4ed8 !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #2563eb !important;
}
section[data-testid="stSidebar"] .stButton button [data-testid="stIconMaterial"] {
    font-size: 18px !important;
}
[data-testid="stMetric"] {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 14px 18px;
}
[data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: 700; }
[data-testid="stMetricLabel"] { font-size: 0.76rem !important; color: #64748b; }
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── datos ──────────────────────────────────────────────────────────────────────
(summary, monthly, metrics, preds, forecast,
 by_hour, by_day, clusters, by_prov, by_type, top_cant) = load_all()

NAV_ITEMS = [
    ("resumen",     ":material/bar_chart:",   "Resumen"),
    ("hotspots",    ":material/location_on:", "Hotspots"),
    ("pronostico",  ":material/show_chart:",  "Pronostico"),
    ("exploracion", ":material/search:",      "Exploracion"),
]

if "page" not in st.session_state:
    st.session_state.page = "resumen"

with st.sidebar:
    st.markdown(
        '<h3 style="color:#f1f5f9;margin-bottom:2px">'
        '<i class="bi bi-car-front-fill" style="color:#3b82f6"></i>'
        ' Ecuador Vial</h3>'
        '<p style="color:#64748b;font-size:11px;margin:0 0 12px 0">'
        'Análisis Espaciotemporal · ANT 2017–2024</p>',
        unsafe_allow_html=True,
    )

    for key, icon, label in NAV_ITEMS:
        active = st.session_state.page == key
        if st.button(
            label, icon=icon,
            key="nav_" + key,
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = key
            st.rerun()

    st.markdown(
        '<div style="margin-top:16px;border-top:1px solid #1e3a5f;padding-top:12px">'
        '<p style="color:#64748b;font-size:11px;margin:0">UDLA · ISWZ3402 AI-II</p>'
        '<p style="color:#64748b;font-size:11px;margin:4px 0 0 0">'
        'González et al., <em>Urban Science</em> 2026</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Inyecta <style> directo en el head del documento padre
    components.html("""
<script>
(function() {
  var CSS = [
    '[data-testid="stSidebarCollapseButton"] {',
    '  background: rgba(255,255,255,0.18) !important;',
    '  background-color: rgba(255,255,255,0.18) !important;',
    '  border-radius: 8px !important;',
    '  border: 1px solid rgba(255,255,255,0.3) !important;',
    '}',
    '[data-testid="stSidebarCollapseButton"] button,',
    'button[kind="headerNoPadding"],',
    'button[data-testid="stBaseButton-headerNoPadding"] {',
    '  background: transparent !important;',
    '  background-color: transparent !important;',
    '  border: none !important;',
    '  box-shadow: none !important;',
    '  outline: none !important;',
    '}',
    '[data-testid="stSidebarCollapseButton"] svg,',
    'button[kind="headerNoPadding"] svg,',
    'button[data-testid="stBaseButton-headerNoPadding"] svg {',
    '  fill: #ffffff !important;',
    '}'
  ].join('\\n');

  function inject() {
    try {
      var doc = window.parent.document;
      var el = doc.getElementById('_ec_sidebar_fix');
      if (!el) {
        el = doc.createElement('style');
        el.id = '_ec_sidebar_fix';
        doc.head.appendChild(el);
      }
      el.textContent = CSS;
    } catch(e) {}
  }

  inject();
  setTimeout(inject, 300);
  setTimeout(inject, 1000);
  try {
    new MutationObserver(inject).observe(
      window.parent.document.head, {childList: true}
    );
  } catch(e) {}
})();
</script>
""", height=0)

page = st.session_state.page

if page == "resumen":
    resumen.render(monthly, metrics, forecast)
elif page == "hotspots":
    hotspots.render(clusters, top_cant)
elif page == "pronostico":
    pronostico.render(monthly, metrics, preds, forecast)
elif page == "exploracion":
    exploracion.render(monthly, by_hour, by_day, by_prov, by_type)
