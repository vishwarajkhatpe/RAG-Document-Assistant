import streamlit as st
from langchain_community.vectorstores import FAISS
# FIX: Import from community (compatible with your current installation)
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorDB:
    INDEX_PATH = "faiss_index"

    @staticmethod
    @st.cache_resource
    def get_embedding_model():
        # This works with your installed libraries
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    @staticmethod
    def create_vector_store(documents):
        """
        Takes Document objects (with page numbers) and creates the DB.
        """
        embeddings = VectorDB.get_embedding_model()
        
        # This preserves the page numbers we extracted in pdf_handler.py
        vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
        
        return vector_store

    @staticmethod
    def save_vector_store(vector_store):
        """Saves the FAISS index to disk."""
        vector_store.save_local(VectorDB.INDEX_PATH)

    @staticmethod
    def load_vector_store():
        """Loads the FAISS index from disk if it exists."""
        import os
        if os.path.exists(VectorDB.INDEX_PATH) and os.path.exists(os.path.join(VectorDB.INDEX_PATH, "index.faiss")):
            embeddings = VectorDB.get_embedding_model()
            return FAISS.load_local(VectorDB.INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        return None