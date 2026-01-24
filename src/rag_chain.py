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
        Initializes the RAG chain using the user-confirmed 'gemini-2.5-flash' model.
        """
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

        # FIX: Using the model you confirmed works: 'gemini-2.5-flash'
        # FIX: Keeping transport="rest" to prevent the 'buffering forever' issue
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.3,
            max_retries=1,
            transport="rest"
        )

        return model, prompt