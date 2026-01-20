import time
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY, EMBEDDING_MODEL, VECTOR_DB_PATH

class VectorDB:
    """
    Manages the FAISS vector database with Rate Limit handling.
    """

    @staticmethod
    def create_vector_store(text_chunks):
        """
        Converts text chunks to embeddings in batches to avoid hitting Google's 429 Rate Limit.
        """
        try:
            # 1. Initialize the embedding model
            embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL, 
                google_api_key=GOOGLE_API_KEY
            )
            
            vector_store = None
            
            # 2. Define Batch Size
            # The Free Tier creates limits around 60 requests/minute.
            # Processing 10 chunks at a time with a delay is safe.
            batch_size = 10 
            total_chunks = len(text_chunks)
            
            print(f"🔄 Processing {total_chunks} chunks in batches of {batch_size}...")

            # 3. Process in batches
            for i in range(0, total_chunks, batch_size):
                # Slice the list to get a sub-list (e.g., chunks 0-9, then 10-19)
                batch = text_chunks[i : i + batch_size]
                
                if vector_store is None:
                    # First batch creates the store
                    vector_store = FAISS.from_texts(batch, embedding=embeddings)
                else:
                    # Subsequent batches allow us to add to the existing store
                    vector_store.add_texts(batch)
                
                # Progress indicator for the logs
                print(f"   ✅ Processed batch {i} to {i + len(batch)}")
                
                # 4. CRITICAL: Sleep to respect Rate Limits
                # Waiting 1 second between batches prevents the 429 error
                time.sleep(2) 
            
            # 5. Save the final result
            if vector_store:
                vector_store.save_local(VECTOR_DB_PATH)
                return vector_store
            else:
                raise ValueError("No vector store created (empty text?).")
            
        except Exception as e:
            print(f"❌ Error creating vector store: {e}")
            raise e

    @staticmethod
    def load_vector_store():
        """
        Loads the saved vector store from the hard drive.
        """
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL, 
                google_api_key=GOOGLE_API_KEY
            )
            
            return FAISS.load_local(
                VECTOR_DB_PATH, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise e