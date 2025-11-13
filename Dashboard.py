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
# FIXED TOP HEADER
# -------------------------------------------------------
top_header = """
    <style>
        .top-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 55px;
            background-color: #2c6bed;
            color: white;
            padding: 12px 20px;
            font-size: 20px;
            font-weight: 700;
            z-index: 9999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
        }
        .block-container {
            padding-top: 70px !important;
            margin-left: 230px !important;  /* content shifts RIGHT */
        }
    </style>

    <div class="top-header">
        <div>MES Application</div>
        <div style="margin-right: 30px; font-weight: 500;">
            Dashboard | Reports | Settings
        </div>
    </div>
"""
st.markdown(top_header, unsafe_allow_html=True)



# -------------------------------------------------------
# PAGE ROUTING
# -------------------------------------------------------
params = st.query_params
page = params.get("page", "dashboard")

DASH_ACTIVE = "active" if page == "dashboard" else ""
REP_ACTIVE  = "active" if page == "reports" else ""
SET_ACTIVE  = "active" if page == "settings" else ""



# -------------------------------------------------------
# FULL-HEIGHT LEFT SIDEBAR MENU
# -------------------------------------------------------
left_menu = f"""
    <style>
        .left-menu {{
            position: fixed;
            top: 55px;              /* BELOW HEADER */
            left: 0;
            width: 220px;
            height: 100%;
            background-color: #f2f5ff;
            padding-top: 30px;
            box-shadow: 2px 0px 4px rgba(0,0,0,0.1);
            z-index: 9998;
        }}

        .menu-item {{
            padding: 12px 25px;
            font-size: 16px;
            color: #1a1a1a;
            display: block;
            text-decoration: none;
            font-weight: 500;
        }}

        .menu-item:hover {{
            background-color: #dbe4ff;
            cursor: pointer;
        }}

        .active {{
            background-color: #2c6bed !important;
            color: white !important;
        }}
    </style>

    <div class="left-menu">
        <a class="menu-item {DASH_ACTIVE}" href="?page=dashboard">📊 Dashboard</a>
        <a class="menu-item {REP_ACTIVE}"  href="?page=reports">📁 Reports</a>
        <a class="menu-item {SET_ACTIVE}"  href="?page=settings">⚙️ Settings</a>
    </div>
"""

st.markdown(left_menu, unsafe_allow_html=True)



# -------------------------------------------------------
# MAIN CONTENT AREA (RIGHT SIDE)
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
# OPTIONAL CUSTOM FOOTER
# -------------------------------------------------------
custom_footer = """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 230px;   /* aligned under content */
            width: calc(100% - 230px);
            background-color: #2c6bed;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 9999;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
