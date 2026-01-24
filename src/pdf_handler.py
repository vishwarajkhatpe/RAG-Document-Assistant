from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import logging

# Configure logging for enterprise auditing
logging.basicConfig(level=logging.INFO)

class PDFHandler:
    @staticmethod
    def get_chunked_documents(pdf_docs: List) -> List[Document]:
        """
        Robustly processes PDFs page-by-page.
        Skips corrupt pages and logs errors instead of crashing.
        """
        all_chunks = []
        
        # Optimized splitter: standard chunk size for technical docs
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""] # improved splitting logic
        )

        for pdf in pdf_docs:
            try:
                pdf_reader = PdfReader(pdf)
                
                for i, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        
                        # Optimization: Skip empty or whitespace-only pages
                        if not text or not text.strip():
                            continue
                            
                        # Metadata injection for citation accuracy
                        page_doc = Document(
                            page_content=text, 
                            metadata={"page": i + 1, "source": pdf.name}
                        )
                        
                        page_chunks = text_splitter.split_documents([page_doc])
                        all_chunks.extend(page_chunks)
                        
                    except Exception as e:
                        logging.warning(f"Skipping page {i+1} in {pdf.name} due to error: {e}")
                        continue
                        
            except Exception as e:
                logging.error(f"Failed to read file {pdf.name}: {e}")
                continue
                    
        return all_chunks