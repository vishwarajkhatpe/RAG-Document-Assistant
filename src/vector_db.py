import time
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY, EMBEDDING_MODEL, VECTOR_DB_PATH

class VectorDB:
    """
    Manages the FAISS vector database with Robust Error Handling.
    """

    @staticmethod
    def create_vector_store(text_chunks):
        """
        Creates vector store with automatic retries for network failures.
        """
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL, 
                google_api_key=GOOGLE_API_KEY
            )
            
            vector_store = None
            
            # REDUCED BATCH SIZE: Smaller packets are less likely to timeout
            batch_size = 5 
            total_chunks = len(text_chunks)
            
            print(f"🔄 Processing {total_chunks} chunks...")

            for i in range(0, total_chunks, batch_size):
                batch = text_chunks[i : i + batch_size]
                
                # --- RETRY LOGIC START ---
                success = False
                attempts = 0
                while not success and attempts < 3:
                    try:
                        if vector_store is None:
                            vector_store = FAISS.from_texts(batch, embedding=embeddings)
                        else:
                            vector_store.add_texts(batch)
                        success = True # It worked! Exit the retry loop
                        
                    except Exception as e:
                        attempts += 1
                        print(f"⚠️ Network error on batch {i} (Attempt {attempts}/3): {e}")
                        if attempts < 3:
                            wait_time = attempts * 5 # Wait 5s, then 10s...
                            print(f"   ⏳ Waiting {wait_time}s before retrying...")
                            time.sleep(wait_time)
                        else:
                            # If it fails 3 times, we have to stop
                            raise RuntimeError(f"❌ Failed to process batch after 3 attempts. Check internet connection.")
                # --- RETRY LOGIC END ---

                print(f"   ✅ Batch {i}-{i+len(batch)} done.")
                time.sleep(1) # Short nap to be nice to the API

            if vector_store:
                vector_store.save_local(VECTOR_DB_PATH)
                return vector_store
            else:
                raise ValueError("No text to process.")
            
        except Exception as e:
            print(f"❌ Final Error: {e}")
            raise e

    @staticmethod
    def load_vector_store():
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