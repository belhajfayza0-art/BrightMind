# components/sidebar.py
import streamlit as st
from utils.session_manager import logout_user

def render_sidebar(technician_name):
    """Affiche le menu latéral commun à toutes les pages"""
    
    with st.sidebar:
        # Menu NAVIGATION
        st.markdown('<div class="menu-title">NAVIGATION</div>', unsafe_allow_html=True)
        
        current_page = st.session_state.get('current_page', 'dashboard')
        
        # Dashboard
        if current_page == 'dashboard':
            st.markdown(f'<div class="menu-active">Dashboard</div>', unsafe_allow_html=True)
        else:
            if st.button("Dashboard", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.switch_page("pages/technician_dashboard.py")
        
        # Alertes IA
        if current_page == 'alerts':
            st.markdown(f'<div class="menu-active">Alertes IA</div>', unsafe_allow_html=True)
        else:
            if st.button("Alertes IA", use_container_width=True):
                st.session_state.current_page = 'alerts'
                st.switch_page("pages/technician_alerts.py")
        
        # Mes missions
        if current_page == 'missions':
            st.markdown(f'<div class="menu-active">Mes missions</div>', unsafe_allow_html=True)
        else:
            if st.button("Mes missions", use_container_width=True):
                st.session_state.current_page = 'missions'
                st.switch_page("pages/technician_missions.py")
        
        # Mon profil
        if current_page == 'profile':
            st.markdown(f'<div class="menu-active">Mon profil</div>', unsafe_allow_html=True)
        else:
            if st.button("Mon profil", use_container_width=True):
                st.session_state.current_page = 'profile'
                st.switch_page("pages/technician_profile.py")
        
        # Carte station
        if current_page == 'map':
            st.markdown(f'<div class="menu-active">Station Noor</div>', unsafe_allow_html=True)
        else:
            if st.button("Station Noor", use_container_width=True):
                st.session_state.current_page = 'map'
                st.switch_page("pages/station_map.py")

        st.markdown('<div class="menu-title">SYSTÈME</div>', unsafe_allow_html=True)
        
        if st.button("Déconnexion", use_container_width=True):
            logout_user()
            st.switch_page("login.py")
        