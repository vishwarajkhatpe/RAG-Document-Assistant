# Updated imports to ensure compatibility
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate  # Updated to use langchain_core
from config.settings import GOOGLE_API_KEY, LLM_MODEL, TEMPERATURE

class RAGChain:
    """
    Manages the RAG (Retrieval-Augmented Generation) chain setup.
    """

    @staticmethod
    def get_conversational_chain():
        """
        Creates a chain that connects the LLM with the prompt template.
        """
        # 1. Define the Prompt Template
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
            # 2. Initialize the Gemini Model
            model = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                temperature=TEMPERATURE,
                google_api_key=GOOGLE_API_KEY
            )

            # 3. Create the Prompt Object
            # We use PromptTemplate from langchain_core to avoid legacy warnings
            prompt = PromptTemplate(
                template=prompt_template, 
                input_variables=["context", "question"]
            )

            # 4. Load the Chain
            # This function requires the 'langchain' package to be installed
            chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
            return chain
            
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
            raise e