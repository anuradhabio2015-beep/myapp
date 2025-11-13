import streamlit as st

# -------------------------------------------------------
# REMOVE STREAMLIT DEFAULT HEADER/FOOTER
# -------------------------------------------------------
hide_default = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 80px;}
    </style>
"""
st.markdown(hide_default, unsafe_allow_html=True)


# -------------------------------------------------------
# SESSION STATE FOR ACTIVE PAGE
# -------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "dashboard"


# -------------------------------------------------------
# BUILD CUSTOM HEADER (PURE STREAMLIT, NO JAVASCRIPT)
# -------------------------------------------------------
st.markdown(
    """
    <style>
    .top-bar {
        background-color: #2c6bed;
        height: 60px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
        padding-left: 20px;
        padding-right: 20px;
        display: flex;
        align-items: center;
    }
    .app-title {
        color: white;
        font-size: 22px;
        font-weight: 700;
    }
    .nav-btn {
        background-color: rgba(255,255,255,0.15);
        color: white;
        padding: 6px 14px;
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.3);
        cursor: pointer;
        font-size: 15px;
    }
    .nav-btn-selected {
        background-color: white !important;
        color: #2c6bed !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# RENDER HEADER
header_col1, header_col2 = st.columns([1, 2])
with header_col1:
    st.markdown('<div class="top-bar"><span class="app-title">MES Application</span></div>',
                unsafe_allow_html=True)

with header_col2:
    st.write("")  # spacing
    st.write("")  # spacing

    nav1, nav2, nav3 = st.columns(3)

    with nav1:
        if st.button("Dashboard", key="btn_dash",
                     use_container_width=True,
                     help="Dashboard",
                     type="secondary" if st.session_state.active_page != "dashboard" else "primary"):
            st.session_state.active_page = "dashboard"

    with nav2:
        if st.button("Reports", key="btn_reports",
                     use_container_width=True,
                     help="Reports",
                     type="secondary" if st.session_state.active_page != "reports" else "primary"):
            st.session_state.active_page = "reports"

    with nav3:
        if st.button("Settings", key="btn_settings",
                     use_container_width=True,
                     help="Settings",
                     type="secondary" if st.session_state.active_page != "settings" else "primary"):
            st.session_state.active_page = "settings"


# -------------------------------------------------------
# PAGE CONTENT
# -------------------------------------------------------
if st.session_state.active_page == "dashboard":
    st.header("📊 Dashboard")
    tab1, tab2 = st.tabs(["Production", "Quality"])
    tab1.write("Production KPIs…")
    tab2.write("Quality KPIs…")

elif st.session_state.active_page == "reports":
    st.header("📁 Reports")
    st.write("Report listing…")

elif st.session_state.active_page == "settings":
    st.header("⚙️ Settings")
    st.write("System configuration…")
