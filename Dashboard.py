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
# FIXED CUSTOM HEADER (Same style & structure as footer)
# -------------------------------------------------------------
custom_header = """
    <style>
        .custom-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #2c6bed;
            color: white;
            padding: 12px 20px;
            font-size: 18px;
            font-weight: 600;
            z-index: 9999;

            display: flex;
            justify-content: space-between;
            align-items: center;

            box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
        }

        .custom-header a {
            color: white;
            margin-left: 20px;
            text-decoration: none;
            font-weight: 500;
        }

        .custom-header a:hover {
            text-decoration: underline;
        }

        /* Push Streamlit content below fixed header */
        .block-container {
            padding-top: 90px !important;
        }
    </style>

    <div class="custom-header">
        <div>MES Application</div>
        <div>
            <a href="?page=dashboard">Dashboard</a>
            <a href="?page=reports">Reports</a>
            <a href="?page=settings">Settings</a>
        </div>
    </div>
"""

st.markdown(custom_header, unsafe_allow_html=True)

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
