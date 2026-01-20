from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import GOOGLE_API_KEY, EMBEDDING_MODEL, VECTOR_DB_PATH

class VectorDB:
    """
    Manages the FAISS vector database: creating, saving, and loading content.
    """

    @staticmethod
    def create_vector_store(text_chunks):
        """
        Takes text chunks, converts them to embeddings (numbers), and saves them locally.
        
        Args:
            text_chunks (list): List of text strings to index.
        """
        try:
            # 1. Initialize the embedding model
            # This model translates text into a list of numbers (vectors)
            embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL, 
                google_api_key=GOOGLE_API_KEY
            )
            
            # 2. Create the vector store
            # FAISS processes the text and organizes the vectors for fast searching
            vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
            
            # 3. Save to disk
            # We save it so we don't have to re-process the PDF every time we ask a question
            vector_store.save_local(VECTOR_DB_PATH)
            return vector_store
            
        except Exception as e:
            print(f"Error creating vector store: {e}")
            raise e

    @staticmethod
    def load_vector_store():
        """
        Loads the previously saved vector store from the hard drive.
        
        Returns:
            FAISS: The loaded vector store object.
        """
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model=EMBEDDING_MODEL, 
                google_api_key=GOOGLE_API_KEY
            )
            
            # Load the FAISS index
            # allow_dangerous_deserialization=True is required by LangChain 
            # when loading pickle files. It is safe here because we created the file ourselves.
            return FAISS.load_local(
                VECTOR_DB_PATH, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise e