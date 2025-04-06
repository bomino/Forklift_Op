import streamlit as st
import base64
import os
from .data_manager import LOGO_PATH

# Custom CSS for modern look
def load_css():
    return """
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1E88E5;
        --background-color: #f9f9f9;
        --secondary-color: #ff9800;
        --text-color: #212121;
        --success-color: #4CAF50;
        --error-color: #F44336;
    }
    
    /* Page background */
    .main {
        background-color: var(--background-color);
        padding: 2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Cards styling */
    .quiz-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: white;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Success message */
    .element-container .stAlert.success {
        border-radius: 8px;
        border-left: 5px solid var(--success-color);
    }
    
    /* Error message */
    .element-container .stAlert.error {
        border-radius: 8px;
        border-left: 5px solid var(--error-color);
    }
    
    /* Progress bar */
    .stProgress .st-bo {
        background-color: var(--primary-color);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        border: none !important;
    }
    
    .dataframe thead tr th {
        background-color: var(--primary-color);
        color: white;
        padding: 12px 8px !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #f3f3f3;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1rem;
    }
    
    .logo-container img {
        max-height: 80px;
    }
    
    /* Certificate styling */
    .certificate-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        text-align: center;
    }
    
    /* Certificate download button */
    .certificate-button {
        display: inline-block;
        background-color: var(--primary-color);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    
    .certificate-button:hover {
        background-color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """

# Helper function to encode images to base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Display company logo
def display_logo():
    # Check if logo file exists
    if os.path.exists(LOGO_PATH):
        # Use actual logo file
        logo_base64 = get_base64_encoded_image(LOGO_PATH)
        logo_html = f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="Company Logo">
        </div>
        """
    else:
        # Use placeholder logo
        logo_html = """
        <div class="logo-container">
            <img src="https://via.placeholder.com/200x80?text=YOUR+COMPANY+LOGO" alt="Your Company Logo">
        </div>
        """
    st.markdown(logo_html, unsafe_allow_html=True)

# Session State and Navigation
def initialize_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.name = None
        st.session_state.current_page = "login"

def navigate_to(page):
    st.session_state.current_page = page
    # Reset quiz state when navigating away from quiz
    if page != "quiz":
        if "current_question" in st.session_state:
            del st.session_state.current_question
        if "score" in st.session_state:
            del st.session_state.score
        if "answered" in st.session_state:
            del st.session_state.answered
        if "quiz_complete" in st.session_state:
            del st.session_state.quiz_complete

# Sidebar Navigation
def show_sidebar():
    with st.sidebar:
        # Apply custom CSS
        st.markdown(load_css(), unsafe_allow_html=True)
        
        # Display logo
        display_logo()
        
        st.title("Navigation")
        if st.session_state.authenticated:
            st.markdown(f"**Welcome, {st.session_state.name}**")
            st.markdown("---")
            
            if st.button("📝 Take Quiz", use_container_width=True):
                navigate_to("quiz")
                
            if st.button("📊 View My Scores", use_container_width=True):
                navigate_to("scores")
            
            if st.session_state.role == "admin":
                st.markdown("---")
                st.markdown("### Admin Controls")
                if st.button("⚙️ Admin Panel", use_container_width=True):
                    navigate_to("admin")
                
                # Only show documentation button to admins
                if st.button("📚 Documentation", use_container_width=True):
                    navigate_to("documentation")
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.role = None
                st.session_state.name = None
                navigate_to("login")
                st.rerun()