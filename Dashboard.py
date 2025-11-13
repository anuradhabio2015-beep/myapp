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
# FIXED CUSTOM HEADER WITH TAB SWITCHING
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
            cursor: pointer;
        }
        .header-links a:hover {
            text-decoration: underline;
        }
        .block-container {
            padding-top: 90px !important;
        }
    </style>

    <div class="custom-header">
        <div>MES Application</div>
        <div class="header-links">
            <a onclick="switchTab(0)">Dashboard</a>
            <a onclick="switchTab(1)">Reports</a>
            <a onclick="switchTab(2)">Settings</a>
        </div>
    </div>

    <script>
        function switchTab(index) {
            const tabs = window.parent.document.querySelectorAll('div[data-testid="stTabs"] button');
            if (tabs && tabs[index]) {
                tabs[index].click();
            }
        }
    </script>
"""

st.markdown(custom_header, unsafe_allow_html=True)


# -------------------------------------------------------
# MAIN TABS (CONTROLLED BY HEADER)
# -------------------------------------------------------
main_tabs = st.tabs(["Dashboard", "Reports", "Settings"])

with main_tabs[0]:
    st.header("📊 Dashboard")
    t1, t2 = st.tabs(["Production", "Quality"])
    t1.write("Production KPIs...")
    t2.write("Quality KPIs...")

with main_tabs[1]:
    st.header("📁 Reports")
    st.write("Report listing...")

with main_tabs[2]:
    st.header("⚙️ Settings")
    st.write("System configuration...")


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
