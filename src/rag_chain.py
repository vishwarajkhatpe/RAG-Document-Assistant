import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class RAGChain:
    @staticmethod
    def get_conversational_chain():
        """
        Initializes the RAG chain with a specific prompt template.
        Returns the chain object that can be invoked with a query.
        """
        # 1. Define the Prompt Template
        prompt_template = """
        Answer the question as detailed as possible from the provided context. 
        If the answer is not in the provided context, just say, "answer is not available in the context", 
        don't provide the wrong answer.

        Context:
        {context}

        Question: 
        {question}

        Answer:
        """

        prompt = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )

        # 2. Initialize Gemini Pro (The Brain)
        # temperature=0.3 means "be creative but stick to facts"
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

        # 3. Return the configuration
        # This is just the LLM + Prompt configuration. 
        # The actual 'chain' is built dynamically in app.py when we have the vector_store.
        return model, prompt