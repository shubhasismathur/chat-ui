"""Azure OpenAI service module with proper error handling and security."""
import os
import logging
import json
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables - ensure we load from the correct path
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureOpenAIService:
    """Service class for Azure OpenAI integration with error handling and retry logic."""
    
    def __init__(self):
        """Initialize Azure OpenAI client with configuration from environment variables."""
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
        
        # Debug logging
        logger.info(f"Loading Azure OpenAI configuration:")
        logger.info(f"Endpoint: {self.endpoint}")
        logger.info(f"API Key: {'***' + self.api_key[-4:] if self.api_key else 'None'}")
        logger.info(f"API Version: {self.api_version}")
        logger.info(f"Deployment: {self.deployment_name}")
        
        # Validate required configuration
        if not self.endpoint or not self.api_key:
            logger.error("Missing required Azure OpenAI configuration in environment variables")
            raise ValueError("Missing required Azure OpenAI configuration in environment variables")
        
        # Initialize headers for API requests
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        # Check if endpoint already contains the full URL or just the base
        if "chat/completions" in self.endpoint:
            # Full URL provided in endpoint
            self.api_url = self.endpoint
        else:
            # Base endpoint provided, build the full URL
            self.api_url = f"{self.endpoint.rstrip('/')}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        logger.info(f"Using API URL: {self.api_url}")
        logger.info("Azure OpenAI service initialized successfully")
    
    def generate_response(self, user_message: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a response from Azure OpenAI.
        
        Args:
            user_message (str): The user's input message
            conversation_history (list, optional): Previous conversation context
            
        Returns:
            str: Generated response from Azure OpenAI
        """
        try:
            # Prepare messages for the API
            messages = []
            
            # Add system message for context
            messages.append({
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
            })
            
            # Add conversation history if provided
            if conversation_history:
                # Take last 10 messages to avoid token limit issues
                recent_history = conversation_history[-10:]
                for msg in recent_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare the request payload - using only supported parameters for gpt-5-mini
            payload = {
                "messages": messages,
                "max_completion_tokens": 800
            }
            
            # Make API call with proper error handling
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    generated_response = response_data["choices"][0]["message"]["content"].strip()
                    logger.info("Successfully generated response from Azure OpenAI")
                    return generated_response
                else:
                    logger.warning("No response generated from Azure OpenAI")
                    return "I apologize, but I couldn't generate a response at the moment. Please try again."
            else:
                logger.error(f"Azure OpenAI API error: {response.status_code} - {response.text}")
                return "I'm sorry, I'm experiencing some technical difficulties. Please try again in a moment."
                
        except Exception as e:
            logger.error(f"Error generating response from Azure OpenAI: {e}")
            # Return a user-friendly error message instead of exposing technical details
            return "I'm sorry, I'm experiencing some technical difficulties. Please try again in a moment."
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return bool(self.endpoint and self.api_key and self.api_url)

# Global instance for use across the application
def get_azure_openai_service():
    """Get or create Azure OpenAI service instance."""
    try:
        service = AzureOpenAIService()
        logger.info("Azure OpenAI service initialized successfully")
        return service
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI service: {e}")
        return None

# Initialize the service
azure_openai_service = get_azure_openai_service()