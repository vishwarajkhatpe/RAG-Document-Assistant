import streamlit as st
import time
from datetime import datetime
from streamlit_option_menu import option_menu
from langchain.chains import RetrievalQA
from src.pdf_handler import PDFHandler
from src.vector_db import VectorDB
from src.rag_chain import RAGChain
from src.ui_utils import UIUtils
from dotenv import load_dotenv

# --- CONFIG ---
st.set_page_config(page_title="DocuMind", page_icon="🧠", layout="wide")
st.markdown(UIUtils.get_clean_style(), unsafe_allow_html=True)
load_dotenv()

# --- STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "vector_store" not in st.session_state: st.session_state.vector_store = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo-title">
            <span style="font-size: 1.5rem;">📂</span>
            <div class="sidebar-title">DocuMind</div>
        </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Home", "Workspace"],
        icons=["house", "layers"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#64748b", "font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px", "color": "#334155"},
            "nav-link-selected": {
                "background-color": "#e6f7f5", 
                "color": "#00b09b",
                "border-left": "4px solid #00b09b",
                "font-weight": "600"
            },
        }
    )

    st.markdown("---")

    # --- WORKSPACE LOGIC (Where pdf_docs is defined) ---
    if selected == "Workspace":
        st.markdown("### 📂 Upload Document")
        
        # 1. DEFINE THE VARIABLE HERE
        pdf_docs = st.file_uploader("Choose PDF", accept_multiple_files=True, type=['pdf'], label_visibility="collapsed")
        
        # 2. USE IT HERE (Must be indented inside the same block)
        if st.button("Process Document", use_container_width=True):
            if not pdf_docs:
                st.toast("⚠️ No file selected.")
            else:
                try:
                    with st.status("Initializing System...", expanded=True) as status:
                        
                        status.write("📂 Reading & Chunking PDF (Page by Page)...")
                        # This calls the new function we created
                        chunked_documents = PDFHandler.get_chunked_documents(pdf_docs)
                        
                        status.write(f"✂️ Generated {len(chunked_documents)} chunks with metadata...")
                        
                        status.write("🧠 Generating Vector Embeddings...")
                        # This passes the documents to the vector DB
                        st.session_state.vector_store = VectorDB.create_vector_store(chunked_documents)
                        
                        status.update(label="System Ready!", state="complete", expanded=False)
                        
                    st.toast("Document Ready!", icon="✅")
                    
                except Exception as e:
                    st.error("Processing Failed.")
                    st.error(f"Error: {e}")

        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown(f"""
        <div class="sidebar-footer" style="position: fixed; bottom: 0; padding: 20px; color: #64748b; font-size: 0.8rem;">
            <span>Developed by <b>Vishwaraj Khatpe</b></span>
        </div>
    """, unsafe_allow_html=True)

# --- PAGE 1: HOME ---
if selected == "Home":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">DocuMind AI</div>
            <div class="hero-subtitle">The intelligent engine for modern document analysis. Generate insights in seconds.</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(UIUtils.render_home_card("🔒", "Local Privacy", "Data processed locally on your machine. No cloud uploads."), unsafe_allow_html=True)
    with col2: st.markdown(UIUtils.render_home_card("⚡", "Instant Speed", "Vectors are stored in RAM for zero-latency retrieval."), unsafe_allow_html=True)
    with col3: st.markdown(UIUtils.render_home_card("💬", "Smart Chat", "Context-aware AI that understands your documents."), unsafe_allow_html=True)
    
# --- PAGE 2: WORKSPACE ---
elif selected == "Workspace":
    st.markdown("""
        <div style="font-size: 2.2rem; font-weight: 700; color: #1e293b; margin-bottom: 25px; 
        padding-bottom: 10px; border-bottom: 3px solid #00b09b; display: inline-block;">
            Document Analysis
        </div>
    """, unsafe_allow_html=True)

    # 1. Render History
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            st.markdown(UIUtils.render_message(message["role"], message["content"]), unsafe_allow_html=True)
            
            if "sources" in message:
                with st.expander("📚 View Verified Sources"):
                    for source in message["sources"]:
                        st.markdown(UIUtils.render_source(source['page'], source['text']), unsafe_allow_html=True)

    # 2. Handle Input
    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(UIUtils.render_message("user", prompt), unsafe_allow_html=True)

        if not st.session_state.vector_store:
            st.warning("⚠️ Please upload a PDF first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    # Initialize Chain
                    model, prompt_template = RAGChain.get_conversational_chain()
                    
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=model,
                        chain_type="stuff",
                        retriever=st.session_state.vector_store.as_retriever(),
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": prompt_template}
                    )
                    
                    # Get Response
                    response = qa_chain.invoke({"query": prompt})
                    answer = response["result"]
                    source_docs = response["source_documents"]
                    
                    # Process Sources
                    formatted_sources = []
                    for doc in source_docs:
                        # Extract Page Number (default to 1 if missing)
                        page = doc.metadata.get("page", 0)
                        # Extract Text Snippet (First 100 chars)
                        text = doc.page_content[:100].replace("\n", " ")
                        formatted_sources.append({"page": page, "text": text})
                    
                    # Save to State
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": formatted_sources
                    })
                    
                    # Render AI Response
                    st.markdown(UIUtils.render_message("assistant", answer), unsafe_allow_html=True)
                    
                    # Render New Citations
                    with st.expander("📚 View Verified Sources", expanded=True):
                        for src in formatted_sources:
                            st.markdown(UIUtils.render_source(src['page'], src['text']), unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"Error: {e}")