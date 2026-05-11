# pages/manager_technicians.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.session_manager import require_manager, get_current_zone
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar

# Appliquer le CSS
apply_global_style()

# Vérification
require_manager()

# Définir l'ID de la page
st.session_state['current_page'] = 'technicians'

# Afficher la sidebar
show_sidebar()

# Récupérer la zone
user_zone = get_current_zone()

# En-tête
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Gestion des techniciens</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# Chargement des données
def load_technicians():
    try:
        df = pd.read_csv("data/users.csv")
        for col in ['phone', 'created_at', 'zone']:
            if col not in df.columns:
                df[col] = ''
        return df
    except FileNotFoundError:
        sample_data = pd.DataFrame([
            {"name": "Ahmed Tech", "email": "ahmed@noor1.com", "password": "tech123", "role": "technician", "zone": "Noor I", "phone": "0612345684", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Fatima Tech", "email": "fatima@noor2.com", "password": "tech123", "role": "technician", "zone": "Noor II", "phone": "0612345685", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Hassan Tech", "email": "hassan@noor3.com", "password": "tech123", "role": "technician", "zone": "Noor III", "phone": "0612345686", "created_at": datetime.now().strftime("%Y-%m-%d")},
            {"name": "Nadia Tech", "email": "nadia@noor4.com", "password": "tech123", "role": "technician", "zone": "Noor IV", "phone": "0612345687", "created_at": datetime.now().strftime("%Y-%m-%d")},
        ])
        sample_data.to_csv("data/users.csv", index=False)
        return sample_data

all_technicians = load_technicians()
technicians = all_technicians[(all_technicians['role'] == 'technician') & (all_technicians['zone'] == user_zone)].copy()
nb_techniciens = len(technicians)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{nb_techniciens}</div>
        <div class="stat-label">Techniciens</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{user_zone}</div>
        <div class="stat-label">Zone actuelle</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">142</div>
        <div class="stat-label">Total missions</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Liste des techniciens
st.markdown('<div class="section-title">Liste des techniciens</div>', unsafe_allow_html=True)

if nb_techniciens > 0:
    display_cols = ['name', 'email', 'zone', 'phone', 'created_at']
    available_cols = [col for col in display_cols if col in technicians.columns]
    display_df = technicians[available_cols].copy()
    column_names = {'name': 'Nom', 'email': 'Email', 'zone': 'Zone', 'phone': 'Téléphone', 'created_at': "Date d'inscription"}
    display_df = display_df.rename(columns=column_names)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info(f"Aucun technicien dans la zone {user_zone}")

st.markdown("<hr>", unsafe_allow_html=True)

# Ajouter un technicien
st.markdown('<div class="section-title">Ajouter un technicien</div>', unsafe_allow_html=True)

with st.form("add_technician_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Nom complet", placeholder="Ex: Jean Dupont")
        new_email = st.text_input("Email", placeholder="jean@solarthermal.com")
    with col2:
        new_phone = st.text_input("Téléphone", placeholder="0612345678")
        new_password = st.text_input("Mot de passe", type="password", placeholder="mot de passe")
    
    st.info(f"Ce technicien sera affecté à la zone {user_zone}")
    
    if st.form_submit_button("Ajouter le technicien", use_container_width=True):
        if new_name and new_email and new_password:
            if new_email in all_technicians['email'].values:
                st.error("Cet email est déjà utilisé.")
            else:
                new_tech = pd.DataFrame([{"name": new_name, "email": new_email, "password": new_password, "role": "technician", "zone": user_zone, "phone": new_phone, "created_at": datetime.now().strftime("%Y-%m-%d")}])
                updated_users = pd.concat([all_technicians, new_tech], ignore_index=True)
                updated_users.to_csv("data/users.csv", index=False)
                st.success(f"Technicien {new_name} ajouté dans la zone {user_zone}")
                st.rerun()
        else:
            st.error("Veuillez remplir tous les champs obligatoires")

st.markdown("<hr>", unsafe_allow_html=True)

# Supprimer un technicien
st.markdown('<div class="section-title">Supprimer un technicien</div>', unsafe_allow_html=True)

if nb_techniciens > 0:
    tech_names = technicians['name'].tolist()
    selected_tech = st.selectbox("Sélectionner un technicien à supprimer", tech_names)
    if st.button("Supprimer", use_container_width=True):
        all_techs = load_technicians()
        updated_techs = all_techs[all_techs['name'] != selected_tech]
        updated_techs.to_csv("data/users.csv", index=False)
        st.success(f"Technicien {selected_tech} supprimé")
        st.rerun()
else:
    st.info(f"Aucun technicien à supprimer dans la zone {user_zone}")

st.markdown("<hr>", unsafe_allow_html=True)

# Actions
st.markdown('<div class="section-title">Actions</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("← Retour au Dashboard", use_container_width=True):
        st.switch_page("pages/manager_dashboard.py")
with col2:
    if st.button("Assigner une mission", use_container_width=True):
        st.switch_page("pages/manager_assign.py")