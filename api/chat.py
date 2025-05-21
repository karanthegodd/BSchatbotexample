from http.server import BaseHTTPRequestHandler
import json
import openai
import os

def handle_chat(message):
    try:
        # Configure OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Create conversation history
        conversation = [
            {"role": "system", "content": """You are a customer service chatbot for BS Transport. 
            Your role is to assist customers with:
            1. Shipment tracking
            2. Answering FAQs about transport services
            3. Providing service information
            4. Handling customer support inquiries
            5. Collecting customer feedback
            
            Always be professional, helpful, and concise in your responses.
            If you don't know something, politely say so and offer to connect the customer with a human representative."""},
            {"role": "user", "content": message}
        ]
        
        # Get response from OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in handle_chat: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team."

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if not data or 'message' not in data:
                self.send_error(400, "No message provided")
                return
            
            response = handle_chat(data['message'])
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({'message': response}).encode())
        except Exception as e:
            print(f"Error in POST handler: {str(e)}")
            self.send_error(500, "Internal server error") 