import os
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Text Splitting Settings
# CHUNK_SIZE: How many characters to read at once (1000 is good for 2.5-Flash)
# CHUNK_OVERLAP: Keeps context between chunks so sentences aren't cut weirdly
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Configurations
# We use the verified model name here
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.3  # Keeps the AI focused on facts, not creativity

# Paths
VECTOR_DB_PATH = "faiss_index"