import requests
import streamlit as st
from streamlit_lottie import st_lottie

class UIUtils:
    """
    Helper class to manage UI styling and animations.
    """

    @staticmethod
    def load_lottie_url(url: str):
        """
        Fetches a Lottie animation JSON from a URL.
        """
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    @staticmethod
    def get_custom_css():
        """
        Returns custom CSS to make the app look modern and colorful.
        """
        return """
        <style>
            /* Main Background Gradient */
            .stApp {
                background: linear-gradient(to right bottom, #f0f2f6, #e2e8f0);
            }
            
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #1e293b;
                color: white;
            }
            
            /* Custom Title Style */
            h1 {
                color: #2563eb;
                font-family: 'Helvetica', sans-serif;
                text-align: center;
                text-shadow: 2px 2px 4px #00000020;
            }
            
            /* Chat Message Box Styling */
            .stTextInput > div > div > input {
                border-radius: 20px;
                border: 2px solid #2563eb;
                padding: 10px;
            }
            
            /* Button Styling */
            .stButton > button {
                background-color: #2563eb;
                color: white;
                border-radius: 20px;
                padding: 10px 24px;
                border: none;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background-color: #1d4ed8;
                transform: scale(1.05);
            }
            
            /* Result Box Styling */
            .success-box {
                padding: 20px;
                border-radius: 10px;
                background-color: #dcfce7;
                border-left: 5px solid #22c55e;
                color: #14532d;
            }
            
            .error-box {
                padding: 20px;
                border-radius: 10px;
                background-color: #fee2e2;
                border-left: 5px solid #ef4444;
                color: #7f1d1d;
            }
        </style>
        """