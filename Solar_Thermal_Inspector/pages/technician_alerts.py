"""
Page des alertes pour les techniciens
Les alertes sont générées automatiquement par l'IA
"""

import streamlit as st
import time
import os
import random
from datetime import datetime
from backend.alert_service import get_pending_alerts, take_alert, is_alert_taken
from backend.ai_monitor import simulate_ai_detection
from components.sidebar import render_sidebar
from components.style import apply_style

# Configuration
st.set_page_config(page_title="Alertes IA", page_icon="🔔", layout="wide")
st.session_state.current_page = 'alerts'

# Vérification accès
if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name

# ============================================
# IA AUTOMATIQUE - Détection sans intervention
# ============================================

# Simulation : 15% de chance qu'une alerte soit créée à chaque chargement
if random.random() < 0.15:
    result = simulate_ai_detection()
    # Notification discrète
    st.toast(f"🤖 IA : {result['defect']['defect_type']} détecté à {result['defect']['location']}", icon="🔔")

# Option : alerte périodique basée sur le temps
current_minute = datetime.now().minute
last_alert = st.session_state.get('last_alert_minute', -1)
if current_minute % 7 == 0 and last_alert != current_minute:  # Toutes les 7 minutes
    st.session_state.last_alert_minute = current_minute
    result = simulate_ai_detection()
    st.toast(f"🤖 IA : Nouveau défaut détecté - {result['defect']['defect_type']}", icon="⚠️")

# ============================================
# STYLE ET MENU
# ============================================
apply_style()
render_sidebar(technician_name)

# ============================================
# TITRE
# ============================================
st.title("🔔 Alertes IA - Défauts détectés")
st.markdown("L'intelligence artificielle surveille en permanence les panneaux solaires")

# Auto-refresh optionnel
auto_refresh = st.checkbox("🔄 Auto-actualisation (10s)", value=False)
if auto_refresh:
    time.sleep(10)
    st.rerun()

st.markdown("---")

# ============================================
# AFFICHAGE DES ALERTES
# ============================================
st.subheader("📢 Alertes en cours")

alerts = get_pending_alerts()

if len(alerts) == 0:
    st.info("✅ Aucune alerte en cours. Tous les panneaux sont en bon état.")
else:
    st.warning(f"⚠️ {len(alerts)} alerte(s) en attente !")
    
    for _, alert in alerts.iterrows():
        severity_color = "🔴" if alert['severity'] == 'critical' else "🟠" if alert['severity'] == 'high' else "🟡"
        border_color = '#ef4444' if alert['severity'] == 'critical' else '#f97316' if alert['severity'] == 'high' else '#eab308'
        
        st.markdown(f"""
        <div style="border: 2px solid {border_color}; border-radius: 20px; padding: 1.5rem; margin-bottom: 1.5rem; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 1.5rem; font-weight: 700;">{severity_color} {alert['defect_type']}</div>
                <div style="background: {'#fee2e2' if alert['severity'] == 'critical' else '#ffedd5'}; color: {'#ef4444' if alert['severity'] == 'critical' else '#f97316'}; padding: 0.3rem 0.8rem; border-radius: 20px;">
                    {alert['severity'].upper()}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_info, col_image = st.columns([2, 1])
        
        with col_info:
            st.markdown(f"""
            <div style="font-size: 1rem; margin: 0.5rem 0;">📍 <strong>Localisation :</strong> {alert['location']}</div>
            <div style="font-size: 1rem; margin: 0.5rem 0;">🌡️ <strong>Température :</strong> <span style="color: {'#ef4444' if alert['temperature'] > 75 else '#f97316' if alert['temperature'] > 60 else '#eab308'}">{alert['temperature']}°C</span></div>
            <div style="font-size: 0.85rem; color: #6b7280; margin: 0.5rem 0;">🕐 Détecté par IA le : {alert['detected_at']}</div>
            """, unsafe_allow_html=True)
        
        with col_image:
            if alert['image_path'] and os.path.exists(alert['image_path']):
                st.image(alert['image_path'], caption="📸 Image du défaut", use_container_width=True)
            else:
                st.markdown(f"""
                <div style="background: #f3f4f6; border-radius: 16px; padding: 2rem; text-align: center;">
                    <div style="font-size: 3rem;">🛸</div>
                    <div style="font-size: 0.8rem;">Image IA</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if not is_alert_taken(alert['id']):
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button(f"📋 PRENDRE CETTE MISSION", key=f"take_{alert['id']}", type="primary", use_container_width=True):
                    mission_id = take_alert(alert['id'], technician_name)
                    st.success(f"✅ Mission #{mission_id} prise en charge ! L'alerte est maintenant désactivée.")
                    st.balloons()
                    st.rerun()
        else:
            st.markdown(f"""
            <div style="background: #fefce8; border-radius: 16px; padding: 0.8rem; text-align: center; margin-top: 0.5rem;">
                ⚠️ Cette mission a déjà été prise par un autre technicien
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# RAPPEL
# ============================================
st.markdown("---")
st.subheader("📋 Rappel")

if st.button("🔧 Voir mes missions en cours", use_container_width=True):
    st.switch_page("pages/technician_dashboard.py")