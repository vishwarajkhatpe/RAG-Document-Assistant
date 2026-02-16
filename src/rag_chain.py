import os
import textwrap
from typing import Tuple
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load environment variables at the module level
load_dotenv()

class RAGChain:
    """
    Configuration factory for the Retrieval-Augmented Generation (RAG) pipeline.
    
    This class centralizes the LLM and Prompt settings to ensure consistency
    across the application. It enforces strict enterprise-grade constraints
    to minimize hallucinations.
    """
    
    @staticmethod
    def get_conversational_chain() -> Tuple[ChatGoogleGenerativeAI, PromptTemplate]:
        """
        Constructs the LLM and Prompt Template for the RAG chain.

        Returns:
            Tuple[ChatGoogleGenerativeAI, PromptTemplate]: Configured model and prompt objects.
        
        Raises:
            ValueError: If GOOGLE_API_KEY is not found in environment variables.
        """
        
        # 1. Security Check
        # Fail fast if the API key is missing to avoid cryptic errors downstream.
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Fatal: GOOGLE_API_KEY not found. Please check your .env file.")

        # 2. Enterprise Prompt Engineering
        # We use strict instructions to force the model to rely ONLY on the context.
        # 'dedent' removes the code indentation so the prompt is clean when sent to the API.
        raw_prompt = textwrap.dedent("""
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
        """)

        prompt_template = PromptTemplate(
            template=raw_prompt, 
            input_variables=["context", "question"]
        )

        # 3. Model Configuration
        # Temperature 0.1: Extremely deterministic (Low creativity, High factual accuracy).
        # max_retries=2: Handles transient network glitches automatically.
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.1,
            max_retries=2,
            transport="rest",
            google_api_key=api_key
        )

        return model, prompt_template