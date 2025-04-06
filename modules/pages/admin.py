import streamlit as st
import pandas as pd
import os
from ..ui import load_css, display_logo
from ..data_manager import (
    load_questions, load_scores, load_users, 
    save_questions, save_users, LOGO_PATH
)
from ..auth import hash_password

# Helper function for removing users
def remove_user_section():
    users = load_users()
    
    if len(users) > 0:
        # Create a list of users with their role for better display
        user_options = [f"{username} ({info['role']})" for username, info in users.items()]
        selected_user_display = st.selectbox("Select User to Remove", user_options, key="remove_user_select")
        
        # Extract the username from the display string
        username_to_remove = selected_user_display.split(" (")[0]
        
        # Don't allow removing the last admin
        admin_count = sum(1 for u, info in users.items() if info["role"] == "admin")
        is_admin = users[username_to_remove]["role"] == "admin"
        
        # Use a form to handle the removal action
        with st.form(key="remove_user_form"):
            st.write(f"You are about to remove user: **{username_to_remove}**")
            
            if is_admin and admin_count <= 1:
                st.error("Cannot remove the last administrator account.")
                submit_button = st.form_submit_button("Remove User", disabled=True)
                return False
            else:
                st.warning("This action cannot be undone. All quiz scores for this user will remain in the system.")
                submit_button = st.form_submit_button("Remove User")
                
                if submit_button:
                    # Remove the user
                    del users[username_to_remove]
                    save_users(users)
                    st.success(f"User '{username_to_remove}' has been removed.")
                    return True
    
    return False

