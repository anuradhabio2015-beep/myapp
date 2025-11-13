import streamlit as st

# ------------------------------------------------------
# MASTER CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="MES Hybrid Pro UI", page_icon="🧭", layout="wide")

# ------------------------------------------------------
# REMOVE STREAMLIT DEFAULT CHROME
# ------------------------------------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER (Modern Glass/Hybrid)
# ======================================================
st.markdown("""
<style>
.top-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 80px;
    padding: 14px 30px;
    display: flex;
    align-items: center;
    background: white;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    z-index: 9999;
}
.top-header img {
    height: 50px;
    width: 50px;
    border-radius: 10px;
    margin-right: 15px;
}
.top-title { font-size: 24px; font-weight: 800; color:#111; }
.block-container { padding-top: 130px !important; margin-left: 220px !important; }
</style>

<div class="top-header">
    <img src="https://placehold.co/60x60?text=LOGO"/>
    <div class="top-title">MES Hybrid System (Tabs + Sidebar)</div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR (Fixed vertical navigation)
# ======================================================
st.markdown("""
<style>
.sidebar-fixed {
    position: fixed;
    top: 80px;
    left: 0;
    width: 200px;
    bottom: 0;
    background: #f7f9ff;
    padding: 20px 10px;
    box-shadow: 3px 0 10px rgba(0,0,0,0.08);
    z-index: 9998;
}
.sidebar-fixed h3 {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 16px;
}
.sidebar-fixed .link {
    display: block;
    padding: 10px 14px;
    margin: 8px 0;
    background: white;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    color: #222;
}
.sidebar-fixed .link:hover {
    background: #e6ecff;
}
</style>

<div class="sidebar-fixed">
    <h3>NAVIGATION</h3>
    <a class="link" href="#dashboard">Dashboard</a>
    <a class="link" href="#reports">Reports</a>
    <a class="link" href="#settings">Settings</a>
</div>
""", unsafe_allow_html=True)

# ======================================================
# PRIMARY NAVIGATION (TOP TABS)
# ======================================================
main_tabs = st.tabs(["📊 Dashboard", "📁 Reports", "⚙️ Settings"])

# ======================================================
# DASHBOARD TAB
# ======================================================
with main_tabs[0]:
    st.markdown("<a id='dashboard'></a>", unsafe_allow_html=True)
    st.subheader("📊 Dashboard")

    dash_tabs = st.tabs(["Overview", "Stations"])

    with dash_tabs[0]:
        st.header("Overview")
        st.write("Real-time KPIs: throughput, OEE, downtime, cycle times…")

    with dash_tabs[1]:
        st.header("Stations")
        st.write("List of stations, live alarms, PLC/IO health…")

# ======================================================
# REPORTS TAB
# ======================================================
with main_tabs[1]:
    st.markdown("<a id='reports'></a>", unsafe_allow_html=True)
    st.subheader("📁 Reports")

    report_tabs = st.tabs(["Daily", "Monthly"])

    with report_tabs[0]:
        st.header("Daily Reports")
        st.write("Shift data, daily performance, operator logs…")

    with report_tabs[1]:
        st.header("Monthly Reports")
        st.write("Monthly trends, scrap, Pareto charts, compliance…")

# ======================================================
# SETTINGS TAB
# ======================================================
with main_tabs[2]:
    st.markdown("<a id='settings'></a>", unsafe_allow_html=True)
    st.subheader("⚙️ Settings")

    set_tabs = st.tabs(["Users", "System Config"])

    with set_tabs[0]:
        st.header("User Management")
        st.write("Roles, permissions, access control groups…")

    with set_tabs[1]:
        st.header("System Configuration")
        st.write("PLC connections, integrations, historian settings…")

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 220px; right: 0;
    bottom: 0;
    padding: 10px;
    background: white;
    text-align: center;
    font-size: 13px;
    border-top: 1px solid #ddd;
}
</style>

<div class="footer">
    © 2025 MES Hybrid UI — Tabs + Sidebar Layout
</div>
""", unsafe_allow_html=True)
