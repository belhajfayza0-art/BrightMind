# utils/sidebar.py
import streamlit as st
from utils.session_manager import get_current_user, get_current_zone, get_current_role, logout_user

def show_sidebar():
    """Affiche la sidebar commune à toutes les pages"""
    
    user = get_current_user()
    user_zone = get_current_zone()
    user_role = get_current_role()
    
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-title">SOLAR THERMAL</div>
            <div class="sidebar-logo-subtitle">INSPECTOR</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Informations utilisateur
        zone_display = "Toutes les zones" if user_zone == "toutes" else user_zone
        role_display = "Manager" if user_role == "manager" else "Technicien"
        
        st.markdown(f"""
        <div class="user-card">
            <div class="user-name">{user.get('name', '')}</div>
            <div class="user-role">{role_display}</div>
            <div class="user-zone">{zone_display}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu principal - TITRE EN BLANC
        st.markdown('<p style="color: #ffffff; font-size: 12px; letter-spacing: 2px; margin: 15px 0 12px 0; font-weight: 600;">MENU PRINCIPAL</p>', unsafe_allow_html=True)
        
        # Navigation Manager - Liens en BLANC
        if user_role == 'manager':
            st.markdown("""
            <style>
                [data-testid="stSidebar"] a {
                    color: white !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            st.page_link("pages/manager_dashboard.py", label="TABLEAU DE BORD", use_container_width=True)
            st.page_link("pages/manager_technicians.py", label="TECHNICIENS", use_container_width=True)
            st.page_link("pages/manager_assign.py", label="ASSIGNER", use_container_width=True)
            st.page_link("pages/manager_reports.py", label="RAPPORTS", use_container_width=True)
            st.page_link("pages/manager_settings.py", label="PARAMÈTRES", use_container_width=True)
        
        st.markdown("---")
        
        # Bouton DECONNEXION - Version corrigée
        if st.button("DÉCONNEXION", use_container_width=True):
            # Nettoyer la session
            st.session_state.clear()
            # Rediriger vers la page de connexion (qui est à la racine)
            st.switch_page("pages/login.py")
        
        st.markdown('<p style="font-size: 10px; text-align: center; opacity: 0.5; margin-top: 30px; color: #ffffff;">Solar Thermal Inspector v2.0</p>', unsafe_allow_html=True)