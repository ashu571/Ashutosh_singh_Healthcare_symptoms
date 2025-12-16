"""
Configuration management for Healthcare Symptom Checker
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Groq API settings (FREE & FAST!)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
    GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '1000'))
    
    # Database settings
    DATABASE_ENABLED = os.getenv('DATABASE_ENABLED', 'True').lower() == 'true'
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'symptom_checker.db')
    
    # Application settings
    MAX_SYMPTOM_LENGTH = int(os.getenv('MAX_SYMPTOM_LENGTH', '1000'))
    RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', '30'))
    
    # Medical disclaimer
    MEDICAL_DISCLAIMER = """
    ⚕️ IMPORTANT MEDICAL DISCLAIMER ⚕️
    
    This tool is for EDUCATIONAL PURPOSES ONLY and does NOT provide medical advice.
    
    - The information provided is NOT a substitute for professional medical advice, diagnosis, or treatment.
    - Always seek the advice of a qualified healthcare provider with any questions about a medical condition.
    - Never disregard professional medical advice or delay seeking it because of information from this tool.
    - If you have a medical emergency, call emergency services immediately.
    
    This AI-generated content may contain inaccuracies or incomplete information.
    """
