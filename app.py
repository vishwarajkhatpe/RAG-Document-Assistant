import streamlit as st
import gc
from streamlit_option_menu import option_menu
from langchain.chains import RetrievalQA
from src.pdf_handler import PDFHandler
from src.vector_db import VectorDB
from src.rag_chain import RAGChain
from src.ui_utils import UIUtils
from dotenv import load_dotenv
import os

# --- STYLE OVERRIDE (Changes Color without touching ui_utils.py) ---
def get_override_style():
    return """
    <style>
        /* Override Hero Banner to Royal Indigo */
        .hero-banner {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        }
        
        /* Override Buttons */
        .stButton > button {
            background: linear-gradient(to right, #4f46e5, #7c3aed) !important;
            border: none;
        }
        .stButton > button:hover {
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4) !important;
        }

        /* Override Citation Borders */
        .source-container {
            border-left: 3px solid #4f46e5 !important;
        }
        .source-header {
            color: #4f46e5 !important;
        }
        
        /* Override User Chat Bubble (Light Indigo) */
        .user-bubble {
            background-color: #e0e7ff !important;
            color: #3730a3 !important;
        }
        
        /* Override Workspace Header Underline */
        div[style*="border-bottom: 3px solid #00b09b"] {
            border-bottom: 3px solid #4f46e5 !important;
        }
    </style>
    """

# --- CONFIG ---
st.set_page_config(page_title="RAG Document Assistant", page_icon="🤖", layout="wide")

# 1. Load the original structure (Layout)
st.markdown(UIUtils.get_clean_style(), unsafe_allow_html=True)

# 2. Inject the new Colors (Theme)
st.markdown(get_override_style(), unsafe_allow_html=True)

load_dotenv()

# --- VALIDATION ---
if not os.getenv("GOOGLE_API_KEY"):
    st.error("🚨 Critical Error: GOOGLE_API_KEY not found. Please configure your .env file.")
    st.stop()

# --- STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "vector_store" not in st.session_state: st.session_state.vector_store = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo-title">
            <span style="font-size: 1.5rem;">🤖</span>
            <div class="sidebar-title">RAG Assistant</div>
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
            # CHANGED: Selected color to Indigo/Blue
            "nav-link-selected": {
                "background-color": "#e0e7ff", 
                "color": "#4f46e5",
                "border-left": "4px solid #4f46e5",
                "font-weight": "600"
            },
        }
    )
    st.markdown("---")

    if selected == "Workspace":
        st.markdown("### 📂 Upload Document")
        
        pdf_docs = st.file_uploader(
            "Choose PDF", 
            accept_multiple_files=True, 
            type=['pdf'], 
            label_visibility="collapsed"
        )
        
        if st.button("Process Document", use_container_width=True):
            if not pdf_docs:
                st.toast("⚠️ No file selected. Please upload a PDF.")
            else:
                try:
                    with st.status("🚀 Initializing Engine...", expanded=True) as status:
                        
                        status.write("📂 Extracting Text & Metadata...")
                        chunked_documents = PDFHandler.get_chunked_documents(pdf_docs)
                        
                        if not chunked_documents:
                            status.update(label="Error: No text found in PDF.", state="error")
                            st.stop()

                        status.write(f"✂️ Optimized {len(chunked_documents)} chunks...")
                        
                        status.write("🧠 Hydrating Vector Database...")
                        st.session_state.vector_store = VectorDB.create_vector_store(chunked_documents)
                        
                        # Memory Optimization
                        del chunked_documents
                        gc.collect()
                        
                        status.update(label="System Ready!", state="complete", expanded=False)
                        
                    st.toast("Knowledge Base Updated!", icon="✅")
                    
                except Exception as e:
                    st.error(f"Processing Error: {str(e)}")

        if st.button("Clear Session", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # UPDATED FOOTER WITH SIGNATURE
    st.markdown(f"""
        <div class="sidebar-footer" style="position: fixed; bottom: 0; padding: 20px; color: #64748b; font-size: 0.8rem;">
            <span>v1.0 <b></b> Developed by <b>Vishwaraj Khatpe</b></span>
        </div>
    """, unsafe_allow_html=True)

# --- PAGE 1: HOME ---
if selected == "Home":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">RAG Document Assistant</div>
            <div class="hero-subtitle">Enterprise-grade document intelligence. Secure. Fast. Accurate.</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(UIUtils.render_home_card("🔒", "Secure Core", "Local embeddings ensure data sovereignty. Zero data leakage."), unsafe_allow_html=True)
    with col2: st.markdown(UIUtils.render_home_card("⚡", "High Velocity", "In-memory FAISS indexing for millisecond retrieval times."), unsafe_allow_html=True)
    with col3: st.markdown(UIUtils.render_home_card("🎯", "Precision RAG", "Strict context windowing prevents AI hallucinations."), unsafe_allow_html=True)
    
# --- PAGE 2: WORKSPACE ---
elif selected == "Workspace":
    # Header with new Blue underline color (handled by CSS override)
    st.markdown("""
        <div style="font-size: 2.2rem; font-weight: 700; color: #1e293b; margin-bottom: 25px; 
        padding-bottom: 10px; border-bottom: 3px solid #00b09b; display: inline-block;">
            Analyst Workspace
        </div>
    """, unsafe_allow_html=True)

    # 1. Render History
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            st.markdown(UIUtils.render_message(message["role"], message["content"]), unsafe_allow_html=True)
            
            if "sources" in message:
                with st.expander("🔍 View Verified Citations"):
                    for source in message["sources"]:
                        st.markdown(UIUtils.render_source(source['page'], source['text']), unsafe_allow_html=True)

    # 2. Handle Input
    if prompt := st.chat_input("Query the knowledge base..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(UIUtils.render_message("user", prompt), unsafe_allow_html=True)

        if not st.session_state.vector_store:
            st.warning("⚠️ Knowledge Base Empty. Please upload and process a document first.")
        else:
            with st.spinner("Analyzing documents..."):
                try:
                    # Initialize Chain
                    model, prompt_template = RAGChain.get_conversational_chain()
                    
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=model,
                        chain_type="stuff",
                        retriever=st.session_state.vector_store.as_retriever(search_kwargs={"k": 3}),
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": prompt_template}
                    )
                    
                    # Execute
                    response = qa_chain.invoke({"query": prompt})
                    answer = response["result"]
                    source_docs = response["source_documents"]
                    
                    # Formatter
                    formatted_sources = []
                    for doc in source_docs:
                        page = doc.metadata.get("page", "Unknown")
                        source_file = doc.metadata.get("source", "Doc")
                        text = doc.page_content[:150].replace("\n", " ") + "..."
                        formatted_sources.append({"page": f"{page} ({source_file})", "text": text})
                    
                    # State Update
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": formatted_sources
                    })
                    
                    # Render
                    st.markdown(UIUtils.render_message("assistant", answer), unsafe_allow_html=True)
                    
                    with st.expander("🔍 View Verified Citations", expanded=True):
                        for src in formatted_sources:
                            st.markdown(UIUtils.render_source(src['page'], src['text']), unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error("Analysis Failed.")
                    st.error(f"Debug Info: {e}")