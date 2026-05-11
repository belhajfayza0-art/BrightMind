# utils/styles.py
import streamlit as st

def apply_global_style():
    """Applique le CSS global à toutes les pages"""
    st.markdown("""
    <style>
        /* Cacher la navigation automatique de Streamlit */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Sidebar - Dégradé Vert + Jaune */
        [data-testid="stSidebar"] {
            background: linear-gradient(145deg, #0a2e1a 0%, #1b5e20 40%, #f9a825 100%);
            border-right: none;
        }
        
        /* === FORCER TOUS LES TEXTES DE LA SIDEBAR EN BLANC === */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Sauf le jaune pour certains éléments */
        [data-testid="stSidebar"] .user-role {
            color: #ffd54f !important;
        }
        
        [data-testid="stSidebar"] .sidebar-logo-subtitle {
            color: #ffd54f !important;
        }
        
        /* Style des liens de navigation */
        [data-testid="stSidebar"] .stPageLink {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 12px 16px;
            margin: 4px 0;
            display: block;
            border: 1px solid rgba(255,255,255,0.2);
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] .stPageLink:hover {
            background: rgba(255,255,255,0.2);
            transform: translateX(6px);
            border-color: #ffd54f;
            color: #ffd54f !important;
        }
        
        [data-testid="stSidebar"] .stPageLink:hover * {
            color: #ffd54f !important;
        }
        
        /* Bouton DECONNEXION */
        [data-testid="stSidebar"] .stButton button {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
            padding: 10px 16px;
            font-weight: 500;
            color: white !important;
        }
        
        [data-testid="stSidebar"] .stButton button:hover {
            background: rgba(255,255,255,0.2);
            color: #ffd54f !important;
        }
        
        /* Logo */
        .sidebar-logo {
            text-align: center;
            padding: 30px 0 20px 0;
            border-bottom: 2px solid rgba(255,215,0,0.5);
            margin-bottom: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 20px;
        }
        
        .sidebar-logo-title {
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 3px;
            color: white !important;
        }
        
        .sidebar-logo-subtitle {
            font-size: 10px;
            opacity: 0.9;
            letter-spacing: 2px;
            color: #ffd54f !important;
        }
        
        /* User card */
        .user-card {
            background: rgba(0,0,0,0.3);
            border-radius: 16px;
            padding: 15px;
            margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .user-name {
            font-size: 15px;
            font-weight: 600;
            color: white !important;
        }
        
        .user-role {
            font-size: 11px;
            opacity: 0.8;
            color: #ffd54f !important;
        }
        
        .user-zone {
            font-size: 11px;
            background: rgba(0,0,0,0.5);
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            color: white !important;
        }
        
        /* Main content */
        .main-header {
            background: linear-gradient(135deg, #0a2e1a 0%, #1b5e20 100%);
            border-radius: 16px;
            padding: 20px 30px;
            margin-bottom: 25px;
        }
        
        .main-header-title {
            color: white;
            font-size: 24px;
            font-weight: 600;
            margin: 0;
        }
        
        .main-header-subtitle {
            color: #ffd54f;
            font-size: 14px;
            margin: 8px 0 0 0;
        }
        
        /* Stat cards */
        .stat-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 700;
            color: #1b5e20;
            margin: 8px 0;
        }
        
        .stat-label {
            font-size: 13px;
            color: #6c757d;
            margin: 0;
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: #1b5e20;
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 3px solid #f9a825;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)