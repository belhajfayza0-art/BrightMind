"""
Service de gestion des alertes IA
Gère les alertes et leur assignation aux techniciens
"""

import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.csv")
MISSIONS_FILE = os.path.join(DATA_DIR, "missions.csv")

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

# Mapping défaut → zone
defect_to_zone = {
    "Hotspot": "Noor IV",
    "Crack": "Noor IV",
    "Dust": "Noor IV",
    "Shading": "Noor IV",
    "Broken Cell": "Noor IV",
    "MirrorMisalignment": "Noor I",
    "AbsorberTubeDegradation": "Noor I",
    "HTFLeak": "Noor II",
    "TrackingFailure": "Noor III",
    "ReceiverTubeLeak": "Noor III",
    "ThermalGradientAnomaly": "Noor III",
    "StringOpenCircuit": "Midelt",
    "StringReversedPolarity": "Midelt"
}

def create_alert(defect):
    """Crée une nouvelle alerte avec la zone appropriée"""
    init_alert_files()
    
    df = pd.read_csv(ALERTS_FILE)
    
    new_id = len(df) + 1 if len(df) > 0 else 1
    
    # Déterminer la zone
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

def get_pending_alerts_by_zone(technician_zone):
    """Récupère les alertes UNIQUEMENT de la zone du technicien"""
    init_alert_files()
    
    if not os.path.exists(ALERTS_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(ALERTS_FILE)
    
    # Si colonne zone n'existe pas, l'ajouter
    if 'zone' not in df.columns:
        df['zone'] = 'Noor IV'
        df.to_csv(ALERTS_FILE, index=False)
    
    pending = df[(df['status'] == 'pending') & (df['zone'] == technician_zone)]
    return pending

def take_alert(alert_id, technician_name):
    """Un technicien prend une alerte"""
    df = pd.read_csv(ALERTS_FILE)
    
    df['taken_by'] = df['taken_by'].astype(str)
    df['taken_at'] = df['taken_at'].astype(str)
    
    mask = df['id'] == alert_id
    df.loc[mask, 'status'] = 'taken'
    df.loc[mask, 'taken_by'] = str(technician_name)
    df.loc[mask, 'taken_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df.to_csv(ALERTS_FILE, index=False)
    
    alert = df[mask].iloc[0]
    from backend.technician_service import create_mission
    
    mission_defect = {
        'class_name': alert['defect_type'],
        'severity': alert['severity'],
        'location': alert['location'],
        'temperature': alert['temperature'],
        'image_path': alert['image_path']
    }
    
    mission_id = create_mission(mission_defect, technician_name, alert['zone'])
    return mission_id

def is_alert_taken(alert_id):
    """Vérifie si une alerte a déjà été prise"""
    df = pd.read_csv(ALERTS_FILE)
    alert = df[df['id'] == alert_id]
    if len(alert) > 0:
        return alert.iloc[0]['status'] != 'pending'  # True si taken
    return False