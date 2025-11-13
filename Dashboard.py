import streamlit as st

# ------------------------------------------------------
# OPTION A — TRUE TAB NAVIGATION (NO URL ROUTING)
# Clean, stable, modern MES UI using Streamlit Tabs
# ------------------------------------------------------

st.set_page_config(page_title="MES Hybrid Tabs UI", page_icon=":factory:", layout="wide")

# ------------------------------------------------------
# HIDE STREAMLIT DEFAULT CHROME
# ------------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# CUSTOM CLEAN HEADER
# ------------------------------------------------------
st.markdown(
    """
    <style>
        .app-header {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 78px;
            background: white;
            display: flex;
            align-items: center;
            padding: 12px 26px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
            z-index: 9999;
        }
        .app-header-title {
            font-size: 24px;
            font-weight: 800;
            margin-left: 12px;
        }
        .block-container {
            padding-top: 120px !important;
        }
    </style>
    <div class="app-header">
        <img src="https://placehold.co/60x60?text=Logo" style="border-radius:10px" />
        <div class="app-header-title">MES Hybrid System — TAB Mode</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# TOP‑LEVEL TABS (Dashboard | Reports | Settings)
# ------------------------------------------------------
main_tabs = st.tabs(["Dashboard", "Reports", "Settings"])

# ------------------------------------------------------
# DASHBOARD PAGE
# ------------------------------------------------------
with main_tabs[0]:
    st.subheader("Dashboard Section")

    sub_tabs = st.tabs(["Overview", "Stations"])

    with sub_tabs[0]:
        st.header("Overview")
        st.write("Summary KPIs, throughput, OEE, etc.")

    with sub_tabs[1]:
        st.header("Stations")
        st.write("Station list, status, alarms, cycle times.")

# ------------------------------------------------------
# REPORTS PAGE
# ------------------------------------------------------
with main_tabs[1]:
    st.subheader("Reports Section")

    sub_tabs = st.tabs(["Daily", "Monthly"])

    with sub_tabs[0]:
        st.header("Daily Reports")
        st.write("Daily production, shift summary.")

    with sub_tabs[1]:
        st.header("Monthly Reports")
        st.write("Monthly trends, paretos, scrap analysis.")

# ------------------------------------------------------
# SETTINGS PAGE
# ------------------------------------------------------
with main_tabs[2]:
    st.subheader("Settings Section")

    sub_tabs = st.tabs(["Users", "System Config"])

    with sub_tabs[0]:
        st.header("User Management")
        st.write("Create / edit users, roles, permissions.")

    with sub_tabs[1]:
        st.header("System Configuration")
        st.write("Integrations, PLC connections, system params.")

# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0; left: 0; right: 0;
            background: white;
            padding: 10px;
            text-align:center;
            border-top:1px solid #ddd;
            font-size:13px;
            box-shadow:0 -2px 12px rgba(0,0,0,0.05);
        }
    </style>
    <div class='footer'>© 2025 MES Hybrid Tabs — Streamlit UI</div>
    """,
    unsafe_allow_html=True,
)
