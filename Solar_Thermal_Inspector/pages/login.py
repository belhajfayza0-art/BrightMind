"""
Page de connexion - Design 50/50 - Tout en haut
Avec sélection de zone pour inscription
"""

import streamlit as st
import base64
from utils.session_manager import (
    init_session_state, init_users_db, authenticate_user, 
    login_user, save_user, is_logged_in
)

# ============================================
# FONCTION POUR L'IMAGE
# ============================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Erreur chargement image : {e}")
        return None

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Solar Thermal Inspector",
    page_icon="☀️",
    layout="wide"
)

# Charger l'image
image_base64 = get_image_base64("assets/images/panneaux-solaires-8.jpg")

# Initialisation
init_users_db()
init_session_state()

if is_logged_in():
    st.switch_page("app.py")

# ============================================
# CSS - SUPPRESSION TOTALE DES ESPACES
# ============================================
st.markdown("""
<style>
    /* Cacher tous les éléments Streamlit */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    [data-testid="stToolbar"] { display: none; }
    footer { display: none; }
    header { display: none; }
    
    /* Supprimer TOUTES les marges */
    * {
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }
    
    html, body, .stApp, .main, .block-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .row-widget {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stColumn {
        padding: 0 !important;
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LAYOUT : 2 COLONNES
# ============================================
col_image, col_form = st.columns([1, 1])

# ============================================
# COLONNE GAUCHE : IMAGE PLEINE HAUTEUR
# ============================================
with col_image:
    if image_base64:
        st.markdown(f"""
        <style>
            .image-container {{
                width: 100%;
                height: 100vh;
                overflow: hidden;
                margin: 0;
                padding: 0;
            }}
            .image-container img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
        </style>
        <div class="image-container">
            <img src="data:image/jpeg;base64,{image_base64}">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .image-container {
                width: 100%;
                height: 100vh;
                background: linear-gradient(135deg, #1a5c3a, #4a9e35);
                display: flex;
                align-items: center;
                justify-content: center;
            }
        </style>
        <div class="image-container">
            <div style="text-align: center; color: white;">
                <div style="font-size: 4rem;">☀️</div>
                <div style="font-size: 1.5rem; margin-top: 1rem;">Solar Thermal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# COLONNE DROITE : FORMULAIRE (TOUT EN HAUT)
# ============================================
with col_form:
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Berkshire+Swash&display=swap" rel="stylesheet">
    <style>
        .form-container {
            width: 100%;
            background: white;
            padding: 2rem 3rem 3rem 3rem !important;
            margin: 0 !important;
        }

        .title {
            font-family: 'Berkshire Swash', cursive;
            font-size: 3rem;
            font-weight: 600;
            color: #257c48;
            margin: 0 0 1.5rem 0 !important;
            padding: 0 !important;
            letter-spacing: 2px;
            text-align: center;
        }
        
        .subtitle {
            font-size: 0.8rem;
            color: #6b8a7a;
            margin: 0 0 1.5rem 0 !important;
            padding: 0 0 0.3rem 0 !important;
            border-bottom: 2px solid #dcda2c;
            display: inline-block;
        }
        
        .label {
            font-size: 0.7rem;
            font-weight: 600;
            color: #1a3c2c;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 0 0 0.5rem 0 !important;
            display: block;
        }
        
        .stTextInput > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stTextInput > div > div > input {
            border-radius: 12px;
            padding: 12px 16px !important;
            border: 1px solid #e0e8e0;
            background: #fafcfa;
            font-size: 0.9rem;
            width: 100%;
            margin-bottom: 1rem !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #dcda2c;
            box-shadow: 0 0 0 2px rgba(220,218,44,0.2);
            outline: none;
        }
        
        .stSelectbox > div {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stSelectbox > div > div {
            border-radius: 12px;
            border: 1px solid #e0e8e0;
            background: #fafcfa;
            margin-bottom: 1rem !important;
        }
        
        .stTabs {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            display: flex !important;
            gap: 1.5rem;
            justify-content: center;
            margin: 0 0 2rem 0 !important;
            padding: 0 !important;
            border-bottom: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 1.1rem;
            font-weight: 600;
            color: white;
            padding: 0.5rem 1.5rem !important;
            background: #9ab89a;
            border-radius: 30px !important;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: #7a9a7a !important;
        }
        .stTabs [aria-selected="true"] {
            background: #1a5c3a !important;
            color: white !important;
            border-bottom: none !important;
        }
        
        .stButton > button {
            border-radius: 40px;
            padding: 12px !important;
            font-weight: 600;
            font-size: 0.9rem;
            width: 100%;
            margin-top: 0.5rem !important;
            background: #1a5c3a;
            color: white;
            border: none;
        }
        
        .stButton > button:hover {
            background: #0d3d24;
            transform: translateY(-1px);
        }
        
        .stAlert {
            border-radius: 12px;
            margin-top: 1rem !important;
        }
        
        .demo-box {
            margin-top: 2rem !important;
            padding: 1rem !important;
            background: #f5f7f5;
            border-radius: 16px;
            border-left: 3px solid #dcda2c;
        }
        
        .demo-title {
            font-size: 0.65rem;
            font-weight: 700;
            color: #1a5c3a;
            margin-bottom: 0.5rem !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .demo-text {
            font-size: 0.65rem;
            color: #6b8a7a;
        }
        
        .footer {
            margin-top: 2rem !important;
            text-align: center;
            font-size: 0.55rem;
            color: #b0c0b0;
        }
        .image-container {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 50% !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        .right-content {
            min-height: 100vh !important;
        }
    </style>
    
    <div class="form-container">
        <div class="title">SOLAR THERMAL</div>
    """, unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    # Liste des zones disponibles
    ZONES = ["Noor I", "Noor II", "Noor III", "Noor IV", "Midelt"]
    
    # ========== CONNEXION ==========
    with tab1:
        st.markdown('<label class="label">EMAIL</label>', unsafe_allow_html=True)
        email = st.text_input("login_email", placeholder="exemple@domaine.com", key="login_email", label_visibility="collapsed")
        
        st.markdown('<label class="label">MOT DE PASSE</label>', unsafe_allow_html=True)
        password = st.text_input("login_password", type="password", placeholder="••••••••", key="login_password", label_visibility="collapsed")
        
        if st.button("Se connecter", type="primary", use_container_width=True, key="login_btn"):
            if email and password:
                user = authenticate_user(email, password)
                if user:
                    login_user(user["email"], user["name"], user["role"], user.get("zone", "toutes"))
                    st.success(f"Bonjour {user['name']} !")
                    st.switch_page("app.py")
                else:
                    st.error("Email ou mot de passe incorrect")
            else:
                st.warning("Veuillez remplir tous les champs")
    
    # ========== INSCRIPTION AVEC ZONE ==========
    with tab2:
        st.markdown('<label class="label">NOM COMPLET</label>', unsafe_allow_html=True)
        name = st.text_input("signup_name", placeholder="Votre nom", key="signup_name", label_visibility="collapsed")
        
        st.markdown('<label class="label">EMAIL</label>', unsafe_allow_html=True)
        email_su = st.text_input("signup_email", placeholder="exemple@domaine.com", key="signup_email", label_visibility="collapsed")
        
        st.markdown('<label class="label">MOT DE PASSE</label>', unsafe_allow_html=True)
        pwd = st.text_input("signup_password", type="password", placeholder="••••••••", key="signup_password", label_visibility="collapsed")
        
        st.markdown('<label class="label">CONFIRMER</label>', unsafe_allow_html=True)
        pwd2 = st.text_input("signup_confirm", type="password", placeholder="••••••••", key="signup_confirm", label_visibility="collapsed")
        
        st.markdown('<label class="label">RÔLE</label>', unsafe_allow_html=True)
        role = st.selectbox("Rôle", ["technician", "manager"], key="signup_role", label_visibility="collapsed")
        
        # ===== NOUVEAU : Sélection de la ZONE =====
        st.markdown('<label class="label">ZONE D’AFFECTATION</label>', unsafe_allow_html=True)
        zone = st.selectbox("Zone", ZONES, key="signup_zone", label_visibility="collapsed")
        st.caption("📍 La zone définit sur quel périmètre vous travaillerez")
        
        if st.button("Créer mon compte", type="primary", use_container_width=True, key="signup_btn"):
            if name and email_su and pwd:
                if pwd != pwd2:
                    st.error("Les mots de passe ne correspondent pas")
                elif len(pwd) < 6:
                    st.warning("6 caractères minimum")
                else:
                    success, msg = save_user(email_su, name, pwd, role, zone)
                    if success:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)
            else:
                st.warning("Veuillez remplir tous les champs")
    
    # Comptes démo (mis à jour avec les zones)
    st.markdown("""
    <div class="demo-box">
        <div class="demo-title">🔐 COMPTES DE DÉMONSTRATION</div>
        <div class="demo-text">👔 SUPER MANAGER : admin@solarthermal.com / admin123 (Toutes zones)</div>
        <div class="demo-text">📊 MANAGER Noor III : karim@noor3.com / manager123</div>
        <div class="demo-text">🔧 TECHNICIEN Noor III : hassan@noor3.com / tech123</div>
        <div class="demo-text" style="margin-top:8px;">📍 Zones disponibles : Noor I, Noor II, Noor III, Noor IV, Midelt</div>
    </div>
    <div class="footer">© 2025 Solar Thermal Inspector</div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)