import streamlit as st

# -------------------------------------------------------------
# REMOVE DEFAULT STREAMLIT HEADER & FOOTER
# -------------------------------------------------------------
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------------------------------------------------
# CUSTOM HEADER WITH MENU
# -------------------------------------------------------------
custom_header = """
  <style>
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2c6bed;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
    <div class="custom-header">
        <div class="custom-header-title">MES Application</div>
        <div class="header-menu">
            <a href="?page=dashboard">Dashboard</a>
            <a href="?page=reports">Reports</a>
            <a href="?page=settings">Settings</a>
        </div>
    </div>
"""

st.markdown(custom_header, unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR MENU
# -------------------------------------------------------------
with st.sidebar:
    st.title("📌 Menu")
    side_selection = st.radio(
        "Navigate",
        ["Dashboard", "Reports", "Settings", "Help"]
    )

# -------------------------------------------------------------
# URL PARAMETER ROUTING
# -------------------------------------------------------------
query_params = st.experimental_get_query_params()
page = query_params.get("page", [side_selection.lower()])[0]

# -------------------------------------------------------------
# PAGE CONTENT ROUTING
# -------------------------------------------------------------
if page == "dashboard":
    st.header("📊 Dashboard")
    
    tab1, tab2 = st.tabs(["Production", "Quality"])

    with tab1:
        st.write("Production KPIs Here...")

    with tab2:
        st.write("Quality KPIs Here...")

elif page == "reports":
    st.header("📁 Reports")
    st.write("Generate or download reports...")

elif page == "settings":
    st.header("⚙️ Settings")
    st.write("User / System configuration...")

elif page == "help":
    st.header("❓ Help")
    st.write("Documentation / Support info...")

# -------------------------------------------------------------
# CUSTOM FOOTER (ALWAYS VISIBLE)
# -------------------------------------------------------------
custom_footer = """
    <style>
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2c6bed;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""

st.markdown(custom_footer, unsafe_allow_html=True)
