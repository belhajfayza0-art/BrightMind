# pages/manager_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session_manager import require_manager, get_current_zone
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar

# Appliquer le CSS
apply_global_style()

# Vérification
require_manager()

# Définir l'ID de la page
st.session_state['current_page'] = 'dashboard'

# Afficher la sidebar
show_sidebar()

# Récupérer la zone
user_zone = get_current_zone()

# En-tête
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Tableau de bord</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# Données par zone
defects_data = {
    "Noor I": {"Hotspot tube": 3, "Fissure miroir": 2, "Poussière": 5, "Désalignement": 1},
    "Noor II": {"Hotspot tube": 4, "Fissure miroir": 1, "Poussière": 3, "Désalignement": 2},
    "Noor III": {"Hotspot récepteur": 2, "Héliostat désaligné": 3, "Fuite sels": 0, "Fissure miroir": 1},
    "Noor IV": {"Hotspot panneau": 8, "Microfissure": 12, "Ombrage": 4, "Délaminage": 1, "Snail trail": 2},
    "Midelt": {"Hotspot": 0, "Fissure": 0, "Ombrage": 0, "Dust": 0},
}

zone_stats = {
    "Noor I": {"panels": "500K", "defects": 11, "efficiency": "92%"},
    "Noor II": {"panels": "660K", "defects": 10, "efficiency": "91%"},
    "Noor III": {"panels": "7 400", "defects": 6, "efficiency": "88%"},
    "Noor IV": {"panels": "240K", "defects": 27, "efficiency": "85%"},
    "Midelt": {"panels": "0", "defects": 0, "efficiency": "0%"},
}

stats = zone_stats.get(user_zone, {"panels": "N/A", "defects": 0, "efficiency": "N/A"})
total_defects = sum(defects_data.get(user_zone, {}).values())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{stats['panels']}</div>
        <div class="stat-label">Panneaux / Miroirs</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{total_defects}</div>
        <div class="stat-label">Défauts actifs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">2</div>
        <div class="stat-label">Techniciens</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{stats['efficiency']}</div>
        <div class="stat-label">Efficacité</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">Défauts par type</div>', unsafe_allow_html=True)
    defects_zone = defects_data.get(user_zone, {})
    if defects_zone:
        df_bar = pd.DataFrame(list(defects_zone.items()), columns=['Type', 'Nombre'])
        fig = px.bar(df_bar, x='Type', y='Nombre', color='Nombre',
                      color_continuous_scale=['#bbdefb', '#1565c0'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=350)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">Indicateurs spécifiques</div>', unsafe_allow_html=True)
    
    if user_zone == "Noor III":
        st.metric("Température récepteur", "545°C", "Normale")
        st.metric("Pression sels fondus", "12.5 bar", "Stable")
        st.metric("Héliostats opérationnels", "7 398/7 400")
    elif user_zone == "Noor IV":
        st.metric("Production", "8.2 MW", "-0.3")
        st.metric("Efficacité moyenne", "87%", "-2%")
        st.metric("Température moyenne", "54°C", "+3°C")
    elif user_zone in ["Noor I", "Noor II"]:
        st.metric("Température fluide", "398°C", "+2°C")
        st.metric("Miroirs alignés", "98%", "+1%")
        st.metric("Propreté miroirs", "92%", "-3%")
    else:
        st.info("Aucun indicateur spécifique pour cette zone")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<div class="section-title">Actions</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Gérer les techniciens", use_container_width=True):
        st.switch_page("pages/manager_technicians.py")

with col2:
    if st.button("Assigner une mission", use_container_width=True):
        st.switch_page("pages/manager_assign.py")

with col3:
    if st.button("Générer un rapport", use_container_width=True):
        st.switch_page("pages/manager_reports.py")