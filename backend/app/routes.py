import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models import QueryRequest, QueryResponse, DocumentListResponse, UploadResponse
from app.rag_service import rag_service
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_extensions = ['pdf', 'txt', 'md', 'docx']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"File type '{file_extension}' not supported. Allowed types: {allowed_extensions}"
            )
        
        # Save uploaded file
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        result = await rag_service.upload_document(file_path, file.filename)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return result
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the knowledge base"""
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        result = await rag_service.query_knowledge_base(
            query=request.query,
            max_chunks=request.max_chunks
        )
        return result
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """List all uploaded documents"""
    try:
        documents = rag_service.list_documents()
        return DocumentListResponse(
            documents=documents,
            total_count=len(documents)
        )
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document from the knowledge base"""
    try:
        success = rag_service.delete_document(document_id)
        if success:
            return JSONResponse(
                status_code=200,
                content={"message": "Document deleted successfully"}
            )
        else:
            raise HTTPException(status_code=404, detail="Document not found")
            
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """Get knowledge base statistics"""
    try:
        stats = rag_service.get_document_stats()
        return JSONResponse(content=stats)
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy", "service": "RAG System POC"})

@router.get("/version")
async def get_version():
    """Get API version"""
    return JSONResponse(content={"version": "1.0.0", "api": "RAG System POC"})
