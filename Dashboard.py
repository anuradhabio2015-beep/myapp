import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="MES App", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Session State defaults
# ---------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"
if "dark" not in st.session_state:
    st.session_state["dark"] = False
if "alerts" not in st.session_state:
    st.session_state["alerts"] = []  # list of dicts: {"text":..., "time":..., "read": False}
if "unread_count" not in st.session_state:
    st.session_state["unread_count"] = 0

# helper to push a simulated alert
def push_alert(msg=None):
    text = msg or random.choice([
        "Machine A: Temperature spike",
        "Order #421 delayed",
        "QC: 3 fails in last run",
        "New firmware available for PLC-7",
        "Shift change at 18:00"
    ])
    st.session_state["alerts"].insert(0, {"text": text, "time": datetime.now().strftime("%H:%M:%S"), "read": False})
    st.session_state["unread_count"] = sum(1 for a in st.session_state["alerts"] if not a["read"])

# mark all as read
def mark_all_read():
    for a in st.session_state["alerts"]:
        a["read"] = True
    st.session_state["unread_count"] = 0

# set page
def set_page(p):
    st.session_state["page"] = p

# toggle dark
def toggle_dark():
    st.session_state["dark"] = not st.session_state["dark"]

# simulate checking remote server for alerts (user-triggered)
def check_alerts():
    # in real app: call your API / websocket to fetch new alerts
    # here we simulate 0-2 new alerts
    for _ in range(random.randint(0, 2)):
        push_alert()
    st.experimental_rerun()

# ---------------------------
# Theme / CSS
# ---------------------------
# Use session_state['dark'] to inject theme CSS
base_css = """
<style>
:root{
    --bg: #ffffff;
    --card: #f7f9ff;
    --text: #111827;
    --accent: #2c6bed;
    --muted: #6b7280;
}
body.block-container{ background: var(--bg); }
.header-logo { width:40px;height:40px;border-radius:6px;object-fit:cover;box-shadow: 0 2px 6px rgba(0,0,0,0.12); }
.custom-header{
    position: fixed; top:0; left:0; width:100%; height:72px;
    background: var(--accent); color:white; display:flex; align-items:center;
    justify-content:space-between; padding:10px 22px; z-index:9999; box-shadow:0 3px 10px rgba(0,0,0,0.12);
}
.header-left { display:flex; align-items:center; gap:12px; }
.header-title{ font-weight:700; font-size:20px; color:white; }
.header-icons { display:flex; align-items:center; gap:10px; font-weight:600; }
.icon-link{ color:white; text-decoration:none; padding:8px 12px; border-radius:8px; display:inline-flex; align-items:center; gap:8px; transition: transform .12s ease, background .12s;}
.icon-link:hover{ transform: translateY(-3px); background: rgba(255,255,255,0.06); }
.dropdown{ position:relative; display:inline-block; }
.dropdown-btn{ background:none; border:none; color:white; font-weight:600; cursor:pointer; padding:8px 12px; border-radius:8px; }
.mega{ display:none; position:absolute; top:46px; left:0; background:white; color:var(--text); min-width:560px; padding:16px; border-radius:8px; box-shadow:0 8px 30px rgba(2,6,23,0.2); z-index:20000;}
.dropdown:hover .mega{ display:flex; gap:16px; }
.mega .col{ min-width:170px; }
.mega h4{ margin:0 0 8px 0; font-size:14px; color:var(--text); }
.mega a{ display:block; padding:6px 8px; color:var(--muted); text-decoration:none; border-radius:6px; transition: background .12s, color .12s; }
.mega a:hover{ background: #f3f6ff; color:var(--text); transform: translateX(6px); }

.profile-dropdown{ position:relative; display:inline-block; }
.profile-content{ display:none; position:absolute; right:0; top:46px; background:white; color:var(--text); min-width:160px; border-radius:8px; box-shadow:0 8px 30px rgba(2,6,23,0.2); z-index:20000; }
.profile-dropdown:hover .profile-content{ display:block; }
.profile-content a{ display:block; padding:10px 12px; color:var(--muted); text-decoration:none; }
.profile-content a:hover{ background:#f3f6ff; color:var(--text); }

.left-nav{
    position: fixed; left:10px; top:96px; width:64px; height:calc(100% - 170px);
    background: transparent; display:flex; flex-direction:column; gap:10px; align-items:center; z-index:9000;
}
.nav-button{
    width:56px; height:56px; border-radius:12px; display:flex; align-items:center; justify-content:center; cursor:pointer;
    background: rgba(44,107,237,0.08); color:var(--accent); font-weight:700; transition: transform .12s, box-shadow .12s;
}
.nav-button:hover{ transform: translateY(-6px); box-shadow: 0 10px 20px rgba(44,107,237,0.12); background: var(--accent); color:white; }
.nav-active{ background: var(--accent); color:white; box-shadow: 0 10px 20px rgba(44,107,237,0.16); }

.content-wrap{ padding: 110px 36px 80px 110px; } /* leave space for header + left nav + footer */

.breadcrumb{ font-size:13px; color:var(--muted); margin-bottom:12px; }
.card{ background:var(--card); padding:18px; border-radius:12px; box-shadow: 0 6px 20px rgba(2,6,23,0.04); color:var(--text); }

.custom-footer{
    position:fixed; bottom:0; left:0; width:100%; background:var(--accent); color:white; text-align:center; padding:10px; z-index:9999;
}

/* notification badge */
.badge{ background:#ff3b30; color:white; min-width:20px; height:20px; padding:2px 6px; border-radius:999px; font-size:12px; display:inline-flex; align-items:center; justify-content:center; margin-left:6px; }

/* hover animation for cards */
.card:hover{ transform: translateY(-6px); transition: transform .18s ease, box-shadow .18s; box-shadow: 0 22px 40px rgba(2,6,23,0.08); }

/* small responsive tweaks */
@media(max-width:900px){
  .content-wrap{ padding-left: 84px; }
  .left-nav{ left:6px; }
}
</style>
"""

