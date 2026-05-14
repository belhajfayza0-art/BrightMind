"""
Suivi des sessions actives pour savoir si un manager est connecté
"""

import json
import os
from datetime import datetime

SESSIONS_FILE = "data/active_sessions.json"

def register_session(email, name, role, zone):
    """Enregistre une session active"""
    import json
    import os
    from datetime import datetime
    
    SESSIONS_FILE = "data/active_sessions.json"
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    sessions = []
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r") as f:
            sessions = json.load(f)
    
    # Supprimer l'ancienne session du même utilisateur
    sessions = [s for s in sessions if s.get('email') != email]
    
    sessions.append({
        'email': email,
        'name': name,
        'role': role,
        'zone': zone,
        'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

def unregister_session(email):
    """Supprime une session active"""
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r") as f:
            sessions = json.load(f)
        
        sessions = [s for s in sessions if s.get('email') != email]
        
        with open(SESSIONS_FILE, "w") as f:
            json.dump(sessions, f, indent=2)