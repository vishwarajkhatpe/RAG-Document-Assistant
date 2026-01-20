from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config.settings import GOOGLE_API_KEY, LLM_MODEL, TEMPERATURE

# Safety import block for compatibility
try:
    from langchain.chains.question_answering import load_qa_chain
except ImportError:
    from langchain.chains import load_qa_chain

class RAGChain:
    """
    Manages the RAG Chain. 
    Connects the context (retrieved locally) to the Brain (Gemini Cloud).
    """

    @staticmethod
    def get_conversational_chain():
        """
        Creates the LLM chain.
        """
        # Prompt: Strict instruction to use only provided context
        prompt_template = """
        Answer the question as detailed as possible from the provided context. 
        If the answer is not in the provided context, just say "The answer is not available in the context", 
        do not provide the wrong answer.

        Context:
        {context}

        Question: 
        {question}

        Answer:
        """

        try:
            # We still use Gemini for the INTELLIGENCE (Answering)
            model = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                temperature=TEMPERATURE,
                google_api_key=GOOGLE_API_KEY
            )

            prompt = PromptTemplate(
                template=prompt_template, 
                input_variables=["context", "question"]
            )

            chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
            return chain
            
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
            raise e