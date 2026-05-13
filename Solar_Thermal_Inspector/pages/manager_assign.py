# pages/manager_assign.py
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
st.session_state['current_page'] = 'assign'

# Afficher la sidebar
show_sidebar()

# Récupérer la zone
user_zone = get_current_zone()

# En-tête
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Assigner une mission</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# Chargement des données
def load_defects():
    try:
        df = pd.read_csv("data/defects.csv")
        if 'zone' not in df.columns:
            df['zone'] = 'Noor III'
        if 'statut' not in df.columns:
            df['statut'] = 'Nouveau'
        non_assigned = df[~df['statut'].isin(['Assigné', 'Résolu', 'Terminé'])].copy()
        non_assigned = non_assigned[non_assigned['zone'] == user_zone]
        return non_assigned
    except FileNotFoundError:
        sample_defects = pd.DataFrame([
            {"id": 1, "type": "Hotspot récepteur", "gravite": "Critique", "localisation": "Tour-Nord", "temperature": 158, "date_detection": datetime.now().strftime("%Y-%m-%d %H:%M"), "statut": "Nouveau", "zone": user_zone},
            {"id": 2, "type": "Microfissure", "gravite": "Haute", "localisation": "L5-C3", "temperature": 89, "date_detection": datetime.now().strftime("%Y-%m-%d %H:%M"), "statut": "Nouveau", "zone": user_zone},
        ])
        sample_defects.to_csv("data/defects.csv", index=False)
        return sample_defects

def load_technicians():
    try:
        df = pd.read_csv("data/users.csv")
        return df[(df['role'] == 'technician') & (df['zone'] == user_zone)].copy()
    except FileNotFoundError:
        return pd.DataFrame()

def load_missions():
    try:
        return pd.read_csv("data/missions_manager.csv")
    except FileNotFoundError:
        return pd.DataFrame()

def save_defect(defects_df):
    defects_df.to_csv("data/defects.csv", index=False)

def save_mission(mission):
    try:
        missions = pd.read_csv("data/missions_manager.csv")
        new_id = len(missions) + 1
        mission['id'] = new_id
        missions = pd.concat([missions, pd.DataFrame([mission])], ignore_index=True)
        missions.to_csv("data/missions_manager.csv", index=False)
    except FileNotFoundError:
        mission['id'] = 1
        pd.DataFrame([mission]).to_csv("data/missions_manager.csv", index=False)

defects = load_defects()
techniciens = load_technicians()
nb_defauts = len(defects)
nb_techniciens = len(techniciens)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{nb_defauts}</div>
        <div class="stat-label">Défauts en attente</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{nb_techniciens}</div>
        <div class="stat-label">Techniciens disponibles</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    missions = load_missions()
    en_cours = len(missions[missions['statut'] == 'En cours']) if len(missions) > 0 else 0
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{en_cours}</div>
        <div class="stat-label">Missions en cours</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Assignation
if nb_defauts == 0:
    st.info(f"Aucun défaut en attente d'assignation dans la zone {user_zone}")
elif nb_techniciens == 0:
    st.warning(f"Aucun technicien disponible dans la zone {user_zone}")
else:
    st.markdown('<div class="section-title">Nouvelle assignation</div>', unsafe_allow_html=True)
    
    st.markdown("**1. Sélectionner un défaut**")
    defect_options = {f"{row['type']} - {row['gravite']} - {row['localisation']} ({row['temperature']}°C)": row['id'] for idx, row in defects.iterrows()}
    selected_defect_label = st.selectbox("Choisir un défaut", list(defect_options.keys()))
    selected_defect_id = defect_options[selected_defect_label]
    selected_defect = defects[defects['id'] == selected_defect_id].iloc[0]
    
    st.markdown(f"""
    <div style="background-color: #f5f5f5; border-radius: 16px; padding: 15px; margin: 10px 0; border-left: 4px solid #f44336;">
        <strong>Détails du défaut</strong><br>
        Type: {selected_defect['type']}<br>
        Gravité: {selected_defect['gravite']}<br>
        Localisation: {selected_defect['localisation']}<br>
        Température: {selected_defect['temperature']}°C<br>
        Date: {selected_defect['date_detection']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**2. Sélectionner un technicien**")
    tech_options = {f"{row['name']} ({row['email']})": row['name'] for idx, row in techniciens.iterrows()}
    selected_tech_label = st.selectbox("Choisir un technicien", list(tech_options.keys()))
    selected_tech_nom = tech_options[selected_tech_label]
    
    gravite_priorite = {'Critique': 'Urgente', 'Haute': 'Haute', 'Moyenne': 'Normale', 'Basse': 'Basse'}
    default_priority = gravite_priorite.get(selected_defect['gravite'], 'Normale')
    
    st.markdown("**3. Définir la priorité**")
    priorite = st.selectbox("Priorité", ["Urgente", "Haute", "Normale", "Basse"], index=["Urgente", "Haute", "Normale", "Basse"].index(default_priority))
    notes = st.text_area("Notes (optionnel)", placeholder="Instructions supplémentaires...")
    
    if st.button("Assigner la mission", use_container_width=True, type="primary"):
        defects.loc[defects['id'] == selected_defect_id, 'statut'] = 'Assigné'
        save_defect(defects)
        save_mission({'defect_id': selected_defect_id, 'technicien_nom': selected_tech_nom, 'zone': user_zone, 'statut': 'En cours', 'priorite': priorite, 'date_assignation': datetime.now().strftime("%Y-%m-%d %H:%M"), 'notes': notes})
        st.success(f"Mission assignée à {selected_tech_nom} dans la zone {user_zone}")
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# Missions en cours
st.markdown('<div class="section-title">Missions en cours</div>', unsafe_allow_html=True)
missions = load_missions()
if len(missions) > 0:
    missions_en_cours = missions[missions['statut'] == 'En cours'].copy()
    if len(missions_en_cours) > 0:
        display_df = missions_en_cours[['id', 'defect_id', 'technicien_nom', 'priorite', 'date_assignation']].copy()
        display_df.columns = ['ID', 'Défaut', 'Technicien', 'Priorité', 'Date']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune mission en cours")
else:
    st.info("Aucune mission enregistrée")

st.markdown("<hr>", unsafe_allow_html=True)

# Actions
st.markdown('<div class="section-title">Actions</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("← Retour au Dashboard", use_container_width=True):
        st.switch_page("pages/manager_dashboard.py")
with col2:
    if st.button("Gérer les techniciens", use_container_width=True):
        st.switch_page("pages/manager_technicians.py")
        # Après avoir sauvegardé la mission
st.success(f" Mission assignée à {selected_tech_nom} dans la zone {user_zone}")

# Optionnel: envoyer une notification (simulée)
st.info(f" Notification envoyée au technicien {selected_tech_nom}")