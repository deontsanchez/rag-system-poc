import React, { useState, useEffect } from 'react';
import { MessageSquare, Database, Settings, AlertCircle } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import DocumentManager from './components/DocumentManager';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState(null);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      await apiService.healthCheck();
      setIsConnected(true);
      setConnectionError(null);
    } catch (error) {
      setIsConnected(false);
      setConnectionError(error.message);
    }
  };

  const tabs = [
    {
      id: 'chat',
      name: 'Chat',
      icon: MessageSquare,
      component: ChatInterface,
    },
    {
      id: 'documents',
      name: 'Documents',
      icon: Database,
      component: DocumentManager,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">RAG System POC</h1>
            <p className="text-sm text-gray-600">Retrieval-Augmented Generation with Knowledge Base</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
              isConnected 
                ? 'bg-green-100 text-green-700' 
                : 'bg-red-100 text-red-700'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                isConnected ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
            
            {!isConnected && (
              <button
                onClick={checkConnection}
                className="text-blue-500 hover:text-blue-700 text-sm"
              >
                Retry
              </button>
            )}
          </div>
        </div>

        {/* Connection Error Banner */}
        {connectionError && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-2">
            <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-red-800 font-medium">Connection Error</div>
              <div className="text-red-700 text-sm">
                Cannot connect to the backend API. Make sure the server is running on port 8000.
              </div>
              <div className="text-red-600 text-xs mt-1">Error: {connectionError}</div>
            </div>
          </div>
        )}
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="px-6">
          <div className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-4 w-4" />
                <span>{tab.name}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1" style={{ height: 'calc(100vh - 200px)' }}>
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`h-full ${activeTab === tab.id ? 'block' : 'hidden'}`}
          >
            <div className="max-w-7xl mx-auto">
              <div className="bg-white h-full shadow-sm">
                <tab.component />
              </div>
            </div>
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;
