# pages/technician_report.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.session_manager import get_current_user, get_current_zone, require_auth
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar

# Configuration
apply_global_style()
require_auth()

st.session_state['current_page'] = 'tech_report'
show_sidebar()

user = get_current_user()
user_zone = get_current_zone()

st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Envoyer un rapport</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# Charger les missions du technicien
def load_technician_missions():
    try:
        missions = pd.read_csv("data/missions.csv")
        
        # Vérifier les colonnes existantes
        print("Colonnes disponibles:", missions.columns.tolist())
        
        # Trouver la colonne qui contient le nom du technicien
        tech_col = None
        for col in ['technicien_nom', 'technicien', 'assigned_to', 'technician_name', 'technicien']:
            if col in missions.columns:
                tech_col = col
                break
        
        if tech_col is None:
            st.error("La colonne technicien est introuvable dans missions.csv")
            return pd.DataFrame()
        
        # Filtrer les missions du technicien
        missions_tech = missions[missions[tech_col] == user.get('name', '')]
        
        # Filtrer les missions terminées
        if 'statut' in missions_tech.columns:
            missions_terminees = missions_tech[missions_tech['statut'] == 'Terminée']
        else:
            missions_terminees = missions_tech
        
        return missions_terminees
    except FileNotFoundError:
        return pd.DataFrame()

# Sauvegarder le rapport
def save_rapport(mission_id, contenu):
    os.makedirs("data", exist_ok=True)
    
    rapport_file = "data/rapports_techniciens.csv"
    new_rapport = pd.DataFrame([{
        "id": int(datetime.now().timestamp()),
        "mission_id": mission_id,
        "technicien_nom": user.get('name', ''),
        "technicien_zone": user_zone,
        "date_rapport": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "contenu": contenu,
        "statut": "Envoyé"
    }])
    
    if os.path.exists(rapport_file):
        df = pd.read_csv(rapport_file)
        df = pd.concat([df, new_rapport], ignore_index=True)
    else:
        df = new_rapport
    
    df.to_csv(rapport_file, index=False)
    return True

missions = load_technician_missions()

if len(missions) > 0:
    st.subheader("Sélectionner une mission terminée")
    
    # Afficher les missions disponibles
    mission_options = {}
    for idx, row in missions.iterrows():
        mission_id = row.get('id', idx)
        date = row.get('date_assignation', 'Date inconnue')
        mission_options[f"Mission {mission_id} - {date}"] = mission_id
    
    selected_mission = st.selectbox("Mission", list(mission_options.keys()))
    mission_id = mission_options[selected_mission]
    
    st.subheader("Rapport d'intervention")
    rapport_contenu = st.text_area("Détail de l'intervention", height=200, 
                                   placeholder="Décrivez votre intervention, les réparations effectuées, le matériel utilisé...")
    
    if st.button("Envoyer rapport au Manager", use_container_width=True, type="primary"):
        if rapport_contenu:
            save_rapport(mission_id, rapport_contenu)
            st.success(" Rapport envoyé au manager de votre zone !")
            st.balloons()
        else:
            st.error("Veuillez remplir le contenu du rapport")
else:
    st.info("📋 Aucune mission terminée à rapporter")