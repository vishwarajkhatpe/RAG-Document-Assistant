import logging
from typing import List, Any
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Initialize a module-specific logger.
# This ensures our logs are tagged with 'src.pdf_handler' for easier debugging.
logger = logging.getLogger(__name__)

class PDFHandler:
    """
    Handles the ingestion, parsing, and chunking of PDF documents.
    
    Design Philosophy:
    - Fault Tolerant: A single corrupt page should not crash the entire ingestion pipeline.
    - Traceable: Every chunk maintains a link to its original source and page number.
    """

    # Configuration: Tuned for technical documents and standard RAG contexts.
    # 1000 chars is approx 200-250 words, suitable for 'embedding-004' or 'all-MiniLM'.
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    SEPARATORS = ["\n\n", "\n", " ", ""]

    @staticmethod
    def get_chunked_documents(pdf_docs: List[Any]) -> List[Document]:
        """
        Robustly processes a stream of PDF files into semantic text chunks.

        Args:
            pdf_docs: List of file-like objects (typically from st.file_uploader).

        Returns:
            List[Document]: Flattened list of chunked documents with metadata.
        """
        all_chunks = []
        
        # Initialize splitter once for efficiency.
        # We use RecursiveCharacterTextSplitter to respect sentence boundaries.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=PDFHandler.CHUNK_SIZE,
            chunk_overlap=PDFHandler.CHUNK_OVERLAP,
            separators=PDFHandler.SEPARATORS
        )

        logger.info(f"Starting ingestion for {len(pdf_docs)} file(s)...")

        for pdf in pdf_docs:
            try:
                # file_name is useful for logging context
                file_name = getattr(pdf, "name", "unknown_file.pdf")
                
                # strict=False allows pypdf to handle slightly malformed PDFs (common in enterprise)
                pdf_reader = PdfReader(pdf, strict=False)
                
                logger.info(f"Processing '{file_name}' with {len(pdf_reader.pages)} pages.")

                for i, page in enumerate(pdf_reader.pages):
                    try:
                        # Extract raw text
                        content = page.extract_text()
                        
                        # Data Hygiene: Skip empty pages or pages with only whitespace (scanned images)
                        if not content or not content.strip():
                            logger.debug(f"Skipping empty page {i+1} in {file_name}")
                            continue

                        # Metadata Injection: This is critical for the 'Citation' feature in the UI.
                        # We attach the page number to the document *before* chunking.
                        raw_doc = Document(
                            page_content=content,
                            metadata={
                                "source": file_name,
                                "page": i + 1  # User-facing page numbers are 1-indexed
                            }
                        )
                        
                        # Split the page content into chunks
                        # Note: We split *per page* to ensure a chunk never spans across two pages,
                        # which would make citation logic ambiguous.
                        page_chunks = text_splitter.split_documents([raw_doc])
                        all_chunks.extend(page_chunks)
                        
                    except Exception as e:
                        # Isolate page-level failures so the rest of the document is still processed
                        logger.warning(f"Failed to process page {i+1} in {file_name}. Reason: {e}")
                        continue
                        
            except Exception as e:
                # Isolate file-level failures so other files in the batch are still processed
                logger.error(f"Critical failure reading file {getattr(pdf, 'name', 'unknown')}. Reason: {e}")
                continue
                
        logger.info(f"Ingestion complete. Generated {len(all_chunks)} total chunks.")
        return all_chunks