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
# CUSTOM HEADER (WITH BUTTONS INSIDE HEADER)
# -------------------------------------------------------
header_html = """
<style>
.custom-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: #2c6bed;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 25px;
    font-size: 22px;
    font-weight: 700;
    z-index: 9999;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.25);
}
.nav-buttons {
    display: flex;
    gap: 30px;
}
.nav-button {
    color: white;
    font-size: 16px;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    opacity: 0.7;
    transition: 0.2s;
}
.nav-button:hover {
    opacity: 1;
    background-color: rgba(255,255,255,0.15);
}
.nav-button.active {
    opacity: 1;
    text-decoration: underline;
}
.block-container {
    padding-top: 90px !important;
}
</style>
<div class="custom-header">
    <div>MES Application</div>
    <div class="nav-buttons">
"""

# Add buttons dynamically
header_html += f"""
        <div class="nav-button {'active' if st.session_state.active_page=='dashboard' else ''}"
             onclick="window.parent.postMessage({{'page':'dashboard'}}, '*')">
             Dashboard
        </div>

        <div class="nav-button {'active' if st.session_state.active_page=='reports' else ''}"
             onclick="window.parent.postMessage({{'page':'reports'}}, '*')">
             Reports
        </div>

        <div class="nav-button {'active' if st.session_state.active_page=='settings' else ''}"
             onclick="window.parent.postMessage({{'page':'settings'}}, '*')">
             Settings
        </div>
"""

header_html += """
    </div>
</div>
<script>
window.addEventListener('message', (event) => {
    if (event.data.page) {
        window.parent.streamlitRerun({value: event.data.page});
    }
});
</script>
"""

st.markdown(header_html, unsafe_allow_html=True)


# -------------------------------------------------------
# UPDATE ACTIVE PAGE ON CLICK (NO PAGE RELOAD)
# -------------------------------------------------------
event = st.session_state.get("_streamlitRerun")
if event:
    st.session_state.active_page = event


# -------------------------------------------------------
# PAGE CONTENT
# -------------------------------------------------------
if st.session_state.active_page == "dashboard":
    st.header("📊 Dashboard")
    tab1, tab2 = st.tabs(["Production", "Quality"])
    tab1.write("Production KPIs…")
    tab2.write("Quality KPIs…")

elif st.session_state.active_page == "reports":
    st.header("📁 Reports")
    st.write("Report Listing…")

elif st.session_state.active_page == "settings":
    st.header("⚙️ Settings")
    st.write("Configuration…")


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
