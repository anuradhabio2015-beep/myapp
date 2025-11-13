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
# SESSION STATE FOR ACTIVE PAGE
# -------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "dashboard"

# -------------------------------------------------------
# CLICK HANDLERS — THESE SWITCH TABS WITHOUT RELOAD
# -------------------------------------------------------
def go_dashboard():
    st.session_state.active_page = "dashboard"

def go_reports():
    st.session_state.active_page = "reports"

def go_settings():
    st.session_state.active_page = "settings"

# -------------------------------------------------------
# CUSTOM HEADER (BUTTONS — SAME PAGE)
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
        .header-links button {
            background: none;
            border: none;
            color: white;
            margin-left: 25px;
            font-size: 16px;
            cursor: pointer;
            opacity: 0.7;
        }
        .header-links button.active {
            opacity: 1;
            text-decoration: underline;
        }
        .block-container {
            padding-top: 90px !important;
        }
    </style>
"""
st.markdown(custom_header, unsafe_allow_html=True)

# Header layout
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown(
        "<div class='custom-header'>MES Application</div>",
        unsafe_allow_html=True
    )

with col2:
    st.write("")  # spacing
    st.write("")  # spacing
    st.write("")

# Render header menu using columns (stays on same page)
header_col1, header_col2, header_col3 = st.columns(3)

with header_col1:
    if st.button("Dashboard", key="dash_btn"):
        go_dashboard()

with header_col2:
    if st.button("Reports", key="rep_btn"):
        go_reports()

with header_col3:
    if st.button("Settings", key="set_btn"):
        go_settings()

# -------------------------------------------------------
# PAGE CONTENT BASED ON session_state
# -------------------------------------------------------
if st.session_state.active_page == "dashboard":
    st.header("📊 Dashboard")
    t1, t2 = st.tabs(["Production", "Quality"])
    t1.write("Production KPIs…")
    t2.write("Quality KPIs…")

elif st.session_state.active_page == "reports":
    st.header("📁 Reports")
    st.write("Report listing…")

elif st.session_state.active_page == "settings":
    st.header("⚙️ Settings")
    st.write("Settings configuration…")

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
