import streamlit as st
from streamlit_lottie import st_lottie
from src.pdf_handler import PDFHandler
from src.vector_db import VectorDB
from src.rag_chain import RAGChain
from src.ui_utils import UIUtils

# --- Configuration (Must be first) ---
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Assets ---
# Using a cleaner, more professional "Document Analysis" animation
LOTTIE_URL = "https://assets9.lottiefiles.com/packages/lf20_w51pcehl.json"
lottie_anim = UIUtils.load_lottie_url(LOTTIE_URL)

# Apply Light Mode CSS
st.markdown(UIUtils.get_custom_css(), unsafe_allow_html=True)

# --- Session State (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    # 1. Project Title (Updated as requested)
    st.markdown("## 🧠 Project Workspace")
    
    # 2. Animation
    if lottie_anim:
        st_lottie(lottie_anim, height=180, key="sidebar_anim")
    
    st.markdown("---")
    
    st.markdown("### 📂 Upload Documents")
    pdf_docs = st.file_uploader(
        "Select PDF files", 
        accept_multiple_files=True,
        type=['pdf']
    )
    
    if st.button("🚀 Process & Index"):
        if not pdf_docs:
            st.warning("⚠️ Please upload a PDF first.")
        else:
            with st.spinner("Processing documents..."):
                try:
                    raw_text = PDFHandler.get_pdf_text(pdf_docs)
                    text_chunks = PDFHandler.get_text_chunks(raw_text)
                    VectorDB.create_vector_store(text_chunks)
                    st.sidebar.success("✅ Indexing Complete!")
                except Exception as e:
                    st.sidebar.error(f"Error: {e}")

    st.markdown("---")
    # Clear Chat is now a secondary action (visually distinct)
    if st.button("🗑️ Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- Main Area ---
st.title("RAG Document Assistant")
st.markdown("""
<div style='text-align: center; color: #666; margin-bottom: 30px;'>
    Upload your research papers or contracts and chat with them instantly.
</div>
""", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # 1. Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
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
                
                # 3. Add bot message
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"System Error: {e}")