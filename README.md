# Dialogflow Account Balance Chatbot 🤖

A simple yet powerful web-based chatbot that integrates with Google Dialogflow to check a user's account balance. This project uses a Flask backend for the API and webhook, and a clean HTML/CSS/JavaScript frontend for the user interface.

## ✨ Features

* **Flask Backend**: A robust Python server to handle chat requests and webhook fulfillment.
* **Dialogflow Integration**: Leverages Google's Natural Language Understanding (NLU) to process user messages.
* **Webhook Fulfillment**: A webhook endpoint (`/webhook`) that provides dynamic responses for specific intents (e.g., fetching an account balance).
* **Interactive UI**: A sleek, responsive chat interface created with HTML, CSS, and vanilla JavaScript.
* **Session Management**: Maintains a unique session ID for each user to track conversation context.

## 📂 Project Structure

```
dialogflow-chatbot/
├── static/
│   └── chatbot.html      # Frontend chat interface
├── .gitignore            # Specifies files to be ignored by Git
├── app.py                # Main Flask application logic
├── LICENSE               # Project license
├── README.md             # This readme file
└── requirements.txt      # Python dependencies
```

## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites

* Python 3.8+
* A Google Cloud Platform (GCP) project with the Dialogflow API enabled.
* A Dialogflow Agent created.

### 2. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/dialogflow-chatbot.git](https://github.com/YOUR_USERNAME/dialogflow-chatbot.git)
cd dialogflow-chatbot
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Google Cloud Credentials

This application requires a service account key from your GCP project to authenticate with the Dialogflow API.

1.  Follow the [Google Cloud documentation](https://cloud.google.com/dialogflow/es/docs/quick/setup#sa-create) to create a service account.
2.  Assign the **"Dialogflow API User"** role to the service account.
3.  Generate a JSON key file for the service account and download it.
4.  **Important**: Rename the downloaded file to `dialogflow_credentials.json` and place it in the root of the `dialogflow-chatbot` directory. The `.gitignore` file is configured to prevent this file from being committed to Git.

### 6. Configure Your Dialogflow Agent

1.  Create an intent in your Dialogflow agent named exactly `get_account_balance`.
2.  In the **Fulfillment** section of this intent, enable the webhook call.
3.  In the **Fulfillment** tab on the left menu, enable the Webhook and set the URL to `http://YOUR_SERVER_IP:5000/webhook`. For local testing, you will need to use a tool like **ngrok** to expose your local server to the internet.

### 7. Run the Application

```bash
python app.py
```

The application will be running at `http://127.0.0.1:5000`.

## 💡 Usage

Open your web browser and navigate to `http://127.0.0.1:5000`. You can start chatting with the bot. Try asking:

* "What is my account balance?"
* "Check my balance"
* "How much money do I have?"

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.