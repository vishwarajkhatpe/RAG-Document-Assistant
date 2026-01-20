import subprocess
import sys

# 1. List of "Modern" packages that conflict with the standard RAG stack
CONFLICTING_PACKAGES = [
    "langchain",
    "langchain-core",
    "langchain-community",
    "langchain-google-genai",
    "langchain-classic",        # The v1.0 legacy adapter
    "langgraph",               # The agentic framework
    "langgraph-checkpoint",    # The specific blocker from your logs
    "langgraph-prebuilt",
    "langchain-text-splitters"
]

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: {e}")

print("🧹 STARTING CLEANUP: Removing conflicting libraries...")

# 2. Uninstall everything forcibly
uninstall_cmd = [sys.executable, "-m", "pip", "uninstall", "-y"] + CONFLICTING_PACKAGES
subprocess.check_call(uninstall_cmd)

print("✅ Cleanup Complete.")
print("📦 INSTALLING STABLE STACK (v0.1.x)...")

# 3. Install the "Golden Standard" versions (Stable, Compatible)
# We use one long command to let pip resolve dependencies together
install_cmd = [
    sys.executable, "-m", "pip", "install",
    "langchain==0.1.20",           # The last "Perfect" standard version
    "langchain-community==0.0.38", # Matching community version
    "langchain-core==0.1.52",      # Matching core version
    "langchain-google-genai==1.0.3",
    "langchain-text-splitters==0.0.1",
    "streamlit",
    "faiss-cpu",
    "pypdf2",
    "python-dotenv"
]

subprocess.check_call(install_cmd)

print("\n🎉 SUCCESS! Environment fixed.")
print("👉 You can now run: streamlit run app.py")