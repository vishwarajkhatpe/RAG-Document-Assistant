import logging
import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

# Initialize module-specific logger
logger = logging.getLogger(__name__)

class VectorDB:
    """
    Manages the Vector Database (FAISS) and Embedding Models.
    
    Architecture:
    - Uses Google Gemini Embeddings (Cloud) for maximum speed and accuracy.
    - Uses FAISS for high-performance retrieval.
    """
    
    # CRITICAL: This is the new, high-performance model.
    # The old 'embedding-001' is dead. This is the replacement.
    MODEL_NAME = "models/text-embedding-004"

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def get_embedding_model():
        """
        Loads the Google GenAI embedding model.
        """
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY missing.")

            logger.info(f"Connecting to Google Cloud Embeddings: {VectorDB.MODEL_NAME}...")
            
            # We configure it to use the new model
            embeddings = GoogleGenerativeAIEmbeddings(
                model=VectorDB.MODEL_NAME,
                google_api_key=api_key
            )
            
            logger.info("Cloud Embedding model connected.")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise RuntimeError(f"Embedding Connection Error: {e}")

    @staticmethod
    def create_vector_store(documents: list[Document]):
        """
        Hydrates a FAISS vector index using Cloud Embeddings.
        """
        try:
            if not documents:
                raise ValueError("No documents provided.")

            logger.info(f"Sending {len(documents)} chunks to Google Cloud for embedding...")
            
            embeddings = VectorDB.get_embedding_model()
            
            # This sends text to Google and gets vectors back instantly
            vector_store = FAISS.from_documents(
                documents=documents, 
                embedding=embeddings
            )
            
            logger.info("Vector store created successfully.")
            return vector_store
            
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            raise RuntimeError(f"Vector Database Error: {e}")