def admin_page():
    # Apply custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Display logo
    display_logo()
    
    st.title("Admin Panel")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Manage Questions", "View User Scores", "Manage Users", "Branding"])
    
    with tab1:
        st.subheader("Question Management")
        
        # Load questions
        questions = load_questions()
        
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        # Import questions from CSV
        st.markdown("### Import Questions from CSV")
        st.write("Upload a CSV file with quiz questions. The CSV should have these columns: question, option1, option2, option3, option4, answer (0-3), explanation, category")

        # Provide a sample CSV for download
        sample_data = [
            {"question": "What should you do before operating a forklift?",
             "option1": "Check fuel only",
             "option2": "Full pre-shift inspection",
             "option3": "Test horn",
             "option4": "Load immediately",
             "answer": 1,
             "explanation": "OSHA requires a pre-shift inspection for safety.",
             "category": "Safety"}
        ]
        sample_df = pd.DataFrame(sample_data)
        sample_csv = sample_df.to_csv(index=False)
        st.download_button(
            label="Download Sample CSV Template",
            data=sample_csv,
            file_name="sample_questions.csv",
            mime="text/csv"
        )

        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                # Read the CSV file
                df = pd.read_csv(uploaded_file)
                
                # Validate the CSV structure
                required_columns = ["question", "option1", "option2", "option3", "option4", "answer", "explanation", "category"]
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"CSV is missing these required columns: {', '.join(missing_columns)}")
                else:
                    # Preview the uploaded data
                    st.write("Preview of uploaded questions:")
                    st.dataframe(df.head(3))
                    
                    # Confirm import
                    if st.button("Import Questions", key="import_questions_btn"):
                        # Load existing questions
                        questions = load_questions()
                        
                        # Get highest existing ID
                        next_id = max([q["id"] for q in questions], default=0) + 1
                        
                        # Convert DataFrame rows to question dictionaries
                        new_questions_count = 0
                        for _, row in df.iterrows():
                            new_q = {
                                "id": next_id,
                                "question": row["question"],
                                "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
                                "answer": int(row["answer"]),
                                "explanation": row["explanation"],
                                "category": row["category"]
                            }
                            questions.append(new_q)
                            next_id += 1
                            new_questions_count += 1
                        
                        # Save updated questions
                        save_questions(questions)
                        st.success(f"Successfully imported {new_questions_count} questions!")
                        
            except Exception as e:
                st.error(f"Error processing CSV file: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export questions to CSV
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Export Questions to CSV")
        if questions:
            # Convert questions to DataFrame format
            export_data = []
            for q in questions:
                q_data = {
                    "question": q["question"],
                    "option1": q["options"][0] if len(q["options"]) > 0 else "",
                    "option2": q["options"][1] if len(q["options"]) > 1 else "",
                    "option3": q["options"][2] if len(q["options"]) > 2 else "",
                    "option4": q["options"][3] if len(q["options"]) > 3 else "",
                    "answer": q["answer"],
                    "explanation": q["explanation"],
                    "category": q.get("category", "General")
                }
                export_data.append(q_data)
            
            export_df = pd.DataFrame(export_data)
            csv = export_df.to_csv(index=False)
            
            st.download_button(
                label="Download All Questions as CSV",
                data=csv,
                file_name="forklift_quiz_questions.csv",
                mime="text/csv"
            )
        else:
            st.info("No questions to export.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Edit existing questions
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Edit Existing Questions")
        if questions:
            question_titles = [f"Q{q['id']}: {q['question'][:50]}..." for q in questions]
            selected_q_idx = st.selectbox("Select Question to Edit", range(len(questions)), format_func=lambda i: question_titles[i])
            
            q_to_edit = questions[selected_q_idx]
            
            with st.form(key="edit_question_form"):
                edited_question = st.text_input("Question", value=q_to_edit["question"])
                
                # Options
                edited_options = []
                for i, opt in enumerate(q_to_edit["options"]):
                    edited_opt = st.text_input(f"Option {i+1}", value=opt, key=f"edit_option_{i}")
                    edited_options.append(edited_opt)
                
                edited_answer = st.selectbox(
                    "Correct Answer",
                    range(len(edited_options)),
                    format_func=lambda i: edited_options[i],
                    index=q_to_edit["answer"]
                )
                
                edited_explanation = st.text_area("Explanation", value=q_to_edit["explanation"])
                edited_category = st.text_input("Category", value=q_to_edit.get("category", "General"))
                
                submit_edit = st.form_submit_button("Save Changes")
                
                if submit_edit:
                    questions[selected_q_idx]["question"] = edited_question
                    questions[selected_q_idx]["options"] = edited_options
                    questions[selected_q_idx]["answer"] = edited_answer
                    questions[selected_q_idx]["explanation"] = edited_explanation
                    questions[selected_q_idx]["category"] = edited_category
                    
                    save_questions(questions)
                    st.success("Question updated successfully!")
        else:
            st.info("No questions available to edit. Add questions manually or import from CSV.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add new question
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Add New Question")
        with st.form(key="new_question_form"):
            new_question = st.text_input("Question", key="new_q")
            
            # Options
            new_options = []
            for i in range(4):  # Assuming we always want 4 options
                new_opt = st.text_input(f"Option {i+1}", key=f"new_option_{i}")
                new_options.append(new_opt)
            
            new_answer = st.selectbox(
                "Correct Answer",
                range(len(new_options)),
                format_func=lambda i: new_options[i] if new_options[i] else f"Option {i+1}"
            )
            
            new_explanation = st.text_area("Explanation", key="new_explanation")
            new_category = st.text_input("Category", value="General", key="new_category")
            
            submit_new = st.form_submit_button("Add Question")
            
            if submit_new:
                if not new_question or "" in new_options or not new_explanation:
                    st.error("All fields are required")
                else:
                    # Load questions again in case they were updated
                    questions = load_questions()
                    
                    # Generate new ID
                    new_id = max([q["id"] for q in questions], default=0) + 1
                    
                    new_q = {
                        "id": new_id,
                        "question": new_question,
                        "options": new_options,
                        "answer": new_answer,
                        "explanation": new_explanation,
                        "category": new_category
                    }
                    
                    questions.append(new_q)
                    save_questions(questions)
                    st.success("New question added successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("User Scores")
        
        # Load all scores
        all_scores = load_scores()
        users = load_users()
        
        if not all_scores:
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.info("No quiz scores recorded yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Convert to DataFrame for analysis
            df = pd.DataFrame(all_scores)
            
            # Add name column
            df["name"] = df["username"].apply(lambda u: users.get(u, {}).get("name", "Unknown"))
            
            # Summary stats
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### Overall Statistics")
            avg_score = df["percentage"].mean()
            st.metric("Average Score", f"{avg_score:.1f}%")
            
            # Score distribution
            st.markdown("### Score Distribution")
            # Create bins for score ranges
            bins = [0, 20, 40, 60, 80, 100]
            labels = ["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"]
            df["score_range"] = pd.cut(df["percentage"], bins=bins, labels=labels, include_lowest=True)
            
            # Count occurrences in each bin and convert to a format Streamlit can display
            score_distribution = df["score_range"].value_counts().sort_index()
            score_distribution_df = pd.DataFrame({
                "Score Range": score_distribution.index,
                "Count": score_distribution.values
            })
            st.bar_chart(score_distribution_df.set_index("Score Range"))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Bar chart of average scores by user
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### Average Scores by User")
            user_avg = df.groupby("name")["percentage"].mean().reset_index()
            st.bar_chart(user_avg.set_index("name"))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export scores to CSV
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### Export All Scores")
            export_scores_csv = df.to_csv(index=False)
            st.download_button(
                label="Download All Scores as CSV",
                data=export_scores_csv,
                file_name="forklift_quiz_scores.csv",
                mime="text/csv"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Table of all scores
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### All Scores")
            st.dataframe(
                df[["name", "username", "timestamp", "score", "max_score", "percentage"]].sort_values("timestamp", ascending=False),
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("User Management")
        
        # Load users
        users = load_users()
        
        # Display users
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Current Users")
        user_df = pd.DataFrame([
            {
                "username": username,
                "name": info["name"],
                "role": info["role"]
            }
            for username, info in users.items()
        ])
        
        st.dataframe(user_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add new user
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Add New User")
        with st.form(key="new_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_name = st.text_input("Full Name")
            new_role = st.selectbox("Role", ["operator", "admin"])
            
            submit_user = st.form_submit_button("Add User")
            
            if submit_user:
                if not new_username or not new_password or not new_name:
                    st.error("All fields are required")
                elif new_username in users:
                    st.error("Username already exists")
                else:
                    users[new_username] = {
                        "password": hash_password(new_password),
                        "name": new_name,
                        "role": new_role
                    }
                    save_users(users)
                    st.success(f"User {new_username} added successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Reset user password
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Reset User Password")
        if len(users) > 0:
            username_to_reset = st.selectbox("Select User", list(users.keys()), key="reset_password_select")
            
            with st.form(key="reset_password_form"):
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                reset_submit = st.form_submit_button("Reset Password")
                
                if reset_submit:
                    if not new_password:
                        st.error("Password cannot be empty")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        users[username_to_reset]["password"] = hash_password(new_password)
                        save_users(users)
                        st.success(f"Password for {username_to_reset} has been reset")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Remove user
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Remove User")
        if remove_user_section():
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Company Branding")
        
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.markdown("### Company Logo")
        st.write("Upload your company logo to display throughout the app and on certificates.")
        
        uploaded_logo = st.file_uploader("Upload Logo (PNG or JPG)", type=["png", "jpg", "jpeg"])
        if uploaded_logo is not None:
            # Display preview
            st.image(uploaded_logo, width=200, caption="Logo Preview")
            
            # Save button
            if st.button("Save Logo", key="save_logo_btn"):
                # Save the uploaded logo
                with open(LOGO_PATH, "wb") as f:
                    f.write(uploaded_logo.getbuffer())
                st.success("Logo uploaded successfully! It will appear throughout the app.")
        
        # Show current logo if it exists
        elif os.path.exists(LOGO_PATH):
            st.write("Current logo:")
            st.image(LOGO_PATH, width=200)
            
            if st.button("Remove Logo", key="remove_logo_btn"):
                os.remove(LOGO_PATH)
                st.success("Logo removed successfully.")
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)