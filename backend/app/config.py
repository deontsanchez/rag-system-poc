import os
from dotenv import load_dotenv
import json

# Load environment variables from root .env file
load_dotenv(dotenv_path='../.env')

class Settings:
    # Environment
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALLOWED_HOSTS: list = json.loads(os.getenv("ALLOWED_HOSTS", '["localhost", "127.0.0.1"]'))
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Database Configuration
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    UPLOAD_DIRECTORY: str = os.getenv("UPLOAD_DIRECTORY", "../data/uploads")
    
    # Document Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    MAX_RETRIEVAL_CHUNKS: int = int(os.getenv("MAX_RETRIEVAL_CHUNKS", "5"))
    MAX_CHUNKS: int = int(os.getenv("MAX_CHUNKS", "10"))
    
    # AI/ML Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # CORS Configuration
    CORS_ORIGINS: list = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://127.0.0.1:3000"]'))
    
    # Telemetry
    ENABLE_TELEMETRY: bool = os.getenv("ENABLE_TELEMETRY", "false").lower() == "true"

settings = Settings()
