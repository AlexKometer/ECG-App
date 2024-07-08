import streamlit as st
import json
import hashlib
import os

# Path to the users.json file
USERS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/users.json')


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Function to authenticate users
def authenticate(username, password):
    with open(USERS_FILE_PATH) as f:
        users = json.load(f)
    for user in users:
        if user['username'] == username and user['password'] == hash_password(password):
            return user
    return None


# Function to handle user login
def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        user = authenticate(username, password)
        if user:
            st.session_state['user'] = user
            st.session_state['current_page'] = 'app'
            st.experimental_rerun()  # Trigger a rerun immediately after setting the page
        else:
            st.error("Invalid username or password")


# Function to handle user registration
def register_user(username, password, role):
    with open(USERS_FILE_PATH, 'r+') as f:
        users = json.load(f)
        users.append({
            "username": username,
            "password": hash_password(password),
            "role": role,
            "subjects": []
        })
        f.seek(0)
        json.dump(users, f, indent=4)


def register():
    st.title("Register")
    username = st.text_input("New Username", key="register_username")
    password = st.text_input("New Password", type="password", key="register_password")

    # Ensure only one admin
    with open(USERS_FILE_PATH) as f:
        users = json.load(f)
        existing_admin = any(user['role'] == 'admin' for user in users)

    if existing_admin:
        role = "custom"
    else:
        role = st.selectbox("Role", ["custom", "admin"], key="register_role")

    if st.button("Register", key="register_button"):
        register_user(username, password, role)
        st.session_state['user'] = authenticate(username, password)
        st.session_state['current_page'] = 'app'
        st.experimental_rerun()  # Trigger a rerun immediately after setting the page
