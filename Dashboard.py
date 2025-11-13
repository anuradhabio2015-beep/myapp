import streamlit as st

# -------------------------------------------------------
# REMOVE STREAMLIT DEFAULT HEADER/FOOTER
# -------------------------------------------------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# READ PAGE + SUBTAB FROM QUERY PARAMS
# -------------------------------------------------------
params = st.query_params

active_page = params.get("page", "dashboard")
active_subtab = params.get("sub", "daily")      # default sub-tab


# -------------------------------------------------------
# FIXED LEFT SIDEBAR MENU
# -------------------------------------------------------
st.markdown("""
<style>
.sidebar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 230px;
    height: 100%;
    background-color: #1d4ed8;
    padding-top: 90px;
    z-index: 9999;
}
.sidebar-item {
    padding: 14px 25px;
    color: white;
    font-size: 17px;
    cursor: pointer;
    text-decoration: none;
    display: block;
    opacity: 0.75;
}
.sidebar-item.active {
    background-color: #2563eb;
    opacity: 1;
}
.sidebar-item:hover {
    background-color: #3b82f6;
}
.subitem {
    padding: 8px 45px;
    color: white;
    font-size: 15px;
    text-decoration: none;
    display: block;
    opacity: 0.7;
}
.subitem.active {
    font-weight: bold;
    opacity: 1;
    text-decoration: underline;
}
.block-container {
    margin-left: 260px !important;
    padding-top: 30px !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# BUILD SIDEBAR HTML
# -------------------------------------------------------
sidebar_html = f"""
<div class="sidebar-container">

    <a href="?page=dashboard" class="sidebar-item {'active' if active_page=='dashboard' else ''}">
        📊 Dashboard
    </a>

    <a href="?page=reports" class="sidebar-item {'active' if active_page=='reports' else ''}">
        📁 Reports
    </a>
"""

# Add subtabs only when Reports is active
if active_page == "reports":
    sidebar_html += f"""
        <a href="?page=reports&sub=daily" class="subitem {'active' if active_subtab=='daily' else ''}">Daily</a>
        <a href="?page=reports&sub=weekly" class="subitem {'active' if active_subtab=='weekly' else ''}">Weekly</a>
        <a href="?page=reports&sub=monthly" class="subitem {'active' if active_subtab=='monthly' else ''}">Monthly</a>
    """

sidebar_html += f"""
    <a href="?page=settings" class="sidebar-item {'active' if active_page=='settings' else ''}">
        ⚙️ Settings
    </a>
</div>
"""

st.markdown(sidebar_html, unsafe_allow_html=True)


# -------------------------------------------------------
# PAGE CONTENT AREA
# -------------------------------------------------------
if active_page == "dashboard":
    st.header("📊 Dashboard")
    t1, t2 = st.tabs(["Production", "Quality"])
    t1.write("Production KPIs…")
    t2.write("Quality KPIs…")

elif active_page == "reports":
    st.header("📁 Reports")

    if active_subtab == "daily":
        st.subheader("📅 Daily Reports")
        st.write("Daily report KPIs…")

    elif active_subtab == "weekly":
        st.subheader("📆 Weekly Reports")
        st.write("Weekly trends…")

    elif active_subtab == "monthly":
        st.subheader("📊 Monthly Reports")
        st.write("Monthly summary…")

elif active_page == "settings":
    st.header("⚙️ Settings")
    st.write("System settings & configuration…")


# -------------------------------------------------------
# CUSTOM FOOTER
# -------------------------------------------------------
st.markdown("""
<style>
.custom-footer {
    position: fixed;
    bottom: 0;
    left: 260px;
    width: calc(100% - 260px);
    background-color: #1d4ed8;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>

<div class="custom-footer">
© 2025 MES System | Powered by Python + Streamlit
</div>
""", unsafe_allow_html=True)
