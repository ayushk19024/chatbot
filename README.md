# Advanced Personal Chatbot 🤖

A modern, smooth, and advanced chatbot application with **Python backend** and beautiful frontend UI.

## ✨ Features

### 🎨 Beautiful UI
- Modern, responsive design
- Dark mode support
- Smooth animations and transitions
- Mobile-friendly interface
- Professional color scheme

### 🧠 Smart AI Responses
- **Python backend** with NLP-like response engine
- Knowledge base for multiple topics (Python, JavaScript, ML, Web Development, Careers)
- Personality-aware responses
- Real answer generation (not random!)
- Context-aware messaging

### 🧠 Personalization
- Multiple personality presets (Friendly, Professional, Creative, Formal)
- Adjustable response length
- Adjustable knowledge level
- Emoji usage control
- Real-time preview of settings

### 💬 Chat Features
- Real-time message sending/receiving
- Typing indicator animations
- Message history with timestamps
- Auto-save conversations
- Export conversations as JSON
- Smooth message animations
- Python backend API integration

### ⚙️ Advanced Settings
- Dark mode toggle
- Sound notifications
- Auto-save conversations
- Animation effects control
- Clear conversation history
- Export functionality

### ⌨️ Keyboard Shortcuts
- `Ctrl+K` - Focus input
- `Ctrl+D` - Toggle dark mode
- `Enter` - Send message

## 🚀 Setup & Installation

### Step 1: Install Python Dependencies

```bash
cd "e:\MY PROJECTS\2.CHATBOT"
pip install -r requirements.txt
```

Or manually install:
```bash
pip install flask flask-cors python-dotenv
```

### Step 2: Start the Python Backend

```bash
cd "e:\MY PROJECTS\2.CHATBOT"
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Open the Frontend

Open `index.html` in your browser or use a local server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (if you have http-server)
npx http-server
```

Then visit: `http://localhost:8000`

## 📁 Project Structure

```
chatbot/
├── index.html           # Frontend UI
├── styles.css           # Styling & animations
├── script.js            # Frontend JavaScript + API calls
├── app.py              # Flask backend server
├── chatbot_engine.py   # AI response generation engine
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 💬 How to Use

### Chatting
1. Open the chatbot in your browser
2. Make sure Python backend is running (should say "✅ Backend connected" in console)
3. Type your question in the chat box
4. Get smart, context-aware responses!

### Topics You Can Ask About
- **Python:** Python language, syntax, libraries, Django, Flask, etc.
- **JavaScript:** JS fundamentals, frameworks (React, Vue), DOM, async/await
- **Machine Learning:** ML concepts, TensorFlow, PyTorch, Neural Networks
- **Web Development:** HTML, CSS, Frontend, Backend, REST APIs
- **Career:** Tech careers, job hunting, internships, interviews

### Example Questions
- "Python ke baare mein batao" 
- "JavaScript kya hai?"
- "Machine Learning seekhne se pehle kya seekhna chahiye?"
- "Data Science career guidance dedo"
- "Web development mein career kaun se skills chahiye?"

### Personalizing Your Bot
1. Click **Personality** tab
2. Choose your preferred tone and settings
3. Bot will respond accordingly!

## 🔧 How It Works

### Frontend (JavaScript)
1. User types a message
2. Message sent to Python backend via REST API
3. Typing indicator shown
4. Response received and displayed

### Backend (Python)
1. Flask API receives the message
2. ChatbotEngine analyzes the text
3. Searches knowledge base for relevant info
4. Generates context-aware response
5. Returns response with personality applied
6. All responses are real, not random!

### Knowledge Base
The bot has information about:
- Greetings and casual chat
- Programming languages and concepts
- Web development technologies
- Machine Learning and AI
- Career guidance and tech jobs

## 🎯 Bot Personalities

### 1. Friendly & Casual
- Warm and approachable
- Hindi-English mix (Hinglish)
- Uses emojis
- Perfect for everyday chat

### 2. Professional
- Formal language
- Minimal emojis
- Business-like tone
- Great for technical discussions

### 3. Creative & Playful
- Imaginative responses
- Lots of emojis
- Fun and engaging
- Perfect for brainstorming

### 4. Formal & Respectful
- Respectful communication
- No emojis
- Traditional approach
- Ideal for formal topics

## 💾 Data Storage

- **Frontend:** Uses LocalStorage for settings and conversation history
- **Backend:** Stores nothing (stateless API)
- All data stays on your computer!

## 🎨 Customization

### Adding More Knowledge
Edit `chatbot_engine.py` and add to `_load_knowledge_base()`:

```python
'new_topic': {
    'keywords': ['keyword1', 'keyword2'],
    'responses': [
        'Your response here',
    ]
}
```

### Changing Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    /* ... */
}
```

## 🌐 Technology Stack

- **Frontend:** HTML5, CSS3 (Grid, Flexbox, Animations), ES6+ JavaScript
- **Backend:** Python 3, Flask, Flask-CORS
- **API:** REST API with JSON
- **Storage:** LocalStorage (browser)

## 🐍 Python Dependencies

- `flask` - Web framework
- `flask-cors` - Enable CORS for frontend
- `python-dotenv` - Environment variables (optional)

## ✅ Troubleshooting

### "Backend not running" message
- Make sure you started `python app.py`
- Check if Flask is listening on port 5000
- Check console for errors

### CORS errors in browser console
- Make sure `flask-cors` is installed
- Backend must be running on http://localhost:5000

### No responses from bot
- Check Python backend is running
- Check network tab in browser dev tools
- If backend failed, fallback to offline mode

### Port 5000 already in use
```bash
# Change port in app.py (last line):
app.run(debug=True, port=5001)  # Use different port

# Update API_URL in script.js:
const API_URL = 'http://localhost:5001/api';
```

## 🚀 Future Enhancements

- Add more topics to knowledge base
- Integrate with real AI APIs (OpenAI, Hugging Face)
- Add voice input/output
- Database integration for conversation history
- User authentication
- Multi-language support
- Advanced NLP with NLTK or spaCy

## 📝 License

Free to use for personal and educational purposes.

---

**Made with ❤️ for better conversations!**

Now your chatbot gives **real answers** from Python backend! 🐍 + 💻 = 🚀

