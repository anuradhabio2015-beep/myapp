header_html = """
<div class="custom-header">

    <!-- LEFT SECTION -->
    <div class="header-left">
        <img class="header-logo" src="https://via.placeholder.com/40" />
        <span class="header-title">MES Application</span>
    </div>

    <!-- CENTER NAVIGATION -->
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

    <!-- NOTIFICATION BELL -->
    <div style="position:relative;">
        <button class="icon-link" onclick="document.querySelector('#alerts').scrollIntoView();">
            🔔 Notifications
        </button>
    </div>

    <!-- PROFILE MENU -->
    <div class="profile-dropdown">
        <button class="dropdown-btn">👤 Rahul ▼</button>
        <div class="profile-content">
            <a href="?page=profile">Profile</a>
            <a href="?page=logout">Logout</a>
        </div>
    </div>

</div>
"""

st.markdown(header_html, unsafe_allow_html=True)
