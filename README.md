# BS Transport Chatbot

A modern, AI-powered customer support chatbot for BS Transport built with Flask and OpenAI's GPT-3.5.

## Features

- Real-time chat interface using WebSocket
- AI-powered responses using OpenAI's GPT-3.5
- Categorized support topics
- Modern, responsive UI with Tailwind CSS
- 24/7 automated customer support

## Tech Stack

- Backend: Python, Flask, Flask-SocketIO
- Frontend: HTML, Tailwind CSS, JavaScript
- AI: OpenAI GPT-3.5
- Real-time Communication: Socket.IO

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bs-transport-chatbot.git
cd bs-transport-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:3030`

## Deployment

The application can be deployed on any platform that supports Python applications, such as:
- Heroku
- PythonAnywhere
- AWS
- Google Cloud Platform

## Author

Karan Kalra

## License

MIT License 