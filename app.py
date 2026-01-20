import streamlit as st
from streamlit_lottie import st_lottie
from src.pdf_handler import PDFHandler
from src.vector_db import VectorDB
from src.rag_chain import RAGChain
from src.ui_utils import UIUtils

# --- Configuration ---
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Load Assets ---
# URL for a free "Robot/AI" animation from LottieFiles
LOTTIE_URL = "https://assets5.lottiefiles.com/packages/lf20_1i1i1i.json" 
lottie_anim = UIUtils.load_lottie_url(LOTTIE_URL)

# Apply Custom CSS
st.markdown(UIUtils.get_custom_css(), unsafe_allow_html=True)

# --- Session State (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    # Show Animation
    if lottie_anim:
        st_lottie(lottie_anim, height=200, key="sidebar_anim")
    
    st.title("📂 Document Hub")
    st.markdown("---")
    
    pdf_docs = st.file_uploader(
        "Upload your PDFs here", 
        accept_multiple_files=True,
        type=['pdf']
    )
    
    if st.button("🚀 Process Documents"):
        if not pdf_docs:
            st.warning("⚠️ Please upload a PDF first.")
        else:
            with st.spinner("⚙️ Reading & Indexing..."):
                try:
                    # Pipeline Logic
                    raw_text = PDFHandler.get_pdf_text(pdf_docs)
                    text_chunks = PDFHandler.get_text_chunks(raw_text)
                    VectorDB.create_vector_store(text_chunks)
                    st.success("✅ Ready to Chat!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Main Area ---
st.title("🤖 Intelligent Document Assistant")
st.markdown("*Ask questions about your documents in real-time.*")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question..."):
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                new_db = VectorDB.load_vector_store()
                docs = new_db.similarity_search(prompt)
                chain = RAGChain.get_conversational_chain()
                
                response = chain(
                    {"input_documents": docs, "question": prompt}, 
                    return_only_outputs=True
                )
                
                response_text = response["output_text"]
                st.markdown(response_text)
                
                # 3. Add bot message to history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Error: {e}")