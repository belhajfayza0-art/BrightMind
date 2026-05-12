"""
Simulateur d'IA - Génère des alertes automatiquement
Pour toutes les zones : Noor I, II, III, IV, Midelt
"""

import random
import os
from datetime import datetime
from backend.alert_service import create_alert
from backend.mock_ai_analyzer import generate_defect_image

# Toutes les anomalies par zone
DEFECTS_BY_ZONE = {
    "Noor I": [
        {"name": "MirrorMisalignment", "severity": "high", "temp_range": (60, 80), "icon": "🪞"},
        {"name": "AbsorberTubeDegradation", "severity": "critical", "temp_range": (80, 100), "icon": "🔧"},
    ],
    "Noor II": [
        {"name": "MirrorMisalignment", "severity": "high", "temp_range": (60, 80), "icon": "🪞"},
        {"name": "AbsorberTubeDegradation", "severity": "critical", "temp_range": (80, 100), "icon": "🔧"},
        {"name": "HTFLeak", "severity": "critical", "temp_range": (85, 105), "icon": "💧"},
    ],
    "Noor III": [
        {"name": "TrackingFailure", "severity": "high", "temp_range": (55, 75), "icon": "🎯"},
        {"name": "ReceiverTubeLeak", "severity": "critical", "temp_range": (75, 95), "icon": "💧"},
        {"name": "ThermalGradientAnomaly", "severity": "medium", "temp_range": (50, 70), "icon": "🌡️"},
    ],
    "Noor IV": [
        {"name": "Hotspot", "severity": "critical", "temp_range": (75, 95), "icon": "🔥"},
        {"name": "Crack", "severity": "high", "temp_range": (60, 75), "icon": "💔"},
        {"name": "Dust", "severity": "low", "temp_range": (35, 45), "icon": "🌫️"},
        {"name": "Shading", "severity": "medium", "temp_range": (45, 60), "icon": "🌑"},
        {"name": "Broken Cell", "severity": "critical", "temp_range": (80, 100), "icon": "⚡"},
    ],
    "Midelt": [
        {"name": "StringOpenCircuit", "severity": "critical", "temp_range": (70, 90), "icon": "⚡"},
        {"name": "StringReversedPolarity", "severity": "high", "temp_range": (65, 85), "icon": "🔄"},
        {"name": "Hotspot", "severity": "critical", "temp_range": (75, 95), "icon": "🔥"},
        {"name": "Crack", "severity": "high", "temp_range": (60, 75), "icon": "💔"},
    ],
}

# Liste de toutes les zones
ALL_ZONES = ["Noor I", "Noor II", "Noor III", "Noor IV", "Midelt"]

def simulate_ai_detection(zone=None):
    """
    Simule la détection d'un défaut par l'IA
    Si zone est spécifié, crée une alerte pour cette zone
    Sinon, choisit une zone aléatoire
    """
    
    # Choisir une zone aléatoire si non spécifiée
    if zone is None:
        zone = random.choice(ALL_ZONES)
    
    # Choisir un défaut dans la zone sélectionnée
    defects = DEFECTS_BY_ZONE[zone]
    defect_type = random.choice(defects)
    
    # Température aléatoire dans la plage
    temperature = round(random.uniform(*defect_type["temp_range"]), 1)
    
    # Générer une localisation
    row = random.randint(1, 12)
    col = random.randint(1, 13)
    location = f"{zone}, Ligne {row}, Colonne {col}"
    
    # Générer une image (optionnel)
    from backend.mock_ai_analyzer import generate_defect_image
    # Créer un objet defect_type simulé pour generate_defect_image
    mock_defect = {
        "name": defect_type["name"],
        "color": (255, 50, 50) if defect_type["severity"] == "critical" else (255, 150, 50),
        "temp": defect_type["temp_range"]
    }
    mock_location = {"name": location}
    
    try:
        image_path = generate_defect_image(mock_defect, mock_location)
    except:
        image_path = ""
    
    # Créer l'alerte
    defect = {
        'defect_type': defect_type["name"],
        'severity': defect_type["severity"],
        'temperature': temperature,
        'location': location,
        'image_path': image_path
    }
    
    alert_id = create_alert(defect)
    
    return {
        'alert_id': alert_id,
        'defect': defect,
        'zone': zone
    }

def simulate_detection_for_zone(zone):
    """Simule une détection spécifiquement pour une zone donnée"""
    return simulate_ai_detection(zone)

def simulate_multiple_detections():
    """Simule plusieurs détections pour tester toutes les zones"""
    results = []
    for zone in ALL_ZONES:
        result = simulate_ai_detection(zone)
        results.append(result)
    return results