import requests
import streamlit as st
from streamlit_lottie import st_lottie

class UIUtils:
    """
    Helper class to manage UI styling and animations (Light Mode Optimized).
    """

    @staticmethod
    def load_lottie_url(url: str):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    @staticmethod
    def get_custom_css():
        return """
        <style>
            /* --- GLOBAL LIGHT MODE SETTINGS --- */
            
            /* Main Background - Clean White/Light Gray */
            .stApp {
                background-color: #ffffff;
            }
            
            /* Sidebar Background - Soft Gray for contrast */
            [data-testid="stSidebar"] {
                background-color: #f8f9fa;
                border-right: 1px solid #e9ecef;
            }
            
            /* Typography - Dark Gray for readability on light bg */
            h1, h2, h3, p, div, span {
                color: #212529 !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            /* Main Heading */
            h1 {
                color: #2563eb !important; /* Professional Blue */
                font-weight: 700;
                text-align: center;
                padding-bottom: 20px;
            }
            
            /* --- INPUT FIELDS --- */
            
            /* Text Input Boxes */
            .stTextInput > div > div > input {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 10px;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #2563eb;
                box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
            }

            /* --- BUTTONS --- */
            
            /* Primary Button Styling */
            .stButton > button {
                background-color: #2563eb; /* Blue */
                color: white !important;
                border-radius: 8px;
                border: none;
                padding: 0.5rem 1rem;
                font-weight: 600;
                transition: all 0.2s ease;
                width: 100%;
            }
            
            .stButton > button:hover {
                background-color: #1d4ed8;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            /* --- CHAT BUBBLES --- */
            
            /* User Message */
            [data-testid="stChatMessage"] {
                background-color: #f3f4f6;
                border-radius: 12px;
                padding: 10px;
                margin-bottom: 10px;
            }
            
            /* Assistant Message Avatar container */
            [data-testid="stChatMessage"] [data-testid="stChatMessageAvatarBackground"] {
                background-color: #2563eb;
            }

            /* --- STATUS BOXES --- */
            
            .success-box {
                padding: 15px;
                border-radius: 8px;
                background-color: #d1fae5; /* Light Green */
                color: #065f46 !important;
                border: 1px solid #a7f3d0;
                margin-bottom: 15px;
            }
            
            .error-box {
                padding: 15px;
                border-radius: 8px;
                background-color: #fee2e2; /* Light Red */
                color: #991b1b !important;
                border: 1px solid #fecaca;
                margin-bottom: 15px;
            }
        </style>
        """