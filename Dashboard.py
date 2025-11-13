import streamlit as st

# -------------------------------------
# PAGE CONFIG
# -------------------------------------
st.set_page_config(page_title="MES Hybrid SPA", layout="wide")

# -------------------------------------
# HIDE STREAMLIT DEFAULT CHROME
# -------------------------------------
st.markdown("""
<style>
#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------
# SESSION STATE FOR SPA NAVIGATION
# -------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "sub" not in st.session_state:
    st.session_state.sub = "overview"

def goto(page=None, sub=None):
    if page:
        st.session_state.page = page
    if sub:
        st.session_state.sub = sub

# -------------------------------------
# HEADER
# -------------------------------------
st.markdown("""
<style>
.header {
    position: fixed;
    top:0; left:0; right:0;
    height: 72px;
    background:white;
    display:flex;
    align-items:center;
    padding:0 20px;
    box-shadow:0 4px 14px rgba(0,0,0,0.08);
    z-index:9999;
}
.header-title {
    font-size:24px;
    font-weight:800;
    margin-left:16px;
}
.block-container { padding-top:120px !important; }
</style>

<div class="header">
    <img src="https://placehold.co/58x58?text=Logo" style="border-radius:10px"/>
    <div class="header-title">MES Hybrid UI — SPA Mode</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------
# TOP SUBMENU (acts like tabs)
# -------------------------------------
submenu_items = {
    "dashboard": ["overview", "stations"],
    "reports": ["daily", "monthly"],
    "settings": ["users", "system"],
}

st.markdown("""
<style>
.submenu {
    position: fixed;
    top: 72px;
    left: 260px;
    right: 0;
    height:48px;
    padding-left:16px;
    display:flex; gap:16px;
    align-items:center;
    background:white;
    border-bottom:1px solid #eee;
    z-index:9998;
}
.sub-btn {
    padding:8px 16px;
    border-radius:6px;
    background:#f0f2ff;
    font-weight:700;
    cursor:pointer;
}
.sub-btn-active {
    background:#2c6bed !important;
    color:white !important;
}
</style>

<div class="submenu" id="submenu"></div>
""", unsafe_allow_html=True)

sub_container = st.container()

with sub_container:
    cols = st.columns(len(submenu_items[st.session_state.page]))
    for i, sub in enumerate(submenu_items[st.session_state.page]):
        if st.session_state.sub == sub:
            cols[i].button(label=sub.upper(), on_click=goto, args=(None, sub), key=f"sub_{sub}", help="", use_container_width=True)
        else:
            cols[i].button(label=sub.capitalize(), on_click=goto, args=(None, sub), key=f"sub_inactive_{sub}", help="", use_container_width=True)

# -------------------------------------
# SIDEBAR NAVIGATION (SPA)
# -------------------------------------
st.markdown("""
<style>
.sidebar {
    position:fixed;
    top:72px; bottom:0; left:0;
    width:260px;
    background:#f8faff;
    padding:20px 16px;
    overflow-y:auto;
    z-index:9998;
}
.sidebar-item {
    padding:12px 14px;
    margin-bottom:8px;
    border-radius:6px;
    font-weight:700;
    cursor:pointer;
}
.sidebar-item-active {
    background:#2c6bed;
    color:white;
}
</style>
<div class="sidebar"></div>
""", unsafe_allow_html=True)

side = st.container()

with side:
    pages = ["dashboard", "reports", "settings"]

    for p in pages:
        if p == st.session_state.page:
            st.button(p.upper(), on_click=goto, args=(p, None), key=f"page_{p}", use_container_width=True)
        else:
            st.button(p.capitalize(), on_click=goto, args=(p, None), key=f"page_inactive_{p}", use_container_width=True)


# -------------------------------------
# MAIN CONTENT
# -------------------------------------
st.title(st.session_state.page.capitalize() + " — " + st.session_state.sub.capitalize())

if st.session_state.page == "dashboard":
    if st.session_state.sub == "overview":
        st.header("Dashboard: Overview")
        st.write("KPIs • OEE • Throughput • Line Status")
    elif st.session_state.sub == "stations":
        st.header("Dashboard: Stations")
        st.write("Station KPIs • Cycles • Alarms")

elif st.session_state.page == "reports":
    if st.session_state.sub == "daily":
        st.header("Daily Reports")
        st.write("Shift Summary • Production Count")
    elif st.session_state.sub == "monthly":
        st.header("Monthly Reports")
        st.write("Pareto • Scrap Analysis")

elif st.session_state.page == "settings":
    if st.session_state.sub == "users":
        st.header("User Management")
        st.write("Create • Edit • Roles • Permissions")
    elif st.session_state.sub == "system":
        st.header("System Configuration")
        st.write("PLC • OPC • MES Settings")

# -------------------------------------
# FOOTER
# -------------------------------------
st.markdown("""
<style>
.footer {
    position:fixed;
    bottom:0; left:260px; right:0;
    background:white;
    border-top:1px solid #ddd;
    padding:10px;
    text-align:center;
    font-size:13px;
    z-index:9998;
}
</style>
<div class="footer">© 2025 MES SPA Navigation UI</div>
""", unsafe_allow_html=True)
