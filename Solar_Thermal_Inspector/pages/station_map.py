"""
Carte des défauts - Station Noor Ouarzazate
La carte se centre automatiquement sur la zone du technicien
"""

import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from backend.technician_service import get_technician_missions_by_zone
from backend.alert_service import get_pending_alerts_by_zone
from components.sidebar import render_sidebar
from components.style import apply_style

st.set_page_config(page_title="Carte des défauts", page_icon="🗺️", layout="wide")
st.session_state.current_page = 'map'

if 'user_role' not in st.session_state or st.session_state.user_role != 'technician':
    st.error("⛔ Accès réservé aux techniciens")
    st.stop()

technician_name = st.session_state.user_name
technician_zone = st.session_state.get('user_zone', 'Noor IV')

apply_style()
render_sidebar(technician_name)

st.title(f"🗺️ Carte des défauts - Zone {technician_zone}")
st.markdown(f"Localisation des panneaux solaires nécessitant une intervention dans la zone **{technician_zone}**")

# ============================================
# COORDONNÉES PAR ZONE
# ============================================
zone_coords = {
    "Noor I": {"lat": 31.0106, "lon": -6.8626, "zoom": 15},
    "Noor II": {"lat": 31.0377, "lon": -6.8696, "zoom": 15},
    "Noor III": {"lat": 31.0623, "lon": -6.8704, "zoom": 15},
    "Noor IV": {"lat": 31.0218, "lon": -6.8306, "zoom": 15},
    "Midelt": {"lat": 32.6850, "lon": -4.7350, "zoom": 14},
}

# Récupérer les coordonnées de la zone
center = zone_coords.get(technician_zone, zone_coords["Noor IV"])
station_lat = center["lat"]
station_lon = center["lon"]
zoom_start = center["zoom"]

# ============================================
# RÉCUPÉRER LES DÉFAUTS DE LA ZONE UNIQUEMENT
# ============================================
# Récupérer les missions en cours (pending ou in_progress) de la zone
missions = get_technician_missions_by_zone(technician_name, technician_zone)
active_defects = missions[missions['status'].isin(['pending', 'in_progress'])]

# ============================================
# CRÉER LA CARTE CENTRÉE SUR LA BONNE ZONE
# ============================================
m = folium.Map(
    location=[station_lat, station_lon],
    zoom_start=zoom_start,
    tiles='OpenStreetMap'
)

# Marqueur de la zone
folium.Marker(
    location=[station_lat, station_lon],
    popup=f"Zone {technician_zone}",
    icon=folium.Icon(color='green', icon='info-sign'),
    tooltip=f"Zone {technician_zone}"
).add_to(m)

# ============================================
# DÉCALAGES POUR SIMULER DES POSITIONS DANS LA ZONE
# ============================================
# Ces décalages sont différents pour chaque zone
zone_offsets = {
    "Noor I": [(0.0005, -0.0003), (0.0002, 0.0002), (-0.0001, 0.0004), (0.0003, -0.0001)],
    "Noor II": [(0.0004, -0.0002), (0.0001, 0.0003), (-0.0002, 0.0005), (0.0002, -0.0002)],
    "Noor III": [(0.0003, -0.0001), (0.0002, 0.0004), (-0.0003, 0.0003), (0.0001, -0.0003)],
    "Noor IV": [(0.0006, -0.0004), (0.0003, 0.0001), (-0.0002, 0.0006), (0.0004, -0.0002)],
    "Midelt": [(0.0008, -0.0005), (0.0004, 0.0002), (-0.0003, 0.0007), (0.0005, -0.0003)]
}

offsets = zone_offsets.get(technician_zone, zone_offsets["Noor IV"])

# ============================================
# AJOUTER LES DÉFAUTS SUR LA CARTE (UNIQUEMENT CEUX DE LA ZONE)
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
        
        # Utiliser un offset différent pour chaque défaut (pour les répartir dans la zone)
        offset_idx = idx % len(offsets)
        lat_offset, lon_offset = offsets[offset_idx]
        lat = station_lat + lat_offset
        lon = station_lon + lon_offset
        
        # Ajouter le marqueur
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
            radius=50,
            color=color,
            fill=True,
            fill_opacity=0.3
        ).add_to(m)
else:
    st.info(f"✅ Aucun défaut actif dans la zone {technician_zone}.")

# ============================================
# LÉGENDE
# ============================================
legend_html = """
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); font-size: 12px;">
    <b>🔴 Légende</b><br>
    🔴 <span style="color:red">●</span> Critique (urgent)<br>
    🟠 <span style="color:orange">●</span> Haute priorité<br>
    🟡 <span style="color:gold">●</span> Priorité normale<br>
    🟢 <span style="color:green">●</span> Zone {technician_zone}
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
    st.markdown(f"### 📊 Défauts - Zone {technician_zone}")
    st.metric("⚠️ Défauts actifs", len(active_defects))
    
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