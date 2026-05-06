"""
Application principale - Après connexion
Redirige vers le dashboard approprié selon le rôle
"""

import streamlit as st
from utils.session_manager import init_session_state, require_auth, get_current_user, logout_user

# Configuration de la page
st.set_page_config(
    page_title="Solar Thermal Inspector - Dashboard",
    page_icon="☀️",
    layout="wide"
)

# Initialiser la session
init_session_state()

# Vérifier si l'utilisateur est connecté
require_auth()

# Récupérer les infos de l'utilisateur
user = get_current_user()

# ============================================
# BARRE LATÉRALE
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/solar-panel.png", width=80)
    st.title("SOLAR THERMAL")
    st.markdown(f"### 👋 {user['name']}")
    st.markdown(f"📧 {user['email']}")
    
    if user['role'] == 'manager':
        st.markdown("🔑 **Rôle:** 📊 Manager")
    else:
        st.markdown("🔑 **Rôle:** 🔧 Technicien")
    
    st.markdown("---")
    
    if st.button("🚪 Déconnexion", use_container_width=True):
        logout_user()
        st.rerun()

# ============================================
# CONTENU PRINCIPAL
# ============================================
st.title("☀️ Solar Thermal Inspector")
st.markdown(f"### Bienvenue {user['name']} !")

if user['role'] == 'manager':
    st.info("📊 **Vue Manager** - Dashboard des statistiques et gestion des techniciens")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Panneaux", "156")
    with col2:
        st.metric("⚠️ Défauts", "12")
    with col3:
        st.metric("🔧 Techniciens", "4")
    with col4:
        st.metric("⚡ Efficacité", "89%")
    
    st.markdown("---")
    st.markdown("### 🎯 Actions disponibles")
    st.markdown("""
    - 📈 Consulter les statistiques de la station
    - 👥 Gérer les techniciens
    - 📋 Assigner des missions
    - 📊 Générer des rapports
    """)
    
else:
    st.info("🔧 **Vue Technicien** - Gestion de vos missions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Missions en cours", "3")
    with col2:
        st.metric("✅ Missions terminées", "24")
    with col3:
        st.metric("⭐ Note moyenne", "4.8/5")
    
    st.markdown("---")
    st.markdown("### 🎯 Actions disponibles")
    st.markdown("""
    - 📋 Voir mes missions assignées
    - 🗺️ Localiser les défauts sur la carte
    - ✅ Confirmer la fin des interventions
    - 📊 Consulter mes statistiques
    """)

st.markdown("---")
st.success(f"✅ Connecté en tant que {user['role']} - {user['name']}")