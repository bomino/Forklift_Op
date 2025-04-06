import os
import json
import datetime

# File paths
USER_DB_FILE = "data/users.json"
QUESTIONS_FILE = "data/questions.json"
SCORES_FILE = "data/scores.json"
LOGO_PATH = "assets/XLC2.png"

# Create necessary directories
def ensure_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

# Initialize data files if they don't exist
def initialize_data_files():
    from .auth import hash_password
    
    # Default admin user
    if not os.path.exists(USER_DB_FILE):
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin",
                "name": "Admin User"
            }
        }
        with open(USER_DB_FILE, "w") as f:
            json.dump(default_users, f)
    
    # Default questions
    if not os.path.exists(QUESTIONS_FILE):
        default_questions = [
            {
                "id": 1,
                "question": "What should you do before operating a forklift?",
                "options": [
                    "Check fuel only", 
                    "Full pre-shift inspection", 
                    "Test horn", 
                    "Load immediately"
                ],
                "answer": 1,
                "explanation": "OSHA requires a pre-shift inspection for safety.",
                "category": "Safety"
            },
            {
                "id": 2,
                "question": "What is the proper way to approach an intersection with a forklift?",
                "options": [
                    "Speed up to get through quickly", 
                    "Honk and proceed without stopping", 
                    "Slow down, honk, and look both ways", 
                    "Always come to a complete stop"
                ],
                "answer": 2,
                "explanation": "Slowing down, honking, and looking both ways ensures visibility and warns pedestrians of your approach.",
                "category": "Operation"
            },
            {
                "id": 3,
                "question": "When parking a forklift at the end of a shift, you should:",
                "options": [
                    "Leave the forks raised for easy access next shift", 
                    "Park anywhere convenient", 
                    "Lower the forks to the ground, set the brake, and turn off the engine", 
                    "Leave the key in the ignition for the next operator"
                ],
                "answer": 2,
                "explanation": "Lowering forks, setting the brake, and turning off the engine are essential safety protocols for parking.",
                "category": "Safety"
            }
        ]
        with open(QUESTIONS_FILE, "w") as f:
            json.dump(default_questions, f)
    
    # Empty scores file
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "w") as f:
            json.dump([], f)

# Load data
def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    return {}

def load_questions():
    """Load questions from JSON file"""
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    return []

def load_scores():
    """Load scores from JSON file"""
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

def save_questions(questions):
    """Save questions to JSON file"""
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(questions, f)

def save_scores(scores):
    """Save scores to JSON file"""
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

# Score Functions
def save_quiz_score(username, score, max_score):
    scores = load_scores()
    score_data = {
        "username": username,
        "score": score,
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    scores.append(score_data)
    save_scores(scores)

def get_user_scores(username):
    scores = load_scores()
    return [s for s in scores if s["username"] == username]