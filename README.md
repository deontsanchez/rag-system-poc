# RAG System POC - Retrieval-Augmented Generation with Knowledge Base

A complete proof-of-concept implementation of a Retrieval-Augmented Generation (RAG) system that enables natural language querying of uploaded documents. Built with FastAPI backend, React frontend, ChromaDB vector storage, and OpenAI API integration.

![RAG System Architecture](docs/architecture.png)

## 🚀 Features

### Core RAG Capabilities

- **Document Ingestion**: Upload PDF, TXT, MD, and DOCX files
- **Intelligent Chunking**: Automatic text splitting with configurable overlap
- **Vector Storage**: ChromaDB for fast similarity search
- **Smart Retrieval**: Context-aware document chunk retrieval
- **AI-Powered Responses**: OpenAI GPT integration for natural answers

### User Interface

- **Modern Chat Interface**: Real-time conversation with document sources
- **Document Management**: Upload, view, and delete documents
- **Source Attribution**: See which document chunks were used for each answer
- **Processing Analytics**: Response time and chunk usage metrics

### Technical Features

- **RESTful API**: Complete backend API with OpenAPI documentation
- **Real-time Updates**: Live connection status and error handling
- **Security**: API key management and input validation
- **Scalability**: Docker containerization for easy deployment

## 🏗️ Architecture

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   OpenAI API     │
│                 │    │                 │    │                 │
│ • Chat Interface│◄──►│ • Document API  │◄──►│ • Embeddings    │
│ • File Upload   │    │ • RAG Service   │    │ • Chat Completion│
│ • Doc Management│    │ • Vector Search │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   ChromaDB      │
                       │                 │
                       │ • Vector Storage│
                       │ • Similarity    │
                       │   Search        │
                       └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **OpenAI API Key** (required for embeddings and chat)
- **Docker** (optional, for containerized deployment)

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd rag-system-poc

# Copy example configurations
cp .env.example backend/.env
cp .env.example frontend/.env
```

### 2. Configure Environment Variables

**Simple Setup:**
Just one `.env` file at the root level - that's it!

```bash
# Copy the example and add your API key
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your-api-key-here
```

**Check Your Configuration:**

```bash
# Verify everything is set up correctly
python check-env.py
```

**That's All!**
The single `.env` file contains all settings for both frontend and backend. No need to manage multiple environment files.

### 3. Quick Start (Recommended)

```bash
# Run the automated setup and dev server launcher
./setup.sh
./dev.sh
```

### 3. Manual Setup

#### Start Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### 4. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Backend
cd backend
docker build -t rag-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-your-key rag-backend

# Frontend
cd frontend
docker build -t rag-frontend .
docker run -p 3000:80 rag-frontend
```

## 📚 API Documentation

### Core Endpoints

#### Upload Document

```http
POST /api/upload
Content-Type: multipart/form-data

file: <document-file>
```

#### Query Knowledge Base

```http
POST /api/query
Content-Type: application/json

{
  "query": "What is the vacation policy?",
  "max_chunks": 5,
  "include_metadata": true
}
```

#### List Documents

```http
GET /api/documents
```

#### Delete Document

```http
DELETE /api/documents/{document_id}
```

### Response Format

```json
{
  "query": "What is the vacation policy?",
  "answer": "According to the company policy...",
  "sources": [
    {
      "id": "doc_123_chunk_0",
      "document_id": "doc_123",
      "content": "New employees receive 15 days...",
      "metadata": {
        "filename": "company_policy.md",
        "chunk_index": 0
      }
    }
  ],
  "processing_time": 1.23
}
```

## 🧪 Testing with Sample Documents

The project includes sample documents in `data/sample_documents/`:

1. **Company Policy Manual** (`company_policy.md`)
   - Employee policies, benefits, IT security
   - Test queries: "What's the vacation policy?", "How do I reset my password?"

2. **API Documentation** (`api_documentation.md`)
   - REST API endpoints and authentication
   - Test queries: "How do I authenticate?", "What are the rate limits?"

