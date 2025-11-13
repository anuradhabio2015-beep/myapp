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
# FIXED CUSTOM HEADER (TOP)
# -------------------------------------------------------
custom_header = """
    <style>
        /* HEADER CONTAINER */
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
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }

        /* LOGO + APP NAME */
        .header-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-logo {
            width: 40px;
            height: 40px;
            border-radius: 6px;
        }

        .header-title {
            font-size: 22px;
            font-weight: 700;
            color: white;
        }

        /* NAVIGATION ICON LINKS */
        .header-icons a {
            margin-left: 25px;
            color: white;
            font-size: 18px;
            text-decoration: none;
            font-weight: 500;
        }

        .header-icons a:hover {
            text-decoration: underline;
        }

        /* Profile Dropdown */
        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropdown-btn {
            background: none;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #ffffff;
            min-width: 160px;
            border-radius: 6px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
            right: 0;
            z-index: 20000;
        }

        .dropdown-content a {
            color: black;
            padding: 10px 15px;
            text-decoration: none;
            display: block;
        }

        .dropdown-content a:hover {
            background-color: #f1f1f1;
        }

        .dropdown:hover .dropdown-content {
            display: block;
        }

        /* Push content below header */
        .block-container {
            padding-top: 110px !important;
        }
    </style>

    <div class="custom-header">
        
        <!-- LEFT SECTION: LOGO + APP NAME -->
        <div class="header-left">
            <img class="header-logo" src="https://via.placeholder.com/40" />
            <span class="header-title">MES Application</span>
        </div>

        <!-- CENTER SECTION: ICON NAVIGATION -->
        <div class="header-icons">
            <a href="?page=dashboard">🏠 Home</a>

            <!-- DROPDOWN MENU UNDER REPORTS -->
            <div class="dropdown" style="display:inline-block;">
                <button class="dropdown-btn">📁 Reports ▼</button>
                <div class="dropdown-content">
                    <a href="?page=daily">Daily Report</a>
                    <a href="?page=shift">Shift Report</a>
                    <a href="?page=quality">Quality Report</a>
                </div>
            </div>

            <a href="?page=settings">⚙️ Settings</a>
        </div>

        <!-- RIGHT SECTION: USER PROFILE -->
        <div class="dropdown">
            <button class="dropdown-btn">👤 User ▼</button>
            <div class="dropdown-content">
                <a href="?page=profile">Profile</a>
                <a href="?page=logout">Logout</a>
            </div>
        </div>

    </div>
"""
st.markdown(custom_header, unsafe_allow_html=True)

# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------
with st.sidebar:
    st.title("📌 Navigation")
    side_page = st.radio(
        "Choose Page",
        ["Dashboard", "Reports", "Settings", "Profile"]
    )

# -------------------------------------------------------
# PAGE ROUTING
# -------------------------------------------------------
params = st.experimental_get_query_params()
page = params.get("page", [side_page.lower()])[0]

# -------------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------------
if page == "dashboard":
    st.header("📊 Dashboard")
    tab1, tab2 = st.tabs(["Production", "Quality"])
    tab1.write("Production KPIs...")
    tab2.write("Quality KPIs...")

elif page == "daily":
    st.header("📝 Daily Report")
    st.write("Daily report details...")

elif page == "shift":
    st.header("⏱ Shift Report")
    st.write("Shift-wise production data...")

elif page == "quality":
    st.header("🔍 Quality Report")
    st.write("Inspection results...")

elif page == "reports":
    st.header("📁 All Reports")
    st.write("List of all available reports...")

elif page == "settings":
    st.header("⚙️ Settings")
    st.write("Configuration options...")

elif page == "profile":
    st.header("👤 User Profile")
    st.write("User info, roles, permissions...")

elif page == "logout":
    st.warning("You have been logged out.")

# -------------------------------------------------------
# FIXED FOOTER
# -------------------------------------------------------
custom_footer = """
    <style>
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #2c6bed;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 9999;
        }
    </style>

    <div class="custom-footer">
        © 2025 MES System | Powered by Python + Streamlit
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)
