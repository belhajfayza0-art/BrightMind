# pages/manager_reports.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from utils.session_manager import require_manager, get_current_zone
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar

# Appliquer le CSS
apply_global_style()

# Vérification
require_manager()

# Définir l'ID de la page
st.session_state['current_page'] = 'reports'

# Afficher la sidebar
show_sidebar()

# Récupérer la zone
user_zone = get_current_zone()

# En-tête
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Consultation des rapports</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# Chargement des données
def load_defects():
    try:
        df = pd.read_csv("data/defects.csv")
        if 'date_detection' in df.columns:
            df['date_detection'] = pd.to_datetime(df['date_detection'])
        if 'zone' in df.columns:
            df = df[df['zone'] == user_zone]
        return df
    except FileNotFoundError:
        dates = [datetime.now() - timedelta(days=i) for i in range(30)]
        data = [{"id": i+1, "type": ["Hotspot", "Crack", "Shading", "Dust", "Broken Cell"][i % 5], "gravite": ["Critique", "Haute", "Moyenne", "Basse"][i % 4], "localisation": f"L{(i%10)+1}-C{(i%8)+1}", "temperature": 50 + (i % 100), "date_detection": date, "statut": ["Nouveau", "Assigné", "Résolu"][i % 3], "zone": user_zone} for i, date in enumerate(dates)]
        return pd.DataFrame(data)

defects = load_defects()
nb_resolus = len(defects[defects['statut'] == 'Résolu']) if len(defects) > 0 else 0
tx_resolution = round((nb_resolus / len(defects)) * 100, 1) if len(defects) > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{len(defects)}</div>
        <div class="stat-label">Total défauts</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{nb_resolus}</div>
        <div class="stat-label">Défauts résolus</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{tx_resolution}%</div>
        <div class="stat-label">Taux de résolution</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Filtres
st.markdown('<div class="section-title">Filtres</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    types = ["Tous"] + sorted(defects['type'].unique().tolist()) if len(defects) > 0 else ["Tous"]
    selected_type = st.selectbox("Type de défaut", types)
with col2:
    gravites = ["Toutes"] + sorted(defects['gravite'].unique().tolist()) if len(defects) > 0 else ["Toutes"]
    selected_gravite = st.selectbox("Gravité", gravites)
with col3:
    period = st.selectbox("Période", ["7 derniers jours", "30 derniers jours", "3 derniers mois", "Tout afficher"])
    today = datetime.now()
    start_date = today - timedelta(days=7) if period == "7 derniers jours" else today - timedelta(days=30) if period == "30 derniers jours" else today - timedelta(days=90) if period == "3 derniers mois" else datetime(2020, 1, 1)

st.markdown("<hr>", unsafe_allow_html=True)

# Application des filtres
def apply_filters(df):
    if len(df) == 0:
        return df
    if selected_type != "Tous":
        df = df[df['type'] == selected_type]
    if selected_gravite != "Toutes":
        df = df[df['gravite'] == selected_gravite]
    if 'date_detection' in df.columns:
        df = df[df['date_detection'] >= start_date]
    return df

filtered_defects = apply_filters(defects)

st.markdown('<div class="section-title">Résultats</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.metric("Nombre de défauts filtrés", len(filtered_defects))
with col2:
    temp_moyenne = round(filtered_defects['temperature'].mean(), 1) if len(filtered_defects) > 0 else "N/A"
    st.metric("Température moyenne", f"{temp_moyenne}°C" if temp_moyenne != "N/A" else "N/A")

st.markdown("<hr>", unsafe_allow_html=True)

# Tableau
st.markdown('<div class="section-title">Détail des défauts</div>', unsafe_allow_html=True)
if len(filtered_defects) > 0:
    display_df = filtered_defects[['type', 'gravite', 'localisation', 'temperature', 'date_detection', 'statut']].copy()
    display_df.columns = ['Type', 'Gravité', 'Localisation', 'Température (°C)', 'Date', 'Statut']
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Aucun défaut ne correspond aux filtres")

st.markdown("<hr>", unsafe_allow_html=True)

# Graphiques
if len(filtered_defects) > 0:
    st.markdown('<div class="section-title">Visualisations</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        type_counts = filtered_defects['type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Nombre']
        fig = px.bar(type_counts, x='Type', y='Nombre', color='Nombre', color_continuous_scale=['#bbdefb', '#1565c0'])
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        gravite_counts = filtered_defects['gravite'].value_counts().reset_index()
        gravite_counts.columns = ['Gravité', 'Nombre']
        fig = px.pie(gravite_counts, values='Nombre', names='Gravité', color='Gravité', color_discrete_map={'Critique': '#d32f2f', 'Haute': '#f57c00', 'Moyenne': '#fbc02d', 'Basse': '#388e3c'})
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Export
st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
if len(filtered_defects) > 0:
    csv = filtered_defects.to_csv(index=False).encode('utf-8')
    st.download_button("Exporter en CSV", data=csv, file_name=f"rapport_{user_zone}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
else:
    st.warning("Aucune donnée à exporter")

st.markdown("<hr>", unsafe_allow_html=True)

# Actions
st.markdown('<div class="section-title">Actions</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("← Retour au Dashboard", use_container_width=True):
        st.switch_page("pages/manager_dashboard.py")
with col2:
    if st.button("Assigner une mission", use_container_width=True):
        st.switch_page("pages/manager_assign.py")
        # Ajouter cette section dans manager_reports.py

st.markdown('<div class="section-title">Rapports des techniciens</div>', unsafe_allow_html=True)

def load_technician_reports():
    try:
        df = pd.read_csv("data/rapports_techniciens.csv")
        # Filtrer par zone du manager
        df = df[df['technicien_zone'] == user_zone]
        return df
    except FileNotFoundError:
        return pd.DataFrame()

tech_reports = load_technician_reports()

if len(tech_reports) > 0:
    for idx, row in tech_reports.iterrows():
        with st.expander(f"📄 Rapport - {row['technicien_nom']} - {row['date_rapport']}"):
            st.markdown(f"**Mission ID:** {row['mission_id']}")
            st.markdown(f"**Technicien:** {row['technicien_nom']}")
            st.markdown(f"**Date:** {row['date_rapport']}")
            st.markdown(f"**Contenu:**")
            st.info(row['contenu'])
            
            # Bouton pour marquer comme lu
            if st.button(f"Marquer comme lu", key=f"mark_read_{row['id']}"):
                st.success("Rapport marqué comme consulté")
else:
    st.info("Aucun rapport reçu des techniciens")