#!/usr/bin/env python3
"""
Simple script to verify environment configuration is working properly
"""
import os
from dotenv import load_dotenv

# Load from root .env file
load_dotenv(dotenv_path='.env')

def check_env():
    print("🔍 Checking Environment Configuration...")
    print("=" * 50)
    
    # Required variables
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'ENV': 'Environment',
        'PORT': 'Backend Port',
        'REACT_APP_API_URL': 'Frontend API URL'
    }
    
    # Optional variables
    optional_vars = {
        'DEBUG': 'Debug Mode',
        'CHROMA_PERSIST_DIRECTORY': 'ChromaDB Directory',
        'UPLOAD_DIRECTORY': 'Upload Directory',
        'LLM_MODEL': 'LLM Model',
        'EMBEDDING_MODEL': 'Embedding Model'
    }
    
    print("📋 REQUIRED VARIABLES:")
    all_good = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask API key for security
            if 'API_KEY' in var:
                display_value = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "***"
            else:
                display_value = value
            print(f"  ✅ {var:<25} = {display_value}")
        else:
            print(f"  ❌ {var:<25} = NOT SET")
            all_good = False
    
    print("\n📝 OPTIONAL VARIABLES:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var:<25} = {value}")
        else:
            print(f"  ⚠️  {var:<25} = Using default")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Environment configuration looks good!")
        print("💡 Run './dev.sh' to start the development servers")
    else:
        print("❌ Some required environment variables are missing!")
        print("💡 Check your .env file and compare with .env.example")
    
    return all_good

if __name__ == "__main__":
    check_env()
