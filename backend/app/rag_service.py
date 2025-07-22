import os
import uuid
import time
from typing import List, Dict, Any
from datetime import datetime
import logging

from app.vector_db import vector_db
from app.document_processor import document_processor
from app.openai_service import openai_service
from app.models import Document, DocumentChunk, QueryResponse, UploadResponse
from app.config import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.documents_metadata: Dict[str, Document] = {}

    async def upload_document(self, file_path: str, original_filename: str) -> UploadResponse:
        """Process and upload a document to the knowledge base"""
        try:
            # Determine file type
            file_type = original_filename.split('.')[-1].lower()
            file_size = os.path.getsize(file_path)
            
            # Process document
            document_id, chunks, metadatas = document_processor.process_document(
                file_path, original_filename, file_type
            )
            
            # Generate embeddings
            embeddings = await openai_service.generate_embeddings(chunks)
            
            # Create chunk IDs
            chunk_ids = [f"{document_id}_{i}" for i in range(len(chunks))]
            
            # Store in vector database
            # Note: ChromaDB handles embeddings automatically when using OpenAI
            success = vector_db.add_documents(chunks, metadatas, chunk_ids)
            
            if not success:
                raise Exception("Failed to store document in vector database")
            
            # Store document metadata
            document = Document(
                id=document_id,
                filename=original_filename,
                original_filename=original_filename,
                file_type=file_type,
                upload_date=datetime.now(),
                chunk_count=len(chunks),
                size_bytes=file_size
            )
            
            self.documents_metadata[document_id] = document
            
            logger.info(f"Successfully uploaded document: {original_filename}")
            
            return UploadResponse(
                document_id=document_id,
                filename=original_filename,
                chunk_count=len(chunks),
                message="Document uploaded and processed successfully"
            )
            
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            raise

    async def query_knowledge_base(
        self, 
        query: str, 
        max_chunks: int = None,
        conversation_history: List[dict] = None
    ) -> QueryResponse:
        """Query the knowledge base and generate response"""
        start_time = time.time()
        max_chunks = max_chunks or settings.MAX_RETRIEVAL_CHUNKS
        
        try:
            # Perform similarity search
            search_results = vector_db.similarity_search(
                query=query,
                n_results=max_chunks
            )
            
            # Extract results
            retrieved_chunks = []
            if search_results["documents"] and search_results["documents"][0]:
                for i, (doc_id, content, metadata) in enumerate(zip(
                    search_results["ids"][0],
                    search_results["documents"][0], 
                    search_results["metadatas"][0]
                )):
                    chunk = DocumentChunk(
                        id=doc_id,
                        document_id=metadata.get("document_id", "unknown"),
                        content=content,
                        metadata=metadata,
                        chunk_index=metadata.get("chunk_index", i)
                    )
                    retrieved_chunks.append(chunk)
            
            # Generate response using retrieved context
            if retrieved_chunks:
                context_texts = [chunk.content for chunk in retrieved_chunks]
                answer = await openai_service.generate_response(
                    query, context_texts, conversation_history
                )
            else:
                answer = "I couldn't find any relevant information in the knowledge base to answer your question. Please try rephrasing your query or upload relevant documents first."
            
            processing_time = time.time() - start_time
            
            return QueryResponse(
                query=query,
                answer=answer,
                sources=retrieved_chunks,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error querying knowledge base: {str(e)}")
            raise

    def list_documents(self) -> List[Document]:
        """List all uploaded documents"""
        return list(self.documents_metadata.values())

    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the knowledge base"""
        try:
            # Delete from vector database
            success = vector_db.delete_documents(document_id)
            
            # Remove from metadata
            if document_id in self.documents_metadata:
                del self.documents_metadata[document_id]
            
            logger.info(f"Deleted document: {document_id}")
            return success
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False

    def get_document_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        total_documents = len(self.documents_metadata)
        total_chunks = vector_db.get_document_count()
        
        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "document_types": list(set([doc.file_type for doc in self.documents_metadata.values()]))
        }

# Global instance
rag_service = RAGService()
