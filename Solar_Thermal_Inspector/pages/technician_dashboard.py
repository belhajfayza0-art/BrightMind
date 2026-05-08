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
    get_technician_missions, get_technician_stats, create_mission
)
from backend.alert_service import get_pending_alerts

# Configuration de la page
st.set_page_config(page_title="Dashboard Technicien", page_icon="🔧", layout="wide")
st.session_state.current_page = 'dashboard'

# Vérification de l'accès
if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name

# Application du style et du menu
apply_style()
render_sidebar(technician_name)

# ============================================
# ALERTE IA
# ============================================
pending_alerts = get_pending_alerts()
if len(pending_alerts) > 0:
    st.warning(f"🔔 {len(pending_alerts)} nouvelle(s) alerte(s) IA ! Cliquez sur 'Alertes IA' dans le menu.")

# ============================================
# CARTE DE BIENVENUE
# ============================================
col_welcome1, col_welcome2 = st.columns([2, 1])

with col_welcome1:
    st.markdown(f"""
    <div class="welcome-card">
        <div style="font-size: 1.8rem; font-weight: 600;">👋 Bonjour {technician_name}</div>
        <div style="opacity: 0.9; margin-top: 0.5rem;">
            Vous avez des missions à traiter aujourd'hui.<br>
            Consultez la liste ci-dessous pour commencer.
        </div>
        <div style="margin-top: 1rem;">
            <span class="badge badge-low">✅ Dernière mission: terminée le {datetime.now().strftime('%d/%m')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_welcome2:
    st.markdown(f"""
    <div style="background: white; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: center;">
        <div style="font-size: 2rem;">📍</div>
        <div style="font-weight: 600; color: var(--vert);">À {random.randint(1, 5)} km du site</div>
        <div style="font-size: 0.7rem; color: var(--gris);">Station solaire principale</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

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
    
    # Récupérer les vraies missions du technicien
    missions = get_technician_missions(1, technician_name)
    
    # Créer la liste des défauts à partir des missions récentes
    recent_defects = []
    for _, mission in missions.tail(3).iterrows():  # 3 dernières missions
        severity = mission['severity']
        temp = mission['temperature']
        
        # Déterminer l'icône selon le type de défaut
        icon_map = {
            "Hotspot": "🔥",
            "Crack": "💔",
            "Dust": "🌫️",
            "Shading": "🌑",
            "Broken Cell": "⚡"
        }
        icon = icon_map.get(mission['defect_type'], "🔧")
        
        # Déterminer la date relative
        from datetime import datetime
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
    
    # AFFICHAGE DES DÉFAUTS (en dehors de la boucle de collecte)
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
                        from backend.technician_service import update_mission_status
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
# SECTION : TEMPS D'INTERVENTION PAR TYPE DE DÉFAUT
# ============================================

st.subheader("⏱️ Temps d'intervention par type de défaut")

# Calculer les vrais temps à partir des missions du technicien
missions = get_technician_missions(1, technician_name)
completed_missions = missions[missions['status'] == 'completed']

# Dictionnaire pour stocker les temps moyens par type de défaut
defect_times = {
    "Hotspot": {"total": 0, "count": 0, "estimated": 35, "icon": "🔥", "risk": "high"},
    "Crack": {"total": 0, "count": 0, "estimated": 45, "icon": "💔", "risk": "high"},
    "Dust": {"total": 0, "count": 0, "estimated": 20, "icon": "🌫️", "risk": "low"},
    "Shading": {"total": 0, "count": 0, "estimated": 30, "icon": "🌑", "risk": "medium"},
    "Broken Cell": {"total": 0, "count": 0, "estimated": 60, "icon": "⚡", "risk": "critical"}
}

# Couleurs pastel selon le niveau de risque
risk_colors = {
    "critical": {"bg": "#FEE2E2", "text": "#991B1B", "border": "#FCA5A5"},  # Rouge pastel (très risque)
    "high": {"bg": "#FFE8D9", "text": "#8B5A2B", "border": "#FFCDA8"},       # Orange pastel (risque élevé)
    "medium": {"bg": "#FEF3C7", "text": "#92400E", "border": "#FDE68A"},      # Jaune pastel (risque moyen)
    "low": {"bg": "#FFFBEB", "text": "#A16207", "border": "#FEF3C7"}          # Jaune clair pastel (risque faible)
}

# Parcourir les missions complétées
for _, mission in completed_missions.iterrows():
    defect_type = mission['defect_type']
    if defect_type in defect_times:
        temp = mission['temperature']
        simulated_time = 20 + (temp - 35) * 0.5
        simulated_time = max(15, min(90, simulated_time))
        defect_times[defect_type]["total"] += simulated_time
        defect_times[defect_type]["count"] += 1

# Créer les colonnes
col_time1, col_time2, col_time3 = st.columns(3)

# Filtrer les types qui ont des données
active_defects = {k: v for k, v in defect_times.items() if v['count'] > 0}

if len(active_defects) > 0:
    defect_list = list(active_defects.keys())
    
    for i, defect_type in enumerate(defect_list[:3]):
        data = defect_times[defect_type]
        avg_time = round(data["total"] / data["count"]) if data["count"] > 0 else data["estimated"]
        estimated = data["estimated"]
        diff = avg_time - estimated
        diff_text = f"{'+' if diff > 0 else ''}{diff} min"
        icon = data["icon"]
        risk = data["risk"]
        colors = risk_colors[risk]
        
        with [col_time1, col_time2, col_time3][i]:
            st.markdown(f"""
            <div style="background: {colors['bg']}; 
                        border-radius: 20px; 
                        padding: 1rem; 
                        text-align: center; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                        border-left: 4px solid {colors['border']};">
                <div style="font-size: 1rem; font-weight: 600;">{icon} {defect_type}</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {colors['text']};">{avg_time} min</div>
                <div style="font-size: 0.7rem; color: #6B7280;">vs estimé {estimated} min</div>
                <div style="font-size: 0.65rem; color: {colors['text']}; margin-top: 0.3rem;">{diff_text}</div>
                <div style="font-size: 0.6rem; color: #6B7280;">Basé sur {data['count']} intervention(s)</div>
            </div>
            """, unsafe_allow_html=True)
    
    if len(defect_list) > 3:
        st.markdown("---")
        col_time4, col_time5 = st.columns(2)
        for i, defect_type in enumerate(defect_list[3:]):
            data = defect_times[defect_type]
            avg_time = round(data["total"] / data["count"]) if data["count"] > 0 else data["estimated"]
            estimated = data["estimated"]
            diff = avg_time - estimated
            diff_text = f"{'+' if diff > 0 else ''}{diff} min"
            icon = data["icon"]
            risk = data["risk"]
            colors = risk_colors[risk]
            
            with [col_time4, col_time5][i]:
                st.markdown(f"""
                <div style="background: {colors['bg']}; 
                            border-radius: 20px; 
                            padding: 1rem; 
                            text-align: center; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                            border-left: 4px solid {colors['border']};">
                    <div style="font-size: 1rem; font-weight: 600;">{icon} {defect_type}</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: {colors['text']};">{avg_time} min</div>
                    <div style="font-size: 0.7rem; color: #6B7280;">vs estimé {estimated} min</div>
                    <div style="font-size: 0.65rem; color: {colors['text']}; margin-top: 0.3rem;">{diff_text}</div>
                    <div style="font-size: 0.6rem; color: #6B7280;">Basé sur {data['count']} intervention(s)</div>
                </div>
                """, unsafe_allow_html=True)

else:
    # Aucune mission complétée - valeurs par défaut avec couleurs pastel
    col_time1, col_time2, col_time3 = st.columns(3)
    
    with col_time1:
        st.markdown("""
        <div style="background: #FEE2E2; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #FCA5A5;">
            <div style="font-size: 1rem; font-weight: 600;">🔥 Hotspot</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #991B1B;">32 min</div>
            <div style="font-size: 0.7rem; color: #6B7280;">vs estimé 35 min</div>
            <div style="font-size: 0.6rem; color: #6B7280;">Basé sur 0 intervention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_time2:
        st.markdown("""
        <div style="background: #FED7AA; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #FDBA74;">
            <div style="font-size: 1rem; font-weight: 600;">💔 Crack</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #9A3412;">48 min</div>
            <div style="font-size: 0.7rem; color: #6B7280;">vs estimé 45 min</div>
            <div style="font-size: 0.6rem; color: #6B7280;">Basé sur 0 intervention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_time3:
        st.markdown("""
        <div style="background: #FEF3C7; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #FDE68A;">
            <div style="font-size: 1rem; font-weight: 600;">🌫️ Dust</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #92400E;">18 min</div>
            <div style="font-size: 0.7rem; color: #6B7280;">vs estimé 20 min</div>
            <div style="font-size: 0.6rem; color: #6B7280;">Basé sur 0 intervention</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
# ============================================
# ACTIVITÉS RÉCENTES
# ============================================

st.subheader("📋 Activités récentes")

# Récupérer les vraies missions
missions = get_technician_missions(1, technician_name)

# Créer la liste des activités à partir des vraies missions
activities = []

# Missions en cours
for _, mission in missions.iterrows():
    from datetime import datetime
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
    
    # Activité selon le statut
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

# Trier par date (plus récent en premier)
activities.sort(key=lambda x: x['time'], reverse=False)

# Afficher les 5 activités les plus récentes
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

# ============================================
# MODE TEST
# ============================================
