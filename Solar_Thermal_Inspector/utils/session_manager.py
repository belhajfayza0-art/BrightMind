"""
Gestionnaire de sessions utilisateur
Gère la connexion, l'inscription et la persistence des données
"""

import streamlit as st
import pandas as pd
import bcrypt
from datetime import datetime
import os

# Clés utilisées dans session_state
SESSION_KEYS = {
    "logged_in": False,
    "user_role": None,
    "user_name": None,
    "user_email": None,
    "user_zone": None
}

def init_session_state():
    """Initialise les variables de session si elles n'existent pas"""
    for key, default_value in SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def get_users_df():
    """Charge la liste des utilisateurs depuis le fichier CSV"""
    try:
        df = pd.read_csv("data/users.csv")
        return df
    except FileNotFoundError:
        init_users_db()
        return pd.read_csv("data/users.csv")

def init_users_db():
    """Crée le fichier users.csv s'il n'existe pas"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists("data/users.csv"):
        df = pd.DataFrame(columns=["email", "name", "password_hash", "role", "zone", "date_inscription"])
        df.to_csv("data/users.csv", index=False)

def save_user(email, name, password, role, zone="Noor IV"):
    """Enregistre un nouvel utilisateur"""
    df = get_users_df()
    
    if email in df['email'].values:
        return False, "Cet email est déjà utilisé."
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    new_user = pd.DataFrame([{
        "email": email,
        "name": name,
        "password_hash": hashed.decode('utf-8'),
        "role": role,
        "zone": zone,
        "date_inscription": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    new_user.to_csv("data/users.csv", mode='a', header=False, index=False)
    return True, "Inscription réussie !"

def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False

def authenticate_user(email, password):
    df = get_users_df()
    if df.empty:
        return None
    
    user = df[df['email'] == email]
    if user.empty:
        return None
    
    user = user.iloc[0]
    
    if verify_password(password, user['password_hash']):
        return {
            "email": user['email'],
            "name": user['name'],
            "role": user['role'],
            "zone": user.get('zone', 'Noor IV')
        }
    return None

def login_user(email, name, role, zone):
    st.session_state.logged_in = True
    st.session_state.user_email = email
    st.session_state.user_name = name
    st.session_state.user_role = role
    st.session_state.user_zone = zone

def logout_user():
    for key in SESSION_KEYS.keys():
        st.session_state[key] = SESSION_KEYS[key]

def is_logged_in():
    return st.session_state.get("logged_in", False)

def get_current_user():
    if is_logged_in():
        return {
            "email": st.session_state.user_email,
            "name": st.session_state.user_name,
            "role": st.session_state.user_role,
            "zone": st.session_state.get('user_zone', 'Noor IV')
        }
    return None

def get_current_role():
    return st.session_state.get('user_role', None)

def get_current_zone():
    return st.session_state.get('user_zone', 'Noor IV')

def require_auth():
    if not is_logged_in():
        st.switch_page("login.py")

def require_manager():
    if not is_logged_in() or get_current_role() != 'manager':
        st.error("⛔ Accès réservé aux managers")
        st.stop()