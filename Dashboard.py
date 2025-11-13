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
# ROUTING
# -------------------------------------------------------
params = st.query_params
page = params.get("page", "dashboard")
sub  = params.get("sub", "")

# -------------------------------------------------------
# TOP HEADER + TOP SUBMENU
# -------------------------------------------------------
top_header = """
    <style>
        .top-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 64px;
            background-color: #2c6bed;
            color: white;
            padding: 12px 20px;
            font-size: 20px;
            font-weight: 700;
            z-index: 9999;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .top-submenu {
            position: fixed;
            top: 64px;
            left: 230px;
            right: 0;
            height: 44px;
            background: #f7f9ff;
            display: flex;
            align-items: center;
            padding-left: 20px;
            gap: 16px;
            border-bottom: 1px solid #e6e6e6;
            z-index: 9998;
        }

        .top-submenu a {
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 6px;
            color: #333;
            font-weight: 600;
        }

        .top-submenu a.active {
            background: #2c6bed;
            color: white;
        }

        .block-container {
            padding-top: 120px !important;
            margin-left: 230px !important;
        }
    </style>

    <div class="top-header">
        <div>MES Application</div>
        <div style="margin-right: 30px;">Dashboard | Reports | Settings</div>
    </div>

    <div class="top-submenu">
        <a href="?page=dashboard&sub=overview" class="{dashboard_overview}">Overview</a>
        <a href="?page=dashboard&sub=stations" class="{dashboard_stations}">Stations</a>

        <a href="?page=reports&sub=daily" class="{reports_daily}">Daily</a>
        <a href="?page=reports&sub=monthly" class="{reports_monthly}">Monthly</a>

        <a href="?page=settings&sub=users" class="{settings_users}">Users</a>
        <a href="?page=settings&sub=system" class="{settings_system}">System</a>
    </div>
"""

# ACTIVE STATES FOR TOP SUBMENU
top_header = top_header.format(
    dashboard_overview="active" if page=="dashboard" and sub in ["overview", ""] else "",
    dashboard_stations="active" if page=="dashboard" and sub=="stations" else "",
    reports_daily="active" if page=="reports" and sub=="daily" else "",
    reports_monthly="active" if page=="reports" and sub=="monthly" else "",
    settings_users="active" if page=="settings" and sub=="users" else "",
    settings_system="active" if page=="settings" and sub=="system" else "",
)

st.markdown(top_header, unsafe_allow_html=True)

# -------------------------------------------------------
# LEFT SIDEBAR (SAFE—NO F-STRING)
# -------------------------------------------------------
left_menu = """
    <style>
        .left-menu {
            position: fixed;
            top: 0;
            left: 0;
            width: 230px;
            height: 100%;
            background: #f5f7ff;
            padding-top: 12px;
            box-shadow: 2px 0 6px rgba(0,0,0,0.1);
            z-index: 9998;
        }

        .brand {
            padding: 14px 18px;
            font-size: 18px;
            font-weight: 800;
            color: #2c6bed;
        }

        details {
            margin: 6px 10px;
            padding: 4px;
        }

        summary {
            padding: 10px 12px;
            font-weight: 700;
            cursor: pointer;
            border-radius: 6px;
            list-style: none;
        }

        summary:hover {
            background: #dfe8ff;
        }

        .sub-item {
            display: block;
            padding: 8px 24px;
            text-decoration: none;
            color: #222;
            margin: 4px 0;
            border-radius: 6px;
            font-weight: 600;
        }

        .sub-item:hover {
            background: #edf2ff;
        }

        .active-main {
            background: #2c6bed !important;
            color: white !important;
        }

        .sub-active {
            background: #1f66d6 !important;
            color: white !important;
        }
    </style>

    <div class="left-menu">
        <div class="brand">MES Application</div>

        <details open>
            <summary class="active-main">📊 Dashboard</summary>
            <a href="?page=dashboard&sub=overview" class="sub-item {dash_ov}">Overview</a>
            <a href="?page=dashboard&sub=stations" class="sub-item {dash_st}">Stations</a>
        </details>

        <details>
            <summary class="{reports_active}">📁 Reports</summary>
            <a href="?page=reports&sub=daily" class="sub-item {rep_d}">Daily</a>
            <a href="?page=reports&sub=monthly" class="sub-item {rep_m}">Monthly</a>
        </details>

        <details>
            <summary class="{settings_active}">⚙️ Settings</summary>
            <a href="?page=settings&sub=users" class="sub-item {set_u}">Users</a>
            <a href="?page=settings&sub=system" class="sub-item {set_s}">System</a>
        </details>
    </div>
"""

# APPLY ACTIVE CLASSES
left_menu = left_menu.format(
    dash_ov="sub-active" if sub in ["overview",""] and page=="dashboard" else "",
    dash_st="sub-active" if sub=="stations" and page=="dashboard" else "",

    reports_active="active-main" if page=="reports" else "",
    rep_d="sub-active" if sub=="daily" and page=="reports" else "",
    rep_m="sub-active" if sub=="monthly" and page=="reports" else "",

    settings_active="active-main" if page=="settings" else "",
    set_u="sub-active" if sub=="users" and page=="settings" else "",
    set_s="sub-active" if sub=="system" and page=="settings" else "",
)

st.markdown(left_menu, unsafe_allow_html=True)

# -------------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------------
st.title(f"{page.capitalize()} - {sub.capitalize() if sub else ''}")

if page == "dashboard":
    if sub in ["overview", ""]:
        st.subheader("Overview")
        st.write("Dashboard Overview Content…")
    elif sub == "stations":
        st.subheader("Stations")
        st.write("Station details, status, KPIs…")

elif page == "reports":
    if sub == "daily":
        st.subheader("Daily Reports")
    elif sub == "monthly":
        st.subheader("Monthly Reports")

elif page == "settings":
    if sub == "users":
        st.subheader("User Management")
    elif sub == "system":
        st.subheader("System Settings")

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 230px;
            width: calc(100% - 230px);
            text-align: center;
            background: #e8ecff;
            padding: 8px;
            border-top: 1px solid #d0d7ff;
            color:#333;
        }
    </style>
    <div class="footer">© 2025 MES System | Streamlit UI</div>
    """,
    unsafe_allow_html=True
)
