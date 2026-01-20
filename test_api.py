import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found.")
    exit()

genai.configure(api_key=api_key)

print("📡 Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   - {m.name}")
            
    # Explicitly test the new model
    print("\n🤖 Testing gemini-2.5-flash...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello! Are you working?")
    print(f"   Response: {response.text}")
    print("✅ Success! API is working.")
    
except Exception as e:
    print(f"❌ Error: {e}")