# 🤖 Hybrid Chatbot Generator

A modular, scalable Python application that combines AI-powered pattern generation with rule-based chatbot testing. Generate regex patterns using Google's Gemini AI and test your chatbot in real-time through an intuitive Gradio interface.

## ✨ Features

- **🎯 AI-Powered Pattern Generation**: Use Google Gemini to generate contextual regex patterns
- **💬 Real-Time Chatbot Testing**: Test your generated patterns instantly
- **📊 Analytics & Statistics**: Monitor pattern usage and conversation metrics
- **🔄 Pattern Editing**: Modify and reinitialize patterns on the fly
- **💾 Export Conversations**: Save chat logs in multiple formats
- **🎨 Beautiful UI**: Clean, intuitive Gradio interface
- **📦 Modular Architecture**: Scalable and maintainable code structure

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd hybrid-chatbot-generator
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Step 5: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_KEY=your_actual_api_key_here
```

## 🎯 Quick Start

1. **Add your API key** to the `.env` file
2. **Run the application**:
   ```bash
   python app.py
   ```
3. **Open your browser** to `http://localhost:7860`
4. **Start generating patterns** and testing your chatbot!

## 📁 Project Structure

```
hybrid-chatbot-generator/
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── pattern_generator.py     # LLM pattern generation logic
│   ├── chatbot.py                # Rule-based chatbot implementation
│   ├── chatbot_manager.py        # Chatbot lifecycle management
│   └── ui/                       # UI components
│       ├── __init__.py
│       ├── components.py         # Reusable Gradio components
│       └── interface.py          # Main interface orchestration
│
├── utils/                        # Utility modules
│   ├── __init__.py
│   ├── validators.py             # Input/code validation
│   └── parser.py                 # Pattern parsing utilities
│
├── config/                       # Configuration
│   ├── __init__.py
│   └── settings.py               # App settings and constants
│
├── assets/                       # Static assets (optional)
│   └── styles.css
│
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example environment file
├── requirements.txt              # Python dependencies
├── app.py                        # Main application entry point
└── README.md                     # This file
```

## ⚙️ Configuration

### Application Settings

Edit `config/settings.py` to customize:

```python
APP_CONFIG = {
    'server_port': 7860,          # Web server port
    'server_name': '0.0.0.0',     # Server address
    'share': False,                # Enable public URL
    'debug': False                 # Debug mode
}

LLM_CONFIG = {
    'model_name': 'gemini-2.0-flash-exp',  # Gemini model
    'temperature': 0.7,                     # Creativity level
    'max_output_tokens': 2048,              # Max response length
}
```

### Pattern Configuration

```python
PATTERN_CONFIG = {
    'min_patterns': 8,             # Minimum patterns to generate
    'max_patterns': 15,            # Maximum patterns to generate
    'include_catch_all': True,     # Always include catch-all pattern
}
```

## 📖 Usage Guide

### 1. Generate Patterns

1. Describe your chatbot's purpose in detail
2. Click "🚀 Generate Patterns"
3. Review the generated regex patterns
4. (Optional) Edit patterns in the code editor

**Example Purpose:**
```
A customer service chatbot for a pizza delivery service that can:
- Take pizza orders
- Answer questions about menu items
- Provide delivery time estimates
- Handle complaints and feedback
```

### 2. Test Your Chatbot

1. Once patterns are generated, the chatbot activates automatically
2. Type messages in the chat input
3. Press Enter or click Send
4. Review responses and pattern matching

### 3. Monitor Statistics

1. Click "📈 Update Statistics" to see:
   - Total messages handled
   - Pattern usage frequency
   - Unused patterns
   - Coverage metrics

### 4. Export Conversations

1. Click "💾 Export Conversation"
2. Copy the exported markdown
3. Save for documentation or analysis

### 5. Reinitialize Chatbot

1. Edit patterns in the code editor
2. Click "🔄 Reinitialize Chatbot"
3. Start testing with updated patterns

## 🔧 API Documentation

### PatternGenerator

```python
from src.pattern_generator import PatternGenerator

generator = PatternGenerator(api_key="your-api-key")
patterns = generator.generate_patterns("chatbot purpose description")
```

**Methods:**
- `generate_patterns(purpose: str) -> str`: Generate patterns from purpose
- `regenerate_with_modifications(purpose: str, feedback: str) -> str`: Regenerate with feedback

### RuleBasedChatbot

```python
from src.chatbot import RuleBasedChatbot

pairs = [
    [r"hi|hello", ["Hello! How can I help?"]],
    [r"bye", ["Goodbye!"]]
]

chatbot = RuleBasedChatbot(pairs)
response = chatbot.respond("Hello there!")
```

**Methods:**
- `respond(user_input: str) -> str`: Get response to user input
- `get_conversation_history() -> List[dict]`: Get full chat history
- `get_pattern_statistics() -> dict`: Get usage statistics
- `export_conversation(format: str) -> str`: Export chat (text/json/markdown)

### ChatbotManager

```python
from src.chatbot_manager import ChatbotManager

manager = ChatbotManager()
success, msg = manager.initialize_chatbot(pairs_code, purpose)

if success:
    response = manager.get_response("Hello!")
```

**Methods:**
- `initialize_chatbot(pairs_code: str, purpose: str) -> Tuple[bool, str]`
- `get_response(user_input: str) -> str`
- `get_statistics() -> dict`
- `export_conversation(format: str) -> str`

## 💡 Examples

### Example 1: Banking Chatbot

```python
Purpose: "A banking chatbot that helps users check balances, 
transfer money, and find ATM locations"

Generated Patterns:
[
    [r"balance|account", ["Your current balance is..."]],
    [r"transfer (.*) to (.*)", ["Transferring %1 to %2..."]],
    [r"atm|location", ["The nearest ATM is..."]]
]
```

### Example 2: Tech Support Chatbot

```python
Purpose: "A technical support chatbot for troubleshooting 
software issues and guiding users through solutions"

Generated Patterns:
[
    [r"error|bug|problem", ["I can help with that. What error are you seeing?"]],
    [r"how (do|can) I (.*)", ["To %2, you need to..."]],
    [r"not working", ["Let's troubleshoot this together..."]]
]
```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: GEMINI_KEY not found in .env file
```
**Solution**: Create `.env` file and add your Gemini API key

**2. NLTK Data Missing**
```
Error: Resource 'punkt' not found
```
**Solution**: Run `python -c "import nltk; nltk.download('punkt')"`

**3. Port Already in Use**
```
Error: Address already in use
```
**Solution**: Change `server_port` in `config/settings.py` or kill the process using port 7860

**4. Import Errors**
```
ModuleNotFoundError: No module named 'gradio'
```
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Debug Mode

Enable debug mode in `config/settings.py`:
```python
APP_CONFIG = {
    'debug': True
}
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Built with [Gradio](https://gradio.app/) for the UI
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/) for AI generation
- Uses [NLTK](https://www.nltk.org/) for natural language processing
---