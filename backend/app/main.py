import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import router
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting RAG System POC...")
    logger.info(f"Chroma DB directory: {settings.CHROMA_PERSIST_DIRECTORY}")
    logger.info(f"Upload directory: {settings.UPLOAD_DIRECTORY}")
    yield
    # Shutdown
    logger.info("Shutting down RAG System POC...")

app = FastAPI(
    title="RAG System POC",
    description="A Retrieval-Augmented Generation system for document-based Q&A",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        content={
            "message": "RAG System POC API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health"
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception handler: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
