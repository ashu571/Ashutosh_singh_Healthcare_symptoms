# Healthcare Symptom Checker

An AI-powered web application that provides educational information about potential health conditions based on user-described symptoms. Built with Flask backend and powered by Groq's free LLM API.

> ⚠️ **IMPORTANT**: This application is for **EDUCATIONAL PURPOSES ONLY** and does NOT provide medical advice. Always consult qualified healthcare professionals for medical concerns.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Groq](https://img.shields.io/badge/Groq-FREE-purple)
![Status](https://img.shields.io/badge/Status-Complete-success)

---

## 📋 Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Safety & Disclaimers](#safety--disclaimers)

---

## ✨ Features

### Core Functionality
- **AI-Powered Analysis**: Uses Groq's Llama 3.3 70B model for intelligent symptom analysis
- **Educational Information**: Provides 3-5 possible conditions with detailed explanations
- **Safety Recommendations**: Guidance on when to seek medical care
- **Emergency Detection**: Automatically highlights symptoms requiring urgent attention
- **Query History**: Optional SQLite database to track past analyses

### User Experience
- **Modern Dark UI**: Premium design with smooth animations and glassmorphism effects
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Real-time Validation**: Character counter and input validation
- **Error Handling**: User-friendly error messages with retry options
- **Loading States**: Professional animations during AI analysis

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0.0**: Lightweight web framework
- **Groq API**: FREE & fast LLM inference (Llama 3.3 70B)
- **SQLite**: Local database for query history
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: No framework dependencies
- **Google Fonts**: Professional typography (Inter & Poppins)

---

## 📁 Project Structure

```
Singh_assign/
├── app.py                  # Main Flask application
├── llm_service.py          # Groq API integration
├── database.py             # SQLite database operations
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── start.bat               # Windows startup script
├── test_groq.py            # API test script
├── README.md               # This file
└── static/                 # Frontend files
    ├── index.html          # Main HTML page
    ├── style.css           # Styling
    └── script.js           # Client-side JavaScript
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

### Step 1: Clone/Download the Repository
```bash
cd Singh_assign
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get FREE Groq API Key

**Groq offers completely FREE API access with generous limits!**

1. Visit: **https://console.groq.com**
2. Sign up with Google/GitHub (takes 30 seconds)
3. Navigate to **"API Keys"** in the sidebar
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_...`)

**Why Groq?**
- ✅ **Completely FREE** - No credit card required
- ✅ **14,400 requests/day** - Very generous limits
- ✅ **Super fast** - Fastest LLM inference available
- ✅ **High quality** - Llama 3.3 70B model

### Step 5: Configure Environment Variables

1. Create `.env` file from template:
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Edit `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

Your `.env` file should look like:
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Groq API Configuration
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1000

# Database Configuration
DATABASE_ENABLED=True
DATABASE_PATH=symptom_checker.db

# Application Settings
MAX_SYMPTOM_LENGTH=1000
RESPONSE_TIMEOUT=30
```

---

## 💻 How to Run

### Method 1: Using Python (Recommended)
```bash
python app.py
```

### Method 2: Using Startup Script (Windows)
```bash
start.bat
```

The application will start on: **http://localhost:5000**

### Testing the API Before Running

Test if your Groq API key works:
```bash
python test_groq.py
```

You should see:
```
✅ SUCCESS! Groq API is working!
```

---

## 📖 Usage

### Using the Web Interface

1. **Open your browser**: Navigate to `http://localhost:5000`

2. **Describe your symptoms** in the text area:
   ```
   Example: I've been experiencing headaches for the past 3 days. 
   The pain is mostly on the left side of my head and gets worse 
   in bright light. I also feel slightly nauseous.
   ```

3. **Click "Analyze Symptoms"**

4. **Review the AI analysis**:
   - Possible conditions
   - Educational information
   - When to seek medical care
   - Recommended next steps

5. **Read the medical disclaimer** - Always consult healthcare professionals!

### Sample Test Queries

**Common Cold/Flu:**
```
I have a headache, fever of 100°F, body aches, sore throat, 
and runny nose for the past 2 days.
```

**Digestive Issue:**
```
Stomach pain and diarrhea for 3 days. Nauseous with no appetite. 
Pain is in lower abdomen and worse after eating.
```

**Respiratory:**
```
Persistent dry cough for 4 days. Short of breath when walking. 
Chest feels tight with slight wheezing.
```

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Analyze Symptoms
**POST** `/api/check-symptoms`

**Request Body:**
```json
{
  "symptoms": "description of symptoms"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "analysis": "Detailed AI analysis...",
  "disclaimer": "Medical disclaimer text...",
  "metadata": {
    "model": "llama-3.3-70b-versatile",
    "tokens_used": 456
  },
  "query_id": 1
}
```

#### 2. Get Query History
**GET** `/api/history?limit=10`

**Response:**
```json
{
  "success": true,
  "history": [...],
  "count": 10
}
```

#### 3. Health Check
**GET** `/api/health`

**Response:**
```json
{
  "status": "healthy",
  "database_enabled": true,
  "model": "llama-3.3-70b-versatile"
}
```

---

## ⚕️ Safety & Disclaimers

### Medical Disclaimer

This application is designed for **EDUCATIONAL PURPOSES ONLY** and is NOT intended to:
- Provide medical advice, diagnosis, or treatment
- Replace professional medical consultation
- Be used as a primary source of medical information
- Make definitive health decisions

### Important Safety Notes

⚠️ **Always Seek Professional Care:**
- Consult qualified healthcare providers for medical concerns
- Get regular check-ups and screenings
- Follow your doctor's treatment plans

🚨 **Emergency Situations:**
If you experience symptoms of a medical emergency, **call emergency services immediately**. Do NOT rely on this tool for urgent medical decisions.

Emergency symptoms include:
- Chest pain or pressure
- Difficulty breathing
- Severe bleeding
- Loss of consciousness
- Severe allergic reactions
- Stroke symptoms (face drooping, arm weakness, speech difficulty)

### AI Limitations

- LLM outputs may contain inaccuracies or incomplete information
- AI cannot perform physical examinations or medical tests
- Medical diagnosis requires professional expertise and clinical judgment
- This tool cannot account for individual medical history or context

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | *Required* | Your Groq API key |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | LLM model to use |
| `GROQ_TEMPERATURE` | `0.7` | Response creativity (0.0-1.0) |
| `GROQ_MAX_TOKENS` | `1000` | Maximum response length |
| `DATABASE_ENABLED` | `True` | Enable query history |
| `DATABASE_PATH` | `symptom_checker.db` | Database file path |
| `MAX_SYMPTOM_LENGTH` | `1000` | Max characters for symptoms |
| `DEBUG` | `True` | Flask debug mode |

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Submit various symptom descriptions
- [ ] Verify emergency keyword detection
- [ ] Check loading states display correctly
- [ ] Test error handling with invalid inputs
- [ ] Verify medical disclaimers are prominent
- [ ] Test on different screen sizes
- [ ] Verify API responses are appropriate

### Test the API
```bash
python test_groq.py
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "GROQ_API_KEY not found"
- **Solution**: Ensure `.env` file exists with your API key

**Issue**: "Module not found" errors
- **Solution**: Activate virtual environment and run `pip install -r requirements.txt`

**Issue**: API authentication failed
- **Solution**: Verify your Groq API key is correct and active

**Issue**: CSS/JS not loading (white page)
- **Solution**: Hard refresh browser (Ctrl+Shift+R)

---

## 📄 License

This project is created for educational purposes as part of an academic assignment.

---

## 🙏 Acknowledgments

- **Groq** for providing FREE & fast LLM API
- **Meta** for the Llama 3.3 70B model
- **Flask** community for the excellent web framework
- **Google Fonts** for beautiful typography

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Ensure environment variables are correctly configured
4. Test with `python test_groq.py`

**Groq Console**: https://console.groq.com  
**Groq Documentation**: https://console.groq.com/docs

---

**Built with ❤️ for educational purposes**

**Remember**: This is an educational tool. Always consult healthcare professionals for medical advice!
