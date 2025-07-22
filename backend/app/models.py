from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    content: str
    metadata: Dict[str, Any]
    chunk_index: int

class Document(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_type: str
    upload_date: datetime
    chunk_count: int
    size_bytes: int

class QueryRequest(BaseModel):
    query: str
    max_chunks: Optional[int] = 5
    include_metadata: Optional[bool] = True

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[DocumentChunk]
    processing_time: float

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    message: str

class DocumentListResponse(BaseModel):
    documents: List[Document]
    total_count: int
