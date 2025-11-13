import streamlit as st

# Hybrid MES + Glassmorphic UI — Single file
# Copy / paste this entire file into Dashboard.py and run with Streamlit.

st.set_page_config(page_title="MES Hybrid UI", page_icon=":factory:", layout="wide")

# -----------------------------
# Hide Streamlit default chrome
# -----------------------------
HIDE = """
<style>
    /* hide built-in header/footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none}
</style>
"""
st.markdown(HIDE, unsafe_allow_html=True)

# -----------------------------
# Routing: page & sub
# -----------------------------
params = st.query_params
page = params.get("page", "dashboard")
sub  = params.get("sub", "")

# -----------------------------
# CSS (no .format or f-strings) — safe
# -----------------------------
CSS = """
<style>
:root{ --primary: #2c6bed; --muted: #f5f7fb; }
/* Glass header */
.custom-glass-header{
  position: fixed; top: 12px; left: 12px; right: 12px;
  display:flex; align-items:center; gap:16px; padding:14px 20px;
  border-radius:14px; background: rgba(255,255,255,0.6);
  backdrop-filter: blur(8px); box-shadow: 0 8px 30px rgba(10,20,50,0.08);
  z-index: 9999;
}
.custom-glass-header .brand{ font-weight:800; font-size:20px; color: #123; }
.custom-glass-header .tag{ color:#445; font-size:13px; }
.custom-glass-header .links{ margin-left:auto; display:flex; gap:10px; align-items:center; }
.custom-glass-header .links a{ text-decoration:none; padding:8px 12px; border-radius:8px; color:#123; font-weight:600 }
.custom-glass-header .links a:hover{ background: rgba(44,107,237,0.08); }

/* Left sidebar */
.left-menu{
  position: fixed; top: 120px; left: 12px; width: 240px; bottom: 12px;
  background: rgba(255,255,255,0.85); border-radius:12px; padding:14px;
  box-shadow: 3px 6px 24px rgba(10,20,50,0.06); overflow:auto; z-index:9998;
}
.left-menu .group{ margin-bottom:12px }
.left-menu summary{ list-style:none; cursor:pointer; padding:10px 12px; border-radius:8px; font-weight:700; }
.left-menu summary:hover{ background:#f0f6ff }
.left-menu a{ display:block; padding:8px 14px; margin:6px 6px; border-radius:8px; text-decoration:none; color:#123; font-weight:600 }
.left-menu a:hover{ background:#eef4ff }
.left-menu .active-main{ background: var(--primary); color:white !important }
.left-menu .sub-active{ background: #1f66d6; color:white !important }

/* Top horizontal submenu */
.top-submenu{ position: fixed; top: 86px; left: 272px; right: 20px; height:44px; display:flex; gap:12px; align-items:center; padding-left:12px; z-index:9997 }
.top-submenu a{ text-decoration:none; padding:8px 12px; border-radius:8px; color:#333; font-weight:700 }
.top-submenu a.active{ background: var(--primary); color:white }

/* shift main content to the right and below header+submenu */
.block-container{ margin-left: 272px !important; padding-top: 160px !important }

/* Footer area aligned to content */
.custom-footer{ position: fixed; bottom: 12px; left: 272px; right: 20px; padding:10px 12px; background: rgba(250,250,255,0.9); border-radius:10px; box-shadow: 0 6px 22px rgba(10,20,50,0.04); text-align:center; z-index:9996 }

/* Toggle button (small) */
.toggle-btn{ position: fixed; top: 140px; left: 12px; width:34px; height:34px; border-radius:8px; background:white; box-shadow: 0 6px 18px rgba(0,0,0,0.08); display:flex; align-items:center; justify-content:center; cursor:pointer; z-index:10000 }
.toggle-btn:hover{ transform: scale(1.03) }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Header HTML (insert logo URL via replace token)
# -----------------------------
LOGO = "https://placehold.co/64x64/png?text=Logo"
header_html = """
<div class="custom-glass-header">
  <img src="%%LOGO%%" width="56" height="56" style="border-radius:10px;" />
  <div>
    <div class="brand">MES Hybrid Application</div>
    <div class="tag">Hybrid — enterprise layout with modern styling</div>
  </div>
  <div class="links">
    <a href="?page=dashboard">Dashboard</a>
    <a href="?page=reports">Reports</a>
    <a href="?page=settings">Settings</a>
  </div>
