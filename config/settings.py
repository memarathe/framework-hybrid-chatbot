"""
Configuration settings for the Hybrid Chatbot Generator
"""

# Application configuration
APP_CONFIG = {
    'title': 'Chatbot Pattern Generator',
    'description': 'Generate patterns using AI and use it as a rule-based chatbots',
    'version': '1.0.0',
    'server_name': '127.0.0.1',
    'server_port': 7860,
    'share': False,
    'debug': False
}

# LLM configuration
LLM_CONFIG = {
    'model_name': 'gemini-2.5-flash',
    'temperature': 0.7,
    'max_output_tokens': 8192,
}

# Pattern generation configuration
PATTERN_CONFIG = {
    'min_patterns': 8,
    'max_patterns': 10,
    'include_catch_all': True,
}

# UI configuration
UI_CONFIG = {
    'theme': 'soft',
    'max_chat_history': 100,
    'default_examples': [
        "A customer service chatbot for a pizza delivery service that can take orders and answer questions about menu items",
        "A technical support chatbot for a software company that helps users troubleshoot common issues",
        "A banking chatbot that helps users check balances, transfer money, and find ATM locations",
        "An educational chatbot that helps students with basic math problems and homework questions",
        "A healthcare chatbot that helps patients schedule appointments and get basic medical information"
    ]
}

# Validation rules
VALIDATION_CONFIG = {
    'max_pattern_length': 500,
    'max_response_length': 1000,
    'required_catch_all': True,
}
