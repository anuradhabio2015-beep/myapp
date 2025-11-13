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
# READ ACTIVE PAGE USING st.query_params (LATEST API)
# -------------------------------------------------------
params = st.query_params
active_page = params.get("page", "dashboard")


# -------------------------------------------------------
# FIXED TOP HEADER (BLUE BAR)
# -------------------------------------------------------
header_html = """
    <style>
        .top-header {
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
            z-index: 1000;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
        }
        .main-content {
            padding-top: 80px;
            padding-left: 200px;
        }
    </style>

    <div class="top-header">MES Application</div>
"""
st.markdown(header_html, unsafe_allow_html=True)


# -------------------------------------------------------
# FIXED LEFT SIDEBAR MENU (CSS + HTML)
# -------------------------------------------------------
sidebar_html = f"""
    <style>
        .sidebar {{
            position: fixed;
            top: 60px;
            left: 0;
            width: 180px;
            height: 100%;
            background-color: #f5f7fa;
            padding-top: 30px;
            border-right: 1px solid #ddd;
            z-index: 999;
        }}

        .menu-item {{
            padding: 12px 20px;
            font-size: 16px;
            font-weight: 600;
            color: #333;
            text-decoration: none;
            display: block;
            border-radius: 6px;
            margin: 6px 10px;
        }}

        .menu-item:hover {{
            background-color: #e6e9ef;
        }}

        .menu-active {{
            background-color: #2c6bed !important;
            color: white !important;
        }}
    </style>

    <div class="sidebar">
        <a href="?page=dashboard" class="menu-item {'menu-active' if active_page=='dashboard' else ''}">Dashboard</a>
        <a href="?page=reports" class="menu-item {'menu-active' if active_page=='reports' else ''}">Reports</a>
        <a href="?page=settings" class="menu-item {'menu-active' if active_page=='settings' else ''}">Settings</a>
    </div>
"""
st.markdown(sidebar_html, unsafe_allow_html=True)


# -------------------------------------------------------
# MAIN CONTENT AREA (SHIFTED RIGHT BELOW HEADER)
# -------------------------------------------------------
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

if active_page == "dashboard":
    st.header("📊 Dashboard")
    t1, t2 = st.tabs(["Production", "Quality"])
    t1.write("Production KPIs…")
    t2.write("Quality KPIs…")

elif active_page == "reports":
    st.header("📁 Reports")
    st.write("Report listing…")

elif active_page == "settings":
    st.header("⚙️ Settings")
    st.write("System configuration…")

st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
footer_html = """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 200px;
            width: calc(100% - 200px);
            background-color: #2c6bed;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 14px;
            z-index: 1000;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