</div>
"""
header_html = header_html.replace("%%LOGO%%", LOGO)
st.markdown(header_html, unsafe_allow_html=True)

# -----------------------------
# Toggle button (JS used for menu collapse) — minimal and safe
# -----------------------------
# We'll use a tiny inline script to toggle a class on the left-menu div.
# This is fine in Streamlit when rendered via unsafe_allow_html.

toggle_html = """
<div class="toggle-btn" onclick="(function(){var m=document.getElementById('leftMenu'); if(!m) return; m.classList.toggle('collapsed'); var cont=document.getElementsByClassName('block-container')[0]; if(!cont) return; if(m.classList.contains('collapsed')){ m.style.marginLeft='-220px'; cont.style.marginLeft='48px'; } else { m.style.marginLeft='0px'; cont.style.marginLeft='272px'; } })()">☰</div>
"""
st.markdown(toggle_html, unsafe_allow_html=True)

# -----------------------------
# Left menu (collapsible groups using <details>)
# We'll set "open" for the active page group.
# -----------------------------
left_menu_html = """
<div id="leftMenu" class="left-menu">
  <div style="font-weight:800; margin-bottom:12px; color:#123">MES Navigation</div>

  <details {DASH_OPEN}>
    <summary class="{DASH_MAIN}">📊 Dashboard</summary>
    <a href="?page=dashboard&sub=overview" class="{DASH_OV}">Overview</a>
    <a href="?page=dashboard&sub=stations" class="{DASH_ST}">Stations</a>
  </details>

  <details {REP_OPEN}>
    <summary class="{REP_MAIN}">📁 Reports</summary>
    <a href="?page=reports&sub=daily" class="{REP_D}">Daily</a>
    <a href="?page=reports&sub=monthly" class="{REP_M}">Monthly</a>
  </details>

  <details {SET_OPEN}>
    <summary class="{SET_MAIN}">⚙️ Settings</summary>
    <a href="?page=settings&sub=users" class="{SET_U}">Users</a>
    <a href="?page=settings&sub=system" class="{SET_S}">System</a>
  </details>
</div>
"""

# compute tokens
left_menu_html = left_menu_html.replace('{DASH_OPEN}', 'open' if page=='dashboard' else '')
left_menu_html = left_menu_html.replace('{REP_OPEN}', 'open' if page=='reports' else '')
left_menu_html = left_menu_html.replace('{SET_OPEN}', 'open' if page=='settings' else '')

left_menu_html = left_menu_html.replace('{DASH_MAIN}', 'active-main' if page=='dashboard' else '')
left_menu_html = left_menu_html.replace('{REP_MAIN}',  'active-main' if page=='reports' else '')
left_menu_html = left_menu_html.replace('{SET_MAIN}',  'active-main' if page=='settings' else '')

left_menu_html = left_menu_html.replace('{DASH_OV}', 'sub-active' if page=='dashboard' and sub in ('overview','') else '')
left_menu_html = left_menu_html.replace('{DASH_ST}', 'sub-active' if page=='dashboard' and sub=='stations' else '')

left_menu_html = left_menu_html.replace('{REP_D}', 'sub-active' if page=='reports' and sub=='daily' else '')
left_menu_html = left_menu_html.replace('{REP_M}', 'sub-active' if page=='reports' and sub=='monthly' else '')

left_menu_html = left_menu_html.replace('{SET_U}', 'sub-active' if page=='settings' and sub=='users' else '')
left_menu_html = left_menu_html.replace('{SET_S}', 'sub-active' if page=='settings' and sub=='system' else '')

st.markdown(left_menu_html, unsafe_allow_html=True)

# -----------------------------
# Top horizontal submenu (mirrors left sub-items)
# -----------------------------
top_sub = """
<div class="top-submenu">
  <a href="?page=dashboard&sub=overview" class="{T_D_OV}">Overview</a>
  <a href="?page=dashboard&sub=stations" class="{T_D_ST}">Stations</a>

  <a href="?page=reports&sub=daily" class="{T_R_D}">Daily</a>
  <a href="?page=reports&sub=monthly" class="{T_R_M}">Monthly</a>

  <a href="?page=settings&sub=users" class="{T_S_U}">Users</a>
  <a href="?page=settings&sub=system" class="{T_S_S}">System</a>
</div>
"""

top_sub = top_sub.replace('{T_D_OV}', 'active' if page=='dashboard' and sub in ('overview','') else '')
top_sub = top_sub.replace('{T_D_ST}', 'active' if page=='dashboard' and sub=='stations' else '')

top_sub = top_sub.replace('{T_R_D}', 'active' if page=='reports' and sub=='daily' else '')
top_sub = top_sub.replace('{T_R_M}', 'active' if page=='reports' and sub=='monthly' else '')

top_sub = top_sub.replace('{T_S_U}', 'active' if page=='settings' and sub=='users' else '')
top_sub = top_sub.replace('{T_S_S}', 'active' if page=='settings' and sub=='system' else '')

st.markdown(top_sub, unsafe_allow_html=True)

# -----------------------------
# MAIN CONTENT — placed to the right and below header/submenu
# -----------------------------
# show a clean title and content area
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

else:
    st.write('Page not found — use the left menu.')

# -----------------------------
# Footer aligned with content
# -----------------------------
st.markdown('\n')
st.markdown("""
<div class='custom-footer'>© 2025 MES Hybrid — Streamlit UI</div>
""", unsafe_allow_html=True)

# -----------------------------
# End of file
# -----------------------------
