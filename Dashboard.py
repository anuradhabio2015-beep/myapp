import streamlit as st

# -------------------------------------------------------
# REMOVE STREAMLIT DEFAULT HEADER/FOOTER
# -------------------------------------------------------
hide_default = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_default, unsafe_allow_html=True)

# -------------------------------------------------------
# INIT ACTIVE TAB IN SESSION
# -------------------------------------------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# -------------------------------------------------------
# TOP FIXED HEADER
# -------------------------------------------------------
header_html = """
    <style>
        .header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #2c6bed;
            color: white;
            padding-left: 20px;
            display: flex;
            align-items: center;
            font-size: 22px;
            font-weight: 700;
            z-index: 999;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
        }
        .content {
            padding-top: 80px;
            padding-left: 200px;
        }
    </style>
    <div class="header">MES Application</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# -------------------------------------------------------
# FIXED SIDEBAR MENU USING SESSION STATE
# -------------------------------------------------------
sidebar_html = """
    <style>
        .side-menu {
            position: fixed;
            top: 60px;
            left: 0;
            width: 180px;
            height: 100%;
            background-color: #f4f7fb;
            padding-top: 20px;
            border-right: 1px solid #ddd;
        }
        .menu-item {
            padding: 12px 18px;
            margin: 4px 10px;
            font-size: 16px;
            font-weight: 600;
            color: #333;
            border-radius: 6px;
            cursor: pointer;
        }
        .menu-item:hover {
            background-color: #e5e9f1;
        }
        .menu-active {
            background-color: #2c6bed;
            color: white !important;
        }
    </style>
"""
st.markdown(sidebar_html, unsafe_allow_html=True)

# SIDEBAR MENU ITEMS
menu_container = st.container()

with menu_container:
    st.markdown(
        f"""
        <div class="side-menu">
            <div class="menu-item {'menu-active' if st.session_state.active_tab=='Dashboard' else ''}"
                 onclick="window.location.href='?clicked=Dashboard'">
                Dashboard
            </div>

            <div class="menu-item {'menu-active' if st.session_state.active_tab=='Reports' else ''}"
                 onclick="window.location.href='?clicked=Reports'">
                Reports
            </div>

            <div class="menu-item {'menu-active' if st.session_state.active_tab=='Settings' else ''}"
                 onclick="window.location.href='?clicked=Settings'">
                Settings
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# HANDLE MENU CLICK
# -------------------------------------------------------
params = st.query_params
if "clicked" in params:
    st.session_state.active_tab = params["clicked"]
    # Clear parameters so URL stays clean
    st.query_params.clear()

# -------------------------------------------------------
# MAIN CONTENT CONTROLLED BY ACTIVE TAB
# -------------------------------------------------------
st.markdown("<div class='content'>", unsafe_allow_html=True)

tab_names = ["Dashboard", "Reports", "Settings"]

# Select correct tab index
tab_index = tab_names.index(st.session_state.active_tab)

tabs = st.tabs(tab_names)

with tabs[0]:
    if st.session_state.active_tab == "Dashboard":
        st.header("📊 Dashboard")
        a, b = st.tabs(["Production", "Quality"])
        a.write("Production KPIs...")
        b.write("Quality KPIs...")

with tabs[1]:
    if st.session_state.active_tab == "Reports":
        st.header("📁 Reports")
        st.write("Report listing...")

with tabs[2]:
    if st.session_state.active_tab == "Settings":
        st.header("⚙️ Settings")
        st.write("System configuration...")

st.markdown("</div>", unsafe_allow_html=True)
