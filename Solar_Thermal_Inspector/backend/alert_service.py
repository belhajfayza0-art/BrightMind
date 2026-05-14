"""
Service de gestion des alertes IA
Gère les alertes et leur assignation aux techniciens
"""

import pandas as pd
import os
import json
from datetime import datetime
import streamlit as st

DATA_DIR = "data"
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.csv")
MISSIONS_FILE = os.path.join(DATA_DIR, "missions.csv")
ACTIVE_SESSIONS_FILE = os.path.join(DATA_DIR, "active_sessions.json")

def init_alert_files():
    """Initialise les fichiers d'alertes"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(ALERTS_FILE):
        alerts_df = pd.DataFrame({
            'id': pd.Series(dtype='int64'),
            'defect_type': pd.Series(dtype='str'),
            'severity': pd.Series(dtype='str'),
            'temperature': pd.Series(dtype='float64'),
            'location': pd.Series(dtype='str'),
            'image_path': pd.Series(dtype='str'),
            'detected_at': pd.Series(dtype='str'),
            'status': pd.Series(dtype='str'),
            'taken_by': pd.Series(dtype='str'),
            'taken_at': pd.Series(dtype='str'),
            'zone': pd.Series(dtype='str')
        })
        alerts_df.to_csv(ALERTS_FILE, index=False)

# Mapping défaut → zone (CORRIGÉ pour couvrir toutes les zones)
defect_to_zone = {
    # Noor IV
    "Hotspot": "Noor IV",
    "Crack": "Noor IV",
    "Dust": "Noor IV",
    "Shading": "Noor IV",
    "Broken Cell": "Noor IV",
    # Noor I
    "MirrorMisalignment": "Noor I",
    "AbsorberTubeDegradation": "Noor I",
    # Noor II
    "HTFLeak": "Noor II",
    # Noor III
    "TrackingFailure": "Noor III",
    "ReceiverTubeLeak": "Noor III",
    "ThermalGradientAnomaly": "Noor III",
    # Midelt
    "StringOpenCircuit": "Midelt",
    "StringReversedPolarity": "Midelt"
}

def create_alert(defect):
    """Crée une nouvelle alerte (status = pending = en attente manager)"""
    init_alert_files()
    
    df = pd.read_csv(ALERTS_FILE)
    new_id = len(df) + 1 if len(df) > 0 else 1
    zone = defect_to_zone.get(defect['defect_type'], "Noor IV")
    
    new_alert = pd.DataFrame([{
        'id': new_id,
        'defect_type': defect['defect_type'],
        'severity': defect['severity'],
        'temperature': defect['temperature'],
        'location': defect['location'],
        'image_path': defect.get('image_path', ''),
        'detected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'pending',
        'taken_by': '',
        'taken_at': '',
        'zone': zone
    }])
    
    df = pd.concat([df, new_alert], ignore_index=True)
    df.to_csv(ALERTS_FILE, index=False)
    
    return new_id

def is_manager_connected(zone):
    """Vérifie si un manager de la zone est connecté"""
    try:
        if os.path.exists(ACTIVE_SESSIONS_FILE):
            with open(ACTIVE_SESSIONS_FILE, "r") as f:
                sessions = json.load(f)
            for session in sessions:
                if session.get('role') == 'manager' and session.get('zone') == zone:
                    # Vérifier si la session est récente (moins de 30 minutes)
                    connected_at = session.get('connected_at', '')
                    if connected_at:
                        try:
                            connected_time = datetime.strptime(connected_at, "%Y-%m-%d %H:%M:%S")
                            if (datetime.now() - connected_time).seconds < 1800:  # 30 minutes
                                return True
                        except:
                            return True
                    return True
        return False
    except:
        return False

def get_least_busy_technician(zone):
    """Trouve le technicien avec le moins de missions en cours dans la zone"""
    from backend.technician_service import get_technician_missions_by_zone
    
    df_users = pd.read_csv("data/users.csv")
    print(f"🔍 Recherche techniciens pour zone: {zone}")
    print(df_users[['name', 'role', 'zone']].to_string())
    
    technicians = df_users[(df_users['role'] == 'technician') & (df_users['zone'] == zone)]
    print(f"🔍 Techniciens trouvés: {len(technicians)}")
    
    if len(technicians) == 0:
        return None
    
    tech_mission_count = []
    for _, tech in technicians.iterrows():
        missions = get_technician_missions_by_zone(tech['name'], zone)
        pending_count = len(missions[missions['status'].isin(['pending', 'in_progress'])])
        tech_mission_count.append({
            'name': tech['name'],
            'count': pending_count,
            'email': tech['email']
        })
    
    tech_mission_count.sort(key=lambda x: x['count'])
    return tech_mission_count[0]['name'] if tech_mission_count else None

def auto_assign_mission(defect, zone):
    """IA assigne automatiquement la mission au technicien le moins chargé"""
    from backend.technician_service import create_mission
    
    technician = get_least_busy_technician(zone)
    
    if technician:
        mission_defect = {
            'class_name': defect['defect_type'],
            'severity': defect['severity'],
            'location': defect['location'],
            'temperature': defect['temperature'],
            'image_path': defect.get('image_path', '')
        }
        mission_id = create_mission(mission_defect, technician, zone, assigned_by="IA")
        return {
            'status': 'assigned', 
            'mission_id': mission_id, 
            'technician': technician
        }
    else:
        return {'status': 'no_technician'}


def get_pending_alerts_by_zone(technician_zone=None):
    init_alert_files()
    
    if not os.path.exists(ALERTS_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(ALERTS_FILE)
    
    if 'zone' not in df.columns:
        df['zone'] = 'Noor IV'
        df.to_csv(ALERTS_FILE, index=False)
    
    if technician_zone:
        # ⚠️ IMPORTANT : Filtre par zone ET par status
        pending = df[(df['status'] == 'pending') & (df['zone'] == technician_zone)]
    else:
        pending = df[df['status'] == 'pending']
    
    return pending

def assign_alert_to_technician(alert_id, technician_name):
    """Manager assigne une alerte à un technicien"""
    df = pd.read_csv(ALERTS_FILE)
    
    mask = df['id'] == alert_id
    alert = df[mask].iloc[0]
    
    # Supprimer l'alerte
    df = df[~mask]
    df.to_csv(ALERTS_FILE, index=False)
    
    # Créer la mission
    from backend.technician_service import create_mission
    
    mission_defect = {
        'class_name': alert['defect_type'],
        'severity': alert['severity'],
        'location': alert['location'],
        'temperature': alert['temperature'],
        'image_path': alert['image_path']
    }
    
    mission_id = create_mission(mission_defect, technician_name, alert['zone'], assigned_by="Manager")
    return mission_id

def is_alert_taken(alert_id):
    """Vérifie si une alerte a déjà été traitée"""
    df = pd.read_csv(ALERTS_FILE)
    alert = df[df['id'] == alert_id]
    if len(alert) > 0:
        return alert.iloc[0]['status'] != 'pending'
    return False

def process_new_defect(defect):
    zone = defect_to_zone.get(defect['defect_type'], "Noor IV")
    #st.write(f"🔍 DEBUG: zone={zone}, manager_connected={is_manager_connected(zone)}")
    
    if is_manager_connected(zone):
        alert_id = create_alert(defect)
        return {'status': 'pending_manager', 'alert_id': alert_id, 'zone': zone}
    else:
        result = auto_assign_mission(defect, zone)
        return {
            'status': 'assigned',
            'zone': zone,
            'technician': result.get('technician'),
            'mission_id': result.get('mission_id')
        }