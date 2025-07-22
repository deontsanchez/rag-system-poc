import React, { useState, useEffect } from 'react';
import { Upload, File, Trash2, RefreshCw, FileText, AlertCircle } from 'lucide-react';
import { apiService } from '../services/api';

const DocumentManager = () => {
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  useEffect(() => {
    loadDocuments();
    loadStats();
  }, []);

  const loadDocuments = async () => {
    setIsLoading(true);
    try {
      const response = await apiService.listDocuments();
      setDocuments(response.documents);
    } catch (error) {
      console.error('Error loading documents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await apiService.getStats();
      setStats(statsData);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsUploading(true);
    setUploadError(null);

    try {
      const response = await apiService.uploadDocument(file);
      console.log('Upload successful:', response);
      await loadDocuments();
      await loadStats();
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setUploadError(errorMessage);
      console.error('Error uploading document:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileUpload(files[0]);
    }
  };

  const handleDeleteDocument = async (documentId, filename) => {
    if (!window.confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }

    try {
      await apiService.deleteDocument(documentId);
      await loadDocuments();
      await loadStats();
    } catch (error) {
      console.error('Error deleting document:', error);
      alert('Error deleting document. Please try again.');
    }
  };

  const getFileIcon = (fileType) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return <FileText className="h-5 w-5 text-red-500" />;
      case 'docx':
      case 'doc':
        return <FileText className="h-5 w-5 text-blue-500" />;
      default:
        return <File className="h-5 w-5 text-gray-500" />;
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Knowledge Base</h2>
          <button
            onClick={() => {
              loadDocuments();
              loadStats();
            }}
            className="text-gray-500 hover:text-gray-700 p-1"
            disabled={isLoading}
          >
            <RefreshCw className={`h-5 w-5 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="text-blue-700 text-sm font-medium">Documents</div>
              <div className="text-blue-900 text-xl font-bold">{stats.total_documents}</div>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <div className="text-green-700 text-sm font-medium">Chunks</div>
              <div className="text-green-900 text-xl font-bold">{stats.total_chunks}</div>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <div className="text-purple-700 text-sm font-medium">Types</div>
              <div className="text-purple-900 text-sm">
                {stats.document_types.join(', ')}
              </div>
            </div>
          </div>
        )}

        {/* Upload Area */}
        <div
          className={`border-2 border-dashed rounded-lg p-4 text-center transition-colors ${
            dragActive
              ? 'border-blue-500 bg-blue-50'
              : isUploading
              ? 'border-gray-300 bg-gray-50'
              : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {isUploading ? (
            <div className="flex items-center justify-center space-x-2">
              <RefreshCw className="h-5 w-5 animate-spin text-blue-500" />
              <span className="text-blue-600">Uploading and processing...</span>
            </div>
          ) : (
            <div>
              <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <div className="text-gray-600 mb-2">
                Drag and drop files here, or{' '}
                <label className="text-blue-500 hover:text-blue-700 cursor-pointer">
                  browse
                  <input
                    type="file"
                    className="hidden"
                    accept=".pdf,.txt,.md,.docx"
                    onChange={handleFileChange}
                  />
                </label>
              </div>
              <div className="text-sm text-gray-500">
                Supports PDF, TXT, MD, DOCX files
              </div>
            </div>
          )}
        </div>

        {/* Upload Error */}
        {uploadError && (
          <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-2">
            <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-red-800 font-medium">Upload Error</div>
              <div className="text-red-700 text-sm">{uploadError}</div>
            </div>
          </div>
        )}
      </div>

      {/* Documents List */}
      <div className="flex-1 overflow-y-auto p-4">
        {documents.length === 0 && !isLoading ? (
          <div className="text-center text-gray-500 py-12">
            <File className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p>No documents uploaded yet</p>
            <p className="text-sm">Upload your first document to get started</p>
          </div>
        ) : (
          <div className="space-y-2">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <div className="flex items-center space-x-3">
                  {getFileIcon(doc.file_type)}
                  <div>
                    <div className="font-medium text-gray-800">{doc.filename}</div>
                    <div className="text-sm text-gray-500">
                      {doc.chunk_count} chunks • {formatFileSize(doc.size_bytes)} • {formatDate(doc.upload_date)}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteDocument(doc.id, doc.filename)}
                  className="text-red-500 hover:text-red-700 p-1"
                  title="Delete document"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentManager;
