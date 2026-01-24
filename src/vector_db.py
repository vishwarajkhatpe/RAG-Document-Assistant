import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class VectorDB:
    @staticmethod
    @st.cache_resource
    def get_embedding_model():
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    @staticmethod
    def create_vector_store(documents):
        """
        Updated to use 'from_documents' to preserve metadata.
        """
        embeddings = VectorDB.get_embedding_model()
        
        # CHANGE: We now use 'from_documents' instead of 'from_texts'
        # This automatically stores the page numbers we created in step 1
        vector_store = FAISS.from_documents(documents=documents, embedding=embeddings)
        
        return vector_store