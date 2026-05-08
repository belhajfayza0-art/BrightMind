"""
Détail d'une mission pour le technicien
Permet de voir les instructions et terminer la mission
"""

import streamlit as st
from backend.technician_service import get_mission_by_id, update_mission_status
from components.sidebar import render_sidebar
from components.style import apply_style

# Configuration de la page
st.set_page_config(page_title="Détail Mission", page_icon="🔧", layout="wide")
st.session_state.current_page = 'missions'

# Vérification de l'accès
if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

if 'selected_mission' not in st.session_state:
    st.warning("Aucune mission sélectionnée")
    if st.button("◀️ Retour au dashboard"):
        st.switch_page("pages/technician_dashboard.py")
    st.stop()

mission_id = st.session_state.selected_mission
mission = get_mission_by_id(mission_id)

if mission is None:
    st.error("Mission non trouvée")
    st.stop()

technician_name = st.session_state.user_name

# Application du style et du menu
apply_style()
render_sidebar(technician_name)

# ============================================
# CONTENU PRINCIPAL
# ============================================

severity_emoji = "🔴" if mission['severity'] == 'critical' else "🟠" if mission['severity'] == 'high' else "🟡"
st.title(f"{severity_emoji} Mission #{mission_id}")
st.markdown("---")

# Informations générales
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Informations générales")
    st.write(f"**Type de défaut :** {mission['defect_type']}")
    st.write(f"**Priorité :** {severity_emoji} {mission['severity']}")
    st.write(f"**📍 Localisation :** {mission['location']}")
    st.write(f"**🌡️ Température :** {mission['temperature']}°C")

with col2:
    st.subheader("📅 Dates")
    st.write(f"**Créée le :** {mission['created_at']}")
    if mission['completed_at'] and mission['completed_at'] != '':
        st.write(f"**Terminée le :** {mission['completed_at']}")
    status_text = {
        'pending': '🆕 En attente',
        'in_progress': '🔄 En cours',
        'completed': '✅ Terminée'
    }.get(mission['status'], mission['status'])
    st.write(f"**Statut :** {status_text}")

st.markdown("---")

# Instructions
st.subheader("🛠️ Instructions d'intervention")

instructions = {
    "Hotspot": """
    1. **Nettoyage** : Utiliser un chiffon microfibre non abrasif
    2. **Refroidissement** : Vérifier la ventilation arrière du panneau
    3. **Contrôle** : Mesurer la température après 30 minutes
    4. **Vérification** : Comparer avec les panneaux voisins
    
    ⚠️ **Précautions** : 
    - Couper le circuit avant intervention
    - Porter des gants isolants
    """,
    
    "Crack": """
    1. **Sécurité** : Couper le circuit électrique
    2. **Inspection** : Vérifier l'étendue de la fissure
    3. **Réparation** : Application de résine de protection
    4. **Test** : Vérifier l'isolation électrique
    
    ⚠️ **Précautions** :
    - Ne pas toucher les parties sous tension
    - Remplacer le panneau si la fissure est profonde
    """,
    
    "Dust": """
    1. **Nettoyage** : Eau déminéralisée + chiffon doux
    2. **Séchage** : Laisser sécher à l'air libre
    3. **Contrôle** : Vérifier l'absence de résidus
    
    ⚠️ **Précautions** :
    - Ne pas utiliser de produits abrasifs
    - Nettoyer tôt le matin ou tard le soir
    """,
    
    "Shading": """
    1. **Identification** : Localiser la source d'ombre
    2. **Élagage** : Tailler les branches si nécessaire
    3. **Nettoyage** : Enlever les débris
    
    ⚠️ **Précautions** :
    - Vérifier les autorisations d'élagage
    """,
    
    "Broken Cell": """
    1. **Sécurité** : Couper immédiatement le circuit
    2. **Isolement** : Isoler le panneau endommagé
    3. **Remplacement** : Commander un nouveau panneau
    4. **Installation** : Faire appel à un installateur certifié
    
    ⚠️ **Précautions** :
    - DANGER ! Ne pas toucher les cellules exposées
    - Contacter le manager immédiatement
    """
}

default_instructions = """
1. **Inspection visuelle** : Identifier la cause
2. **Nettoyage** : Si nécessaire
3. **Test** : Vérifier le fonctionnement
4. **Rapport** : Documenter l'intervention
"""

defect_type = mission['defect_type']
st.markdown(instructions.get(defect_type, default_instructions))

st.markdown("---")

# Rapport d'intervention
if mission['status'] != 'completed':
    st.subheader("📝 Rapport d'intervention")
    
    notes = st.text_area("Notes de l'intervention", height=150, 
                         placeholder="Décrivez les actions effectuées, le matériel utilisé, etc...")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✅ Marquer comme terminée", type="primary"):
            if notes:
                update_mission_status(mission_id, 'completed', notes)
            else:
                update_mission_status(mission_id, 'completed', "Intervention terminée")
            st.success("🎉 Mission terminée avec succès !")
            del st.session_state.selected_mission
            st.switch_page("pages/technician_dashboard.py")
    
    with col_btn2:
        if st.button("◀️ Retour au dashboard"):
            del st.session_state.selected_mission
            st.switch_page("pages/technician_dashboard.py")

else:
    st.subheader("📝 Rapport d'intervention")
    if mission['notes'] and mission['notes'] != '':
        st.write(mission['notes'])
    else:
        st.write("Aucun rapport disponible")
    
    if st.button("◀️ Retour au dashboard"):
        del st.session_state.selected_mission
        st.switch_page("pages/technician_dashboard.py")