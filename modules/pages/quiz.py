import streamlit as st


def quiz_page():
    # Apply custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Display logo
    display_logo()
    
    st.title("Forklift Operator Safety Quiz")
    
    # Load all questions
    all_questions = load_questions()
    
    # Initialize quiz with randomized questions
    if 'quiz_questions' not in st.session_state:
        # Create a copy of the questions and shuffle them
        import random
        quiz_questions = all_questions.copy()
        random.shuffle(quiz_questions)
        st.session_state.quiz_questions = quiz_questions
    
    # Use the randomized questions
    quiz_questions = st.session_state.quiz_questions
    
    # Initialize session state for tracking quiz progress
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.quiz_complete = False
        st.session_state.quiz_in_progress = True

    # Function to handle answer submission
    def check_answer(selected_option, question_idx):
        correct_answer = quiz_questions[question_idx]["answer"]
        if selected_option == correct_answer:
            st.session_state.score += 1
            return True
        return False

    # Function to go to next question
    def next_question():
        if st.session_state.current_question < len(quiz_questions) - 1:
            st.session_state.current_question += 1
            st.session_state.answered = False
        else:
            st.session_state.quiz_complete = True
            st.session_state.quiz_in_progress = False
            
            # Save the score when quiz is complete
            score = st.session_state.score
            max_score = len(quiz_questions)
            save_quiz_score(st.session_state.username, score, max_score)

    # Function to restart quiz
    def restart_quiz():
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.quiz_complete = False
        st.session_state.quiz_in_progress = True
        
        # Remove quiz_questions to get a new random set on restart
        if 'quiz_questions' in st.session_state:
            del st.session_state.quiz_questions

    # Display quiz completion screen
    if st.session_state.quiz_complete:
        score = st.session_state.score
        max_score = len(quiz_questions)
        percentage = (score / max_score) * 100
        
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        st.success(f"Quiz complete! Your score: {score}/{max_score} ({percentage:.1f}%)")
        
        # Show recommendation based on score
        if percentage >= 80:
            st.balloons()
            st.markdown("### Great job! You have a solid understanding of forklift safety.")
            
            # Generate certificate for passing score
            st.markdown("### Certificate of Completion")
            st.markdown('<div class="certificate-container">', unsafe_allow_html=True)
            
            cert_html = create_certificate(
                st.session_state.name, 
                f"{percentage:.1f}", 
                datetime.datetime.now().strftime("%B %d, %Y")
            )
            
            b64 = base64.b64encode(cert_html.encode()).decode()
            download_button = f'<a href="data:text/html;base64,{b64}" download="forklift_certificate.html" class="certificate-button">Download Certificate</a>'
            st.markdown(download_button, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif percentage >= 60:
            st.markdown("### Good effort! Review the areas where you made mistakes.")
        else:
            st.markdown("### Please review the forklift safety manual and try again.")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View My Scores", key="view_scores_btn"):
                navigate_to("scores")
                st.rerun()
        
        with col2:
            if st.button("Take Quiz Again", key="restart_quiz_btn"):
                restart_quiz()
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    # Display current question if quiz isn't complete
    elif not st.session_state.quiz_complete:
        current_q = quiz_questions[st.session_state.current_question]
        
        # Show progress
        st.progress((st.session_state.current_question) / len(quiz_questions))
        st.markdown(f"**Question {st.session_state.current_question + 1} of {len(quiz_questions)}**")
        
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        
        # Display the question
        st.subheader(current_q["question"])
        
        # Use radio buttons for options
        selected_option = st.radio(
            "Select your answer:",
            options=range(len(current_q["options"])),
            format_func=lambda x: current_q["options"][x],
            key=f"q{st.session_state.current_question}"
        )
        
        # Submit button
        if not st.session_state.answered:
            if st.button("Submit Answer", key=f"submit_btn_{st.session_state.current_question}"):
                is_correct = check_answer(selected_option, st.session_state.current_question)
                st.session_state.answered = True
                
                if is_correct:
                    st.success("✅ Correct!")
                else:
                    correct_answer_text = current_q["options"][current_q["answer"]]
                    st.error(f"❌ Incorrect! The correct answer is: {correct_answer_text}")
                
                # Show explanation
                st.info(f"Explanation: {current_q['explanation']}")
        
        # Next question button (only show after answering)
        if st.session_state.answered:
            if st.button("Next Question", key=f"next_btn_{st.session_state.current_question}"):
                next_question()
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)