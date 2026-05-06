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
    "user_email": None
}

def init_session_state():
    """Initialise les variables de session si elles n'existent pas"""
    for key, default_value in SESSION_KEYS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def init_users_db():
    """
    Crée le fichier users.csv s'il n'existe pas
    """
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists("data/users.csv"):
        df = pd.DataFrame(columns=["email", "name", "password_hash", "role", "date_inscription"])
        df.to_csv("data/users.csv", index=False)
        
        # Ajouter un utilisateur admin par défaut (optionnel)
        default_password = "admin123"
        hashed = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        
        admin_row = pd.DataFrame([{
            "email": "admin@solar.com",
            "name": "Administrateur",
            "password_hash": hashed.decode('utf-8'),
            "role": "manager",
            "date_inscription": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        admin_row.to_csv("data/users.csv", mode='a', header=False, index=False)

def get_users_df():
    """
    Charge la liste des utilisateurs depuis le fichier CSV
    """
    try:
        df = pd.read_csv("data/users.csv")
        return df
    except FileNotFoundError:
        init_users_db()
        return pd.read_csv("data/users.csv")

def save_user(email, name, password, role="technician"):
    """
    Enregistre un nouvel utilisateur dans la base de données
    """
    df = get_users_df()
    
    # Vérifier si l'email existe déjà
    if email in df['email'].values:
        return False, "Cet email est déjà utilisé. Veuillez vous connecter."
    
    # Hacher le mot de passe
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Créer le nouvel utilisateur
    new_user = pd.DataFrame([{
        "email": email,
        "name": name,
        "password_hash": hashed.decode('utf-8'),
        "role": role,
        "date_inscription": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    # Ajouter au fichier CSV
    new_user.to_csv("data/users.csv", mode='a', header=False, index=False)
    
    return True, "Inscription réussie ! Vous pouvez maintenant vous connecter."

def verify_password(plain_password, hashed_password):
    """
    Vérifie si le mot de passe correspond au hash stocké
    """
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False

def authenticate_user(email, password):
    """
    Vérifie les identifiants et retourne les informations utilisateur
    """
    df = get_users_df()
    
    if df.empty:
        return None
    
    # Chercher l'utilisateur par email
    user = df[df['email'] == email]
    
    if user.empty:
        return None
    
    user = user.iloc[0]
    
    # Vérifier le mot de passe
    if verify_password(password, user['password_hash']):
        return {
            "email": user['email'],
            "name": user['name'],
            "role": user['role']
        }
    
    return None

def login_user(email, name, role):
    """
    Connecte l'utilisateur en stockant ses informations
    """
    st.session_state.logged_in = True
    st.session_state.user_email = email
    st.session_state.user_name = name
    st.session_state.user_role = role

def logout_user():
    """
    Déconnecte l'utilisateur et vide la session
    """
    for key in SESSION_KEYS.keys():
        st.session_state[key] = SESSION_KEYS[key]

def is_logged_in():
    """
    Vérifie si un utilisateur est connecté
    """
    return st.session_state.get("logged_in", False)

def get_current_user():
    """
    Retourne les informations de l'utilisateur connecté
    """
    if is_logged_in():
        return {
            "email": st.session_state.user_email,
            "name": st.session_state.user_name,
            "role": st.session_state.user_role
        }
    return None

def require_auth():
    """
    Redirige vers la page de login si non connecté
    """
    if not is_logged_in():
        st.switch_page("login.py")