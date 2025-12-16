"""
Test Groq API - Simple Demo
Run this to test if your Groq API key works!
"""
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test Groq API with a simple health query"""
    
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in .env file")
        print("\nPlease:")
        print("1. Get FREE API key from: https://console.groq.com")
        print("2. Add it to .env file: GROQ_API_KEY=gsk_your_key_here")
        return
    
    print("🚀 Testing Groq API...")
    print(f"📋 API Key: {api_key[:20]}...")
    print(f"🤖 Model: llama-3.3-70b-versatile\n")
    
    # Prepare API request
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful medical education assistant. Provide brief, educational information."
            },
            {
                "role": "user",
                "content": "What are common causes of headache? Keep it brief (2-3 lines)."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    try:
        print("⏳ Sending request to Groq API...")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            tokens = result['usage']['total_tokens']
            
            print("\n✅ SUCCESS! Groq API is working!\n")
            print("="*60)
            print("RESPONSE:")
            print("="*60)
            print(answer)
            print("="*60)
            print(f"\n📊 Tokens used: {tokens}")
            print("💡 Your API key is working perfectly!")
            print("\n🎉 You can now run: python app.py")
            
        else:
            print(f"\n❌ ERROR: API returned status code {response.status_code}")
            print(f"Response: {response.text}\n")
            
            if response.status_code == 401:
                print("🔑 Your API key is invalid or expired")
                print("👉 Get a new one at: https://console.groq.com")
            elif response.status_code == 429:
                print("⏰ Rate limit exceeded - wait a moment and try again")
            
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timed out")
        print("Check your internet connection")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: Network error - {e}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    print("="*60)
    print("  GROQ API TEST - Healthcare Symptom Checker")
    print("="*60)
    print()
    test_groq_api()
