import os
import json
import uuid
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core import exceptions

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#set Google Application Credentials

if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    here = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(here, "dialogflow_credentials.json")
    if os.path.exists(credentials_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        logger.info("Using local credentials file: %s", credentials_path)
    else:
        logger.critical("FATAL: GOOGLE_APPLICATION_CREDENTIALS not set and dialogflow_credentials.json not found.")
        # Exit if no credentials can be found at all.
        exit("Credentials not configured.")

PROJECT_ID = ""
try:
    with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], 'r') as f:
        creds = json.load(f)
        PROJECT_ID = creds.get('project_id')
        if not PROJECT_ID:
            raise ValueError("project_id not found in credentials file.")
    logger.info("Successfully loaded Project ID from credentials: %s", PROJECT_ID)
except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
    logger.critical("FATAL: Could not determine Project ID from credentials file. Error: %s", e)
    exit("Project ID configuration failed.")

#Dialogflow Helper
def detect_intent_texts(project_id: str, session_id: str, text: str, language_code: str) -> str:
    """Calls Dialogflow's detect_intent API and returns the fulfillment text."""
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    request_payload = {"session": session_path, "query_input": query_input}
    response = session_client.detect_intent(request=request_payload)
    
    return response.query_result.fulfillment_text

#API Routes
@app.route('/', methods=['GET'])
def serve_frontend():
    """Serves the main HTML file for the chatbot UI."""
    return send_from_directory('static', 'chatbot.html')

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return jsonify({"status": "ok", "project_id": PROJECT_ID})

@app.route('/api/chat', methods=['POST'])
def chat_handler():
    """Main endpoint to handle chat messages from the user."""
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get('message', '').strip()
        session_id = data.get('sessionId') or str(uuid.uuid4())
        language_code = data.get('languageCode', 'en-US')

        if not user_message:
            return jsonify({"error": "Message cannot be empty."}), 400

        logger.info("Received chat message: '%s' (Session: %s)", user_message, session_id)
        
        fulfillment_text = detect_intent_texts(PROJECT_ID, session_id, user_message, language_code)
        
        return jsonify({'response': fulfillment_text, 'sessionId': session_id})

    except exceptions.PermissionDenied as e:
        logger.error("GCP PERMISSION DENIED: %s", e)
        error_message = "IAM Permission Denied. Please check that the service account has the 'Dialogflow API User' role in your GCP project."
        return jsonify({"error": error_message}), 500
    except Exception as e:
        logger.exception("An unexpected error occurred in /api/chat")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500
@app.route('/webhook', methods=['POST'])
def webhook():
    """This endpoint handles fulfillment requests from Dialogflow."""
    req = request.get_json(force=True)
    
    # Log the incoming request for debugging
    logger.info("Webhook request received: %s", json.dumps(req, indent=2))

    # Get the intent name from the request
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName')

    
    if intent_name == 'get_account_balance': # IMPORTANT: You must create an intent with this exact name in Dialogflow
    
        account_balance = "$1,234.56"
        
        # Format the response for Dialogflow
        response_text = f"Your current account balance is {account_balance}."
        
        # The response must be in the format Dialogflow expects
        response = {
            "fulfillmentText": response_text
        }
        return jsonify(response)
    
    # If the intent is not recognized, return a default response
    return jsonify({"fulfillmentText": "I'm not sure how to handle that request."})

if __name__ == '__main__':
    # Use Gunicorn or another WSGI server in production
    app.run(host='0.0.0.0', port=5000, debug=True)
   