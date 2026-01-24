from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFHandler:
    @staticmethod
    def get_pdf_text(pdf_docs):
        """
        Loops through uploaded PDF files and extracts raw text.
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
        Splits the raw text into manageable chunks for vectorization.
        We use a chunk_size of 1000 with 200 overlap to maintain context.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(text)
        return chunks