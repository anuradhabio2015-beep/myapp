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
# TOP HEADER + TOP SUBMENU (use token placeholders)
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
        <a href="?page=dashboard&sub=overview" class="%%DASH_OVERVIEW%%">Overview</a>
        <a href="?page=dashboard&sub=stations" class="%%DASH_STATIONS%%">Stations</a>

        <a href="?page=reports&sub=daily" class="%%REPORTS_DAILY%%">Daily</a>
        <a href="?page=reports&sub=monthly" class="%%REPORTS_MONTHLY%%">Monthly</a>

        <a href="?page=settings&sub=users" class="%%SETTINGS_USERS%%">Users</a>
        <a href="?page=settings&sub=system" class="%%SETTINGS_SYSTEM%%">System</a>
    </div>
"""

# compute token values for top submenu
top_header = top_header.replace("%%DASH_OVERVIEW%%", "active" if page=="dashboard" and sub in ["overview", ""] else "")
top_header = top_header.replace("%%DASH_STATIONS%%", "active" if page=="dashboard" and sub=="stations" else "")
top_header = top_header.replace("%%REPORTS_DAILY%%", "active" if page=="reports" and sub=="daily" else "")
top_header = top_header.replace("%%REPORTS_MONTHLY%%", "active" if page=="reports" and sub=="monthly" else "")
top_header = top_header.replace("%%SETTINGS_USERS%%", "active" if page=="settings" and sub=="users" else "")
top_header = top_header.replace("%%SETTINGS_SYSTEM%%", "active" if page=="settings" and sub=="system" else "")

st.markdown(top_header, unsafe_allow_html=True)

# -------------------------------------------------------
# LEFT SIDEBAR (use token placeholders again)
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
            overflow: auto;
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

        <details %%DASH_OPEN%%>
            <summary class="%%DASH_MAIN_ACTIVE%%">📊 Dashboard</summary>
            <a href="?page=dashboard&sub=overview" class="sub-item %%DASH_OV%%">Overview</a>
            <a href="?page=dashboard&sub=stations" class="sub-item %%DASH_ST%%">Stations</a>
        </details>

        <details %%REP_OPEN%%>
            <summary class="%%REP_MAIN_ACTIVE%%">📁 Reports</summary>
            <a href="?page=reports&sub=daily" class="sub-item %%REP_D%%">Daily</a>
            <a href="?page=reports&sub=monthly" class="sub-item %%REP_M%%">Monthly</a>
        </details>

        <details %%SET_OPEN%%>
            <summary class="%%SET_MAIN_ACTIVE%%">⚙️ Settings</summary>
            <a href="?page=settings&sub=users" class="sub-item %%SET_U%%">Users</a>
            <a href="?page=settings&sub=system" class="sub-item %%SET_S%%">System</a>
        </details>
    </div>
"""

# compute left menu tokens
# open the group if it's the current page, otherwise closed
left_menu = left_menu.replace("%%DASH_OPEN%%", "open" if page=="dashboard" else "")
left_menu = left_menu.replace("%%REP_OPEN%%", "open" if page=="reports" else "")
left_menu = left_menu.replace("%%SET_OPEN%%", "open" if page=="settings" else "")

left_menu = left_menu.replace("%%DASH_MAIN_ACTIVE%%", "active-main" if page=="dashboard" else "")
left_menu = left_menu.replace("%%REP_MAIN_ACTIVE%%", "active-main" if page=="reports" else "")
left_menu = left_menu.replace("%%SET_MAIN_ACTIVE%%", "active-main" if page=="settings" else "")

left_menu = left_menu.replace("%%DASH_OV%%", "sub-active" if page=="dashboard" and sub in ["overview", ""] else "")
left_menu = left_menu.replace("%%DASH_ST%%", "sub-active" if page=="dashboard" and sub=="stations" else "")

left_menu = left_menu.replace("%%REP_D%%", "sub-active" if page=="reports" and sub=="daily" else "")
left_menu = left_menu.replace("%%REP_M%%", "sub-active" if page=="reports" and sub=="monthly" else "")

left_menu = left_menu.replace("%%SET_U%%", "sub-active" if page=="settings" and sub=="users" else "")
left_menu = left_menu.replace("%%SET_S%%", "sub-active" if page=="settings" and sub=="system" else "")

st.markdown(left_menu, unsafe_allow_html=True)

# -------------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------------
# Title shown on the content area
display_title = f"{page.capitalize()}" + (f" — {sub.capitalize()}" if sub else "")
st.title(display_title)

if page == "dashboard":
    if sub in ["overview", ""]:
        st.subheader("Overview")
        st.write("Summary KPIs, throughput, OEE, etc.")
    elif sub == "stations":
        st.subheader("Stations")
        st.write("Station list, status, alarms, cycle times.")

elif page == "reports":
    st.subheader("Reports")
    if sub == "daily":
        st.write("Daily production, shift summary.")
    elif sub == "monthly":
        st.write("Monthly trends, paretos, scrap analysis.")
    else:
        st.write("Select a report from the submenu.")

elif page == "settings":
    st.subheader("Settings")
    if sub == "users":
        st.write("Create / edit users, roles, permissions.")
    elif sub == "system":
        st.write("Integrations, PLC connections, system params.")
    else:
        st.write("Select a settings option from the submenu.")

else:
    st.write("Page not found — use the left menu.")

# -------------------------------------------------------
# FOOTER (aligned with content area)
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
            z-index: 9996;
        }
    </style>
    <div class="footer">© 2025 MES System | Streamlit UI</div>
    """,
    unsafe_allow_html=True,
)
