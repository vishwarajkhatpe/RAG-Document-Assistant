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
            
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                background-color: #f8fafc; /* Slate-50 */
                color: #0f172a; /* Slate-900 */
            }

            /* --- SIDEBAR --- */
            [data-testid="stSidebar"] {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
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
                background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
                color: white;
                padding: 4rem 2rem;
                border-radius: 16px;
                text-align: center;
                margin-bottom: 3rem;
                box-shadow: 0 10px 25px -5px rgba(0, 176, 155, 0.4);
            }
            .hero-title {
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 1rem;
                letter-spacing: -0.05rem;
            }
            .hero-subtitle {
                font-size: 1.25rem;
                font-weight: 500;
                opacity: 0.95;
            }

            /* --- FEATURE CARDS --- */
            .feature-card {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                height: 100%;
                border: 1px solid #e2e8f0;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                border-color: #00b09b;
            }
            .card-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
                background: #f0fdf4;
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
            }
            .card-title {
                font-weight: 700;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                color: #1e293b;
            }
            .card-desc {
                color: #64748b;
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
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            }
            
            /* User Bubble (Green Theme) */
            .user-bubble {
                background-color: #dcfce7; /* Green-100 */
                color: #166534; /* Green-800 */
                border-top-right-radius: 0.25rem;
            }
            
            /* AI Bubble (White) */
            .ai-bubble {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                color: #334155;
                border-top-left-radius: 0.25rem;
            }

            /* --- CITATIONS --- */
            .source-container {
                margin-top: 0.75rem;
                background-color: #f8fafc;
                border-left: 3px solid #00b09b;
                padding: 0.75rem;
                border-radius: 0.25rem;
            }
            .source-header {
                font-size: 0.75rem;
                font-weight: 600;
                color: #00b09b;
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
                background: linear-gradient(to right, #00b09b, #96c93d);
                color: white;
                border: none;
                font-weight: 600;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                transition: opacity 0.2s;
            }
            .stButton > button:hover {
                opacity: 0.9;
                box-shadow: 0 4px 6px -1px rgba(0, 176, 155, 0.4);
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