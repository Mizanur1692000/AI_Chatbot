# Production-Ready AI Chatbot with Django and Channels

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.x-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A scalable, production-ready, session-based AI chatbot built with Django, Django REST Framework, and Django Channels. It uses Google Gemini for AI-powered conversations and supports real-time, asynchronous communication via WebSockets.

## Features

-   **Real-time & Asynchronous**: Built with Django Channels for scalable, low-latency WebSocket communication.
-   **AI-Powered Conversations**: Integrates with Google Gemini via LangChain for intelligent and context-aware responses.
-   **RESTful API**: Provides a clean API for session management and communication.
-   **Session Management**: Uses email-based session handling to maintain distinct conversation histories.
-   **Performance Optimized**: Implements caching to reduce latency and minimize redundant AI API calls.
-   **Error Handling**: Gracefully handles potential issues with external AI services.
-   **Production-Ready**: Securely configured for deployment with environment variables for sensitive data.

## Architecture Overview

This project uses a standard Django setup for the core application logic and REST API. For real-time chat functionality, it leverages **Django Channels** to handle WebSocket connections.

1.  **Web Server (Nginx)**: Handles incoming HTTP requests, serves static files, and acts as a reverse proxy for the application server.
2.  **Application Server (Daphne)**: An ASGI server that runs the Django application, handling both HTTP and WebSocket traffic.
3.  **Django Backend**: Manages API endpoints, session logic, and database interactions.
4.  **Channels & Consumers**: The `chatbot` app contains a `ChatConsumer` that manages individual WebSocket connections, receives messages, interacts with the AI service, and broadcasts responses.
5.  **Cache**: An in-memory cache is used to store results from the AI service, improving performance for repeated queries.

## Tech Stack

-   **Backend**: Django, Django REST Framework, Django Channels
-   **Application Server**: Daphne
-   **AI**: Google Gemini, LangChain
-   **Database**: SQLite (development), PostgreSQL (recommended for production)
-   **Real-time Communication**: WebSockets

## Local Development Setup

### 1. Prerequisites

-   Python 3.9+
-   `pip` and `venv`

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd ai_chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root directory. This file will store your sensitive credentials.

```
# .env
SECRET_KEY='your-super-secret-django-key'
GEMINI_API_KEY='your-google-gemini-api-key'
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Run the Development Server

Since the project uses Django Channels, you need to run it with an ASGI server like Daphne.

```bash
daphne -p 8000 ai_chatbot.asgi:application
```

The application will be available at `http://localhost:8000`.

## API and WebSocket Endpoints

### REST API

#### Create Session

-   **Endpoint**: `POST /api/set_email/`
-   **Description**: Creates a new chat session associated with an email.
-   **Body**:
    ```json
    {
      "email": "user@example.com"
    }
    ```
-   **Response**:
    ```json
    {
      "session_id": "your_session_id"
    }
    ```

### WebSocket for Real-time Chat

Once you have a `session_id`, you can connect to the chat consumer via a WebSocket.

-   **URL**: `ws://localhost:8001/ws/chat/<room_name>/`
    -   Replace `<room_name>` with a unique identifier for the chat room. You can use the `session_id` for a private chat.
-   **Sending Messages**: Send a JSON object with a `message` key.
    ```json
    {
      "message": "Hello, how are you?"
    }
    ```
-   **Receiving Messages**: The server will respond with a JSON object containing the AI's response.
    ```json
    {
      "message": "AI response to: Hello, how are you?"
    }
    ```

## Running Tests

To run the test suite, execute the following command:

```bash
python manage.py test
```

## Deployment

For a production environment, it is recommended to use:

-   **Database**: PostgreSQL or another robust database.
-   **Web Server**: Nginx to act as a reverse proxy and serve static files.
-   **Application Server**: Gunicorn for managing Daphne workers.
-   **Process Manager**: `systemd` or `supervisor` to manage the Gunicorn process.

Remember to set `DEBUG = False` in `settings.py` for production.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.