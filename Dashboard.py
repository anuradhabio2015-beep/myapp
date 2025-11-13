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
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {display:none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# SESSION STATE (NO URL ROUTING — FULLY STABLE)
# ------------------------------------------------------
if "main" not in st.session_state:
    st.session_state.main = "dashboard"
if "sub" not in st.session_state:
    st.session_state.sub = "overview"

# Helper

def nav(main, sub):
    st.session_state.main = main
    st.session_state.sub = sub

# ------------------------------------------------------
# CUSTOM FIXED HEADER
# ------------------------------------------------------
st.markdown(
    """
    <style>
        .app-header {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 74px;
            background: white;
            display: flex;
            align-items: center;
            padding: 12px 26px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
            z-index: 9999;
        }
        .app-header-title {
            font-size: 22px;
            font-weight: 800;
            margin-left: 12px;
        }
        .block-container {
            padding-top: 120px !important;
            margin-left: 260px !important;
        }
    </style>
    <div class="app-header">
        <img src="https://placehold.co/56x56?text=Logo" style="border-radius:10px" />
        <div class="app-header-title">MES Hybrid System</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# SIDEBAR (COLLAPSIBLE)
# ------------------------------------------------------
st.markdown(
    """
    <style>
        .sidebar-container {
            position: fixed;
            top: 74px; left: 0; bottom: 0;
            width: 260px;
            background: #f7f9ff;
            padding: 20px 14px;
            overflow-y: auto;
            box-shadow: 2px 0 12px rgba(0,0,0,0.05);
        }
        .sidebar-title {
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 12px;
        }
        summary {
            padding: 10px 12px;
            border-radius: 8px;
            cursor: pointer;
            list-style: none;
            font-weight: 700;
            color:#222;
        }
        summary:hover { background:#e7edff; }
        .item {
            display:block;
            padding: 8px 16px;
            border-radius: 8px;
            margin: 4px 0;
            font-weight: 600;
            color:#333;
            text-decoration:none;
        }
        .item:hover { background:#dfe7ff; }
        .active-main { background:#2c6bed; color:white !important; }
        .active-sub { background:#155cd6; color:white !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar structure
with st.container():
    st.markdown("<div class='sidebar-container'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)

    # ---------------- DASHBOARD ----------------
    dash_open = "open" if st.session_state.main == "dashboard" else ""
    dash_main = "active-main" if st.session_state.main == "dashboard" else ""

    st.markdown(f"<details {dash_open}><summary class='{dash_main}'>📊 Dashboard</summary>", unsafe_allow_html=True)

    st.markdown(
        f"<a class='item {'active-sub' if st.session_state.sub=='overview' and st.session_state.main=='dashboard' else ''}' href='javascript:void(0);' onclick=\"window.parent.location.reload();\">Overview</a>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<a class='item {'active-sub' if st.session_state.sub=='stations' and st.session_state.main=='dashboard' else ''}' href='javascript:void(0);' onclick=\"window.parent.location.reload();\">Stations</a>",
        unsafe_allow_html=True,
    )

    st.markdown("</details>", unsafe_allow_html=True)

    # ---------------- REPORTS ----------------
    rep_open = "open" if st.session_state.main == "reports" else ""
    rep_main = "active-main" if st.session_state.main == "reports" else ""

    st.markdown(f"<details {rep_open}><summary class='{rep_main}'>📁 Reports</summary>", unsafe_allow_html=True)

    st.markdown(
        f"<a class='item {'active-sub' if st.session_state.sub=='daily' and st.session_state.main=='reports' else ''}' href='#'>Daily</a>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<a class='item {'active-sub' if st.session_state.sub=='monthly' and st.session_state.main=='reports' else ''}' href='#'>Monthly</a>",
        unsafe_allow_html=True,
    )

    st.markdown("</details>", unsafe_allow_html=True)

    # ---------------- SETTINGS ----------------
    set_open = "open" if st.session_state.main == "settings" else ""
    set_main = "active-main" if st.session_state.main == "settings" else ""

    st.markdown(f"<details {set_open}><summary class='{set_main}'>⚙ Settings</summary>", unsafe_allow_html=True)

    st.markdown(
        f"<a class='item {'active-sub' if st.session_state.sub=='users' and st.session_state.main=='settings' else ''}' href='#'>Users</a>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<a class='item {'active-sub' if st.session_state.sub=='system' and st.session_state.main=='settings' else ''}' href='#'>System</a>",
        unsafe_allow_html=True,
    )

    st.markdown("</details>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------
# MAIN CONTENT
# ------------------------------------------------------
main = st.session_state.main
sub  = st.session_state.sub

st.title(main.capitalize() + " — " + sub.capitalize())

if main == "dashboard":
    if sub == "overview":
        st.header("Overview")
        st.write("Production KPIs, throughput, OEE, etc.")
    elif sub == "stations":
        st.header("Stations")
        st.write("Station status, cycle time, alarms.")

elif main == "reports":
    if sub == "daily":
        st.header("Daily Reports")
        st.write("Daily production summary")
    elif sub == "monthly":
        st.header("Monthly Reports")
        st.write("Monthly trends and analytics")

elif main == "settings":
    if sub == "users":
        st.header("User Management")
        st.write("Add / remove users, edit roles.")
    elif sub == "system":
        st.header("System Settings")
        st.write("PLC connections, MES configs.")

# ------------------------------------------------------
# FOOTER (optional)
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
    <div class='custom-footer'>© 2025 MES System — Powered by Streamlit</div>"
)
