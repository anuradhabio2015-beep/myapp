
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
# ROUTING: page & sub
# -------------------------------------------------------
params = st.experimental_get_query_params()

page = params.get("page", ["dashboard"])[0]
sub  = params.get("sub", [""])[0]



# -------------------------------------------------------
# TOP HEADER + HORIZONTAL SUB-MENU (below header)
# -------------------------------------------------------
top_header = f"""
    <style>
        /* top header */
        .top-header {{
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
            box-shadow: 0px 2px 4px rgba(0,0,0,0.15);
        }}

        /* horizontal sub menu below header */
        .top-submenu {{
            position: fixed;
            top: 64px;
            left: 230px;             /* same as left sidebar width */
            right: 0;
            height: 44px;
            background: linear-gradient(90deg, rgba(255,255,255,0.98), rgba(250,250,250,0.98));
            display: flex;
            align-items: center;
            padding-left: 18px;
            gap: 14px;
            border-bottom: 1px solid #ececec;
            z-index: 9997;
        }}

        .top-submenu a {{
            text-decoration: none;
            color: #444;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
        }}

        .top-submenu a:hover {{
            background: #eef4ff;
            color: #0b3ea6;
        }}

        .top-submenu .active {{
            background: #2c6bed;
            color: white !important;
        }}

        /* push main Streamlit content below header + submenu and right of sidebar */
        .block-container {{
            padding-top: 120px !important; /* header (64) + submenu (44) + gap */
            margin-left: 230px !important;  /* width of left sidebar */
            margin-right: 20px !important;
        }}
    </style>

    <div class="top-header">
        <div>MES Application</div>
        <div style="margin-right: 30px; font-weight: 600;">
            <a style="color:white; text-decoration:none;" href="?page=dashboard">Dashboard</a>
        </div>
    </div>

    <div class="top-submenu">
        <!-- dashboard subs -->
        <a class="{('active' if (page=='dashboard' and sub in ['overview','stations',''] ) else '')}" href="?page=dashboard&sub=overview">Overview</a>
        <a class="{('active' if (page=='dashboard' and sub=='stations') else '')}" href="?page=dashboard&sub=stations">Stations</a>

        <!-- reports subs -->
        <a class="{('active' if (page=='reports' and sub=='daily') else '')}" href="?page=reports&sub=daily">Daily</a>
        <a class="{('active' if (page=='reports' and sub=='monthly') else '')}" href="?page=reports&sub=monthly">Monthly</a>

        <!-- settings subs -->
        <a class="{('active' if (page=='settings' and sub=='users') else '')}" href="?page=settings&sub=users">Users</a>
        <a class="{('active' if (page=='settings' and sub=='system') else '')}" href="?page=settings&sub=system">System</a>
    </div>
"""
st.markdown(top_header, unsafe_allow_html=True)


# -------------------------------------------------------
# LEFT SIDEBAR with collapsible sub-menus (DETAILS/SUMMARY)
# -------------------------------------------------------
# compute active classes for main and sub items
dash_active = "active" if page == "dashboard" else ""
rep_active  = "active" if page == "reports" else ""
set_active  = "active" if page == "settings" else ""

dash_sub_overview = "sub-active" if (page=="dashboard" and sub in ["overview",""]) else ""
dash_sub_stations = "sub-active" if (page=="dashboard" and sub=="stations") else ""

rep_sub_daily  = "sub-active" if (page=="reports" and sub=="daily") else ""
rep_sub_monthly= "sub-active" if (page=="reports" and sub=="monthly") else ""

set_sub_users  = "sub-active" if (page=="settings" and sub=="users") else ""
set_sub_system = "sub-active" if (page=="settings" and sub=="system") else ""

left_menu = """
    <style>
        .left-menu {
            position: fixed;
            top: 0;
            left: 0;
            width: 230px;
            height: 100%;
            background-color: #f8fbff;
            padding-top: 12px;
            box-shadow: 2px 0px 6px rgba(0,0,0,0.06);
            z-index: 9998;
            overflow: auto;
        }
        ...
    </style>

    <div class="left-menu">
        <div class="brand">MES Application</div>

        <details open>
            <summary class="menu-link {dash_active}">📊 Dashboard</summary>
            <a class="sub-item {dash_sub_overview}" href="?page=dashboard&sub=overview">Overview</a>
            <a class="sub-item {dash_sub_stations}" href="?page=dashboard&sub=stations">Stations</a>
        </details>

        <details>
            <summary class="menu-link {rep_active}">📁 Reports</summary>
            <a class="sub-item {rep_sub_daily}" href="?page=reports&sub=daily">Daily</a>
            <a class="sub-item {rep_sub_monthly}" href="?page=reports&sub=monthly">Monthly</a>
        </details>

        <details>
            <summary class="menu-link {set_active}">⚙️ Settings</summary>
            <a class="sub-item {set_sub_users}" href="?page=settings&sub=users">Users</a>
            <a class="sub-item {set_sub_system}" href="?page=settings&sub=system">System</a>
        </details>
    </div>
""".format(
    dash_active=dash_active,
    dash_sub_overview=dash_sub_overview,
    dash_sub_stations=dash_sub_stations,
    rep_active=rep_active,
    rep_sub_daily=rep_sub_daily,
    rep_sub_monthly=rep_sub_monthly,
    set_active=set_active,
    set_sub_users=set_sub_users,
    set_sub_system=set_sub_system
)


# -------------------------------------------------------
# MAIN CONTENT AREA (right side) — show based on page & sub
# -------------------------------------------------------
def show_dashboard(subpage):
    st.header("📊 Dashboard")
    if subpage in ["overview", ""]:
        st.subheader("Overview")
        st.write("Summary KPIs, throughput, OEE, etc.")
    elif subpage == "stations":
        st.subheader("Stations")
        st.write("Station list, status, alarms, cycle times.")

def show_reports(subpage):
    st.header("📁 Reports")
    if subpage == "daily":
        st.subheader("Daily Reports")
        st.write("Daily production, shift summary.")
    elif subpage == "monthly":
        st.subheader("Monthly Reports")
        st.write("Monthly trends, paretos, scrap analysis.")
    else:
        st.write("Select a report from the submenu.")

def show_settings(subpage):
    st.header("⚙️ Settings")
    if subpage == "users":
        st.subheader("User Management")
        st.write("Create / edit users, roles, permissions.")
    elif subpage == "system":
        st.subheader("System Configuration")
        st.write("Integrations, PLC connections, system params.")
    else:
        st.write("Select a settings option from the submenu.")


if page == "dashboard":
    show_dashboard(sub)
elif page == "reports":
    show_reports(sub)
elif page == "settings":
    show_settings(sub)
else:
    st.write("Page not found — use the left menu.")


# -------------------------------------------------------
# OPTIONAL FOOTER (aligned with content area)
# -------------------------------------------------------
custom_footer = """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 230px;   /* aligned under content area */
            width: calc(100% - 230px);
            background-color: #f1f5ff;
            color: #333;
            text-align: center;
            padding: 10px;
            font-size: 13px;
            z-index: 9996;
            border-top: 1px solid #e6ecff;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
