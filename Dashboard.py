import streamlit as st

st.set_page_config(page_title="MES App", layout="wide")

#----------------------------------------------------------
# REMOVE STREAMLIT DEFAULT HEADER
#----------------------------------------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

#----------------------------------------------------------
# HEADER CSS
#----------------------------------------------------------
st.markdown("""
<style>

.custom-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    background-color: #2c6bed;
    color: white;
    padding: 10px 25px;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
}

.header-left { display: flex; align-items: center; gap: 12px; }

.header-logo {
    width: 40px;
    height: 40px;
    border-radius: 6px;
}

.header-title {
    font-size: 21px;
    font-weight: 700;
    color: white;
}

.header-icons {
    display: flex;
    align-items: center;
    gap: 18px;
}

.icon-link {
    color: white;
    text-decoration: none;
    font-size: 16px;
    font-weight: 600;
}

.icon-link:hover { text-decoration: underline; }

.dropdown { position: relative; display: inline-block; }

.dropdown-btn {
    background: none;
    border: none;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: white;
    min-width: 160px;
    right: 0;
    top: 42px;
    border-radius: 6px;
    padding: 8px 0;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    z-index: 10000;
}

.dropdown-content a {
    padding: 10px 14px;
    display: block;
    color: black;
    text-decoration: none;
}

.dropdown-content a:hover { background-color: #eeeeee; }

.dropdown:hover .dropdown-content { display: block; }

.profile-dropdown { position: relative; }

.profile-content {
    display: none;
    position: absolute;
    background-color: white;
    min-width: 140px;
    right: 0;
    top: 42px;
    border-radius: 6px;
    padding: 8px 0;
    color: black;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
}

.profile-content a {
    padding: 10px 14px;
    display: block;
    color: black;
    text-decoration: none;
}

.profile-content a:hover { background-color: #eeeeee; }

.profile-dropdown:hover .profile-content { display: block; }

.block-container { padding-top: 110px !important; }

</style>
""", unsafe_allow_html=True)

#----------------------------------------------------------
# HEADER HTML
#----------------------------------------------------------
st.markdown("""
<div class="custom-header">

    <div class="header-left">
        <img class="header-logo" src="https://via.placeholder.com/40" />
        <span class="header-title">MES Application</span>
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
# ROUTER
#----------------------------------------------------------
params = st.experimental_get_query_params()
page = params.get("page", ["dashboard"])[0]

#----------------------------------------------------------
# CONTENT
#----------------------------------------------------------
if page == "dashboard":
    st.header("📊 Dashboard")

elif page == "daily":
    st.header("📝 Daily Report")

elif page == "shift":
    st.header("⏱ Shift Report")

elif page == "quality":
    st.header("🔍 Quality Report")

elif page == "settings":
    st.header("⚙️ Settings")

elif page == "profile":
    st.header("👤 Profile")

elif page == "logout":
    st.warning("Logged out")

#----------------------------------------------------------
# ALERT PLACEHOLDER
#----------------------------------------------------------
st.markdown("<h3 id='alerts'>🔔 Notifications</h3>", unsafe_allow_html=True)
st.info("No notifications.")

#----------------------------------------------------------
# FOOTER
#----------------------------------------------------------
st.markdown("""
<br><br><br>
<div style="
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:#2c6bed;
    color:white;
    text-align:center;
    padding:10px;
    font-size:14px;">
    © 2025 MES System | Powered by Python + Streamlit
</div>
""", unsafe_allow_html=True)
