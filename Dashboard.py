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
# INITIALIZE SESSION STATE FOR ACTIVE PAGE
# -------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "dashboard"

# -------------------------------------------------------
# CUSTOM HEADER — CONTROLS PAGE SWITCHING
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
            cursor: pointer;
            opacity: 0.7;
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
            <a class="{ 'active' if st.session_state.active_page=='dashboard' else ''}"
               onclick="switchPage('dashboard')">Dashboard</a>

            <a class="{ 'active' if st.session_state.active_page=='reports' else ''}"
               onclick="switchPage('reports')">Reports</a>

            <a class="{ 'active' if st.session_state.active_page=='settings' else ''}"
               onclick="switchPage('settings')">Settings</a>
        </div>
    </div>

    <script>
        function switchPage(pageName) {{
            window.parent.postMessage(
                {{
                    isStreamlitMessage: true,
                    type: "streamlit:setComponentValue",
                    value: pageName
                }},
                "*"
            );
        }}
    </script>
"""
st.markdown(custom_header, unsafe_allow_html=True)

# -------------------------------------------------------
# CAPTURE HEADER CLICK EVENTS
# -------------------------------------------------------
event = st.experimental_get_query_params()
if "_component_value" in event:
    st.session_state.active_page = event["_component_value"][0]

# -------------------------------------------------------
# PAGE CONTENT BASED ON HEADER TAB
# -------------------------------------------------------
if st.session_state.active_page == "dashboard":
    st.header("📊 Dashboard")
    tab1, tab2 = st.tabs(["Production", "Quality"])
    tab1.write("Production KPIs…")
    tab2.write("Quality KPIs…")

elif st.session_state.active_page == "reports":
    st.header("📁 Reports")
    st.write("Report listing…")

elif st.session_state.active_page == "settings":
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
            font-size: 14px;
            z-index: 9999;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
