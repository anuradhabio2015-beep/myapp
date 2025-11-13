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
# FIXED TOP HEADER (FULL WIDTH)
# -------------------------------------------------------
top_header = """
    <style>
        .top-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 58px;
            background-color: #2c6bed;
            color: white;
            padding: 14px 25px;
            font-size: 21px;
            font-weight: 700;
            z-index: 10000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.25);
        }

        /* Push Streamlit layout down + right */
        .block-container {
            padding-top: 80px !important;
            margin-left: 240px !important;  
            max-width: 100% !important;
        }
    </style>

    <div class="top-header">
        <div>MES Application</div>
        <div style="margin-right: 30px; font-weight: 500; font-size: 16px;">
            Dashboard | Reports | Settings
        </div>
    </div>
"""
st.markdown(top_header, unsafe_allow_html=True)


# -------------------------------------------------------
# PAGE ROUTING (USING NEW API)
# -------------------------------------------------------
params = st.query_params
page = params.get("page", "dashboard")

DASH = "active" if page == "dashboard" else ""
REPO = "active" if page == "reports" else ""
SETT = "active" if page == "settings" else ""


# -------------------------------------------------------
# FULL HEIGHT LEFT NAVIGATION PANEL
# -------------------------------------------------------
left_nav = f"""
    <style>
        .left-nav {{
            position: fixed;
            top: 58px;
            left: 0;
            width: 240px;
            height: calc(100% - 58px);
            background-color: #eef2ff;
            padding-top: 20px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            z-index: 9999;
        }}

        .menu-item {{
            padding: 14px 25px;
            font-size: 17px;
            color: #1a1a1a;
            display: block;
            text-decoration: none;
            font-weight: 500;
        }}

        .menu-item:hover {{
            background-color: #d6dfff;
        }}

        .active {{
            background-color: #2c6bed !important;
            color: white !important;
        }}
    </style>

    <div class="left-nav">
        <a class="menu-item {DASH}" href="?page=dashboard">📊 Dashboard</a>
        <a class="menu-item {REPO}" href="?page=reports">📁 Reports</a>
        <a class="menu-item {SETT}" href="?page=settings">⚙️ Settings</a>
    </div>
"""
st.markdown(left_nav, unsafe_allow_html=True)


# -------------------------------------------------------
# MAIN PAGE CONTENT (RIGHT SIDE)
# -------------------------------------------------------
if page == "dashboard":
    st.header("📊 Dashboard")
    tab1, tab2 = st.tabs(["Production", "Quality"])
    tab1.write("Production KPIs…")
    tab2.write("Quality KPIs…")

elif page == "reports":
    st.header("📁 Reports")
    st.write("Report listing…")

elif page == "settings":
    st.header("⚙️ Settings")
    st.write("System configuration…")


# -------------------------------------------------------
# OPTIONAL CUSTOM FOOTER (ALIGNED)
# -------------------------------------------------------
custom_footer = """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 240px;
            width: calc(100% - 240px);
            background-color: #2c6bed;
            color: white;
            text-align: center;
            padding: 10px;
            z-index: 9999;
            font-size: 14px;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
