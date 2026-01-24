import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class VectorDB:
    @staticmethod
    @st.cache_resource
    def get_embedding_model():
        """
        Loads the HuggingFace embedding model.
        Decorated with @st.cache_resource to prevent reloading on every run.
        """
        # This model runs locally on your CPU
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return embedding_model

    @staticmethod
    def create_vector_store(text_chunks):
        """
        Takes text chunks and creates a FAISS Vector Store.
        """
        # 1. Get the cached embedding model
        embeddings = VectorDB.get_embedding_model()
        
        # 2. Create the Vector Store
        # This effectively 'indexes' your document
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        
        return vector_store