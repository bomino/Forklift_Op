import streamlit as st
import os

# Import modules
from modules.ui import initialize_session_state, show_sidebar
from modules.data_manager import ensure_directories, initialize_data_files
from modules.pages.login import login_page
from modules.pages.quiz import quiz_page
from modules.pages.scores import scores_page
from modules.pages.documentation import documentation_page
from modules.pages.admin import admin_page

# Configure the app
st.set_page_config(
    page_title="Forklift Operator Training",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize app data and state
def initialize_app():
    # Ensure directories exist
    ensure_directories()
    
    # Initialize data files
    initialize_data_files()
    
    # Initialize session state
    initialize_session_state()

# Main app function
def main():
    # Initialize the app
    initialize_app()
    
    # Show the sidebar for navigation
    show_sidebar()
    
    # Render the appropriate page
    if not st.session_state.authenticated:
        login_page()
    elif st.session_state.current_page == "quiz":
        quiz_page()
    elif st.session_state.current_page == "scores":
        scores_page()
    elif st.session_state.current_page == "documentation"and st.session_state.role == "admin":
        documentation_page()
    elif st.session_state.current_page == "admin" and st.session_state.role == "admin":
        admin_page()
    else:
        # Default to quiz page
        st.session_state.current_page = "quiz"
        quiz_page()

# Run the app
if __name__ == "__main__":
    main()