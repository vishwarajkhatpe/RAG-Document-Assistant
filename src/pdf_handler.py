from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class PDFHandler:
    """
    Handles processing of PDF files: extracting text and chunking it.
    """

    @staticmethod
    def get_pdf_text(pdf_docs):
        """
        Reads a list of PDF files and extracts all text from them.
        
        Args:
            pdf_docs: List of uploaded PDF files from Streamlit.
            
        Returns:
            str: A single string containing all the text from all PDFs.
        """
        text = ""
        # Loop through each PDF file uploaded
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            # Loop through each page in the PDF
            for page in pdf_reader.pages:
                # Extract text and append it to our variable
                text += page.extract_text()
        return text

    @staticmethod
    def get_text_chunks(text):
        """
        Splits the raw text into smaller, manageable chunks.
        
        Args:
            text (str): The raw text extracted from PDFs.
            
        Returns:
            list: A list of text chunks.
        """
        # We use RecursiveCharacterTextSplitter because it tries to split 
        # at logical places (paragraphs, newlines) rather than mid-word.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        
        # Perform the split
        chunks = text_splitter.split_text(text)
        return chunks