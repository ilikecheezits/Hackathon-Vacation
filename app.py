from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.')

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("Please set GOOGLE_API_KEY in your environment variables")

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    logger.info("Successfully configured Gemini API")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/gemini', methods=['POST'])
def gemini_api():
    try:
        data = request.get_json()
        logger.debug(f"Received request data: {data}")
        
        prompt = data.get('prompt')
        if not prompt:
            logger.error("No prompt provided in request")
            return jsonify({'error': 'No prompt provided'}), 400
            
        logger.debug(f"Sending prompt to Gemini: {prompt[:100]}...")  # Log first 100 chars
        response = model.generate_content(prompt)
        logger.debug("Successfully received response from Gemini")
        
        return jsonify({'response': response.text})
        
    except Exception as e:
        logger.error(f"Error in gemini_api: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
