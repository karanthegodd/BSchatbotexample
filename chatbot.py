import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint
from colorama import init, Fore, Style
import openai
from dotenv import load_dotenv

# Initialize colorama and rich
init()
console = Console()

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class AdvancedChatbot:
    def __init__(self):
        self.conversation_history = []
        self.console = Console()
        
    def get_ai_response(self, user_input):
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=150
            )
            
            # Extract and store the response
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        except Exception as e:
            return f"Error: {str(e)}"

    def display_welcome(self):
        welcome_text = """
        🤖 Welcome to the Advanced Chatbot! 🤖
        
        I'm here to help you with any questions or tasks you have.
        Type 'exit' or 'quit' to end the conversation.
        """
        console.print(Panel(welcome_text, title="Welcome", border_style="blue"))

    def run(self):
        self.display_welcome()
        
        while True:
            # Get user input with a nice prompt
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[bold green]Goodbye! Have a great day! 👋[/bold green]")
                break
            
            # Get and display AI response
            response = self.get_ai_response(user_input)
            
            # Display response in a nice panel
            console.print(Panel(
                Markdown(response),
                title="🤖 Assistant",
                border_style="green"
            ))

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]Error: OPENAI_API_KEY not found in environment variables![/bold red]")
        console.print("Please create a .env file with your OpenAI API key.")
        exit(1)
        
    chatbot = AdvancedChatbot()
    chatbot.run() 