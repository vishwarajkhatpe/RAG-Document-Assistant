import logging
import streamlit as st
from typing import List, Any
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Initialize module-specific logger
logger = logging.getLogger(__name__)

class VectorDB:
    """
    Manages the Vector Database (FAISS) and Embedding Models.
    
    Architecture:
    - Uses Local Embeddings (HuggingFace) to avoid API costs and rate limits.
    - Uses FAISS (Facebook AI Similarity Search) for high-performance dense retrieval.
    - Implements strict caching to prevent re-loading heavy models on every user interaction.
    """
    
    # Configuration
    # 'all-MiniLM-L6-v2' is the industry standard for lightweight, fast, local embeddings.
    # It maps sentences to a 384-dimensional dense vector space.
    MODEL_NAME = "all-MiniLM-L6-v2"

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def get_embedding_model() -> HuggingFaceEmbeddings:
        """
        Loads the HuggingFace embedding model.
        Cached by Streamlit to ensure it only loads ONCE per session.
        
        Returns:
            HuggingFaceEmbeddings: The loaded model instance.
        """
        try:
            logger.info(f"Loading embedding model: {VectorDB.MODEL_NAME}...")
            
            # We use the CPU version for compatibility with free-tier cloud instances
            embeddings = HuggingFaceEmbeddings(
                model_name=VectorDB.MODEL_NAME,
                model_kwargs={'device': 'cpu'}
            )
            
            logger.info("Embedding model loaded successfully.")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise RuntimeError(f"Embedding Model Error: {e}")

    @staticmethod
    def create_vector_store(documents: List[Document]) -> FAISS:
        """
        Hydrates a FAISS vector index from a list of Document objects.
        
        Args:
            documents: List of Document objects (must contain 'page_content' and 'metadata').

        Returns:
            FAISS: An in-memory vector store ready for retrieval.
        """
        try:
            if not documents:
                logger.warning("Attempted to create vector store with empty document list.")
                raise ValueError("No documents provided for indexing.")

            logger.info(f"Creating FAISS index for {len(documents)} document chunks...")
            
            embeddings = VectorDB.get_embedding_model()
            
            # This step converts text -> vectors and builds the index
            # It preserves the metadata (page numbers) we extracted earlier
            vector_store = FAISS.from_documents(
                documents=documents, 
                embedding=embeddings
            )
            
            logger.info("Vector store created successfully.")
            return vector_store
            
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            raise RuntimeError(f"Vector Database Error: {e}")