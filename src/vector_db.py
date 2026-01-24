import streamlit as st
from langchain_community.vectorstores import FAISS
# FIX: In the stable version, we import from community, not the new separate package
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorDB:
    @staticmethod
    @st.cache_resource
    def get_embedding_model():
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    @staticmethod
    def create_vector_store(text_chunks):
        embeddings = VectorDB.get_embedding_model()
        vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_store