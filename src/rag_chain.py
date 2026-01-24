import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class RAGChain:
    @staticmethod
    def get_conversational_chain():
        """
        Returns a strict, enterprise-grade RAG chain configuration.
        """
        # Enterprise Prompt: Strict, Professional, Concise.
        prompt_template = """
        You are an expert Document Analyst for a corporate enterprise.
        Your task is to answer the user's question STRICTLY based on the provided Context.

        Rules:
        1. If the answer is not in the Context, respond EXACTLY: "I cannot find the answer in the provided documents."
        2. Do not hallucinate or use outside knowledge.
        3. Keep your answer professional, concise, and formatted (use bullet points if needed).
        4. Cite the page number if mentioned in the text.

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

        # Optimization: Temperature 0.1 for high determinism (Fact-focused)
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.1,
            max_retries=2,
            transport="rest"
        )

        return model, prompt