dark_css = """
<style>
:root{
    --bg: #0b1220;
    --card: #071328;
    --text: #e6eef8;
    --accent: #2c6bed;
    --muted: #9aa6bf;
}
</style>
"""

# Inject base CSS and conditional dark CSS
st.markdown(base_css, unsafe_allow_html=True)
if st.session_state["dark"]:
    st.markdown(dark_css, unsafe_allow_html=True)

# ---------------------------
# Header HTML (renders top bar)
# ---------------------------
header_html = """
<div>
    <div>
        <div>
        </div>
    </div>
</div>

<a class="icon-link" href="?page=settings">⚙️ Settings</a>

<div style="position:relative;">
  <button class="icon-link" onclick="document.querySelector('#alerts').scrollIntoView();">
    🔔 Notifications
  </button>
</div>

<div class="profile-dropdown" style="margin-left:6px;">
  <button class="dropdown-btn">👤 Rahul ▼</button>
  <div class="profile-content">
    <a href="?page=profile">Profile</a>
    <a href="?page=logout">Logout</a>
  </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)



# ---------------------------
# Left vertical icon nav
# ---------------------------
left_nav_html = """
<div class="left-nav">
  <div onclick="window.location='?page=dashboard'" class="nav-button" id="nav-dashboard" title="Dashboard">🏠</div>
  <div onclick="window.location='?page=reports'" class="nav-button" id="nav-reports" title="Reports">📁</div>
  <div onclick="window.location='?page=settings'" class="nav-button" id="nav-settings" title="Settings">⚙️</div>
  <div onclick="window.location='?page=profile'" class="nav-button" id="nav-profile" title="Profile">👤</div>
