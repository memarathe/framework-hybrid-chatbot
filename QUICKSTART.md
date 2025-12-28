# 🚀 Quick Start Guide

Get your Hybrid Chatbot Generator up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] pip package manager
- [ ] Google Gemini API key ([Get one free here](https://makersuite.google.com/app/apikey))

## Installation Steps

### 1️⃣ Clone & Navigate

```bash
cd framework-hybrid-chatbot
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Setup Script

```bash
python setup.py
```

This will:
- ✅ Verify all dependencies
- ✅ Download NLTK data
- ✅ Create .env file if needed

### 5️⃣ Add Your API Key

Edit the `.env` file:
```bash
GEMINI_KEY=your_actual_gemini_api_key_here
```

### 6️⃣ Launch the Application

```bash
python app.py
```

### 7️⃣ Open in Browser

Navigate to: **http://localhost:7860**

## 🎯 Your First Chatbot

1. **Describe Purpose**: 
   ```
   A friendly customer service chatbot for a coffee shop that can 
   take orders, answer menu questions, and provide store hours.
   ```

2. **Click "Generate Patterns"** - Wait ~10 seconds

3. **Test Your Chatbot**: Try these inputs:
   - "Hello!"
   - "What drinks do you have?"
   - "I'd like to order a latte"
   - "What are your hours?"
   - "Goodbye"

4. **View Statistics**: Click "Update Statistics" to see pattern usage

5. **Export**: Click "Export Conversation" to save your chat

## 🔧 Customization

### Change Server Port

Edit `config/settings.py`:
```python
APP_CONFIG = {
    'server_port': 8080,  # Change to your preferred port
}
```

### Adjust Pattern Count

Edit `config/settings.py`:
```python
PATTERN_CONFIG = {
    'min_patterns': 10,   # More patterns
    'max_patterns': 20,
}
```

## 🐛 Troubleshooting

### Port Already in Use?
```bash
# Change port in config/settings.py or
# Kill process on port 7860 (macOS/Linux):
lsof -ti:7860 | xargs kill -9
```

### Missing NLTK Data?
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Import Errors?
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Next Steps

- 📖 Read the full [README.md](README.md)
- 🔍 Explore the code in `src/`
- 🎨 Customize UI in `src/ui/components.py`
- ⚙️ Adjust settings in `config/settings.py`

## 💡 Pro Tips

1. **Be Specific**: The more detailed your purpose, the better the patterns
2. **Test Thoroughly**: Use the suggested test inputs
3. **Edit Patterns**: Feel free to modify generated patterns
4. **Monitor Stats**: Check which patterns are unused
5. **Export Often**: Save good conversations for reference

---

**Need Help?** Open an issue on GitHub or check the troubleshooting section in README.md
