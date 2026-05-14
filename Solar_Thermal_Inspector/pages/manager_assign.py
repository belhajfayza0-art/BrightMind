# pages/manager_assign.py
import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
from utils.session_manager import require_manager, get_current_zone
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar
from backend.alert_service import get_pending_alerts_by_zone, assign_alert_to_technician
from backend.ai_monitor import simulate_ai_detection

# Appliquer le CSS
apply_global_style()
require_manager()

st.set_page_config(page_title="Assigner une mission", page_icon="📋", layout="wide")
st.session_state['current_page'] = 'assign'

show_sidebar()
user_zone = get_current_zone()

# ============================================
# FONCTIONS DE CHARGEMENT DES DONNÉES
# ============================================

def load_pending_alerts():
    """Charge les alertes en attente UNIQUEMENT pour la zone du manager"""
    try:
        df = pd.read_csv("data/alerts.csv")
        # ⚠️ Filtre par zone du manager ET status pending
        df = df[(df['zone'] == user_zone) & (df['status'] == 'pending')]
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def load_technicians():
    """Charge les techniciens de la zone"""
    try:
        df = pd.read_csv("data/users.csv")
        return df[(df['role'] == 'technician') & (df['zone'] == user_zone)].copy()
    except FileNotFoundError:
        return pd.DataFrame()

def load_defects():
    """Charge les défauts enregistrés"""
    try:
        df = pd.read_csv("data/defects.csv")
        if 'status' in df.columns and 'statut' not in df.columns:
            df['statut'] = df['status']
        if 'zone' not in df.columns:
            df['zone'] = user_zone
        if 'statut' not in df.columns:
            df['statut'] = 'Nouveau'
        non_assigned = df[~df['statut'].isin(['Assigné', 'Résolu', 'Terminé', 'completed'])].copy()
        if 'zone' in non_assigned.columns:
            non_assigned = non_assigned[non_assigned['zone'] == user_zone]
        return non_assigned
    except FileNotFoundError:
        return pd.DataFrame()

def load_missions():
    """Charge les missions"""
    try:
        df = pd.read_csv("data/missions.csv")
        if 'status' in df.columns and 'statut' not in df.columns:
            df['statut'] = df['status']
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def load_active_missions():
    """Charge les missions en cours"""
    try:
        df = pd.read_csv("data/missions.csv")
        # Filtrer par zone et statut (pending ou in_progress)
        missions_en_cours = df[(df['zone'] == user_zone) & (df['status'].isin(['pending', 'in_progress']))]
        return missions_en_cours
    except FileNotFoundError:
        return pd.DataFrame()
    
    
def save_defect(defects_df):
    """Sauvegarde les défauts"""
    defects_df.to_csv("data/defects.csv", index=False)

def save_mission(mission):
    """Sauvegarde une mission"""
    try:
        missions = pd.read_csv("data/missions.csv")
        new_id = len(missions) + 1
        mission['id'] = new_id
        missions = pd.concat([missions, pd.DataFrame([mission])], ignore_index=True)
        missions.to_csv("data/missions.csv", index=False)
    except FileNotFoundError:
        mission['id'] = 1
        pd.DataFrame([mission]).to_csv("data/missions.csv", index=False)

# ============================================
# GÉNÉRATION AUTOMATIQUE D'ALERTES IA
# ============================================

# Génération aléatoire (70% de chance)
if random.random() < 0.7:
    result = simulate_ai_detection()
    if result['status'] == 'pending_manager':
        st.toast(f"🤖 IA : Nouveau défaut - {result['defect']['defect_type']} dans la zone {result['zone']}", icon="🔔")
    elif result['status'] == 'assigned':
        tech_name = result.get('technician', 'inconnu')
        st.toast(f"🤖 IA : Auto-assigné à {tech_name} dans la zone {result['zone']} (manager absent)", icon="ℹ️")

# Génération périodique (toutes les 3 minutes)
current_minute = datetime.now().minute
last_key = 'last_alert_minute_manager'

if st.session_state.get(last_key, -1) != current_minute and current_minute % 3 == 0:
    st.session_state[last_key] = current_minute
    result = simulate_ai_detection()
    if result['status'] == 'pending_manager':
        st.toast(f"🤖 IA : Alerte périodique - {result['defect']['defect_type']} dans {result['zone']}", icon="⚠️")
    elif result['status'] == 'assigned':
        tech_name = result.get('technician', 'inconnu')
        st.toast(f"🤖 IA : Auto-assigné à {tech_name} dans la zone {result['zone']} (manager absent)", icon="ℹ️")

# ============================================
# EN-TÊTE
# ============================================
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Assigner une mission</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# SECTION 1 : DÉFAUTS EN ATTENTE D'ASSIGNATION (IA)
# ============================================
st.markdown('<div class="section-title">🚨 Défauts en attente d\'assignation (IA)</div>', unsafe_allow_html=True)

alerts = load_pending_alerts()

if len(alerts) == 0:
    st.success(f"✅ Aucun défaut en attente dans la zone {user_zone}")
