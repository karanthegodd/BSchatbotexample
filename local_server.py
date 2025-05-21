from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='templates')
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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
            print(f"Error in get_ai_response: {str(e)}")
            return f"I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team."

# Create chatbot instance
chatbot = BSTransportChatbot()

@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message']
        response = chatbot.get_ai_response(user_message)
        return jsonify({'message': response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000) 