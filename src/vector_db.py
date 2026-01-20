import os
from langchain_community.vectorstores import FAISS
# UPDATED: Importing the local embedding model wrapper
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import VECTOR_DB_PATH

class VectorDB:
    """
    Manages the FAISS vector database using LOCAL Embeddings.
    This eliminates 429 (Rate Limit) and 503 (Network) errors.
    """

    @staticmethod
    def get_embedding_function():
        """
        Returns the local embedding model.
        'all-MiniLM-L6-v2' is a standard, lightweight model (80MB) 
        that runs fast on standard CPUs.
        """
        # model_name="all-MiniLM-L6-v2" is the industry standard for lightweight CPU embeddings
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    @staticmethod
    def create_vector_store(text_chunks):
        """
        Creates vector store locally. No API keys or internet needed for this part.
        """
        try:
            print("🔄 Initializing local embedding model...")
            # This will download the model the first time you run it (takes ~30s)
            embeddings = VectorDB.get_embedding_function()
            
            print(f"📊 Processing {len(text_chunks)} chunks locally...")
            
            # Create FAISS index using local CPU
            vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
            
            # Save to disk
            vector_store.save_local(VECTOR_DB_PATH)
            print("✅ Vector store saved successfully.")
            return vector_store
            
        except Exception as e:
            print(f"❌ Error creating vector store: {e}")
            raise e

    @staticmethod
    def load_vector_store():
        """
        Loads the saved vector store from disk.
        """
        try:
            # We must use the SAME embedding function to load that we used to create
            embeddings = VectorDB.get_embedding_function()
            
            if not os.path.exists(VECTOR_DB_PATH):
                raise FileNotFoundError("Index not found. Please upload a PDF first.")

            return FAISS.load_local(
                VECTOR_DB_PATH, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise e