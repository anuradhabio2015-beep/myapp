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
# READ ACTIVE PAGE FROM URL
# -------------------------------------------------------
params = st.experimental_get_query_params()
active_page = params.get("page", ["dashboard"])[0]

# -------------------------------------------------------
# TOP HEADER (NO JS, PURE LINKS)
# -------------------------------------------------------
custom_header = f"""
    <style>
        .custom-header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #2c6bed;
            color: white;
            padding: 14px 22px;
            font-size: 20px;
            font-weight: 700;
            z-index: 9999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
        }}
        .header-links a {{
            color: white;
            margin-left: 25px;
            font-size: 16px;
            font-weight: 500;
            text-decoration: none;
            opacity: 0.6;
        }}
        .header-links a.active {{
            opacity: 1;
            text-decoration: underline;
        }}
        .block-container {{
            padding-top: 90px !important;
        }}
    </style>

    <div class="custom-header">
        <div>MES Application</div>
        <div class="header-links">
            <a href="?page=dashboard" class="{ 'active' if active_page=='dashboard' else ''}">Dashboard</a>
            <a href="?page=reports" class="{ 'active' if active_page=='reports' else ''}">Reports</a>
            <a href="?page=settings" class="{ 'active' if active_page=='settings' else ''}">Settings</a>
        </div>
    </div>
"""
st.markdown(custom_header, unsafe_allow_html=True)

# -------------------------------------------------------
# PAGE CONTENT
# -------------------------------------------------------
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

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
custom_footer = """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
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
