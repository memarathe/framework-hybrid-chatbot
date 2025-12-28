"""
Hybrid Chatbot Generator - Main Application Entry Point
A modular application for generating and testing rule-based chatbots using AI
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.interface import HybridChatbotInterface
from config.settings import APP_CONFIG


def main():
    """Main entry point for the application"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Verify API key exists
        api_key = os.getenv("GEMINI_KEY")
        if not api_key:
            print("Error: GEMINI_KEY not found in .env file")
            print("Please create a .env file with: GEMINI_KEY=your_api_key_here")
            print("You can use .env.example as a template")
            return
        
        # Initialize and launch interface
        print("Launching Hybrid Chatbot Generator...")
        print(f"Server will start at: http://{APP_CONFIG['server_name']}:{APP_CONFIG['server_port']}")
        
        interface = HybridChatbotInterface(api_key)
        interface.launch(
            share=APP_CONFIG['share'],
            server_name=APP_CONFIG['server_name'],
            server_port=APP_CONFIG['server_port'],
            debug=APP_CONFIG['debug']
        )
        
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Application error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
