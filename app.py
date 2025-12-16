"""
Healthcare Symptom Checker - Flask Backend API
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from config import Config
from llm_service import LLMService
from database import Database

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
CORS(app)

# Initialize services
llm_service = LLMService()
db = Database() if Config.DATABASE_ENABLED else None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/check-symptoms', methods=['POST'])
def check_symptoms():
    """
    Endpoint to analyze symptoms
    
    Expected JSON payload:
    {
        "symptoms": "description of symptoms"
    }
    
    Returns:
    {
        "success": true/false,
        "analysis": "LLM analysis",
        "disclaimer": "medical disclaimer",
        "metadata": {...}
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        symptoms = data.get('symptoms', '').strip()
        
        # Validate symptoms
        is_valid, error_message = llm_service.validate_symptoms(symptoms)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message
            }), 400
        
        # Analyze symptoms using LLM
        result = llm_service.analyze_symptoms(symptoms)
        
        if not result.get('success'):
            return jsonify(result), 500
        
        # Save to database if enabled
        if db and Config.DATABASE_ENABLED:
            try:
                query_id = db.save_query(symptoms, result['analysis'])
                result['query_id'] = query_id
            except Exception as e:
                # Log error but don't fail the request
                app.logger.error(f"Database error: {e}")
        
        # Return successful response
        return jsonify({
            "success": True,
            "analysis": result['analysis'],
            "disclaimer": result['disclaimer'],
            "metadata": {
                "model": result['model'],
                "tokens_used": result.get('tokens_used', 0)
            },
            "query_id": result.get('query_id')
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your request"
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get query history
    
    Query parameters:
    - limit: Number of queries to return (default: 10)
    
    Returns:
    {
        "success": true,
        "history": [...]
    }
    """
    if not db or not Config.DATABASE_ENABLED:
        return jsonify({
            "success": False,
            "error": "Database not enabled"
        }), 400
    
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)  # Cap at 50
        
        history = db.get_recent_queries(limit)
        
        return jsonify({
            "success": True,
            "history": history,
            "count": len(history)
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error retrieving history: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred while retrieving history"
        }), 500

@app.route('/api/query/<int:query_id>', methods=['GET'])
def get_query(query_id):
    """
    Get a specific query by ID
    
    Returns:
    {
        "success": true,
        "query": {...}
    }
    """
    if not db or not Config.DATABASE_ENABLED:
        return jsonify({
            "success": False,
            "error": "Database not enabled"
        }), 400
    
    try:
        query = db.get_query_by_id(query_id)
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query not found"
            }), 404
        
        return jsonify({
            "success": True,
            "query": query
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error retrieving query: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred while retrieving the query"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "database_enabled": Config.DATABASE_ENABLED,
        "model": Config.GROQ_MODEL
    }), 200

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
