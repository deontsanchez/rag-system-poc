import openai
from typing import List
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=texts
            )
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    async def generate_response(
        self, 
        query: str, 
        context_chunks: List[str], 
        conversation_history: List[dict] = None
    ) -> str:
        """Generate response using retrieved context"""
        try:
            # Create context from chunks
            context = "\n\n".join([f"Source {i+1}:\n{chunk}" for i, chunk in enumerate(context_chunks)])
            
            # Create system prompt
            system_prompt = """You are a helpful AI assistant that answers questions based on the provided context. 
            
Rules:
1. Answer questions using ONLY the information provided in the context
2. If the context doesn't contain enough information to answer the question, say so clearly
3. Always cite which source(s) you used by referring to "Source X" 
4. Be concise and accurate
5. If asked about something not in the context, politely explain you can only answer based on the provided documents

Context:
{context}""".format(context=context)

            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 3 exchanges
            
            messages.append({"role": "user", "content": query})

            # Generate response
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Generated response for query: {query[:50]}...")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

# Global instance
openai_service = OpenAIService()
