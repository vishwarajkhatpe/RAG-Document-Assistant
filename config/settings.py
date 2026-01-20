import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Text Splitting Settings
# CHUNK_SIZE: Number of characters per text chunk. 1000 is a good balance for Gemini.
# CHUNK_OVERLAP: Overlap ensures context isn't lost at the break points.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Configurations
EMBEDDING_MODEL = "models/embedding-001"
LLM_MODEL = "gemini-pro"
TEMPERATURE = 0.3  # Lower temperature (0.3) makes the model more factual/deterministic

# Paths
VECTOR_DB_PATH = "faiss_index"