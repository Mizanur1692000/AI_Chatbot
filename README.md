# AI Chatbot

This is a real-time AI-powered chatbot built with Django Channels. The backend is a Django application that uses WebSockets to communicate with the frontend, and the AI logic is handled by a separate utility module.

## Features

-   Real-time, two-way communication using Django Channels.
-   AI-powered responses.
-   Conversation history is stored in a database.
-   Scalable project structure.

## Project Structure

-   `ai_chatbot/`: The main Django project folder.
    -   `settings.py`: Django project settings.
    -   `urls.py`: Main URL configuration.
    -   `asgi.py`: ASGI configuration for Django Channels.
-   `chatbot/`: The chatbot Django app.
    -   `consumers.py`: Handles WebSocket connections and chat logic.
    -   `ai_utils.py`: Contains the AI logic for generating responses.
    -   `models.py`: Defines the database model for storing chat messages.
    -   `routing.py`: URL routing for WebSocket connections.
    -   `urls.py`: URL configuration for the chatbot app.
-   `db.sqlite3`: The SQLite database file.
-   `manage.py`: Django's command-line utility.
-   `requirements.txt`: A list of Python packages required for this project.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Mizanur1692000/AI_Chatbot
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

## Running the Application

1.  **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```

2.  **Open your web browser** and navigate to `http://127.0.0.1:8000/`. You will need to create a simple frontend to interact with the chatbot.

## How It Works

### Backend (Django Channels)

The backend uses Django Channels to handle WebSocket connections. When a client connects to the `/ws/chat/` endpoint, the `ChatConsumer` in `chatbot/consumers.py` is instantiated.

-   When a message is received from the client, the `receive` method is called.
-   The message is passed to the AI utility in `chatbot/ai_utils.py` to generate a response.
-   The user's message and the bot's response are saved to the database.
-   The bot's response is sent back to the client over the WebSocket.

### Frontend (WebSocket Client)

You will need to create a frontend with JavaScript to connect to the WebSocket. The frontend should:

1.  Establish a WebSocket connection to `ws://127.0.0.1:8000/ws/chat/`.
2.  Send messages to the server in JSON format (e.g., `{"message": "Hello"}`).
3.  Listen for messages from the server and display them in the chat interface.
