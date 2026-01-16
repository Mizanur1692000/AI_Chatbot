import os
import hashlib
from django.core.cache import cache
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(message: str) -> str:
    """
    Gets a response from the AI, using cache if available.
    """
    # Define a system prompt to set the behavior of the AI
    system_prompt = "You are a helpful, friendly, and knowledgeable assistant. Your responses must be in natural language and should not contain any emojis."
    
    # Create a safe cache key (hash to avoid illegal chars/length)
    raw_key = f"{system_prompt}|{message}"
    cache_key = "ai:" + hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    try:
        llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.environ.get("GEMINI_API_KEY"))
        
        # Create a prompt template that includes the system prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])

        # Create a chain that combines the prompt and the language model
        chain = prompt | llm
        
        # Invoke the chain with the user's message
        response = chain.invoke({"input": message})

        # Normalize response to string for caching/return
        text = response.content if hasattr(response, "content") else str(response)

        # Cache the response
        cache.set(cache_key, text, timeout=300)  # Cache for 5 minutes
        return text
    except Exception as e:
        print(f"Error calling AI service: {e}")
        return "Sorry, I'm having trouble connecting to the AI service."