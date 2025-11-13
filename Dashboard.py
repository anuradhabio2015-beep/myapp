import streamlit as st

st.set_page_config(page_title="MES App", layout="wide")

#----------------------------------------------------------
# CLEAN CSS
#----------------------------------------------------------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}

.custom-header {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 70px;
    background: #2c6bed;
    color:white;
    padding: 10px 25px;
    z-index: 99999;
    display:flex;
    align-items:center;
    justify-content:space-between;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.header-left {
    display:flex; align-items:center; gap:12px;
}

.header-icons {
    display:flex; align-items:center; gap:18px;
}

.icon-link {
    color:white; text-decoration:none; font-weight:600;
}

.dropdown { position:relative; }

.dropdown-btn {
    background:none; border:none; color:white; font-weight:600; cursor:pointer;
}

.dropdown-content {
    display:none;
    position:absolute;
    background:white;
    min-width:160px;
    right:0; top:40px;
    border-radius:6px;
    padding:6px 0;
    box-shadow:0 4px 10px rgba(0,0,0,0.15);
}

.dropdown-content a {
    display:block; padding:10px 14px;
    color:black; text-decoration:none;
}

.dropdown:hover .dropdown-content { display:block; }

.profile-dropdown { position:relative; }

.profile-content {
    display:none;
    position:absolute;
    background:white;
    min-width:160px;
    right:0; top:40px;
    border-radius:6px;
    padding:6px 0;
    box-shadow:0 4px 10px rgba(0,0,0,0.15);
}

.profile-dropdown:hover .profile-content { display:block; }

.block-container { padding-top:110px !important; }

</style>
""", unsafe_allow_html=True)

#----------------------------------------------------------
# HEADER HTML
#----------------------------------------------------------
st.markdown("""
<div class="custom-header">

    <div class="header-left">
        <img src="https://via.placeholder.com/40" style="width:40px;height:40px;border-radius:6px;">
        <span style="font-size:21px;font-weight:700;">MES Application</span>
    </div>

    <div class="header-icons">
        <a class="icon-link" href="?page=dashboard">🏠 Home</a>

        <div class="dropdown">
            <button class="dropdown-btn">📁 Reports ▼</button>
            <div class="dropdown-content">
                <a href="?page=daily">Daily Report</a>
                <a href="?page=shift">Shift Report</a>
                <a href="?page=quality">Quality Report</a>
            </div>
        </div>

        <a class="icon-link" href="?page=settings">⚙️ Settings</a>
    </div>

    <div style="position:relative;">
        <button class="icon-link" onclick="document.querySelector('#alerts').scrollIntoView();">
            🔔 Notifications
        </button>
    </div>

    <div class="profile-dropdown">
        <button class="dropdown-btn">👤 Rahul ▼</button>
        <div class="profile-content">
            <a href="?page=profile">Profile</a>
            <a href="?page=logout">Logout</a>
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

#----------------------------------------------------------
# PAGE ROUTER
#----------------------------------------------------------
params = st.experimental_get_query_params()
page = params.get("page", ["dashboard"])[0]

#----------------------------------------------------------
# CONTENT
#----------------------------------------------------------
st.header(page.upper())

st.markdown("<h3 id='alerts'>🔔 Notifications</h3>", unsafe_allow_html=True)
st.info("No notifications.")

#----------------------------------------------------------
# FOOTER
#----------------------------------------------------------
st.markdown("""
<div style="
position:fixed;
bottom:0;
left:0;
width:100%;
background:#2c6bed;
color:white;
text-align:center;
padding:10px;">
© 2025 MES System | Powered by Python + Streamlit
</div>
""", unsafe_allow_html=True)
