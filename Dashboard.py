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
# READ ACTIVE PAGE FROM st.query_params (LATEST API)
# -------------------------------------------------------
params = st.query_params
active_page = params.get("page", "dashboard")

# -------------------------------------------------------
# TOP HEADER (FIXED)
# -------------------------------------------------------
custom_header = """
    <style>
        .top-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #2c6bed;
            color: white;
            padding: 15px 25px;
            font-size: 22px;
            font-weight: 700;
            z-index: 9999;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
        }
        .block-container {
            padding-top: 80px !important;
        }
    </style>
    <div class="top-header">MES Application</div>
"""
st.markdown(custom_header, unsafe_allow_html=True)

# -------------------------------------------------------
# SIDEBAR MENU (LEFT)
# -------------------------------------------------------
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Reports", "Settings"],
    index=["dashboard", "reports", "settings"].index(active_page),
)

# Update URL automatically when user clicks menu
st.query_params["page"] = menu.lower()


# -------------------------------------------------------
# PAGE CONTENT - TAB-LIKE BEHAVIOR
# -------------------------------------------------------
if menu == "Dashboard":
    st.header("📊 Dashboard")
    t1, t2 = st.tabs(["Production", "Quality"])
    t1.write("Production KPIs…")
    t2.write("Quality KPIs…")

elif menu == "Reports":
    st.header("📁 Reports")
    st.write("Report listing…")

elif menu == "Settings":
    st.header("⚙️ Settings")
    st.write("System configuration…")


# -------------------------------------------------------
# CUSTOM FOOTER
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
            font-size: 13px;
            z-index: 9999;
        }
    </style>
    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
