import streamlit as st

# ------------------------------------------------------
# MES HYBRID UI — SINGLE PAGE APP (FIXED + CLEAN)
# ------------------------------------------------------

st.set_page_config(page_title="MES Hybrid UI", layout="wide")

# ------------------------------------------------------
# HIDE STREAMLIT DEFAULT UI
# ------------------------------------------------------
st.markdown(
    """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 260px;
            width: calc(100% - 260px);
            background: #eef3ff;
            padding: 8px;
            text-align:center;
            font-size: 12px;
            color:#444;
            border-top:1px solid #d6ddff;
            z-index:999;
        }
    </style>
    <div class='custom-footer'>© 2025 MES System — Powered by Streamlit</div>
    """,
    unsafe_allow_html=True,
)
