import streamlit as st
from streamlit_option_menu import option_menu

# -------------------------------------------------------
# REMOVE DEFAULT STREAMLIT HEADER & FOOTER
# -------------------------------------------------------
hide_default = """
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
"""
st.markdown(hide_default, unsafe_allow_html=True)

# -------------------------------------------------------
# CUSTOM HEADER (TOP BAR)
# -------------------------------------------------------
custom_header = """
<style>
.custom-header {
    background-color: #1a73e8;
    padding: 12px 25px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: white;
    font-size: 22px;
    font-weight: 700;
}
</style>

<div class="custom-header">
🚀 MES Application – Smart Factory Dashboard
</div>
"""
st.markdown(custom_header, unsafe_allow_html=True)


# -------------------------------------------------------
# SIDE MENU
# -------------------------------------------------------
with st.sidebar:
    st.image("https://static.streamlit.io/examples/dice.jpg", width=140)
    st.markdown("### Navigation")

    selected = option_menu(
        menu_title="",  
        options=["Dashboard", "Orders", "Production", "Quality", "Settings"],
        icons=["bar-chart", "list-task", "cpu", "check2-square", "gear"],
        menu_icon="cast",
        default_index=0,
    )

# -------------------------------------------------------
# BODY CONTENT
# -------------------------------------------------------
st.write(f"### You selected: **{selected}**")

if selected == "Dashboard":
    st.info("Dashboard KPIs & charts here…")
elif selected == "Orders":
    st.success("Order Management UI…")
elif selected == "Production":
    st.warning("Production Status UI…")
elif selected == "Quality":
    st.error("Quality Dashboard UI…")
elif selected == "Settings":
    st.write("Settings page…")


# -------------------------------------------------------
# CUSTOM FOOTER (FIXED BOTTOM)
# -------------------------------------------------------
custom_footer = """
<style>
.custom-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #1a73e8;
    color: white;
    text-align: center;
    padding: 8px 0;
    font-size: 14px;
}
</style>

<div class="custom-footer">
© 2025 MES System | Designed & Developed by Rahul
</div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
