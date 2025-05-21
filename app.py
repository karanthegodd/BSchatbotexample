from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Define categories and their descriptions
CATEGORIES = {
    "shipment_tracking": "Track your shipment status and location",
    "faq": "Frequently asked questions about our services",
    "service_info": "Information about our transport services",
    "customer_support": "Get help with your inquiries",
    "feedback": "Provide feedback about our services"
}

class BSTransportChatbot:
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = """You are a customer service chatbot for BS Transport. 
        Your role is to assist customers with:
        1. Shipment tracking
        2. Answering FAQs about transport services
        3. Providing service information
        4. Handling customer support inquiries
        5. Collecting customer feedback
        
        Always be professional, helpful, and concise in your responses.
        If you don't know something, politely say so and offer to connect the customer with a human representative."""
    
    def get_ai_response(self, user_input):
        try:
            # Add system prompt at the start of conversation
            if not self.conversation_history:
                self.conversation_history.append({"role": "system", "content": self.system_prompt})
            
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=200
            )
            
            # Extract and store the response
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team."

# Create chatbot instance
chatbot = BSTransportChatbot()

@app.route('/')
def home():
    return render_template('index.html', categories=CATEGORIES)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    response = chatbot.get_ai_response(user_message)
    return jsonify({'message': response})

# For local development
if __name__ == '__main__':
    socketio.run(app, debug=True) 