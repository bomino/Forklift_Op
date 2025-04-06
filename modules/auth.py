import hashlib
from .data_manager import load_users, save_users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return True, users[username]["role"], users[username]["name"]
    return False, None, None

def add_user(username, password, name, role="operator"):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": hash_password(password),
        "role": role,
        "name": name
    }
    save_users(users)
    return True, "User added successfully"