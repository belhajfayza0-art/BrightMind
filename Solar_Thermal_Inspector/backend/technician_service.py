"""
Service de gestion des techniciens
Gère les missions, notifications et statistiques
"""

import pandas as pd
import os
from datetime import datetime

# Chemins des fichiers
DATA_DIR = "data"
MISSIONS_FILE = os.path.join(DATA_DIR, "missions.csv")
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, "notifications.csv")
DEFECTS_FILE = os.path.join(DATA_DIR, "defects.csv")

def init_data_files():
    """Crée les fichiers de données s'ils n'existent pas"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(MISSIONS_FILE):
        missions_df = pd.DataFrame({
            'id': pd.Series(dtype='int64'),
            'defect_id': pd.Series(dtype='int64'),
            'technician_id': pd.Series(dtype='int64'),
            'technician_name': pd.Series(dtype='str'),
            'defect_type': pd.Series(dtype='str'),
            'severity': pd.Series(dtype='str'),
            'location': pd.Series(dtype='str'),
            'temperature': pd.Series(dtype='float64'),
            'status': pd.Series(dtype='str'),
            'created_at': pd.Series(dtype='str'),
            'completed_at': pd.Series(dtype='str'),
            'notes': pd.Series(dtype='str')
        })
        missions_df.to_csv(MISSIONS_FILE, index=False)
    
    if not os.path.exists(NOTIFICATIONS_FILE):
        notif_df = pd.DataFrame({
            'id': pd.Series(dtype='int64'),
            'technician_id': pd.Series(dtype='int64'),
            'technician_name': pd.Series(dtype='str'),
            'message': pd.Series(dtype='str'),
            'defect_type': pd.Series(dtype='str'),
            'created_at': pd.Series(dtype='str'),
            'read': pd.Series(dtype='bool'),
            'mission_id': pd.Series(dtype='int64')
        })
        notif_df.to_csv(NOTIFICATIONS_FILE, index=False)
    
    if not os.path.exists(DEFECTS_FILE):
        defects_df = pd.DataFrame({
            'id': pd.Series(dtype='int64'),
            'type': pd.Series(dtype='str'),
            'severity': pd.Series(dtype='str'),
            'location': pd.Series(dtype='str'),
            'temperature': pd.Series(dtype='float64'),
            'image_path': pd.Series(dtype='str'),
            'detected_at': pd.Series(dtype='str'),
            'status': pd.Series(dtype='str')
        })
        defects_df.to_csv(DEFECTS_FILE, index=False)

def get_technician_missions(technician_id, technician_name):
    """Récupère les missions d'un technicien"""
    init_data_files()  # ← AJOUTER CETTE LIGNE
    
    if not os.path.exists(MISSIONS_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(MISSIONS_FILE)
    
    if 'technician_name' in df.columns:
        missions = df[df['technician_name'] == technician_name]
    else:
        missions = df[df['technician_id'] == technician_id]
    
    return missions

def get_mission_by_id(mission_id):
    """Récupère une mission par son ID"""
    df = pd.read_csv(MISSIONS_FILE)
    mission = df[df['id'] == mission_id]
    if len(mission) > 0:
        return mission.iloc[0]
    return None

def update_mission_status(mission_id, status, notes=""):
    """Met à jour le statut d'une mission"""
    init_data_files()
    
    # Lire le fichier
    df = pd.read_csv(MISSIONS_FILE)
    
    # Convertir la colonne completed_at en string (pour éviter l'erreur)
    if 'completed_at' in df.columns:
        df['completed_at'] = df['completed_at'].astype(str)
    else:
        df['completed_at'] = ""
    
    # Convertir notes en string
    if 'notes' in df.columns:
        df['notes'] = df['notes'].astype(str)
    
    mask = df['id'] == mission_id
    
    # Mettre à jour le statut
    df.loc[mask, 'status'] = str(status)
    df.loc[mask, 'notes'] = str(notes) if notes else ""
    
    if status == "completed":
        df.loc[mask, 'completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Remplacer les NaN par des chaînes vides
    df = df.fillna("")
    
    # Sauvegarder
    df.to_csv(MISSIONS_FILE, index=False)
    return True
def get_technician_stats(technician_name):
    """Calcule les statistiques du technicien"""
    init_data_files()  # ← AJOUTER CETTE LIGNE
    
    df = pd.read_csv(MISSIONS_FILE)
    tech_missions = df[df['technician_name'] == technician_name]
    
    total = len(tech_missions)
    completed = len(tech_missions[tech_missions['status'] == 'completed'])
    pending = len(tech_missions[tech_missions['status'] == 'pending'])
    in_progress = len(tech_missions[tech_missions['status'] == 'in_progress'])
    
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
        'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
    }

def get_technician_notifications(technician_name):
    """Récupère les notifications non lues"""
    init_data_files()  # ← AJOUTER CETTE LIGNE
    
    if not os.path.exists(NOTIFICATIONS_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(NOTIFICATIONS_FILE)
    notifs = df[(df['technician_name'] == technician_name) & (df['read'] == False)]
    return notifs

def get_all_notifications(technician_name):
    """Récupère toutes les notifications (lues et non lues)"""
    init_data_files()
    
    if not os.path.exists(NOTIFICATIONS_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(NOTIFICATIONS_FILE)
    notifs = df[df['technician_name'] == technician_name]
    return notifs

def mark_notification_read(notif_id):
    """Marque une notification comme lue"""
    df = pd.read_csv(NOTIFICATIONS_FILE)
    df.loc[df['id'] == notif_id, 'read'] = True
    df.to_csv(NOTIFICATIONS_FILE, index=False)

def mark_all_notifications_read(technician_name):
    """Marque toutes les notifications comme lues"""
    df = pd.read_csv(NOTIFICATIONS_FILE)
    df.loc[df['technician_name'] == technician_name, 'read'] = True
    df.to_csv(NOTIFICATIONS_FILE, index=False)

def create_mission(defect, technician_name):
    """Crée une nouvelle mission pour un technicien"""
    init_data_files()
    
    df = pd.read_csv(MISSIONS_FILE)
    
    new_id = len(df) + 1 if len(df) > 0 else 1
    
    new_mission = pd.DataFrame([{
        'id': new_id,
        'defect_id': defect.get('id', new_id),
        'technician_id': 1,
        'technician_name': technician_name,
        'defect_type': defect['class_name'],
        'severity': defect['severity'],
        'location': defect['location'],
        'temperature': defect['temperature'],
        'status': 'pending',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'completed_at': '',
        'notes': ''
    }])
    
    df = pd.concat([df, new_mission], ignore_index=True)
    df.to_csv(MISSIONS_FILE, index=False)
    
    # Créer une notification
    create_notification(technician_name, defect, new_id)
    
    return new_id

def create_notification(technician_name, defect, mission_id):
    """Crée une notification pour le technicien"""
    df = pd.read_csv(NOTIFICATIONS_FILE)
    
    new_id = len(df) + 1 if len(df) > 0 else 1
    
    severity_emoji = "🔴" if defect['severity'] == 'critical' else "🟠" if defect['severity'] == 'high' else "🟡"
    
    new_notif = pd.DataFrame([{
        'id': new_id,
        'technician_id': 1,
        'technician_name': technician_name,
        'message': f"{severity_emoji} Nouvelle mission : {defect['class_name']} détecté à {defect['location']} ({defect['temperature']}°C)",
        'defect_type': defect['class_name'],
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'read': False,
        'mission_id': mission_id
    }])
    
    df = pd.concat([df, new_notif], ignore_index=True)
    df.to_csv(NOTIFICATIONS_FILE, index=False)

def get_unread_notifications_count(technician_name):
    """Retourne le nombre de notifications non lues"""
    notifs = get_technician_notifications(technician_name)
    return len(notifs)