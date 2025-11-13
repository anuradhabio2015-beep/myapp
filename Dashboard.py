import streamlit as st

# Page config
st.set_page_config(page_title="My App", page_icon=":sparkles:", layout="wide")

# === Hide default Streamlit header/menu/footer ===
HIDE_STEAMLIT_STYLE = """
<style>
/* Hide the top header (Streamlit logo) */
header {visibility: hidden;}
/* Hide the hamburger menu and "Made with Streamlit" footer */
footer {visibility: hidden;}
/* Optional: hide the toolbar in newer Streamlit versions */
[data-testid="stToolbar"] {display: none}
</style>
"""
st.markdown(HIDE_STEAMLIT_STYLE, unsafe_allow_html=True)

# === Custom header ===
# You can replace the logo path with a URL or local file (e.g., "./assets/logo.png")
LOGO_PATH = "https://placehold.co/80x80/png?text=Logo"  # replace with your logo

CUSTOM_HEADER_STYLE = """
<style>
.custom-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  background: linear-gradient(90deg, rgba(255,255,255,0.9), rgba(250,250,255,0.6));
}
.custom-header .title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}
.custom-header .subtitle {
  font-size: 13px;
  color: #555;
  margin: 0;
}
/* Make header sticky at top (optional) */
.stApp > div:first-child {
  position: sticky;
  top: 8px;
  z-index: 999;
}
</style>
"""

st.markdown(CUSTOM_HEADER_STYLE, unsafe_allow_html=True)

header_html = f"""
<div class="custom-header">
  <img src="{LOGO_PATH}" width="64" height="64" style="border-radius:12px;"/>
  <div>
    <p class="title">My Customized App</p>
    <p class="subtitle">Short description or tagline goes here</p>
  </div>
  <div style="margin-left:auto; display:flex; gap:8px; align-items:center;">
    <!-- Add small action buttons/links -->
    <a href="#" target="_self">Docs</a>
    <a href="#" target="_self">Support</a>
  </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# === Side Menu (Custom) ===
SIDE_MENU_STYLE = """
<style>
.custom-side-menu {
  position: fixed;
  top: 90px;
  left: 0;
  width: 220px;
  height: 100%;
  background: #ffffff;
  padding: 20px 15px;
  box-shadow: 4px 0 15px rgba(0,0,0,0.08);
  border-radius: 0 12px 12px 0;
  z-index: 998;
}
.custom-side-menu a {
  display: block;
  padding: 10px 12px;
  margin-bottom: 6px;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
}
.custom-side-menu a:hover {
  background: #f2f2ff;
}
</style>
"""
st.markdown(SIDE_MENU_STYLE, unsafe_allow_html=True)

side_menu_html = """
<div class="custom-side-menu">
  <a href="#">🏠 Dashboard</a>
  <a href="#">📦 Orders</a>
  <a href="#">🏭 Production</a>
  <a href="#">🔧 Settings</a>
  <a href="#">📊 Reports</a>
</div>
"""

st.markdown(side_menu_html, unsafe_allow_html=True)

# Shift main layout right to avoid overlap
st.markdown("""
<style>
.block-container {
  margin-left: 240px;
}
</style>
""", unsafe_allow_html=True)

# === Rest of app content ===
st.write("Welcome — the default Streamlit header is hidden and a custom header is shown instead.")

# Example layout
col1, col2 = st.columns([3,1])
with col1:
    st.header("Main content area")
    st.write("Put your app UI here — charts, tables, controls, forms, etc.")
with col2:
    st.header("Sidebar-like area")
    st.button("Primary Action")

# Notes for customization (keep these comments in the file):
# - Replace LOGO_PATH with your logo file or URL. For a local file, use st.image('./assets/logo.png') instead.
# - Tweak CSS in CUSTOM_HEADER_STYLE to change colors, spacing, or make the header full-width.
# - If Streamlit updates its DOM structure, the CSS selectors (header, footer, [data-testid]) may need adjustment.
# - For accessibility, ensure alt text and semantic HTML if you expand the header.
