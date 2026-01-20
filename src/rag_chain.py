from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from config.settings import GOOGLE_API_KEY, LLM_MODEL, TEMPERATURE

class RAGChain:
    """
    Manages the RAG (Retrieval-Augmented Generation) chain setup.
    """

    @staticmethod
    def get_conversational_chain():
        """
        Creates a chain that connects the LLM with the prompt template.
        
        Returns:
            Chain: A LangChain object ready to process documents and questions.
        """
        # 1. Define the Prompt Template
        # This is the most critical part. We are giving the AI strict instructions:
        # "Only use the provided context. If you don't know, say you don't know."
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
            # We use the model name defined in settings.py (gemini-2.5-flash)
            model = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                temperature=TEMPERATURE,
                google_api_key=GOOGLE_API_KEY
            )

            # 3. Create the Prompt Object
            prompt = PromptTemplate(
                template=prompt_template, 
                input_variables=["context", "question"]
            )

            # 4. Load the Chain
            # 'chain_type="stuff"' means we "stuff" all the relevant text chunks 
            # into the prompt at once. It's simple and effective for this scale.
            chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
            return chain
            
        except Exception as e:
            print(f"Error initializing RAG chain: {e}")
            raise e