</div>
"""
st.markdown(left_nav_html, unsafe_allow_html=True)

# ---------------------------
# Invisible controls for Dark toggle to integrate with Streamlit
# (we use a hidden st.button to toggle and a visible control below)
# ---------------------------
# create an invisible control used by header JS hook (we emulate using a visible toggle below)
if "dark_toggle_trigger" not in st.session_state:
    st.session_state["dark_toggle_trigger"] = 0

# PUT primary content inside content-wrap
st.markdown("<div class='content-wrap'>", unsafe_allow_html=True)

# Breadcrumb
page = st.session_state["page"]  # keep single source truth
# if URL param sets page, allow it (user may have clicked header links)
params = st.experimental_get_query_params()
if "page" in params:
    st.session_state["page"] = params.get("page")[0]
    page = st.session_state["page"]

# show breadcrumb
breadcrumb_map = {
    "dashboard": "Home / Dashboard",
    "daily": "Home / Reports / Daily",
    "shift": "Home / Reports / Shift",
    "quality": "Home / Reports / Quality",
    "reports": "Home / Reports",
    "settings": "Home / Settings",
    "profile": "Home / Profile",
    "logout": "Home / Logout",
    "order": "Home / Reports / Order trace",
    "pm": "Home / Reports / Maintenance / Preventive",
    "cm": "Home / Reports / Maintenance / Corrective",
    "spares": "Home / Reports / Maintenance / Spares",
    "nc": "Home / Reports / Quality / Non-conformance",
    "metrology": "Home / Reports / Quality / Metrology"
}
crumb = breadcrumb_map.get(page, "Home / " + page.title())
st.markdown(f"<div class='breadcrumb'>{crumb}</div>", unsafe_allow_html=True)

# Top controls row (Dark mode toggle & Check alerts)
col1, col2, col3 = st.columns([1,2,7])
with col1:
    if st.button("🌓 Toggle theme"):
        toggle_dark()
        st.experimental_rerun()
with col2:
    if st.button("🔔 Check alerts"):
        check_alerts()
with col3:
    if st.button("Mark all alerts read"):
        mark_all_read()

# MAIN PAGE CONTENT
if page == "dashboard":
    st.markdown("<div class='card'><h3>Production Overview</h3><p>Realtime KPIs, machine status and throughput.</p></div>", unsafe_allow_html=True)
    st.write("")  # spacer
    # sample two columns
    a,b = st.columns(2)
    with a:
        st.markdown("<div class='card'><h4>OEE</h4><p>85% (target 90%)</p></div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='card'><h4>Throughput</h4><p>1,240 units / day</p></div>", unsafe_allow_html=True)

elif page in ("reports","daily","shift","quality","order","pm","cm","spares","nc","metrology"):
    st.markdown("<div class='card'><h3>Reports</h3><p>Choose a report from the header mega menu or the left nav.</p></div>", unsafe_allow_html=True)
    # sample table
    st.table({
        "Metric":["Produced","Rejected","Uptime"],
        "Value":[1240, 32, "96%"]
    })

elif page == "settings":
    st.markdown("<div class='card'><h3>Settings</h3><p>System & user settings.</p></div>", unsafe_allow_html=True)

elif page == "profile":
    st.markdown("<div class='card'><h3>User Profile</h3><p>Name: Rahul</p><p>Role: Technical Lead</p></div>", unsafe_allow_html=True)

elif page == "logout":
    st.warning("You have been logged out (simulated).")
    # in real app: clear session / call API

# Alerts area / notification panel rendered in page
st.markdown("<hr />", unsafe_allow_html=True)
st.markdown("<h4 id='alerts'>🔔 Notifications</h4>", unsafe_allow_html=True)

if len(st.session_state["alerts"]) == 0:
    st.info("No notifications. Click 'Check alerts' to simulate new messages.")
else:
    for idx, a in enumerate(st.session_state["alerts"]):
        status = "🔴" if not a["read"] else "⚪"
        st.markdown(f"<div class='card' style='margin-bottom:8px;'><b>{status} {a['text']}</b><div style='font-size:12px;color:var(--muted);margin-top:6px;'>Time: {a['time']}</div></div>", unsafe_allow_html=True)

# small control to add simulated alert (dev)
if st.button("Simulate new alert"):
    push_alert()
    st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)  # spacing so footer doesn't overlap
st.markdown("<div class='custom-footer'>© 2025 MES System | Powered by Python + Streamlit</div>", unsafe_allow_html=True)

# ---- Sync left-nav active style (small JS injection to highlight active)
active_js = f"""
<script>
try {{
  const page = "{st.session_state['page']}";
  document.querySelectorAll('.nav-button').forEach(el=>el.classList.remove('nav-active'));
  const map = {{
    'dashboard':'nav-dashboard',
    'reports':'nav-reports',
    'settings':'nav-settings',
    'profile':'nav-profile'
  }};
  const id = map[page];
  if(document.getElementById(id)) document.getElementById(id).classList.add('nav-active');
}} catch(e) {{console.log(e)}}
</script>
"""
st.markdown(active_js, unsafe_allow_html=True)
