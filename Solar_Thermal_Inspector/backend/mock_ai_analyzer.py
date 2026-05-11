"""
Simulateur d'IA pour les tests - En attendant le vrai modèle de l'équipe IA
À remplacer par le vrai modèle quand il sera prêt
"""

import random
from datetime import datetime

class MockAnalyzer:
    """Simulateur d'analyse IA pour les tests"""
    
    def __init__(self):
        self.defect_types = [
            {"name": "Hotspot", "severity": "critical", "temp_range": (75, 95)},
            {"name": "Crack", "severity": "high", "temp_range": (60, 75)},
            {"name": "Shading", "severity": "medium", "temp_range": (45, 60)},
            {"name": "Dust", "severity": "low", "temp_range": (35, 45)},
            {"name": "Broken Cell", "severity": "critical", "temp_range": (80, 100)},
        ]
        
        self.locations = [
            {"row": 3, "col": 7, "name": "Ligne 3, Colonne 7"},
            {"row": 5, "col": 12, "name": "Ligne 5, Colonne 12"},
            {"row": 1, "col": 4, "name": "Ligne 1, Colonne 4"},
            {"row": 8, "col": 2, "name": "Ligne 8, Colonne 2"},
            {"row": 2, "col": 15, "name": "Ligne 2, Colonne 15"},
            {"row": 10, "col": 8, "name": "Ligne 10, Colonne 8"},
            {"row": 4, "col": 3, "name": "Ligne 4, Colonne 3"},
            {"row": 7, "col": 11, "name": "Ligne 7, Colonne 11"},
        ]
    
    def analyze_image(self, image_path):
        """
        Simule l'analyse d'une image thermique
        Retourne une liste de défauts simulés
        """
        num_defects = random.randint(0, 3)
        defects = []
        
        for _ in range(num_defects):
            defect_type = random.choice(self.defect_types)
            location = random.choice(self.locations)
            
            defect = {
                'id': random.randint(1000, 9999),
                'class_name': defect_type['name'],
                'severity': defect_type['severity'],
                'confidence': round(random.uniform(0.75, 0.98), 2),
                'temperature': round(random.uniform(*defect_type['temp_range']), 1),
                'location': location['name'],
                'row': location['row'],
                'col': location['col'],
                'bbox': [random.randint(50, 300) for _ in range(4)],
                'image_path': image_path,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            defects.append(defect)
        
        return defects
    
    def analyze_batch(self, image_paths):
        """Analyse plusieurs images"""
        all_defects = []
        for path in image_paths:
            defects = self.analyze_image(path)
            all_defects.extend(defects)
        return all_defects


# Instance unique
_analyzer_instance = None

def get_analyzer():
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = MockAnalyzer()
    return _analyzer_instance
# ============================================
# CONSTANTES POUR LA SIMULATION D'ALERTES
# ============================================

DEFECT_TYPES = [
    {"name": "Hotspot", "severity": "critical", "temp": (75, 95), "color": (255, 50, 50), "icon": "🔥"},
    {"name": "Crack", "severity": "high", "temp": (60, 75), "color": (255, 150, 50), "icon": "💔"},
    {"name": "Broken Cell", "severity": "critical", "temp": (80, 100), "color": (200, 0, 0), "icon": "⚡"},
    {"name": "Shading", "severity": "medium", "temp": (45, 60), "color": (255, 200, 50), "icon": "🌑"},
    {"name": "Dust", "severity": "low", "temp": (35, 45), "color": (150, 150, 150), "icon": "🌫️"},
]

LOCATIONS = [
    {"row": 3, "col": 7, "name": "Ligne 3, Colonne 7"},
    {"row": 5, "col": 12, "name": "Ligne 5, Colonne 12"},
    {"row": 1, "col": 4, "name": "Ligne 1, Colonne 4"},
    {"row": 8, "col": 2, "name": "Ligne 8, Colonne 2"},
    {"row": 2, "col": 15, "name": "Ligne 2, Colonne 15"},
    {"row": 10, "col": 8, "name": "Ligne 10, Colonne 8"},
    {"row": 4, "col": 3, "name": "Ligne 4, Colonne 3"},
    {"row": 7, "col": 11, "name": "Ligne 7, Colonne 11"},
]

def generate_defect_image(defect_type, location):
    """Génère une image simulée d'un défaut"""
    import os
    import random
    from PIL import Image, ImageDraw
    from datetime import datetime
    
    # Dossier des images simulées
    SIMULATED_IMAGES_DIR = "data/simulated_images"
    os.makedirs(SIMULATED_IMAGES_DIR, exist_ok=True)
    
    # Créer une image de base (simule une image thermique)
    img = Image.new('RGB', (600, 400), color=(30, 30, 50))
    draw = ImageDraw.Draw(img)
    
    # Dessiner un carré rouge (zone du défaut)
    defect_color = defect_type['color']
    x1, y1 = 200, 150
    x2, y2 = 400, 250
    draw.rectangle([x1, y1, x2, y2], fill=defect_color, outline=(255, 255, 255), width=3)
    
    # Ajouter du texte
    try:
        draw.text((x1 + 20, y1 + 20), defect_type['name'], fill=(255, 255, 255))
        temp_value = random.uniform(*defect_type['temp'])
        draw.text((x1 + 20, y1 + 50), f"{temp_value:.1f}°C", fill=(255, 255, 255))
        draw.text((x1 + 20, y1 + 80), location['name'], fill=(255, 255, 255))
    except:
        pass
    
    # Sauvegarder l'image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"defect_{defect_type['name']}_{timestamp}.png"
    filepath = os.path.join(SIMULATED_IMAGES_DIR, filename)
    img.save(filepath)
    
    return filepath