else:
    st.warning(f"⚠️ {len(alerts)} défaut(s) détecté(s) par l'IA en attente d'assignation")
    
    for idx, (_, alert) in enumerate(alerts.iterrows()):
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 16px; padding: 1rem; margin-bottom: 1rem; border-left: 4px solid #ef4444;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="font-weight: 700;">{alert['defect_type']}</span>
                        <div style="font-size: 0.8rem; color: #6b7280;">📍 {alert['location']}</div>
                        <div style="font-size: 0.8rem;">🌡️ {alert['temperature']}°C</div>
                        <div style="font-size: 0.7rem; color: #9ca3af;">🕐 Détecté le : {alert['detected_at']}</div>
                    </div>
                    <div>
                        <span class="badge-critical">En attente</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                technicians = load_technicians()
                if len(technicians) > 0:
                    tech_options = {row['name']: row['name'] for _, row in technicians.iterrows()}
                    selected_tech = st.selectbox("Assigner à", list(tech_options.keys()), key=f"tech_alert_{idx}")
                else:
                    selected_tech = None
                    st.error("❌ Aucun technicien disponible")
            
            with col2:
                if selected_tech:
                    if st.button("📋 Assigner", key=f"assign_alert_{idx}", type="primary"):
                        mission_id = assign_alert_to_technician(alert['id'], selected_tech)
                        st.success(f"✅ Mission #{mission_id} assignée à {selected_tech}")
                        st.rerun()
            
            st.markdown("---")

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# SECTION 2 : STATISTIQUES
# ============================================

# ============================================
# SECTION 2 : STATISTIQUES
# ============================================

defects = load_defects()
techniciens = load_technicians()
active_missions = load_active_missions()  # ← Utiliser cette fonction

nb_defauts = len(alerts)
nb_techniciens = len(techniciens)
en_cours = len(active_missions)  # ← Déjà filtré

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
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{en_cours}</div>
        <div class="stat-label">Missions en cours</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# SECTION 3 : ASSIGNATION MANUELLE
# ============================================

if len(defects) == 0:
    st.info(f"Aucun défaut enregistré dans la zone {user_zone}")
elif nb_techniciens == 0:
    st.warning(f"Aucun technicien disponible dans la zone {user_zone}")
else:
    st.markdown('<div class="section-title">➕ Assigner un défaut existant</div>', unsafe_allow_html=True)
    st.markdown("**1. Sélectionner un défaut**")
    defect_options = {f"{row['type']} - {row['gravite']} - {row['localisation']} ({row['temperature']}°C)": row['id'] for idx, row in defects.iterrows()}
    selected_defect_label = st.selectbox("Choisir un défaut", list(defect_options.keys()), key="select_defect")
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
    selected_tech_label = st.selectbox("Choisir un technicien", list(tech_options.keys()), key="select_tech")
    selected_tech_nom = tech_options[selected_tech_label]
    
    gravite_priorite = {'Critique': 'Urgente', 'Haute': 'Haute', 'Moyenne': 'Normale', 'Basse': 'Basse'}
    default_priority = gravite_priorite.get(selected_defect['gravite'], 'Normale')
    
    st.markdown("**3. Définir la priorité**")
    priorite = st.selectbox("Priorité", ["Urgente", "Haute", "Normale", "Basse"], index=["Urgente", "Haute", "Normale", "Basse"].index(default_priority), key="priorite")
    notes = st.text_area("Notes (optionnel)", placeholder="Instructions supplémentaires...", key="notes_assign")
    
    if st.button("Assigner la mission", use_container_width=True, type="primary", key="assign_btn"):
        defects.loc[defects['id'] == selected_defect_id, 'statut'] = 'Assigné'
        save_defect(defects)
        save_mission({
            'defect_id': selected_defect_id, 
            'technicien_nom': selected_tech_nom,  # ← ICI ça existe
            'zone': user_zone, 
            'statut': 'En cours', 
            'priorite': priorite, 
            'date_assignation': datetime.now().strftime("%Y-%m-%d %H:%M"), 
            'notes': notes
        })
        st.success(f"Mission assignée à {selected_tech_nom} dans la zone {user_zone}")
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# SECTION 4 : MISSIONS EN COURS
# ============================================
st.markdown('<div class="section-title">📋 Missions en cours</div>', unsafe_allow_html=True)
missions = load_missions()
if len(missions) > 0:
    if 'statut' in missions.columns:
        missions_en_cours = missions[missions['statut'] == 'En cours'].copy()
    elif 'status' in missions.columns:
        missions_en_cours = missions[missions['status'] == 'in_progress'].copy()
    else:
        missions_en_cours = pd.DataFrame()
    
    if len(missions_en_cours) > 0:
        display_df = missions_en_cours[['id', 'defect_id', 'technicien_nom', 'priorite', 'date_assignation']].copy()
        display_df.columns = ['ID', 'Défaut', 'Technicien', 'Priorité', 'Date']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune mission en cours")
else:
    st.info("Aucune mission enregistrée")

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================
# SECTION 5 : ACTIONS
# ============================================
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

# Bouton rafraîchissement
if st.button("🔄 Rafraîchir les données", use_container_width=True):
    st.rerun()