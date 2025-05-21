from http.server import BaseHTTPRequestHandler
import json
import os
import openai

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Read the HTML template
            with open('templates/index.html', 'r') as file:
                html_content = file.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(html_content.encode())
        except Exception as e:
            print(f"Error in GET handler: {str(e)}")
            self.send_error(500, "Internal server error")

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if not data or 'message' not in data:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No message provided"}).encode())
                return
            
            user_message = data['message']
            response = chatbot.get_ai_response(user_message)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({'message': response}).encode())
        except Exception as e:
            print(f"Error in POST handler: {str(e)}")
            self.send_error(500, "Internal server error")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 