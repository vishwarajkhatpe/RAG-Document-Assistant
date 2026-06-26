import requests
import streamlit as st

class UIUtils:
    @staticmethod
    def load_lottie_url(url: str):
        """
        Uses the 'requests' library to load Lottie animations.
        """
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    @staticmethod
    def get_clean_style():
        """
        Defines the Global CSS for the application.
        """
        return """
        <style>
            /* --- FONTS & GLOBAL --- */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            :root {
                --glass-bg: rgba(255, 255, 255, 0.4);
                --glass-border: rgba(255, 255, 255, 0.5);
                --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
                --glass-blur: blur(12px);
                --indigo-light: rgba(79, 70, 229, 0.1);
                --indigo-solid: #4f46e5;
            }

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                color: #0f172a;
            }
            
            /* Ambient Background */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                background-attachment: fixed;
            }

            /* --- SIDEBAR --- */
            [data-testid="stSidebar"] {
                background-color: rgba(255, 255, 255, 0.3) !important;
                backdrop-filter: var(--glass-blur) !important;
                -webkit-backdrop-filter: var(--glass-blur) !important;
                border-right: 1px solid var(--glass-border) !important;
            }
            .sidebar-logo-title {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 25px;
                padding: 10px 0;
            }
            .sidebar-title {
                font-size: 1.4rem;
                font-weight: 700;
                color: #0f172a;
            }

            /* --- HERO BANNER --- */
            .hero-banner {
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                -webkit-backdrop-filter: var(--glass-blur);
                padding: 4rem 2rem;
                border-radius: 16px;
                text-align: center;
                margin-bottom: 3rem;
                border: 1px solid var(--glass-border);
                box-shadow: var(--glass-shadow);
            }
            .hero-title {
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 1rem;
                letter-spacing: -0.05rem;
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .hero-subtitle {
                font-size: 1.25rem;
                font-weight: 500;
                color: #475569;
            }

            /* --- FEATURE CARDS --- */
            .feature-card {
                background: var(--glass-bg);
                backdrop-filter: var(--glass-blur);
                -webkit-backdrop-filter: var(--glass-blur);
                border-radius: 16px;
                padding: 1.5rem;
                height: 100%;
                border: 1px solid var(--glass-border);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: var(--glass-shadow);
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
                border-color: rgba(255, 255, 255, 0.8);
            }
            .card-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
                background: rgba(255, 255, 255, 0.5);
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                box-shadow: inset 0 2px 4px rgba(255,255,255,0.8);
            }
            .card-title {
                font-weight: 700;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                color: #1e293b;
            }
            .card-desc {
                color: #475569;
                font-size: 0.95rem;
                line-height: 1.5;
            }

            /* --- CHAT MESSAGES --- */
            .chat-row { display: flex; width: 100%; margin-bottom: 1.5rem; }
            .row-reverse { justify-content: flex-end; }
            .row-standard { justify-content: flex-start; }
            
            .chat-bubble {
                padding: 1rem 1.25rem;
                border-radius: 1rem;
                max-width: 80%;
                line-height: 1.6;
                font-size: 1rem;
                position: relative;
                backdrop-filter: var(--glass-blur);
                -webkit-backdrop-filter: var(--glass-blur);
                box-shadow: var(--glass-shadow);
            }
            
            /* Animations */
            @keyframes slideUp {
                0% { opacity: 0; transform: translateY(15px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            /* User Bubble (Indigo Theme) */
            .user-bubble {
                background: var(--indigo-light);
                border: 1px solid rgba(79, 70, 229, 0.2);
                color: #3730a3;
                border-top-right-radius: 0.25rem;
                animation: slideUp 0.4s ease-out forwards;
            }
            
            /* AI Bubble (White) */
            .ai-bubble {
                background: rgba(255, 255, 255, 0.6);
                border: 1px solid var(--glass-border);
                color: #334155;
                border-top-left-radius: 0.25rem;
                animation: slideUp 0.4s ease-out forwards;
            }

            /* --- CITATIONS --- */
            .source-container {
                margin-top: 0.75rem;
                background: rgba(255, 255, 255, 0.5);
                backdrop-filter: blur(4px);
                border-left: 3px solid var(--indigo-solid);
                border-radius: 0.25rem;
                padding: 0.75rem;
                animation: slideUp 0.5s ease-out forwards;
            }
            .source-header {
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--indigo-solid);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.25rem;
            }
            .source-text {
                font-size: 0.85rem;
                color: #475569;
                font-style: italic;
            }

            /* --- BUTTONS --- */
            .stButton > button {
                background: rgba(255, 255, 255, 0.4) !important;
                backdrop-filter: var(--glass-blur) !important;
                -webkit-backdrop-filter: var(--glass-blur) !important;
                color: var(--indigo-solid) !important;
                border: 1px solid rgba(79, 70, 229, 0.3) !important;
                font-weight: 600 !important;
                padding: 0.5rem 1rem !important;
                border-radius: 0.75rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            }
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                background: rgba(255, 255, 255, 0.8) !important;
                box-shadow: 0 8px 25px rgba(79, 70, 229, 0.2) !important;
                border-color: var(--indigo-solid) !important;
            }
            
            /* --- INPUT FIELDS --- */
            .stChatInput > div {
                background: rgba(255, 255, 255, 0.5) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid var(--glass-border) !important;
                border-radius: 1rem !important;
            }
        </style>
        """

    @staticmethod
    def render_home_card(emoji, title, desc):
        """
        Renders the cards used on the Home Screen.
        """
        return f"""
        <div class="feature-card">
            <div class="card-icon">{emoji}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>
        """

    @staticmethod
    def render_message(role, content):
        """
        Renders the Chat Bubbles.
        """
        if role == "user":
            return f"""
            <div class="chat-row row-reverse">
                <div class="chat-bubble user-bubble">{content}</div>
            </div>
            """
        else:
            return f"""
            <div class="chat-row row-standard">
                <div class="chat-bubble ai-bubble">{content}</div>
            </div>
            """

    @staticmethod
    def render_source(page, text):
        """
        Renders the Citation Box for Feature 2.
        """
        return f"""
        <div class="source-container">
            <div class="source-header">Page {page}</div>
            <div class="source-text">"...{text}..."</div>
        </div>
        """