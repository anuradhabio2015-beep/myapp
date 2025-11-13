import streamlit as st

# -------------------------------------------------------
# REMOVE STREAMLIT DEFAULT HEADER/FOOTER
# -------------------------------------------------------
hide_default = """
    <style>
        # MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_default, unsafe_allow_html=True)


# -------------------------------------------------------
# FIXED CUSTOM HEADER (Top)
# -------------------------------------------------------
custom_header = """
    <style>
        .custom-header {
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
        }

        .header-links a {
            color: white;
            margin-left: 25px;
            text-decoration: none;
            font-size: 16px;
            font-weight: 500;
        }

        .header-links a:hover {
            text-decoration: underline;
        }

        /* Push content below fixed header */
        .block-container {
            padding-top: 90px !important;
        }
    </style>

    <div class="custom-header">
        <div>MES Application</div>
        <div class="header-links">
            <a href="?page=dashboard">Dashboard</a>
            <a href="?page=reports">Reports</a>
            <a href="?page=settings">Settings</a>
        </div>
    </div>
"""
st.markdown(custom_header, unsafe_allow_html=True)



# -------------------------------------------------------
# URL MODE (Optional)
# -------------------------------------------------------
params = st.experimental_get_query_params()
page = params.get("page", [side_sel.lower()])[0]


# -------------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------------
if page == "dashboard":
    st.header("📊 Dashboard")
    tab1, tab2 = st.tabs(["Production", "Quality"])
    tab1.write("Production KPIs...")
    tab2.write("Quality KPIs...")

elif page == "reports":
    st.header("📁 Reports")
    st.write("Report listing...")

elif page == "settings":
    st.header("⚙️ Settings")
    st.write("System configuration...")


# -------------------------------------------------------
# FIXED CUSTOM FOOTER (Bottom)
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
