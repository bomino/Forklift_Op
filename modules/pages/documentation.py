import streamlit as st
from ..ui import load_css, display_logo

def documentation_page():
    # Security check - only allow admins to view documentation
    if st.session_state.role != "admin":
        st.error("You do not have permission to access this page.")
        st.button("Return to Quiz", on_click=lambda: navigate_to("quiz"))
        return

    # Apply custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Display logo
    display_logo()
    
    st.title("Forklift Operator Quiz App Documentation")
    
    # Create an expandable section for each part of the documentation
    with st.expander("Overview", expanded=True):
        st.markdown("""
        The Forklift Operator Quiz App is a web-based application that provides 
        safety training and assessment for forklift operators in a manufacturing environment. 
        The app allows operators to test their knowledge of safety protocols, track their progress, 
        and earn certificates for passing scores. Supervisors can manage questions, view operator 
        performance, and administer user accounts.
        """)
    
    with st.expander("User Guide"):
        st.markdown("### Registration and Login")
        st.markdown("""
        1. **Registration**:
           - Click the "Register" tab on the login page
           - Fill in username, password, and full name
           - Click "Register" to create your account
           - All new self-registered users receive "operator" role

        2. **Login**:
           - Enter your username and password
           - Click "Login" to access the application
        """)
        
        st.markdown("### Taking a Quiz")
        st.markdown("""
        1. Navigate to the Quiz page using the sidebar
        2. Read each question carefully
        3. Select your answer from the provided options
        4. Click "Submit Answer" to check your answer
        5. Review feedback and explanation
        6. Click "Next Question" to proceed
        7. After completing all questions, view your score
        8. Download a certificate if you achieved a passing score (80% or higher)
        """)
        
        st.markdown("### Viewing Scores")
        st.markdown("""
        1. Navigate to the Scores page using the sidebar
        2. View your latest quiz score
        3. Check your score progression over time (line chart)
        4. Review statistics (best score, average score)
        5. See all your quiz attempts in the table
        """)
        
        st.markdown("### Logging Out")
        st.markdown("""
        1. Click "Logout" in the sidebar to end your session
        """)
    
    if st.session_state.role == "admin":
        with st.expander("Administrator Guide"):
            st.markdown("### Managing Questions")
            st.markdown("""
            1. **Viewing Questions**:
               - Navigate to the Admin Panel using the sidebar
               - Go to "Manage Questions" tab

            2. **Adding Questions**:
               - Scroll to "Add New Question" section
               - Fill in question text, options, correct answer, and explanation
               - Click "Add Question" to save

            3. **Editing Questions**:
               - Select a question from the dropdown
               - Modify any fields as needed
               - Click "Save Changes" to update

            4. **Importing Questions**:
               - Create a CSV file with proper columns (use sample template)
               - Upload the CSV file
               - Review preview and click "Import Questions"

            5. **Exporting Questions**:
               - Click "Download All Questions as CSV"
               - Save the file to your computer
            """)
            
            st.markdown("### Managing Users")
            st.markdown("""
            1. **Viewing Users**:
               - Navigate to "Manage Users" tab
               - All users are listed in the table

            2. **Adding Users**:
               - Fill in username, password, name, and role
               - Click "Add User" to create

            3. **Resetting Passwords**:
               - Select a user from the dropdown
               - Enter and confirm new password
               - Click "Reset Password"

            4. **Removing Users**:
               - Select a user to remove
               - Confirm removal
               - Note: You cannot remove the last admin user
            """)
            
            st.markdown("### Viewing Analytics")
            st.markdown("""
            1. **Score Analytics**:
               - Navigate to "View User Scores" tab
               - View overall statistics and visualizations
               - Export all scores to CSV if needed
               - Review the detailed score history table
            """)
            
            st.markdown("### Customizing Branding")
            st.markdown("""
            1. **Setting Company Logo**:
               - Navigate to "Branding" tab
               - Upload an image file (PNG or JPG)
               - Click "Save Logo" to apply throughout the app
               - The logo will appear in the header, sidebar, and certificates
            """)
    
    with st.expander("Features"):
        st.markdown("### Core Features")
        st.markdown("""
        1. **Authentication System**
           - User registration and login
           - Role-based access control (admin vs. operator)
           - Password hashing for security

        2. **Quiz Module**
           - Multiple-choice questions on forklift safety
           - Randomized question ordering
           - Immediate feedback with explanations
           - Pass/fail scoring with certificate generation

        3. **Score Tracking**
           - Historical record of all quiz attempts
           - Progress visualization with charts
           - Achievement tracking (best scores, averages)

        4. **Administrator Tools**
           - Question management (add, edit, import/export)
           - User management (add, reset passwords, remove)
           - Score analytics and reporting
           - Company branding customization

        5. **Professional Certificates**
           - Customizable completion certificates
           - Company logo integration
           - Downloadable in HTML format
        """)
    
    with st.expander("Troubleshooting"):
        st.markdown("### Common Issues")
        st.markdown("""
        1. **Error: Cannot connect to Streamlit server**
           - Ensure you've installed all dependencies
           - Check if another application is using port 8501
           - Restart your computer and try again

        2. **Error: Module not found**
           - Ensure your virtual environment is activated
           - Verify all dependencies are installed
           - Check if you're running from the correct directory

        3. **Missing data files**
           - The application should create necessary files on first run
           - Ensure the app has write permissions to the data directory
        """)