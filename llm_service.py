"""
LLM Service for symptom analysis using Groq API (FREE & FAST!)
"""
import requests
import json
from typing import Dict, Tuple
from config import Config

class LLMService:
    """Service for interacting with Groq API for symptom analysis"""
    
    def __init__(self):
        """Initialize Groq client"""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables. Get free API key at https://console.groq.com")
        
        self.api_key = Config.GROQ_API_KEY
        self.model = Config.GROQ_MODEL
        self.temperature = Config.GROQ_TEMPERATURE
        self.max_tokens = Config.GROQ_MAX_TOKENS
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for symptom analysis"""
        return """You are a medical education assistant designed to help people understand potential health conditions based on symptoms.

Your role is to:
1. Analyze the symptoms provided by the user
2. Suggest 3-5 possible conditions that could cause these symptoms (ordered by likelihood)
3. Provide educational information about each condition
4. Recommend appropriate next steps

CRITICAL REQUIREMENTS:
- Start EVERY response with: "⚠️ EDUCATIONAL INFORMATION ONLY - NOT MEDICAL ADVICE ⚠️"
- Always emphasize that this is for educational purposes only
- Recommend consulting a healthcare professional for proper diagnosis
- If symptoms suggest emergency conditions (heart attack, stroke, severe injury, etc.), STRONGLY emphasize seeking immediate emergency care
- Be clear about uncertainty - medical diagnosis is complex
- Avoid definitive diagnoses
- Use clear, accessible language

Format your response as follows:
1. Safety Alert (if applicable)
2. Possible Conditions (3-5 items with brief descriptions)
3. General Information & Self-Care
4. When to Seek Medical Care
5. Recommended Next Steps

Be helpful, educational, and prioritize user safety above all."""

    def analyze_symptoms(self, symptoms: str) -> Dict[str, any]:
        """
        Analyze symptoms using Groq API
        
        Args:
            symptoms: User's symptom description
            
        Returns:
            Dictionary containing analysis results and metadata
        """
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": self.get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": f"I am experiencing the following symptoms:\n\n{symptoms}\n\nWhat could these symptoms indicate? Please provide educational information."
                    }
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": 0.9
            }
            
            # Call Groq API
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Groq API error: {response.status_code} - {response.text}",
                    "error_type": "api_error"
                }
            
            # Extract response
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            
            # Add disclaimer if not present
            if "EDUCATIONAL" not in analysis.upper() and "NOT MEDICAL ADVICE" not in analysis.upper():
                analysis = "⚠️ EDUCATIONAL INFORMATION ONLY - NOT MEDICAL ADVICE ⚠️\n\n" + analysis
            
            # Get token usage
            tokens_used = result.get('usage', {}).get('total_tokens', 0)
            
            return {
                "success": True,
                "analysis": analysis,
                "model": self.model,
                "tokens_used": tokens_used,
                "disclaimer": Config.MEDICAL_DISCLAIMER
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Please try again.",
                "error_type": "timeout"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "error_type": "network_error"
            }
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific error types
            if "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
                return {
                    "success": False,
                    "error": "API authentication failed. Please check your Groq API key.",
                    "error_type": "auth_error"
                }
            elif "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
                return {
                    "success": False,
                    "error": "Rate limit exceeded. Please try again in a moment.",
                    "error_type": "rate_limit"
                }
            else:
                return {
                    "success": False,
                    "error": f"Error: {str(e)}",
                    "error_type": "api_error"
                }
    
    def validate_symptoms(self, symptoms: str) -> (bool, str):
        """
        Validate symptom input
        
        Args:
            symptoms: User's symptom description
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not symptoms or not symptoms.strip():
            return False, "Please provide a description of your symptoms"
        
        if len(symptoms) < 10:
            return False, "Please provide a more detailed description of your symptoms (at least 10 characters)"
        
        if len(symptoms) > Config.MAX_SYMPTOM_LENGTH:
            return False, f"Symptom description is too long (maximum {Config.MAX_SYMPTOM_LENGTH} characters)"
        
        return True, ""
