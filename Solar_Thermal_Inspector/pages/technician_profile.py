"""
Profil et statistiques du technicien
"""
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px
from backend.technician_service import (
    get_technician_stats, get_technician_missions,
    get_all_notifications, get_unread_notifications_count,
    mark_all_notifications_read
)
from components.sidebar import render_sidebar
from components.style import apply_style

# Configuration de la page
st.set_page_config(page_title="Mon Profil", page_icon="👤", layout="wide")
st.session_state.current_page = 'profile'

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
st.title(f"👤 {technician_name}")
st.markdown("---")

# Informations personnelles et statistiques
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("📋 Informations personnelles")
    st.write(f"**Nom :** {technician_name}")
    st.write(f"**Email :** {st.session_state.user_email}")
    st.write(f"**Rôle :** 🔧 Technicien de maintenance certifié")

with col_info2:
    st.subheader("🏆 Statistiques")
    stats = get_technician_stats(technician_name)
    st.write(f"**Missions complétées :** {stats['completed']}")
    st.write(f"**Taux de réussite :** {stats['completion_rate']}%")
    st.write(f"**En cours :** {stats['in_progress']}")

st.markdown("---")

# Graphique d'évolution
# ============================================
# SECTION : STATISTIQUES STYLE "TIME SPENT"
# ============================================

# ============================================
# SECTION : ÉVOLUTION DES MISSIONS
# ============================================

st.subheader("📊 Missions traitées")

# Récupérer les missions
missions = get_technician_missions(1, technician_name)

# Calculer le nombre total de missions
total_missions = len(missions)
completed_missions = len(missions[missions['status'] == 'completed'])

# Calculer l'évolution (simulée)
evolution = 12

col_stats, col_chart = st.columns([1, 1.5])

with col_stats:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #257c48 0%, #1a5c3a 100%); 
                border-radius: 24px; 
                padding: 1.5rem; 
                text-align: center;
                color: white;">
        <div style="font-size: 0.8rem; opacity: 0.8;">MISSIONS</div>
        <div style="font-size: 2.8rem; font-weight: 700;">{completed_missions}</div>
        <div style="font-size: 0.8rem; margin-top: 0.5rem;">
            <span style="color: #FFD787;">↑ {evolution}%</span> vs semaine dernière
        </div>
        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem;">
            📋 Total : {total_missions} missions
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    import plotly.graph_objects as go
    from datetime import datetime
    
    # Dictionnaire pour stocker les missions par jour
    daily_data = {}
    
    for _, mission in missions.iterrows():
        try:
            created_date = datetime.strptime(mission['created_at'][:10], "%Y-%m-%d")
            date_str = created_date.strftime("%d/%m")
            daily_data[date_str] = daily_data.get(date_str, 0) + 1
        except:
            pass
    
    if len(daily_data) == 0:
        st.info("📭 Aucune mission effectuée pour le moment.")
    else:
        # Trier par date
        sorted_dates = sorted(daily_data.keys(), key=lambda x: (x.split('/')[1], x.split('/')[0]))
        daily_counts = [daily_data[date] for date in sorted_dates]
        
        # Couleurs PASTEL : Jaune pastel (#FFF3C4) et Bleu pastel (#B8E1F7)
        bar_colors = ['#FFF3C4' if i % 2 == 0 else '#B8E1F7' for i in range(len(sorted_dates))]
        
        # Bordures aux mêmes couleurs mais plus foncées
        border_colors = ['#E6C800' if i % 2 == 0 else '#7EC8E3' for i in range(len(sorted_dates))]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=sorted_dates,
            y=daily_counts,
            marker_color=bar_colors,
            marker_line_color=border_colors,
            marker_line_width=2,
            text=daily_counts,
            textposition='outside',
            textfont=dict(color='#4B5563', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Date",
            yaxis_title="Nombre de missions",
            height=250,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis=dict(
                tickfont=dict(size=11, color='#6B7280'),
                gridcolor='#E5E7EB',
                tickangle=-45
            ),
            yaxis=dict(
                gridcolor='#E5E7EB',
                dtick=1,
                range=[0, max(daily_counts) + 1] if daily_counts else [0, 5]
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# Dernières missions
st.subheader("📜 Dernières missions effectuées")

completed_missions = missions[missions['status'] == 'completed'].sort_values('completed_at', ascending=False)

if len(completed_missions) > 0:
    for _, mission in completed_missions.head(10).iterrows():
        with st.expander(f"✅ {mission['defect_type']} - {mission['location']}"):
            st.write(f"**Terminée le :** {mission['completed_at']}")
            st.write(f"**Temps estimé :** 45 minutes")
            if mission['notes'] and mission['notes'] != '':
                st.write(f"**Notes :** {mission['notes']}")
else:
    st.info("Aucune mission terminée pour le moment")