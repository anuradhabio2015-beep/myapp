import streamlit as st

# -----------------------------------
# Remove Streamlit Default UI
# -----------------------------------
st.markdown("""
<style>
    header[data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)



# -----------------------------------
# Groww Sidebar Style (Vertical Navbar)
# -----------------------------------
groww_sidebar_css = """
<style>

[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    padding-top: 20px;
    border-right: 1px solid #e5e5e5;
    width: 220px !important;
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    color: #1f4df5;
    margin-bottom: 30px;
    margin-left: 10px;
}

.nav-item {
    font-size: 16px;
    padding: 10px 18px;
    border-radius: 10px;
    margin-bottom: 5px;
    cursor: pointer;
    color: #333333;
}

.nav-item:hover {
    background-color: #f2f6ff;
    color: #1f4df5;
}

.nav-selected {
    background-color: #e7edff;
    color: #1f4df5;
    font-weight: 600;
}

</style>
"""

st.markdown(groww_sidebar_css, unsafe_allow_html=True)



# -----------------------------------
# Sidebar Menu
# -----------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Groww Dashboard</div>', unsafe_allow_html=True)

    menu_items = [
        "🏠 Home",
        "📈 Markets",
        "💼 Portfolio",
        "🔍 Research",
        "⚙️ Settings",
        "🤖 AI Insights"
    ]

    selected_menu = st.radio(
        "",
        menu_items,
        label_visibility="collapsed"
    )



# -----------------------------------
# Top Groww Header with Search Bar
# -----------------------------------
st.markdown("""
<style>
.top-header {
    background-color: #ffffff;
    padding: 15px 25px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
    position: sticky;
    top: 0;
    z-index: 999;
}

.search-box {
    flex: 1;
    max-width: 400px;
}

.search-input {
    width: 100%;
    padding: 10px 16px;
    border-radius: 12px;
    border: 1px solid #dcdcdc;
    font-size: 16px;
}

.search-input:focus {
    outline: none;
    border: 1px solid #1f4df5;
}

.profile-icon {
    font-size: 22px;
    margin-left: 25px;
    cursor: pointer;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-header">
    <div class="search-box">
        <input class="search-input" type="text" placeholder="Search stocks, mutual funds, ETFs...">
    </div>
    <div class="profile-icon">👤</div>
</div>
""", unsafe_allow_html=True)



# -----------------------------------
# Page Content Renderer
# -----------------------------------
st.write("")

if selected_menu == "🏠 Home":
    st.header("🏠 Home")
    st.write("Welcome to your Groww-style dashboard!")

elif selected_menu == "📈 Markets":
    st.header("📈 Markets")
    st.write("View live markets, indices, and top gainers.")

elif selected_menu == "💼 Portfolio":
    st.header("💼 Portfolio")
    st.write("Your holdings will appear here.")

elif selected_menu == "🔍 Research":
    st.header("🔍 Research")
    st.write("Search for stocks, mutual funds, and ETFs.")

elif selected_menu == "⚙️ Settings":
    st.header("⚙️ Settings")
    st.write("Manage your preferences.")

elif selected_menu == "🤖 AI Insights":
    st.header("🤖 AI Insights")
    st.write("Your AI market assistant is ready!")
