"""
Dashboard Technicien - Version simplifiée
Utilise les composants centralisés
"""

import streamlit as st
import random
import pandas as pd
from datetime import datetime
from components.sidebar import render_sidebar
from components.style import apply_style
from backend.technician_service import (
    get_technician_missions, get_technician_stats, create_mission, update_mission_status
)
from backend.alert_service import get_pending_alerts_by_zone

# Configuration de la page
st.set_page_config(page_title="Dashboard Technicien", page_icon="🔧", layout="wide")
st.session_state.current_page = 'dashboard'

# Vérification de l'accès
if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name

# ============================================
# RÉCUPÉRATION DE LA ZONE ET PERSONNALISATION
# ============================================

# Récupérer la zone du technicien connecté
technician_zone = st.session_state.get('user_zone', 'Noor IV')

# Pour les statistiques
from backend.technician_service import get_technician_stats_by_zone
stats = get_technician_stats_by_zone(technician_name, technician_zone)

# Pour les missions
from backend.technician_service import get_technician_missions_by_zone
missions = get_technician_missions_by_zone(technician_name, technician_zone)

# Pour les alertes
from backend.alert_service import get_pending_alerts_by_zone
pending_alerts = get_pending_alerts_by_zone(technician_zone)
# Informations spécifiques à la zone
zone_info = {
    "Noor I": {
        "name": "Noor I",
        "color": "#FF6B6B",
        "icon": "🔴",
        "type": "CSP - Miroirs paraboliques",
        "capacity": "160 MW",
        "anomalies": ["MirrorMisalignment", "AbsorberTubeDegradation", "HTFLeak"]
    },
    "Noor II": {
        "name": "Noor II",
        "color": "#FF9F43",
        "icon": "🟠",
        "type": "CSP - Miroirs paraboliques",
        "capacity": "200 MW",
        "anomalies": ["MirrorMisalignment", "AbsorberTubeDegradation", "HTFLeak"]
    },
    "Noor III": {
        "name": "Noor III",
        "color": "#FDCB6E",
        "icon": "🟡",
        "type": "CSP - Tour solaire",
        "capacity": "150 MW",
        "anomalies": ["TrackingFailure", "ReceiverTubeLeak", "ThermalGradientAnomaly"]
    },
    "Noor IV": {
        "name": "Noor IV",
        "color": "#6C5CE7",
        "icon": "🟣",
        "type": "Photovoltaïque",
        "capacity": "72 MW",
        "anomalies": ["Hotspot", "Crack", "Dust", "Shading", "Broken Cell"]
    },
    "Midelt": {
        "name": "Midelt",
        "color": "#00B894",
        "icon": "🟢",
        "type": "Mixte CSP + PV",
        "capacity": "800 MW",
        "anomalies": ["StringOpenCircuit", "StringReversedPolarity", "Hotspot", "Crack"]
    }
}

current_zone_info = zone_info.get(technician_zone, zone_info["Noor IV"])

# Application du style et du menu
apply_style()
render_sidebar(technician_name)

# ============================================
# ALERTE IA (FILTRÉE PAR ZONE)
# ============================================
# ============================================
# ALERTE IA - Version finale
# ============================================

# Compter les alertes
alerts_df = get_pending_alerts_by_zone(technician_zone)
nb_alerts = len(alerts_df)

if nb_alerts > 0:
    # Utiliser les colonnes pour aligner message et bouton
    col_msg, col_btn = st.columns([3, 1])
    with col_msg:
        st.error(f"🚨 {nb_alerts} ALERTE(S) IA DÉTECTÉE(S) ! Intervention requise.")
    with col_btn:
        if st.button("📋 VOIR LES ALERTES", type="primary", use_container_width=True):
            st.switch_page("pages/technician_alerts.py")
else:
    st.success("✅ Aucune alerte IA. Tous les panneaux fonctionnent normalement.")

