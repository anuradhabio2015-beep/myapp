import streamlit as st

# ------------------------------------------------------
# CLEAN + STABLE HYBRID MES UI (ENTERPRISE + MODERN)
# 100% FIXED — NO OVERLAPS, NO BROKEN LAYOUT
# ------------------------------------------------------

st.set_page_config(page_title="MES Hybrid UI", page_icon=":factory:", layout="wide")

# -----------------------------
# Hide Streamlit default chrome
# -----------------------------
HIDE = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none}
</style>
"""
st.markdown(HIDE, unsafe_allow_html=True)

# -----------------------------
# Routing
# -----------------------------
params = st.query_params
page = params.get("page", "dashboard")
sub  = params.get("sub", "")

# -----------------------------
# Stable CSS (no f-strings inside)
# -----------------------------
CSS = """
<style>
:root{
    --primary: #2c6bed;
    --text: #1d1d1f;
    --card-bg: #ffffff;
    --sidebar: #f8faff;
    --shadow: rgba(0,0,0,0.06);
}

/* ---------------- HEADER ---------------- */
.header {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 72px;
    background: white;
    box-shadow: 0 4px 14px var(--shadow);
    display: flex;
    align-items: center;
    padding: 0 24px;
    z-index: 9999;
}
.header img {
    border-radius: 8px;
    margin-right: 14px;
}
.header-title{ font-size:22px; font-weight:800; color:var(--text); }
.header-sub{ font-size:13px; color:#666; margin-top:-4px; }
.header-links{ margin-left:auto; display:flex; gap:20px; }
.header-links a{
    text-decoration:none;
    font-weight:700;
    color:#111;
    padding:6px 8px;
    border-radius:6px;
}
.header-links a:hover{ background:#eef3ff; }

/* --------------- TOP SUBMENU ---------------- */
.submenu{
    position: fixed;
    top: 72px;
    left: 260px; right: 0;
    height: 48px;
    display:flex;
    align-items:center;
    gap:14px;
    background:white;
    border-bottom:1px solid #ececec;
    padding-left:18px;
    z-index:9998;
}
.submenu a{
    text-decoration:none;
    padding:8px 14px;
    border-radius:6px;
    font-weight:700;
    color:#333;
}
.submenu .active{ background:var(--primary); color:white; }

/* --------------- SIDEBAR ---------------- */
.sidebar{
    position: fixed;
    top: 72px; left: 0;
    width: 260px; bottom: 0;
    background: var(--sidebar);
    padding: 20px 16px;
    overflow-y:auto;
    box-shadow: 2px 0 12px var(--shadow);
    z-index: 9997;
}
.sidebar-title{
    font-size:18px;
    font-weight:800;
    margin-bottom:12px;
}
.sidebar details{ margin-bottom:12px; }
.sidebar summary{
    padding:10px 12px;
    border-radius:8px;
    cursor:pointer;
    font-weight:700;
    color:#222;
}
.sidebar summary:hover{ background:#eef4ff; }

.sidebar a{
    display:block;
    padding:8px 18px;
    font-weight:600;
    border-radius:8px;
    margin:4px 0;
    text-decoration:none;
    color:#333;
}
.sidebar a:hover{ background:#e7edff; }
.sidebar .active-main{ background:var(--primary); color:white !important; }
.sidebar .sub-active{ background:#155cd6; color:white !important; }

/* --------------- MAIN CONTENT -------------- */
.block-container{
    margin-left: 280px !important;
    padding-top: 140px !important;
}

/* --------------- FOOTER -------------- */
.footer{
    position: fixed;
    bottom: 0; left: 280px; right: 0;
    padding: 12px;
    background:white;
    text-align:center;
    border-top:1px solid #ddd;
    font-size:13px;
    box-shadow:0 -2px 10px var(--shadow);
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
HEADER = """
<div class="header">
  <img src="https://placehold.co/56x56?text=Logo" width="56" height="56" />
  <div>
    <div class="header-title">MES Hybrid Application</div>
    <div class="header-sub">Hybrid — enterprise layout with modern styling</div>
  </div>
  <div class="header-links">
    <a href="?page=dashboard">Dashboard</a>
    <a href="?page=reports">Reports</a>
    <a href="?page=settings">Settings</a>
  </div>
</div>
"""
st.markdown(HEADER, unsafe_allow_html=True)

# -----------------------------
# Submenu
# -----------------------------
sub_html = """
<div class="submenu">
  <a href="?page=dashboard&sub=overview" class="{D_OV}">Overview</a>
  <a href="?page=dashboard&sub=stations" class="{D_ST}">Stations</a>

  <a href="?page=reports&sub=daily" class="{R_D}">Daily</a>
  <a href="?page=reports&sub=monthly" class="{R_M}">Monthly</a>

  <a href="?page=settings&sub=users" class="{S_U}">Users</a>
  <a href="?page=settings&sub=system" class="{S_S}">System</a>
</div>
"""

sub_html = sub_html.replace('{D_OV}', 'active' if page=='dashboard' and sub in ('overview','') else '')
sub_html = sub_html.replace('{D_ST}', 'active' if page=='dashboard' and sub=='stations' else '')
sub_html = sub_html.replace('{R_D}', 'active' if page=='reports' and sub=='daily' else '')
sub_html = sub_html.replace('{R_M}', 'active' if page=='reports' and sub=='monthly' else '')
sub_html = sub_html.replace('{S_U}', 'active' if page=='settings' and sub=='users' else '')
sub_html = sub_html.replace('{S_S}', 'active' if page=='settings' and sub=='system' else '')

st.markdown(sub_html, unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
sidebar = """
<div class="sidebar">
  <div class="sidebar-title">Navigation</div>

  <details {D_OPEN}>
    <summary class="{D_MAIN}">📊 Dashboard</summary>
    <a href="?page=dashboard&sub=overview" class="{D_OV}">Overview</a>
    <a href="?page=dashboard&sub=stations" class="{D_ST}">Stations</a>
  </details>

  <details {R_OPEN}>
    <summary class="{R_MAIN}">📁 Reports</summary>
    <a href="?page=reports&sub=daily" class="{R_D}">Daily</a>
    <a href="?page=reports&sub=monthly" class="{R_M}">Monthly</a>
  </details>

  <details {S_OPEN}>
    <summary class="{S_MAIN}">⚙️ Settings</summary>
    <a href="?page=settings&sub=users" class="{S_U}">Users</a>
    <a href="?page=settings&sub=system" class="{S_S}">System</a>
  </details>
</div>
"""

sidebar = sidebar.replace('{D_OPEN}', 'open' if page=='dashboard' else '')
sidebar = sidebar.replace('{R_OPEN}', 'open' if page=='reports' else '')
sidebar = sidebar.replace('{S_OPEN}', 'open' if page=='settings' else '')

sidebar = sidebar.replace('{D_MAIN}', 'active-main' if page=='dashboard' else '')
sidebar = sidebar.replace('{R_MAIN}', 'active-main' if page=='reports' else '')
sidebar = sidebar.replace('{S_MAIN}', 'active-main' if page=='settings' else '')

sidebar = sidebar.replace('{D_OV}', 'sub-active' if page=='dashboard' and sub in ('overview','') else '')
sidebar = sidebar.replace('{D_ST}', 'sub-active' if page=='dashboard' and sub=='stations' else '')
sidebar = sidebar.replace('{R_D}', 'sub-active' if page=='reports' and sub=='daily' else '')
sidebar = sidebar.replace('{R_M}', 'sub-active' if page=='reports' and sub=='monthly' else '')
sidebar = sidebar.replace('{S_U}', 'sub-active' if page=='settings' and sub=='users' else '')
sidebar = sidebar.replace('{S_S}', 'sub-active' if page=='settings' and sub=='system' else '')

st.markdown(sidebar, unsafe_allow_html=True)

# -----------------------------
# MAIN CONTENT
# -----------------------------
title_text = page.capitalize() + (f" — {sub.capitalize()}" if sub else "")
st.title(title_text)

if page == 'dashboard':
    if sub in ('overview',''):
        st.header('Overview')
        st.write('Summary KPIs, throughput, OEE, etc.')
    elif sub == 'stations':
        st.header('Stations')
        st.write('Station list, status, alarms, cycle times.')

elif page == 'reports':
    if sub == 'daily':
        st.header('Daily Reports')
        st.write('Daily production, shift summary.')
    elif sub == 'monthly':
        st.header('Monthly Reports')
        st.write('Monthly trends, paretos, scrap analysis.')

elif page == 'settings':
    if sub == 'users':
        st.header('User Management')
        st.write('Create / edit users, roles, permissions.')
    elif sub == 'system':
        st.header('System Configuration')
        st.write('Integrations, PLC connections, system params.')

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class='footer'>© 2025 MES Hybrid — Streamlit UI</div>
""", unsafe_allow_html=True)
