import streamlit as st
from src.pdf_handler import PDFHandler
from src.vector_db import VectorDB
from src.rag_chain import RAGChain

def process_documents(pdf_docs):
    """
    Orchestrates the entire document ingestion pipeline:
    Read PDF -> Split Text -> Create Vector Index
    """
    try:
        # 1. Get raw text from PDFs
        raw_text = PDFHandler.get_pdf_text(pdf_docs)
        
        # 2. Split text into manageable chunks
        text_chunks = PDFHandler.get_text_chunks(raw_text)
        
        # 3. Create and save the Vector Store
        VectorDB.create_vector_store(text_chunks)
        
        st.success("Documents processed successfully! You can now ask questions.")
        
    except Exception as e:
        st.error(f"Error processing documents: {e}")

def handle_user_input(user_question):
    """
    Handles the Q&A process:
    Load Index -> Search Context -> Ask Gemini -> Show Answer
    """
    try:
        # 1. Load the persisted vector store
        new_db = VectorDB.load_vector_store()
        
        # 2. Find the most relevant chunks (Context)
        # We search for the answer in our "index card" library
        docs = new_db.similarity_search(user_question)
        
        # 3. Get the Conversational Chain (The Brain)
        chain = RAGChain.get_conversational_chain()
        
        # 4. Generate the response
        response = chain(
            {"input_documents": docs, "question": user_question}, 
            return_only_outputs=True
        )
        
        # 5. Display the result
        st.write("Reply: ", response["output_text"])
        
    except Exception as e:
        st.error(f"Error generating response: {e}")

def main():
    # Setup the page configuration
    st.set_page_config(page_title="RAG Document Assistant", layout="wide")
    st.header("🤖 Chat with your PDFs using Gemini 2.5")

    # Sidebar for file upload
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button", 
            accept_multiple_files=True
        )
        
        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Processing..."):
                    process_documents(pdf_docs)

    # Main Chat Area
    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        handle_user_input(user_question)

if __name__ == "__main__":
    main()