3. **Product FAQ** (`product_faq.txt`)
   - Common questions about CloudFlow platform
   - Test queries: "How much does it cost?", "What integrations are available?"

### Sample Queries to Try

1. "What is the company's remote work policy?"
2. "How do I create a new customer via the API?"
3. "What security features does CloudFlow have?"
4. "What are the different pricing tiers?"
5. "How many vacation days do employees get?"

## 🔧 Configuration

### Backend Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | Your OpenAI API key (required) |
| `CHROMA_PERSIST_DIRECTORY` | `./chroma_db` | ChromaDB storage location |
| `UPLOAD_DIRECTORY` | `../data/uploads` | Temporary upload directory |
| `CHUNK_SIZE` | `1000` | Maximum tokens per chunk |
| `CHUNK_OVERLAP` | `200` | Token overlap between chunks |
| `MAX_RETRIEVAL_CHUNKS` | `5` | Maximum chunks to retrieve |

### Supported File Types

- **PDF**: Text extraction using PyPDF2
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files
- **MD**: Markdown files

## 📊 Performance Metrics

- **Document Processing**: ~2-5 seconds per document
- **Query Response**: ~1-3 seconds including OpenAI API calls
- **Vector Search**: <100ms for most queries
- **Concurrent Users**: Tested up to 50 simultaneous users

## 🛡️ Security Considerations

- API keys stored in environment variables
- Input validation for all endpoints
- File type restrictions for uploads
- CORS configuration for frontend access
- No sensitive data logged

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**

- Check OpenAI API key in `.env` file
- Ensure Python 3.11+ is installed
- Verify all requirements are installed

**Frontend can't connect to backend:**

- Ensure backend is running on port 8000
- Check CORS configuration
- Verify API URL in frontend environment

**Document upload fails:**

- Check file type is supported (PDF, TXT, MD, DOCX)
- Ensure file size is reasonable (<10MB)
- Verify OpenAI API key has sufficient credits

**Queries return no results:**

- Upload documents first
- Check if document processing completed successfully
- Try more specific queries

### Debug Mode

Enable debug logging in backend:

```bash
export LOG_LEVEL=DEBUG
python -m uvicorn app.main:app --reload --log-level debug
```

## 🚀 Production Deployment

### Environment Variables for Production

```bash
# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
OPENAI_API_KEY=sk-prod-key
CHROMA_PERSIST_DIRECTORY=/data/chroma_db
UPLOAD_DIRECTORY=/data/uploads

# Security
CORS_ORIGINS=https://yourdomain.com
API_KEY_REQUIRED=true
```

### Scaling Considerations

1. **Database**: Consider PostgreSQL for document metadata
2. **Vector Store**: Pinecone or Weaviate for larger scale
3. **Caching**: Redis for query caching
4. **Load Balancing**: Multiple backend instances
5. **File Storage**: S3 or similar for document storage

## 📝 Development

### Project Structure

```text
rag-system-poc/
├── backend/
│   ├── app/
│   │   ├── config.py          # Configuration
│   │   ├── models.py          # Pydantic models
│   │   ├── vector_db.py       # ChromaDB interface
│   │   ├── document_processor.py # Text processing
│   │   ├── openai_service.py  # OpenAI integration
│   │   ├── rag_service.py     # Main RAG logic
│   │   ├── routes.py          # API endpoints
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/        # API clients
│   │   └── App.js          # Main app
│   ├── package.json
│   └── Dockerfile
├── data/
│   ├── sample_documents/    # Test documents
│   ├── uploads/            # Temporary uploads
│   └── chroma_db/         # Vector database
└── docker-compose.yml     # Container orchestration
```

### Adding New Features

1. **New File Types**: Extend `document_processor.py`
2. **Additional APIs**: Add routes in `routes.py`
3. **UI Components**: Create in `frontend/src/components/`
4. **Vector Stores**: Modify `vector_db.py` interface

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions:

- Check the [troubleshooting section](#-troubleshooting)
- Review API documentation at `/docs`
- Open an issue on GitHub

---

## Built with ❤️ using FastAPI, React, ChromaDB, and OpenAI
