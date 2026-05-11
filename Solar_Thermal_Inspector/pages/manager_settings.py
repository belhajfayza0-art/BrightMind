# pages/manager_settings.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.session_manager import require_manager, get_current_zone
from utils.styles import apply_global_style
from utils.sidebar import show_sidebar

# Appliquer le CSS
apply_global_style()

# Vérification
require_manager()

# Définir l'ID de la page
st.session_state['current_page'] = 'settings'

# Afficher la sidebar
show_sidebar()

# Récupérer la zone
user_zone = get_current_zone()

# En-tête
st.markdown(f"""
<div class="main-header">
    <div class="main-header-title">Configuration du système</div>
    <div class="main-header-subtitle">Zone {user_zone}</div>
</div>
""", unsafe_allow_html=True)

# Configuration
def load_station_config():
    try:
        df = pd.read_csv("data/station.csv")
        if len(df) > 0:
            return df.iloc[0].to_dict()
        else:
            return get_default_config()
    except FileNotFoundError:
        return get_default_config()

def get_default_config():
    configs = {
        "Noor I": {
            "station_name": "Noor I - CSP",
            "total_panels": 500000,
            "critical_temp": 120,
            "high_temp": 90,
            "medium_temp": 70
        },
        "Noor II": {
            "station_name": "Noor II - CSP",
            "total_panels": 660000,
            "critical_temp": 120,
            "high_temp": 90,
            "medium_temp": 70
        },
        "Noor III": {
            "station_name": "Noor III - Tour",
            "total_panels": 7400,
            "critical_temp": 565,
            "high_temp": 500,
            "medium_temp": 450
        },
        "Noor IV": {
            "station_name": "Noor IV - PV",
            "total_panels": 240000,
            "critical_temp": 85,
            "high_temp": 75,
            "medium_temp": 65
        },
        "Midelt": {
            "station_name": "Midelt - Hybride",
            "total_panels": 0,
            "critical_temp": 120,
            "high_temp": 90,
            "medium_temp": 70
        },
    }
    if user_zone in configs:
        return configs[user_zone]
    else:
        return configs["Noor I"]

def save_station_config(config):
    df = pd.DataFrame([config])
    df.to_csv("data/station.csv", index=False)

config = load_station_config()

# Informations zone
st.markdown('<div class="section-title">Informations zone</div>', unsafe_allow_html=True)

with st.form("station_info_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        station_name = st.text_input("Nom de la zone", value=config.get("station_name", ""))
        
        # Valeur par défaut sécurisée pour total_panels
        default_panels = config.get("total_panels", 0)
        if default_panels is None:
            default_panels = 0
        total_panels = st.number_input(
            "Nombre de panneaux/miroirs",
            min_value=1,
            max_value=1000000,
            value=int(default_panels)
        )
    
    with col2:
        last_maintenance = st.date_input("Dernière maintenance", value=datetime.now().date())
        status = st.selectbox("Statut", ["Active", "Maintenance", "Arrêt"])
    
    submitted_info = st.form_submit_button("Enregistrer", use_container_width=True)
    
    if submitted_info:
        config["station_name"] = station_name
        config["total_panels"] = total_panels
        config["last_maintenance"] = last_maintenance.strftime("%Y-%m-%d")
        config["status"] = status
        save_station_config(config)
        st.success("✅ Informations mises à jour")

st.markdown("<hr>", unsafe_allow_html=True)

# Seuils d'alerte
st.markdown('<div class="section-title">Seuils d\'alerte</div>', unsafe_allow_html=True)

with st.form("thresholds_form"):
    col1, col2, col3 = st.columns(3)
    
    # Valeurs par défaut sécurisées
    default_critical = config.get("critical_temp", 120)
    if default_critical is None:
        default_critical = 120
        
    default_high = config.get("high_temp", 90)
    if default_high is None:
        default_high = 90
        
    default_medium = config.get("medium_temp", 70)
    if default_medium is None:
        default_medium = 70
    
    with col1:
        critical_temp = st.number_input(
            "Critique (°C)",
            min_value=30,
            max_value=600,
            value=int(default_critical)
        )
    
    with col2:
        high_temp = st.number_input(
            "Haute (°C)",
            min_value=20,
            max_value=600,
            value=int(default_high)
        )
    
    with col3:
        medium_temp = st.number_input(
            "Moyenne (°C)",
            min_value=10,
            max_value=600,
            value=int(default_medium)
        )
    
    submitted_thresholds = st.form_submit_button("Enregistrer les seuils", use_container_width=True)
    
    if submitted_thresholds:
        # Vérifier la cohérence des seuils
        if medium_temp >= high_temp:
            st.error("⚠️ Le seuil Moyenne doit être inférieur au seuil Haute")
        elif high_temp >= critical_temp:
            st.error("⚠️ Le seuil Haute doit être inférieur au seuil Critique")
        else:
            config["critical_temp"] = critical_temp
            config["high_temp"] = high_temp
            config["medium_temp"] = medium_temp
            save_station_config(config)
            st.success("✅ Seuils mis à jour")

st.markdown("<hr>", unsafe_allow_html=True)

# Aperçu
st.markdown('<div class="section-title">Aperçu</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Valeur des panneaux (avec formatage conditionnel)
panels_value = config.get("total_panels", "N/A")
if isinstance(panels_value, (int, float)):
    panels_display = f"{panels_value:,}"
else:
    panels_display = str(panels_value)

with col1:
    st.markdown(f"**Zone** : {user_zone}")
    st.markdown(f"**Nom** : {config.get('station_name', 'N/A')}")
    st.markdown(f"**Panneaux** : {panels_display}")

with col2:
    st.markdown(f"**Critique** : > {config.get('critical_temp', 'N/A')}°C")
    st.markdown(f"**Haute** : > {config.get('high_temp', 'N/A')}°C")
    st.markdown(f"**Moyenne** : > {config.get('medium_temp', 'N/A')}°C")

st.markdown("<hr>", unsafe_allow_html=True)

# Actions
st.markdown('<div class="section-title">Actions</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("← Retour au Dashboard", use_container_width=True):
        st.switch_page("pages/manager_dashboard.py")

with col2:
    if st.button("Voir les rapports", use_container_width=True):
        st.switch_page("pages/manager_reports.py")