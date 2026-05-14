"""
Page des alertes pour les techniciens
Affiche les missions assignées au technicien
"""

import streamlit as st
import pandas as pd
from backend.technician_service import get_technician_missions_by_zone
from components.sidebar import render_sidebar
from components.style import apply_style

# Configuration
st.set_page_config(page_title="Mes Missions", page_icon="📋", layout="wide")
st.session_state.current_page = 'alerts'

if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name
technician_zone = st.session_state.get('user_zone', 'Noor IV')

apply_style()
render_sidebar(technician_name)

st.title("📋 Mes missions assignées")
st.markdown(f"Zone: **{technician_zone}**")
st.markdown("---")

# Récupérer les missions assignées au technicien
missions = get_technician_missions_by_zone(technician_name, technician_zone)

if len(missions) == 0:
    st.info("✅ Aucune mission assignée pour le moment.")
else:
    # Séparer par statut
    pending = missions[missions['status'] == 'pending']
    in_progress = missions[missions['status'] == 'in_progress']
    completed = missions[missions['status'] == 'completed']
    
    # Missions en attente
    if len(pending) > 0:
        st.subheader(f"🆕 Missions assignées ({len(pending)})")
        for _, mission in pending.iterrows():
            assigned_by = mission.get('assigned_by', 'IA')
            st.markdown(f"""
            <div style="border: 1px solid #dcda2c; border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="font-weight: 700;">{mission['defect_type']}</span>
                        <div style="font-size: 0.8rem;">📍 {mission['location']}</div>
                    </div>
                    <div>{mission['temperature']}°C</div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <span class="badge-pending">En attente</span>
                    <span style="font-size: 0.7rem;">Assignée par: {assigned_by}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔍 Voir détails", key=f"detail_{mission['id']}", use_container_width=True):
                st.session_state.selected_mission = mission['id']
                st.switch_page("pages/technician_mission_detail.py")
    
    # Missions en cours
    if len(in_progress) > 0:
        st.subheader(f"🔄 Missions en cours ({len(in_progress)})")
        for _, mission in in_progress.iterrows():
            assigned_by = mission.get('assigned_by', 'IA')
            st.markdown(f"""
            <div style="border: 1px solid #3b82f6; border-radius: 16px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="font-weight: 700;">{mission['defect_type']}</span>
                        <div style="font-size: 0.8rem;">📍 {mission['location']}</div>
                    </div>
                    <div>{mission['temperature']}°C</div>
                </div>
                <div style="margin-top: 0.5rem;">
                    <span class="badge-progress">En cours</span>
                    <span style="font-size: 0.7rem;">Assignée par: {assigned_by}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🔍 Voir détails", key=f"detail_{mission['id']}", use_container_width=True):
                    st.session_state.selected_mission = mission['id']
                    st.switch_page("pages/technician_mission_detail.py")
            with col2:
                if st.button(f"✅ Terminer", key=f"complete_{mission['id']}", use_container_width=True):
                    st.session_state.selected_mission = mission['id']
                    st.switch_page("pages/technician_mission_detail.py")
    
    # Missions terminées
    if len(completed) > 0:
        with st.expander(f"✅ Missions terminées ({len(completed)})"):
            for _, mission in completed.tail(10).iterrows():
                st.markdown(f"✅ {mission['defect_type']} - {mission['location']} (terminée)")