# ============================================
# CARTE DE BIENVENUE
# ============================================

col_welcome1, col_welcome2 = st.columns([2, 1])

with col_welcome1:
    st.markdown(f"""
    <div class="welcome-card">
        <div style="font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0;">👋 Bonjour {technician_name}</div>
        <div style="opacity: 0.9; margin: 0.5rem 0;">
            Vous avez des missions à traiter aujourd'hui.<br>
            Consultez la liste ci-dessous pour commencer.
        </div>
        <div style="margin-top: 0.8rem;">
            <span class="badge badge-low">✅ Dernière mission: terminée le {datetime.now().strftime('%d/%m')}</span>
        </div>
        <div style="margin-top: 0.8rem; font-size: 0.7rem; opacity: 0.7;">
            Technicien: {technician_name}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_welcome2:
    st.markdown(f"""
    <div style="background: {current_zone_info['color']}10; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: center; border: 1px solid {current_zone_info['color']}30;">
        <div style="font-size: 2rem;">{current_zone_info['icon']}</div>
        <div style="font-weight: 600; color: {current_zone_info['color']};">{current_zone_info['name']}</div>
        <div style="font-size: 0.7rem; color: var(--gris);">{current_zone_info['type']}</div>
        <div style="font-size: 0.7rem; color: var(--gris); margin-top: 0.3rem;">{current_zone_info['capacity']}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# STATISTIQUES
# ============================================
stats = get_technician_stats(technician_name)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{stats['total']}</div>
        <div class="stat-label">📋 Missions totales</div>
        <div class="stat-trend trend-up">+{stats['completed']} cette semaine ↑</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: var(--jaune);">
        <div class="stat-value" style="color: var(--jaune);">{stats['completed']}</div>
        <div class="stat-label">✅ Missions complétées</div>
        <div class="stat-trend trend-up">+2 cette semaine ↑</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: var(--bleu);">
        <div class="stat-value" style="color: var(--bleu);">{stats['in_progress']}</div>
        <div class="stat-label">🔄 Missions en cours</div>
        <div class="stat-trend">{stats['in_progress']} mission(s) active(s)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{stats['completion_rate']}%</div>
        <div class="stat-label">⭐ Taux de réussite</div>
        <div class="stat-trend trend-up">Excellent ! ↑</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================
# SECTION PRINCIPALE
# ============================================
col_left, col_right = st.columns([1, 1])

# COLONNE GAUCHE : Derniers défauts
with col_left:
    st.markdown("### 🖼️ Derniers défauts détectés")
    
    missions = get_technician_missions(1, technician_name)
    
    recent_defects = []
    for _, mission in missions.tail(3).iterrows():
        severity = mission['severity']
        temp = mission['temperature']
        
        icon_map = {
            "Hotspot": "🔥", "Crack": "💔", "Dust": "🌫️",
            "Shading": "🌑", "Broken Cell": "⚡",
            "MirrorMisalignment": "🪞", "AbsorberTubeDegradation": "🔧",
            "TrackingFailure": "🎯", "ReceiverTubeLeak": "💧",
            "StringOpenCircuit": "⚡", "StringReversedPolarity": "🔄"
        }
        icon = icon_map.get(mission['defect_type'], "🔧")
        
        try:
            created_date = datetime.strptime(mission['created_at'], "%Y-%m-%d %H:%M:%S")
            days_ago = (datetime.now() - created_date).days
            if days_ago == 0:
                date_str = "Aujourd'hui"
            elif days_ago == 1:
                date_str = "Hier"
            else:
                date_str = f"Il y a {days_ago} jours"
        except:
            date_str = mission['created_at'][:10]
        
        recent_defects.append({
            "type": mission['defect_type'],
            "location": mission['location'],
            "temp": temp,
            "severity": severity,
            "date": date_str,
            "icon": icon
        })
    
    if len(recent_defects) > 0:
        for defect in recent_defects:
            temp_class = "temp-critical" if defect['temp'] > 75 else "temp-high" if defect['temp'] > 60 else "temp-normal"
            badge_class = f"badge-{defect['severity']}"
            
            st.markdown(f"""
            <div class="defect-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="defect-title">{defect['icon']} {defect['type']}</span>
                        <div class="defect-location">📍 {defect['location']}</div>
                    </div>
                    <div class="defect-temp {temp_class}">{defect['temp']}°C</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                    <span class="badge {badge_class}">{defect['severity']}</span>
                    <span style="font-size: 0.7rem; color: var(--gris);">📅 {defect['date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun défaut détecté pour le moment.")

# COLONNE DROITE : Missions en cours
with col_right:
    st.markdown("### 🔧 Missions en cours")
    
    missions = get_technician_missions(1, technician_name)
    pending_missions = missions[missions['status'] == 'pending']
    in_progress_missions = missions[missions['status'] == 'in_progress']
    
    all_active = pd.concat([pending_missions, in_progress_missions]) if len(pending_missions) > 0 or len(in_progress_missions) > 0 else pd.DataFrame()
    
    if len(all_active) > 0:
        for _, mission in all_active.iterrows():
            progress = 50 if mission['status'] == 'in_progress' else 25
            progress_color = "var(--jaune)" if mission['status'] == 'pending' else "var(--vert)"
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="font-weight: 600;">{mission['defect_type']}</span>
                        <div style="font-size: 0.7rem; color: var(--gris);">📍 {mission['location']}</div>
                    </div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {progress_color};">{mission['temperature']}°C</div>
                </div>
                <div style="margin-top: 0.8rem;">
                    <div style="background: var(--gris-clair); border-radius: 10px; height: 6px; overflow: hidden;">
                        <div style="background: {progress_color}; width: {progress}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span style="font-size: 0.7rem;">Statut: {'🔄 En cours' if mission['status'] == 'in_progress' else '🆕 Nouvelle'}</span>
                        <span style="font-size: 0.7rem;">⏱️ Estimé: 45 min</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(f"🔍 Voir détail", key=f"detail_{mission['id']}"):
                    st.session_state.selected_mission = mission['id']
                    st.switch_page("pages/technician_mission_detail.py")
            with col_btn2:
                if mission['status'] == 'pending':
                    if st.button(f"🚀 Commencer", key=f"start_{mission['id']}"):
                        update_mission_status(mission['id'], 'in_progress')
                        st.rerun()
                elif mission['status'] == 'in_progress':
                    if st.button(f"✅ Terminer", key=f"complete_{mission['id']}"):
                        st.session_state.selected_mission = mission['id']
                        st.switch_page("pages/technician_mission_detail.py")
    else:
        st.info("Aucune mission en cours. Créez une mission de test ci-dessous.")

st.markdown("---")

# ============================================
# TEMPS D'INTERVENTION
# ============================================
# ============================================
# TEMPS D'INTERVENTION PAR ZONE
# ============================================
st.subheader("⏱️ Temps d'intervention par type de défaut")

# Récupérer la zone du technicien
technician_zone = st.session_state.get('user_zone', 'Noor IV')

# Définir les anomalies par zone
anomalies_by_zone = {
    "Noor I": {
        "MirrorMisalignment": {"icon": "🪞", "estimated": 50, "risk": "high"},
        "AbsorberTubeDegradation": {"icon": "🔧", "estimated": 70, "risk": "critical"}
    },
    "Noor II": {
        "MirrorMisalignment": {"icon": "🪞", "estimated": 50, "risk": "high"},
        "AbsorberTubeDegradation": {"icon": "🔧", "estimated": 70, "risk": "critical"},
        "HTFLeak": {"icon": "💧", "estimated": 80, "risk": "critical"}
    },
    "Noor III": {
        "TrackingFailure": {"icon": "🎯", "estimated": 40, "risk": "high"},
        "ReceiverTubeLeak": {"icon": "💧", "estimated": 80, "risk": "critical"},
        "ThermalGradientAnomaly": {"icon": "🌡️", "estimated": 35, "risk": "medium"}
    },
    "Noor IV": {
        "Hotspot": {"icon": "🔥", "estimated": 35, "risk": "critical"},
        "Crack": {"icon": "💔", "estimated": 45, "risk": "high"},
        "Dust": {"icon": "🌫️", "estimated": 20, "risk": "low"},
        "Shading": {"icon": "🌑", "estimated": 30, "risk": "medium"},
        "Broken Cell": {"icon": "⚡", "estimated": 60, "risk": "critical"}
    },
    "Midelt": {
        "StringOpenCircuit": {"icon": "⚡", "estimated": 55, "risk": "critical"},
        "StringReversedPolarity": {"icon": "🔄", "estimated": 45, "risk": "high"},
        "Hotspot": {"icon": "🔥", "estimated": 35, "risk": "critical"},
        "Crack": {"icon": "💔", "estimated": 45, "risk": "high"}
    }
}

# Récupérer les anomalies de la zone
zone_anomalies = anomalies_by_zone.get(technician_zone, anomalies_by_zone["Noor IV"])

# Calculer les temps réels à partir des missions complétées
missions = get_technician_missions_by_zone(technician_name, technician_zone)
completed_missions = missions[missions['status'] == 'completed']

# Compter les temps réels
real_times = {}
for _, mission in completed_missions.iterrows():
    defect_type = mission['defect_type']
    if defect_type in zone_anomalies:
        if defect_type not in real_times:
            real_times[defect_type] = {"total": 0, "count": 0}
        # Simuler un temps basé sur la température
        temp = mission['temperature']
        simulated_time = 20 + (temp - 35) * 0.5
        simulated_time = max(15, min(90, simulated_time))
        real_times[defect_type]["total"] += simulated_time
        real_times[defect_type]["count"] += 1

# Afficher les cartes (2 ou 3 par ligne selon le nombre)
anomaly_list = list(zone_anomalies.keys())
num_anomalies = len(anomaly_list)

if num_anomalies > 0:
    # Créer les colonnes (3 max par ligne)
    for i in range(0, num_anomalies, 3):
        cols = st.columns(min(3, num_anomalies - i))
        for j, col in enumerate(cols):
            if i + j < num_anomalies:
                defect_type = anomaly_list[i + j]
                data = zone_anomalies[defect_type]
                
                # Utiliser le temps réel si disponible
                if defect_type in real_times:
                    avg_time = round(real_times[defect_type]["total"] / real_times[defect_type]["count"])
                    count = real_times[defect_type]["count"]
                    source = f"Basé sur {count} intervention(s)"
                else:
                    avg_time = data["estimated"]
                    source = "Valeur estimée (aucune intervention)"
                
                estimated = data["estimated"]
                diff = avg_time - estimated
                diff_text = f"{'+' if diff > 0 else ''}{diff} min"
                
                # Couleurs selon risque
                if data["risk"] == "critical":
                    bg_color = "#FEE2E2"
                    text_color = "#991B1B"
                    border_color = "#FCA5A5"
                elif data["risk"] == "high":
                    bg_color = "#FFE8D9"
                    text_color = "#8B5A2B"
                    border_color = "#FFCDA8"
                else:
                    bg_color = "#FEF3C7"
                    text_color = "#92400E"
                    border_color = "#FDE68A"
                
                with col:
                    st.markdown(f"""
                    <div style="background: {bg_color}; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid {border_color};">
                        <div style="font-size: 1rem; font-weight: 600;">{data['icon']} {defect_type}</div>
                        <div style="font-size: 1.8rem; font-weight: 700; color: {text_color};">{avg_time} min</div>
                        <div style="font-size: 0.7rem; color: #6B7280;">vs estimé {estimated} min</div>
                        <div style="font-size: 0.65rem; color: {text_color}; margin-top: 0.3rem;">{diff_text}</div>
                        <div style="font-size: 0.6rem; color: #6B7280;">{source}</div>
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.info(f"Aucune anomalie définie pour la zone {technician_zone}.")

# ============================================
# ACTIVITÉS RÉCENTES
# ============================================
st.subheader("📋 Activités récentes")

missions = get_technician_missions(1, technician_name)
activities = []

for _, mission in missions.iterrows():
    try:
        created_date = datetime.strptime(mission['created_at'], "%Y-%m-%d %H:%M:%S")
        days_ago = (datetime.now() - created_date).days
        hours_ago = int((datetime.now() - created_date).total_seconds() / 3600)
        
        if days_ago == 0:
            if hours_ago == 0:
                time_str = "À l'instant"
            elif hours_ago == 1:
                time_str = "Il y a 1 heure"
            else:
                time_str = f"Il y a {hours_ago} heures"
        elif days_ago == 1:
            time_str = "Hier"
        else:
            time_str = f"Il y a {days_ago} jours"
    except:
        time_str = mission['created_at'][:10]
    
    if mission['status'] == 'pending':
        activities.append({
            "icon": "🆕",
            "text": f"Mission #{mission['id']} créée - {mission['defect_type']} ({mission['location']})",
            "time": time_str,
            "type": "info"
        })
    elif mission['status'] == 'in_progress':
        activities.append({
            "icon": "🔄",
            "text": f"Mission #{mission['id']} commencée - {mission['defect_type']} ({mission['location']})",
            "time": time_str,
            "type": "warning"
        })
    elif mission['status'] == 'completed':
        activities.append({
            "icon": "✅",
            "text": f"Mission #{mission['id']} terminée - {mission['defect_type']} ({mission['location']})",
            "time": time_str,
            "type": "success"
        })

activities.sort(key=lambda x: x['time'], reverse=False)

if len(activities) > 0:
    for activity in activities[:5]:
        icon_class = f"activity-icon-{activity['type']}"
        st.markdown(f"""
        <div class="activity-item">
            <div class="activity-icon {icon_class}">{activity['icon']}</div>
            <div style="flex: 1;">
                <div style="font-size: 0.9rem;">{activity['text']}</div>
                <div style="font-size: 0.7rem; color: var(--gris);">{activity['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Aucune activité récente.")

st.markdown("---")

# ============================================
# MODE TEST
# ============================================
with st.expander("🔧 Mode test - Créer des missions"):
    st.warning("⚠️ Mode de démonstration - Permet de créer des missions de test")
    
    col_test1, col_test2, col_test3 = st.columns(3)
    with col_test1:
        if st.button("🔥 Créer Hotspot (Urgent)", use_container_width=True):
            test_defect = {
                'class_name': 'Hotspot',
                'severity': 'critical',
                'location': f'{technician_zone}, Ligne 3, Colonne 7',
                'temperature': 87.5
            }
            create_mission(test_defect, technician_name)
            st.success("Mission créée !")
            st.rerun()
    
    with col_test2:
        if st.button("💔 Créer Crack (Haute)", use_container_width=True):
            test_defect = {
                'class_name': 'Crack',
                'severity': 'high',
                'location': f'{technician_zone}, Ligne 8, Colonne 2',
                'temperature': 65.2
            }
            create_mission(test_defect, technician_name)
            st.success("Mission créée !")
            st.rerun()
    
    with col_test3:
        if st.button("🌫️ Créer Dust (Basse)", use_container_width=False):
            test_defect = {
                'class_name': 'Dust',
                'severity': 'low',
                'location': f'{technician_zone}, Ligne 2, Colonne 15',
                'temperature': 42.0
            }
            create_mission(test_defect, technician_name)
            st.success("Mission créée !")
            st.rerun()