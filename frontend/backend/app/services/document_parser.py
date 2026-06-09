import PyPDF2
from docx import Document
import io
from typing import Union

class DocumentParser:
    @staticmethod
    async def parse_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    async def parse_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")
    
    @staticmethod
    async def parse_txt(file_bytes: bytes) -> str:
        """Extract text from TXT file"""
        try:
            return file_bytes.decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to parse TXT: {str(e)}")
    
    @staticmethod
    async def parse_file(file_bytes: bytes, file_type: str) -> str:
        """Route file to appropriate parser"""
        if file_type == "application/pdf":
            return await DocumentParser.parse_pdf(file_bytes)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return await DocumentParser.parse_docx(file_bytes)
        elif file_type == "text/plain":
            return await DocumentParser.parse_txt(file_bytes)
        else:
            raise Exception(f"Unsupported file type: {file_type}")