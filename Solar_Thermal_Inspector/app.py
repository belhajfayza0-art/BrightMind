# app.py
import streamlit as st
from utils.session_manager import init_session_state, require_auth, get_current_user, get_current_role, get_current_zone
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar

# Configuration
st.set_page_config(
    page_title="Solar Thermal Inspector",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le CSS global
apply_global_style()

# Initialisation
init_session_state()
require_auth()

user = get_current_user()
user_role = get_current_role()
user_zone = get_current_zone()

# Définir l'ID de la page pour la clé unique
st.session_state['current_page'] = 'home'

# Afficher la sidebar
show_sidebar()

# Contenu principal
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Solar Thermal Inspector</div>
    <div class="main-header-subtitle">Bienvenue {user.get('name', '')}</div>
</div>
""", unsafe_allow_html=True)

if user_role == 'manager':
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">1.4M</div>
            <div class="stat-label">Panneaux inspectés</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">42</div>
            <div class="stat-label">Défauts actifs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">8</div>
            <div class="stat-label">Techniciens</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">97%</div>
            <div class="stat-label">Précision IA</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Actions rapides</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Tableau de bord détaillé", use_container_width=True):
            st.switch_page("pages/manager_dashboard.py")
    
    with col2:
        if st.button("Assigner une mission", use_container_width=True):
            st.switch_page("pages/manager_assign.py")
    
    with col3:
        if st.button("Générer un rapport", use_container_width=True):
            st.switch_page("pages/manager_reports.py")
    
    st.info("Utilisez le menu latéral pour accéder à toutes les fonctionnalités.")

else:
    st.markdown(f"Zone d'affectation : **{user_zone}**")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Missions en cours", "3")
    with col2:
        st.metric("Missions terminées", "24")
    with col3:
        st.metric("Efficacité", "96%")