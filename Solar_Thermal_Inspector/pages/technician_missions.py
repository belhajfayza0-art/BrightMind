"""
Page de liste des missions du technicien
"""

import streamlit as st
from backend.technician_service import get_technician_missions
from components.sidebar import render_sidebar
from components.style import apply_style

# Configuration de la page
st.set_page_config(page_title="Mes Missions", page_icon="📋", layout="wide")
st.session_state.current_page = 'missions'

# Vérification de l'accès
if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name

# Application du style et du menu
apply_style()
render_sidebar(technician_name)

# ============================================
# CONTENU PRINCIPAL
# ============================================
st.title("📋 Mes missions")
st.markdown("---")

# Récupérer les missions
missions = get_technician_missions(1, technician_name)

if len(missions) == 0:
    st.info("📭 Aucune mission pour le moment.")
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem;">🔧</div>
        <div style="margin-top: 0.5rem;">Les missions apparaîtront ici lorsque l'IA détectera des défauts.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Séparer les missions par statut
    pending = missions[missions['status'] == 'pending']
    in_progress = missions[missions['status'] == 'in_progress']
    completed = missions[missions['status'] == 'completed']
    
    # Missions en attente
    if len(pending) > 0:
        st.subheader(f"🆕 En attente ({len(pending)})")
        for _, mission in pending.iterrows():
            severity_emoji = "🔴" if mission['severity'] == 'critical' else "🟠" if mission['severity'] == 'high' else "🟡"
            
            st.markdown(f"""
            <div class="mission-card" style="border-left-color: #dcda2c;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; font-size: 1rem;">{severity_emoji} {mission['defect_type']}</span>
                        <div style="font-size: 0.8rem; color: #6b7280;">📍 {mission['location']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 600; color: #f97316;">{mission['temperature']}°C</div>
                        <span class="badge-pending">En attente</span>
                    </div>
                </div>
                <div style="margin-top: 0.8rem;">
                    <div style="font-size: 0.7rem; color: #6b7280;">📅 Créée le : {mission['created_at'][:16]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🚀 Commencer cette mission", key=f"start_{mission['id']}", use_container_width=True):
                from backend.technician_service import update_mission_status
                update_mission_status(mission['id'], 'in_progress')
                st.rerun()
    
    # Missions en cours
    if len(in_progress) > 0:
        st.subheader(f"🔄 En cours ({len(in_progress)})")
        for _, mission in in_progress.iterrows():
            severity_emoji = "🔴" if mission['severity'] == 'critical' else "🟠" if mission['severity'] == 'high' else "🟡"
            
            st.markdown(f"""
            <div class="mission-card" style="border-left-color: #3b82f6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; font-size: 1rem;">{severity_emoji} {mission['defect_type']}</span>
                        <div style="font-size: 0.8rem; color: #6b7280;">📍 {mission['location']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-weight: 600; color: #f97316;">{mission['temperature']}°C</div>
                        <span class="badge-progress">En cours</span>
                    </div>
                </div>
                <div style="margin-top: 0.8rem;">
                    <div style="font-size: 0.7rem; color: #6b7280;">📅 Créée le : {mission['created_at'][:16]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(f"🔍 Voir détails", key=f"detail_{mission['id']}", use_container_width=True):
                    st.session_state.selected_mission = mission['id']
                    st.switch_page("pages/technician_mission_detail.py")
            with col_btn2:
                if st.button(f"✅ Terminer", key=f"complete_{mission['id']}", use_container_width=True):
                    st.session_state.selected_mission = mission['id']
                    st.switch_page("pages/technician_mission_detail.py")
    
    # Missions terminées
    if len(completed) > 0:
        with st.expander(f"✅ Missions terminées ({len(completed)})"):
            for _, mission in completed.tail(10).iterrows():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #e5e7eb;">
                    <div>
                        <span style="font-weight: 500;">✅ {mission['defect_type']}</span>
                        <div style="font-size: 0.75rem; color: #6b7280;">📍 {mission['location']}</div>
                    </div>
                    <div style="font-size: 0.7rem; color: #6b7280;">📅 {mission['completed_at'][:16] if mission['completed_at'] else mission['created_at'][:16]}</div>
                </div>
                """, unsafe_allow_html=True)