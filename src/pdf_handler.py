from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class PDFHandler:
    @staticmethod
    def get_chunked_documents(pdf_docs):
        """
        Processes PDFs page-by-page to preserve page numbers.
        Returns a list of Document objects with metadata.
        """
        all_chunks = []
        
        # 1. Define the Splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        # 2. Loop through every uploaded file
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            
            # 3. Loop through every page in the file
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text:
                    # Create a "Document" object for this page
                    # We store the page number (i+1) in the metadata
                    page_doc = Document(
                        page_content=text, 
                        metadata={"page": i + 1}
                    )
                    
                    # Split this specific page into chunks
                    page_chunks = text_splitter.split_documents([page_doc])
                    all_chunks.extend(page_chunks)
                    
        return all_chunks