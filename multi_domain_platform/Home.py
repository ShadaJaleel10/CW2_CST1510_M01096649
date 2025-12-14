# multi_domain_platform/Home.py
import streamlit as st
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager

st.set_page_config(
    page_title="Multi-Domain Platform",
    layout="wide"
)

# --- Singleton Initialization (Run only once) ---
# Initialize DatabaseManager and AuthManager as singletons in session state
if 'db' not in st.session_state:
    # Use the correct path to your database file
    st.session_state['db'] = DatabaseManager("database/platform.db")
    st.session_state['auth'] = AuthManager(st.session_state['db'])
    st.session_state['db'].connect() # Connect once on startup

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- Application Flow Control ---
if not st.session_state.get('current_user'):
    # If not logged in, show the login message and hide the pages
    st.title("Welcome to the Multi-Domain Platform")
    st.info("Please log in using the 'Login' page.")
    
    # Hide all pages except Home and Login if not logged in
    # This is often achieved by renaming or using custom sidebar logic
    # In a simple setup, you rely on the user to use the sidebar page.
else:
    # User is logged in, show main content
    st.title(f"Dashboard for {st.session_state['current_user']}")
    st.write(f"Role: {st.session_state['current_role']}")

    if st.button("Logout"):
        del st.session_state['current_user']
        del st.session_state['current_role']
        st.rerun()

    st.success("Use the sidebar to navigate to the domains.")
    # Here you would typically add high-level dashboard metrics