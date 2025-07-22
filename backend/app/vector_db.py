import chromadb
from chromadb.config import Settings as ChromaSettings
import uuid
from typing import List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorDatabase:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self, 
        chunks: List[str], 
        metadatas: List[Dict[str, Any]], 
        ids: List[str]
    ) -> bool:
        """Add document chunks to the vector database"""
        try:
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(chunks)} chunks to vector database")
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return False

    def similarity_search(
        self, 
        query: str, 
        n_results: int = 5,
        where: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Perform similarity search"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

    def delete_documents(self, document_id: str) -> bool:
        """Delete all chunks for a specific document"""
        try:
            # Get all chunks for this document
            results = self.collection.get(
                where={"document_id": document_id}
            )
            
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error deleting document chunks: {str(e)}")
            return False

    def get_document_count(self) -> int:
        """Get total number of documents in the database"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}")
            return 0

    def list_documents(self) -> List[str]:
        """List all unique document IDs"""
        try:
            results = self.collection.get()
            document_ids = set()
            for metadata in results.get("metadatas", []):
                if metadata and "document_id" in metadata:
                    document_ids.add(metadata["document_id"])
            return list(document_ids)
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return []

# Global instance
vector_db = VectorDatabase()
