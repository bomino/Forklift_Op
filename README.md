I'll provide both files with proper formatting:

## README.md

```markdown
# Forklift Operator Quiz App

A Streamlit web application for training and assessing forklift operators on safety protocols and operational procedures.

## Features

- Interactive quiz with randomized questions
- Immediate feedback and explanations
- Score tracking and progress visualization
- Completion certificates for passing scores
- Admin panel for question and user management

## Project Overview

The Forklift Operator Quiz App is designed to help manufacturing facilities train and certify their forklift operators. The application provides:

- **Safety Training**: Test knowledge of OSHA regulations and best practices
- **Performance Tracking**: Monitor operator progress over time
- **Administration Tools**: Easily manage questions and user accounts

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/forklift-quiz-app.git
cd forklift-quiz-app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Project Structure

```
forklift_app/
│
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
│
├── assets/                # Static files
│   └── company_logo.png   # Logo file (when uploaded)
│
├── data/                  # Data storage
│   ├── users.json         # User credentials and information
│   ├── questions.json     # Quiz questions, options, and answers
│   └── scores.json        # Quiz attempt history and scores
│
└── modules/               # Application modules
    ├── __init__.py
    ├── auth.py            # Authentication functions
    ├── data_manager.py    # Data loading/saving functions
    ├── ui.py              # UI components and styling
    ├── certificate.py     # Certificate generation
    ├── pages/             # Page modules
    │   ├── __init__.py
    │   ├── login.py       # Login page
    │   ├── quiz.py        # Quiz page
    │   ├── scores.py      # Scores page
    │   ├── documentation.py # Documentation page
    │   └── admin.py       # Admin panel
    └── utils.py           # Utility functions
```

## User Roles

- **Operators**: Take quizzes, view scores, download certificates
- **Administrators**: Manage questions, view analytics, manage users

## Default Admin Login

- Username: `admin`
- Password: `admin123`

**Important**: Change the default admin password after first login.

## Deployment

This application is configured for easy deployment on Streamlit Cloud:

1. Push the project to a GitHub repository
2. Connect the repository to Streamlit Cloud
3. Specify `app.py` as the main file

## License

This project is licensed under the MIT License.
```

