import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key not found.")
else:
    genai.configure(api_key=api_key)
    print("📡 Contacting Google API to fetch available models...\n")
    
    try:
        found_any = False
        for m in genai.list_models():
            # Only show models that can generate text/content
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Available: {m.name}")
                found_any = True
        
        if not found_any:
            print("⚠️ Connected, but no 'generateContent' models found. Check your API key permissions.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")