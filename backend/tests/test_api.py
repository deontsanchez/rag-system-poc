import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_stats_endpoint():
    """Test the stats endpoint"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_documents" in data
    assert "total_chunks" in data
    assert "document_types" in data

def test_list_documents():
    """Test listing documents"""
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert "total_count" in data

def test_query_without_documents():
    """Test querying with no documents uploaded"""
    response = client.post("/api/query", json={
        "query": "What is the company policy?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) == 0

def test_query_empty_string():
    """Test querying with empty string"""
    response = client.post("/api/query", json={
        "query": ""
    })
    assert response.status_code == 400

def test_upload_invalid_file_type():
    """Test uploading an unsupported file type"""
    # This would need a mock file for a complete test
    pass

# Note: Full integration tests would require OpenAI API key
# and actual file uploads, which should be in a separate test suite
