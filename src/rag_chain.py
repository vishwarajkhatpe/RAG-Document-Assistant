from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config.settings import GOOGLE_API_KEY, LLM_MODEL, TEMPERATURE

# Safety import block
try:
    from langchain.chains.question_answering import load_qa_chain
except ImportError:
    from langchain.chains import load_qa_chain

class RAGChain:
    """
    Manages the RAG Chain with improved social intelligence and professional tone.
    """

    @staticmethod
    def get_conversational_chain():
        """
        Creates the LLM chain with a smart prompt that handles greetings 
        and missing information gracefully.
        """
        
        # --- THE FIX IS HERE ---
        # We give the AI a "Persona" and specific rules for different scenarios.
        prompt_template = """
        You are an intelligent and professional document assistant. Your goal is to help the user understand their PDF files.

        Instructions:
        1. GREETINGS: If the user greets you (e.g., "Hi", "Hello", "Good morning"), politely greet them back and ask what they would like to know about their documents. Do not look for context for greetings.
        2. CONTEXTUAL QUESTIONS: Answer the question ONLY using the facts from the provided context below.
        3. TONE: Maintain a helpful, clear, and professional tone. Use bullet points if the answer is long.
        4. MISSING INFO: If the answer is NOT in the context, do not make it up. Simply say: "I analyzed the documents, but I couldn't find information regarding that specific topic."

        Context:
        {context}

        User Question: 
        {question}

        Answer:
        """

        try:
            model = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                temperature=TEMPERATURE,
                google_api_key=GOOGLE_API_KEY
            )

            prompt = PromptTemplate(
                template=prompt_template, 
                input_variables=["context", "question"]
            )

            # We use chain_type="stuff" which simply inserts the context into the prompt above
            chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
            return chain
            
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
            raise e