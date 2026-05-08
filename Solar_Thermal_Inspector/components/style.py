# components/style.py
import streamlit as st
import base64
import os

def apply_style():
    """Applique le style CSS commun à toutes les pages"""
    
    # Charger l'image en base64
    image_path = "assets/images/sidebar-bg.png"
    image_base64 = ""
    
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode()
    
    # Si l'image existe, l'utiliser, sinon utiliser un dégradé
    if image_base64:
        background_style = f"background-image: url('data:image/png;base64,{image_base64}'); background-size: cover; background-position: center;"
    else:
        background_style = "background: linear-gradient(180deg, #FEFCE8 0%, #FDF4E6 100%);"
    
    st.markdown(f"""
    <style>
        /* Palette de couleurs */
        :root {{
            --vert: #257c48;
            --vert-clair: #e8f5e9;
            --jaune: #dcda2c;
            --jaune-clair: #fefce8;
            --bleu: #3b82f6;
            --bleu-clair: #eff6ff;
            --gris: #6b7280;
            --gris-clair: #f3f4f6;
        }}
        
        /* ===== MENU LATÉRAL AVEC IMAGE BASE64 ===== */
        [data-testid="stSidebar"] {{
            {background_style}
            background-repeat: no-repeat;
            border-right: none !important;
            padding-top: 0 !important;
            position: relative;
        }}
        
        /* Overlay pour rendre le texte lisible */
        [data-testid="stSidebar"]::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.86);
            z-index: 0;
        }}
        
        /* Assurer que le contenu est au-dessus de l'overlay */
        [data-testid="stSidebar"] > div {{
            position: relative;
            z-index: 1;
        }}
        
        [data-testid="stSidebar"] .stButton button {{
            background: transparent;
            border: none;
            color: #4B5563;
            font-weight: 500;
            text-align: left;
            padding: 12px 16px;
            margin: 4px 8px;
            border-radius: 12px;
            transition: all 0.2s ease;
            width: calc(100% - 16px);
        }}
        
        [data-testid="stSidebar"] .stButton button:hover {{
            background: rgba(37, 124, 72, 0.1);
            color: #257c48;
            border-left: 3px solid #257c48;
        }}
        
        /* Menu actif */
        .menu-active {{
            background: rgba(37, 124, 72, 0.15) !important;
            color: #257c48 !important;
            border-left: 3px solid #257c48 !important;
            padding: 12px 16px;
            margin: 4px 8px;
            border-radius: 12px;
            font-weight: 500;
        }}
        
        /* Titre du menu */
        .menu-title {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #6B7280;
            padding: 0 16px 8px 16px;
            margin-top: 1rem;
        }}
        
        /* Cacher l'en-tête sidebar */
        .sidebar-header {{
            display: none !important;
        }}
        
        .user-info {{
            display: none !important;
        }}
        
        /* Cartes statistiques */
        .stat-card {{
            background: white;
            border-radius: 20px;
            padding: 1.2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 4px solid var(--vert);
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--vert);
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            color: var(--gris);
            margin-top: 0.3rem;
        }}
        
        .stat-trend {{
            font-size: 0.7rem;
            margin-top: 0.5rem;
        }}
        
        .trend-up {{ color: var(--vert); }}
        .trend-down {{ color: #ef4444; }}
        
        /* Carte de bienvenue */
        .welcome-card {{
            background: linear-gradient(135deg, var(--vert) 0%, #1a5c3a 100%);
            border-radius: 24px;
            padding: 1.5rem;
            color: white;
            margin-bottom: 1.5rem;
        }}
        
        /* Carte des défauts */
        .defect-card {{
            background: white;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            border-left: 4px solid var(--jaune);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .defect-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .defect-title {{
            font-weight: 600;
            font-size: 1rem;
        }}
        
        .defect-location {{
            font-size: 0.75rem;
            color: var(--gris);
        }}
        
        .defect-temp {{
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .temp-critical {{ color: #ef4444; }}
        .temp-high {{ color: #f97316; }}
        .temp-normal {{ color: var(--vert); }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 500;
        }}
        
        .badge-critical {{ background: #fee2e2; color: #ef4444; }}
        .badge-high {{ background: #ffedd5; color: #f97316; }}
        .badge-medium {{ background: #fefce8; color: var(--jaune); }}
        .badge-low {{ background: #e8f5e9; color: var(--vert); }}
        
        /* Timeline activités */
        .activity-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.8rem 0;
            border-bottom: 1px solid var(--gris-clair);
        }}
        
        .activity-icon {{
            width: 40px;
            height: 40px;
            border-radius: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }}
        
        .activity-icon-success {{ background: #e8f5e9; color: var(--vert); }}
        .activity-icon-warning {{ background: #fefce8; color: var(--jaune); }}
        .activity-icon-info {{ background: #eff6ff; color: var(--bleu); }}
        
        /* Mission card */
        .mission-card {{
            background: white;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #257c48;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }}
        
        .mission-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .badge-pending {{
            background: #fefce8;
            color: #dcda2c;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
        }}
        
        .badge-progress {{
            background: #eff6ff;
            color: #3b82f6;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
        }}
        
        .badge-completed {{
            background: #e8f5e9;
            color: #257c48;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
        }}
        
        /* Cacher menu Streamlit par défaut */
        [data-testid="stSidebarNav"] {{
            display: none !important;
        }}
        
        .stApp > header {{
            display: none !important;
        }}
        
        footer {{
            display: none !important;
        }}
        
        button[kind="header"] {{
            display: none !important;
        }}
        
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
    </style>
    """, unsafe_allow_html=True)