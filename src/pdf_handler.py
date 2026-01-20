from PyPDF2 import PdfReader
# UPDATED IMPORT: We now import from 'langchain_text_splitters' instead of 'langchain.text_splitter'
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class PDFHandler:
    """
    Handles processing of PDF files: extracting text and chunking it.
    """

    @staticmethod
    def get_pdf_text(pdf_docs):
        """
        Reads a list of PDF files and extracts all text from them.
        """
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def get_text_chunks(text):
        """
        Splits the raw text into smaller, manageable chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks