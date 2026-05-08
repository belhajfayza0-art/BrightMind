"""
Simulateur d'IA - Génère des alertes automatiquement
À exécuter périodiquement ou via un bouton "Simuler"
"""

import random
import os
from datetime import datetime
from backend.alert_service import create_alert
from backend.mock_ai_analyzer import DEFECT_TYPES, LOCATIONS, generate_defect_image

def simulate_ai_detection():
    """Simule la détection d'un défaut par l'IA"""
    
    # Choisir un défaut aléatoire
    defect_type = random.choice(DEFECT_TYPES)
    location = random.choice(LOCATIONS)
    temperature = round(random.uniform(*defect_type['temp']), 1)
    
    # Générer une image du défaut (utiliser la fonction adaptée)
    image_path = generate_defect_image(defect_type, location)
    
    # Créer l'alerte
    defect = {
        'defect_type': defect_type['name'],
        'severity': defect_type['severity'],
        'temperature': temperature,
        'location': location['name'],
        'image_path': image_path
    }
    
    alert_id = create_alert(defect)
    
    return {
        'alert_id': alert_id,
        'defect': defect,
        'image_path': image_path
    }