# utils/session_manager.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Fichier CSV des utilisateurs
USERS_FILE = "data/users.csv"

def init_session_state():
    """Initialise les variables de session"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_zone' not in st.session_state:
        st.session_state.user_zone = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

def init_users_db():
    """Initialise la base de données utilisateurs"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(USERS_FILE):
        sample_users = pd.DataFrame([
            {"name": "Ali Manager", "email": "ali@noor1.com", "password": "manager123", "role": "manager", "zone": "Noor I", "phone": "0612345679", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Sara Manager", "email": "sara@noor2.com", "password": "manager123", "role": "manager", "zone": "Noor II", "phone": "0612345680", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Karim Manager", "email": "karim@noor3.com", "password": "manager123", "role": "manager", "zone": "Noor III", "phone": "0612345681", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Leila Manager", "email": "leila@noor4.com", "password": "manager123", "role": "manager", "zone": "Noor IV", "phone": "0612345682", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Ahmed Tech", "email": "ahmed@noor1.com", "password": "tech123", "role": "technician", "zone": "Noor I", "phone": "0612345684", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Fatima Tech", "email": "fatima@noor2.com", "password": "tech123", "role": "technician", "zone": "Noor II", "phone": "0612345685", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Hassan Tech", "email": "hassan@noor3.com", "password": "tech123", "role": "technician", "zone": "Noor III", "phone": "0612345686", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Nadia Tech", "email": "nadia@noor4.com", "password": "tech123", "role": "technician", "zone": "Noor IV", "phone": "0612345687", "created_at": datetime.now().strftime("%Y-%m-%d")},
        ])
        sample_users.to_csv(USERS_FILE, index=False)
        print("✅ Base de données utilisateurs créée")

def check_auth(email, password):
    """Vérifie les identifiants"""
    try:
        if not os.path.exists(USERS_FILE):
            init_users_db()
        
        df = pd.read_csv(USERS_FILE)
        user = df[df['email'] == email]
        
        if len(user) == 0:
            return False, None
        
        user = user.iloc[0]
        stored_password = str(user['password']) if not pd.isna(user['password']) else ""
        
        if stored_password == password:
            user_dict = user.to_dict()
            for key in ['role', 'zone', 'name', 'email']:
                user_dict[key] = str(user_dict.get(key, ''))
            return True, user_dict
        
        return False, None
    except Exception as e:
        print(f"Erreur check_auth: {e}")
        return False, None

def authenticate_user(email, password):
    """Authentifie l'utilisateur"""
    success, user_data = check_auth(email, password)
    if success:
        st.session_state.logged_in = True
        st.session_state.user = user_data
        st.session_state.user_role = user_data.get('role', 'technician')
        st.session_state.user_zone = user_data.get('zone', 'toutes')
        st.session_state.user_name = user_data.get('name', '')
        st.session_state.user_email = user_data.get('email', '')
        return user_data
    return None

def login_user(email, name, role, zone="toutes"):
    """Connecte l'utilisateur directement"""
    st.session_state.logged_in = True
    st.session_state.user = {"email": email, "name": name, "role": role, "zone": zone}
    st.session_state.user_role = role
    st.session_state.user_zone = zone
    st.session_state.user_name = name
    st.session_state.user_email = email

def logout_user():
    """Déconnecte l'utilisateur"""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_role = None
    st.session_state.user_zone = None
    st.session_state.user_name = None
    st.session_state.user_email = None

def is_logged_in():
    """Vérifie si l'utilisateur est connecté"""
    return st.session_state.get('logged_in', False)

def require_auth():
    """Vérifie que l'utilisateur est connecté"""
    if not is_logged_in():
        st.switch_page("pages/login.py")
        st.stop()

def require_manager():
    """Vérifie que l'utilisateur est manager"""
    role = st.session_state.get('user_role', '')
    if role != 'manager':
        st.error("⛔ Accès réservé aux managers")
        st.stop()

def get_current_user():
    """Retourne l'utilisateur courant"""
    return st.session_state.get('user', {})

def get_current_zone():
    """Retourne la zone de l'utilisateur courant"""
    return st.session_state.get('user_zone', 'toutes')

def get_current_role():
    """Retourne le rôle de l'utilisateur courant"""
    return st.session_state.get('user_role', '')

def save_user(email, name, password, role, zone="toutes"):
    """Enregistre un nouvel utilisateur"""
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE)
        if email in df['email'].values:
            return False, "Cet email est déjà utilisé"
    else:
        df = pd.DataFrame(columns=['name', 'email', 'password', 'role', 'zone', 'phone', 'created_at'])
    
    new_user = pd.DataFrame([{
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "zone": zone,
        "phone": "",
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }])
    
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    
    return True, "Compte créé avec succès !"