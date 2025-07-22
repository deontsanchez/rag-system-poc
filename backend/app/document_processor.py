import os
import uuid
from typing import List, Dict, Any, Tuple
from datetime import datetime
import PyPDF2
import docx
import tiktoken
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))

    def extract_text_from_file(self, file_path: str, file_type: str) -> str:
        """Extract text from various file types"""
        try:
            if file_type.lower() == 'pdf':
                return self._extract_from_pdf(file_path)
            elif file_type.lower() in ['docx', 'doc']:
                return self._extract_from_docx(file_path)
            elif file_type.lower() in ['txt', 'md']:
                return self._extract_from_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _extract_from_text(self, file_path: str) -> str:
        """Extract text from text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def chunk_text(
        self, 
        text: str, 
        chunk_size: int = None, 
        overlap: int = None
    ) -> List[str]:
        """Split text into overlapping chunks"""
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = overlap or settings.CHUNK_OVERLAP
        
        # Split by sentences first, then by tokens
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Add sentence to current chunk
            test_chunk = current_chunk + sentence + ". "
            
            # Check if adding this sentence would exceed chunk size
            if self.count_tokens(test_chunk) > chunk_size and current_chunk:
                # Save current chunk and start new one with overlap
                chunks.append(current_chunk.strip())
                
                # Create overlap by taking last few sentences
                overlap_text = self._create_overlap(current_chunk, overlap)
                current_chunk = overlap_text + sentence + ". "
            else:
                current_chunk = test_chunk
        
        # Add the final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks

    def _create_overlap(self, text: str, overlap_tokens: int) -> str:
        """Create overlap text with approximately overlap_tokens"""
        sentences = text.strip().split('. ')
        overlap_text = ""
        
        # Work backwards through sentences
        for sentence in reversed(sentences):
            test_overlap = sentence + ". " + overlap_text
            if self.count_tokens(test_overlap) > overlap_tokens:
                break
            overlap_text = test_overlap
        
        return overlap_text

    def process_document(
        self, 
        file_path: str, 
        filename: str, 
        file_type: str
    ) -> Tuple[str, List[str], List[Dict[str, Any]]]:
        """Process a document: extract text, chunk it, and create metadata"""
        document_id = str(uuid.uuid4())
        
        # Extract text
        text = self.extract_text_from_file(file_path, file_type)
        
        # Chunk text
        chunks = self.chunk_text(text)
        
        # Create metadata for each chunk
        metadatas = []
        for i, chunk in enumerate(chunks):
            metadata = {
                "document_id": document_id,
                "filename": filename,
                "file_type": file_type,
                "chunk_index": i,
                "chunk_count": len(chunks),
                "upload_date": datetime.now().isoformat(),
                "token_count": self.count_tokens(chunk)
            }
            metadatas.append(metadata)
        
        logger.info(f"Processed document {filename}: {len(chunks)} chunks")
        return document_id, chunks, metadatas

# Global instance
document_processor = DocumentProcessor()
