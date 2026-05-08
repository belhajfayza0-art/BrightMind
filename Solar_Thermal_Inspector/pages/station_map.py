"""
Carte des défauts - Station Noor Ouarzazate
Affiche uniquement les panneaux avec des défauts détectés
"""

import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from backend.technician_service import get_technician_missions
from components.sidebar import render_sidebar
from components.style import apply_style

st.set_page_config(page_title="Carte des défauts", page_icon="🗺️", layout="wide")
st.session_state.current_page = 'map'

if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name

apply_style()
render_sidebar(technician_name)

st.title("🗺️ Carte des défauts - Station Noor Ouarzazate")
st.markdown("Localisation des panneaux solaires nécessitant une intervention")

# ============================================
# COORDONNÉES DE LA STATION
# ============================================
station_lat = 31.0106
station_lon = -6.8626

# ============================================
# RÉCUPÉRER LES MISSIONS AVEC DÉFAUTS
# ============================================
missions = get_technician_missions(1, technician_name)

# Afficher toutes les missions (pending et in_progress)
active_defects = missions[missions['status'].isin(['pending', 'in_progress'])]

# Afficher un message de débogage (optionnel, à retirer après)
# st.write(f"Nombre total de missions actives trouvées : {len(active_defects)}")

# ============================================
# DICTIONNAIRE DES COORDONNÉES PAR LOCALISATION
# ============================================
location_coords = {
    "Ligne 1, Colonne 4": (station_lat + 0.0005, station_lon - 0.0005),
    "Ligne 2, Colonne 15": (station_lat + 0.0004, station_lon - 0.0001),
    "Ligne 3, Colonne 7": (station_lat + 0.0003, station_lon - 0.0002),
    "Ligne 4, Colonne 3": (station_lat + 0.0001, station_lon + 0.0001),
    "Ligne 5, Colonne 12": (station_lat + 0.0002, station_lon + 0.0002),
    "Ligne 6, Colonne 8": (station_lat, station_lon + 0.0003),
    "Ligne 7, Colonne 11": (station_lat - 0.0001, station_lon + 0.0002),
    "Ligne 8, Colonne 2": (station_lat - 0.0002, station_lon + 0.0001),
    "Ligne 9, Colonne 5": (station_lat - 0.0003, station_lon),
    "Ligne 10, Colonne 8": (station_lat - 0.0002, station_lon - 0.0002),
    "Ligne 11, Colonne 3": (station_lat - 0.0001, station_lon - 0.0003),
    "Ligne 12, Colonne 9": (station_lat, station_lon - 0.0002),
}

# ============================================
# CRÉER LA CARTE
# ============================================
m = folium.Map(
    location=[station_lat, station_lon],
    zoom_start=15,
    tiles='OpenStreetMap'
)

# Marqueur de la station
folium.Marker(
    location=[station_lat, station_lon],
    popup="Station Noor Ouarzazate",
    icon=folium.Icon(color='green', icon='info-sign'),
    tooltip="Station principale"
).add_to(m)

# ============================================
# AJOUTER TOUS LES DÉFAUTS SUR LA CARTE
# ============================================
if len(active_defects) > 0:
    for idx, (_, mission) in enumerate(active_defects.iterrows()):
        # Déterminer la couleur selon la gravité
        if mission['severity'] == 'critical':
            color = 'red'
            icon = 'exclamation-sign'
        elif mission['severity'] == 'high':
            color = 'orange'
            icon = 'warning-sign'
        else:
            color = 'yellow'
            icon = 'info-sign'
        
        # Récupérer les coordonnées selon la localisation
        loc_key = mission['location']
        if loc_key in location_coords:
            lat, lon = location_coords[loc_key]
        else:
            # Coordonnées par défaut avec un décalage basé sur l'index
            lat = station_lat + (idx * 0.0001)
            lon = station_lon - (idx * 0.0001)
        
        # Ajouter le marqueur du défaut
        folium.Marker(
            location=[lat, lon],
            popup=f"""
            <b>{mission['defect_type']}</b><br>
            📍 {mission['location']}<br>
            🌡️ {mission['temperature']}°C<br>
            ⚠️ {mission['severity']}<br>
            📌 {mission['status']}
            """,
            icon=folium.Icon(color=color, icon=icon),
            tooltip=f"{mission['defect_type']} - {mission['temperature']}°C"
        ).add_to(m)
        
        # Cercle autour du défaut
        folium.Circle(
            location=[lat, lon],
            radius=40,
            color=color,
            fill=True,
            fill_opacity=0.3,
            popup=f"Zone: {mission['defect_type']}"
        ).add_to(m)
        
        # Afficher un message de confirmation (optionnel)
        # st.write(f"✅ Défaut ajouté : {mission['defect_type']} - {mission['location']}")
else:
    st.info("✅ Aucun défaut actif. Tous les panneaux sont en bon état.")

# ============================================
# LÉGENDE
# ============================================
legend_html = """
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); font-size: 12px;">
    <b>🔴 Légende</b><br>
    🔴 <span style="color:red">●</span> Critique (urgent)<br>
    🟠 <span style="color:orange">●</span> Haute priorité<br>
    🟡 <span style="color:gold">●</span> Priorité normale<br>
    🟢 <span style="color:green">●</span> Station
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ============================================
# AFFICHAGE
# ============================================
col_map, col_info = st.columns([3, 1])

with col_map:
    folium_static(m, width=700, height=500)

with col_info:
    st.markdown("### 📊 Défauts actifs")
    st.metric("⚠️ Total défauts", len(active_defects))
    
    if len(active_defects) > 0:
        st.markdown("---")
        st.markdown("### 📋 Liste des défauts")
        for _, mission in active_defects.iterrows():
            emoji = "🔴" if mission['severity'] == 'critical' else "🟠" if mission['severity'] == 'high' else "🟡"
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid {'red' if mission['severity'] == 'critical' else 'orange' if mission['severity'] == 'high' else 'gold'};">
                <b>{emoji} {mission['defect_type']}</b><br>
                📍 {mission['location']}<br>
                🌡️ {mission['temperature']}°C
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

if st.button("🔄 Actualiser la carte", use_container_width=True):
    st.rerun()