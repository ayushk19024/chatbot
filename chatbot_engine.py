import re
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Optional: Try importing google generativeai if available
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except:
    GENAI_AVAILABLE = False

# Load API key from .env file
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
if api_key and GENAI_AVAILABLE:
    try:
        genai.configure(api_key=api_key)
    except:
        GENAI_AVAILABLE = False

class ChatbotEngine:
    """Advanced chatbot engine with Gemini AI"""
    
    def __init__(self):
        # Initialize model only if API is available
        self.model = None
        if GENAI_AVAILABLE:
            try:
                # Try multiple models in order of preference
                try:
                    self.model = genai.GenerativeModel('gemini-2.0-flash')
                except:
                    try:
                        self.model = genai.GenerativeModel('gemini-1.5-flash')
                    except:
                        self.model = genai.GenerativeModel('gemini-pro')
            except:
                self.model = None
        
        self.knowledge_base = self._load_knowledge_base()
        self.personality_styles = {
            'friendly': {'prefix': '😊 ', 'tone': 'casual and friendly'},
            'professional': {'prefix': '', 'tone': 'formal and professional'},
            'creative': {'prefix': '✨ ', 'tone': 'creative and playful'},
            'formal': {'prefix': '', 'tone': 'respectful and formal'}
        }
    
    def _load_knowledge_base(self):
        """Load knowledge base for responses"""
        return {
            'greetings': {
                'keywords': ['hello', 'hi', 'hey', 'namaste', 'salaam', 'shukriya'],
                'responses': [
                    'Namaste! Mujhe aap se milkar khushi hui! 👋',
                    'Hey! Main yahan hoon aapki madad karne ke liye! 🤖',
                    'Shukriya poochne ke liye! Main ready hoon! 💪',
                    'Salaam! Kya main kuch kar sakta hoon?'
                ]
            },
            'programming': {
                'keywords': ['python', 'javascript', 'java', 'c++', 'programming', 'coding', 'code'],
                'responses': {
                    'python': [
                        'Python ek powerful aur easy programming language hai! Python machine learning, web development, data science sabmein use hoti hai.',
                        'Python learning ke liye Python.org par ja sakte ho ya YouTube par tutorials dekh sakte ho.',
                        'Python beginner-friendly hai aur syntax bhi bahut simple hai!'
                    ],
                    'javascript': [
                        'JavaScript web development ka heart hai! Ye browser mein chaltaa hai aur interactive websites banate hain.',
                        'Frontend development ke liye JavaScript zaroori hai. React, Vue, Angular jaise frameworks hain.',
                        'JavaScript sikhne se web development ka raasta khul jata hai!'
                    ],
                    'programming': [
                        'Programming sikhne ke liye basics se shuru karo - variables, loops, functions samajho.',
                        'Regular practice karoge toh programming aasan ho jayegi!',
                        'Choose ek language aur usi mein expert ban jao!'
                    ]
                }
            },
            'ai_ml': {
                'keywords': ['ai', 'machine learning', 'deep learning', 'neural', 'tensorflow', 'pytorch', 'data science'],
                'responses': {
                    'machine learning': [
                        'Machine Learning ek aise algorithms use karta hai jo data se seekhte hain aur predictions karate hain.',
                        'ML ke 3 types hain: Supervised Learning, Unsupervised Learning, Reinforcement Learning',
                        'ML seekhne ke liye Python, Math (Linear Algebra, Probability) zaroori hai!'
                    ],
                    'ai': [
                        'Artificial Intelligence ka matlab machine ko human-like intelligence dena.',
                        'AI future ka field hai! ChatGPT, DALL-E ye sab AI examples hain.',
                        'AI seekhne se pehle ML ke fundamentals samajh lo.'
                    ],
                    'data science': [
                        'Data Science = Programming + Statistics + Domain Knowledge',
                        'Data scientist ko data analyze karke insights nikalne hote hain.',
                        'Python, SQL, Pandas, NumPy data science ke essential tools hain!'
                    ]
                }
            },
            'web_development': {
                'keywords': ['web', 'website', 'frontend', 'backend', 'html', 'css', 'react', 'node', 'express'],
                'responses': {
                    'web': [
                        'Web development mein HTML, CSS, JavaScript use hote hain.',
                        'Frontend aur Backend ye dono parts hain web development mein.',
                        'Responsive websites banane ke liye modern CSS frameworks use karo!'
                    ],
                    'frontend': [
                        'Frontend wo part hai jo user ko dikhta hai - UI/UX',
                        'React, Vue, Angular ye popular frontend frameworks hain.',
                        'HTML, CSS, JavaScript frontend development ke basics hain.'
                    ],
                    'backend': [
                        'Backend mein database, server, logic sab hota hai.',
                        'Python (Flask, Django), Node.js, Java ye backend ke liye use hote hain.',
                        'Backend secure aur scalable hona zaroori hai!'
                    ]
                }
            },
            'career': {
                'keywords': ['career', 'job', 'salary', 'internship', 'company', 'interview', 'hiring'],
                'responses': {
                    'career': [
                        'Tech career mein bahut scope hai! Aap front-end, back-end, full-stack, data science choose kar sakte ho.',
                        'Resume strong banao aur portfolio projects banaao!',
                        'Interviews ke liye DSA (Data Structures & Algorithms) important hai.'
                    ],
                    'job': [
                        'Job dhundne ke liye LinkedIn, Indeed, Glassdoor use karo.',
                        'Internships se experience milega aur first job aasan ho jayega.',
                        'Networking bhi important hai - tech communities mein join karo!'
                    ]
                }
            }
        }
    
    def get_response(self, user_message, personality='friendly'):
        """Get response from chatbot using Gemini AI or enhanced knowledge base"""
        try:
            # Try Gemini API first if available
            if self.model and GENAI_AVAILABLE:
                try:
                    # Get personality tone
                    tone = self.personality_styles.get(personality, self.personality_styles['friendly'])['tone']
                    
                    # Create enhanced prompt with better instructions
                    system_prompt = f"""You are an expert tech assistant who specializes in programming, web development, machine learning, and AI.
Your tone should be: {tone}
Important instructions:
- Respond in Hindi-English mix (Hinglish) style
- Provide detailed, informative, and helpful answers
- Give practical examples and tips when relevant
- Be conversational but professional
- Add relevant emojis based on the personality (3-4 max)
- Keep responses clear and well-structured
- If appropriate, break down complex topics into simple parts

User message: {user_message}

Provide a comprehensive and helpful response:"""
                    
                    # Generate response using Gemini with better parameters
                    response = self.model.generate_content(
                        system_prompt,
                        generation_config={
                            'temperature': 0.7,
                            'top_p': 0.9,
                        }
                    )
                    
                    if response and response.text:
                        return response.text.strip()
                except Exception as e:
                    print(f"Gemini API Error: {e}")
                    # Fall through to fallback
            
            # Fallback to knowledge base
            return self._fallback_response(user_message, personality)
                
        except Exception as e:
            # Final fallback
            print(f"Error: {e}")
            return self._fallback_response(user_message, personality)
    
    def _fallback_response(self, user_message, personality='friendly'):
        """Fallback response using knowledge base"""
        user_message_lower = user_message.lower()
        
        # Try smart response first for better quality
        smart_response = self._generate_smart_response(user_message)
        if smart_response:
            return smart_response
        
        # Check for greetings
        if self._matches_keywords(user_message_lower, self.knowledge_base['greetings']['keywords']):
            response = self._get_random_response(self.knowledge_base['greetings']['responses'])
            return response
        
        # Check for programming topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['programming']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['programming']['responses'])
            if response:
                return response
        
        # Check for AI/ML topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['ai_ml']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['ai_ml']['responses'])
            if response:
                return response
        
        # Check for web development topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['web_development']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['web_development']['responses'])
            if response:
                return response
        
        # Check for career topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['career']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['career']['responses'])
            if response:
                return response
        
        # Default response for unknown topics
        default_response = self._generate_default_response(user_message, personality)
        return default_response
    
    def _matches_keywords(self, text, keywords):
        """Check if text contains any keywords"""
        return any(keyword in text for keyword in keywords)
    
    def _get_random_response(self, responses):
        """Get random response from list"""
        import random
        return random.choice(responses)
    
    def _get_specific_response(self, user_message, responses_dict):
        """Get specific response based on detailed keywords"""
        import random
        
        # First try exact matches
        for key, content in responses_dict.items():
            if isinstance(content, list) and any(keyword in user_message for keyword in [key]):
                return random.choice(content)
            elif isinstance(content, dict):
                for sub_key, sub_content in content.items():
                    if isinstance(sub_content, list) and sub_key in user_message:
                        return random.choice(sub_content)
        
        # If no exact match, try partial matches
        for key, content in responses_dict.items():
            if isinstance(content, list):
                for keyword in key.split():
                    if len(keyword) > 2 and keyword in user_message:
                        return random.choice(content)
            elif isinstance(content, dict):
                for sub_key, sub_content in content.items():
                    if isinstance(sub_content, list):
                        for keyword in sub_key.split():
                            if len(keyword) > 2 and keyword in user_message:
                                return random.choice(sub_content)
        
        return None
    
    def _generate_smart_response(self, user_message):
        """Generate smart response using keyword extraction and context"""
        import random
        
        message_lower = user_message.lower()
        
        # Detect intent and context
        if any(word in message_lower for word in ['kaise', 'how', 'sikhun', 'learn', 'seekhun', 'samajhun']):
            # Learning intent
            if 'python' in message_lower:
                steps = [
                    "Python seekhne ke steps:\n1. Basics (variables, loops, functions) sikho\n2. OOPS concepts samajho\n3. Libraries use karna seekho (NumPy, Pandas)\n4. Real projects banao\n5. Practice karte raho!",
                    "Python roadmap:\n→ Fundamentals (syntax, data types)\n→ Functions aur modules\n→ OOP concepts\n→ File handling aur exceptions\n→ Libraries (Requests, BeautifulSoup)\n→ Projects banao!",
                ]
                return random.choice(steps)
            elif 'javascript' in message_lower:
                return "JavaScript sikho:\n1. Basics (variables, operators, loops)\n2. DOM manipulation\n3. ES6+ features (arrow functions, classes)\n4. Async/Await\n5. React/Vue frameworks\n6. Build projects!"
            elif 'web' in message_lower:
                return "Web development ka path:\n1. HTML/CSS fundamentals\n2. JavaScript (vanilla)\n3. Frontend frameworks (React)\n4. Backend (Node.js, Python)\n5. Databases (MongoDB, PostgreSQL)\n6. Deploy karo!"
            else:
                return f"'{user_message}' sikkhne ke liye:\n1. Fundamentals samajho\n2. Online resources/tutorials dekho\n3. Practice problems karo\n4. Real projects banao\n5. Community mein engage raho\n6. Constantly improve karo!"
        
        elif any(word in message_lower for word in ['kya', 'what', 'explain', 'define']):
            # Definition/explanation intent
            if 'machine learning' in message_lower or 'ml' in message_lower:
                return "Machine Learning kya hai?\nMachine Learning = Programs jo data se learn karte hain aur predictions karte hain!\n\nTypes:\n• Supervised Learning (labeled data)\n• Unsupervised Learning (unlabeled data)\n• Reinforcement Learning (trial-error)\n\nCommon algorithms: Linear Regression, Decision Trees, Neural Networks"
            elif 'api' in message_lower:
                return "API (Application Programming Interface) kya hai?\nAPI = ek interface jo alag-alag applications ko communicate karne deta hai!\n\nExample:\nWeather app → Weather API → Weather data\n\nTypes: REST, GraphQL, SOAP\nUse: Data exchange, third-party integration"
            elif 'database' in message_lower or 'sql' in message_lower:
                return "Database kya hai?\nDatabase = organized data ka collection!\n\nTypes:\n• Relational (SQL) - Tables\n• NoSQL - Documents, Key-Value\n• Graph - Relationships\n\nPopular: MySQL, PostgreSQL, MongoDB, Firebase"
            else:
                return f"'{user_message}' ke baare mein basic jaankari:\n\nMain concepts:\n→ Definition aur purpose\n→ Kaise kaam karta hai\n→ Use cases\n→ Benefits aur drawbacks\n→ Real world examples\n\nKya aap more specific detail chaahte ho?"
        
        elif any(word in message_lower for word in ['salary', 'job', 'career', 'work', 'company']):
            return "Tech Career Guide:\n\n1. Entry Level: Intern/Junior Dev\n   → 2-5 LPA (India)\n   → Learn karte raho\n   \n2. Mid Level: Senior Dev (3-5 yrs)\n   → 8-15 LPA\n   → Leadership seekho\n   \n3. Senior: Tech Lead (5+ yrs)\n   → 15-30+ LPA\n   → Architecture decide karo\n\nTips: Portfolio banao, GitHub contribute karo, networking karo!"
        
        elif any(word in message_lower for word in ['hello', 'hi', 'hii', 'hey', 'namaste', 'salaam']):
            greetings = [
                f"Namaste! Welcome to your AI chatbot! 🚀 Kya main aapki help kar sakta hoon?",
                f"Hey there! Main tech topics mein expert hoon! Pooch lo anything about Python, Web Dev, ML, etc.",
                f"Shukriya! Mujhe khushi hui aapse milkar! Tech-related koi bhi sawaal poocho! 💻"
            ]
            return random.choice(greetings)
        
        else:
            # Generic smart response
            return f"'{user_message}' - Interesting question! 🤔\n\nMain topics mein madad kar sakta hoon:\n• Programming (Python, JavaScript)\n• Web Development\n• Machine Learning & AI\n• Data Science\n• Career guidance\n\nKya koi specific topic explore karna chaahte ho?"
    
    def _generate_default_response(self, user_message, personality):
        """Generate default response for unknown topics"""
        import random
        
        # Try smart response generation first
        smart_response = self._generate_smart_response(user_message)
        if smart_response:
            return smart_response
        
        # Fallback default responses
        default_responses = [
            f"Acha, tum pucha: '{user_message}' - Ye bahut interesting sawal hai! 🤔 Kya tum aur details de sakte ho?",
            f"Ye topic ke baare mein main poora jankari rakhta hoon! 📚 Agar aap Python, JavaScript, Machine Learning ya Web Development ke baare mein poochte ho toh main aur help kar sakta hoon.",
            f"Mujhe lagta hai ye ek bahut accha sawal hai! 💡 Kya aap kisi specific tech topic ke baare mein seekhna chahte ho?",
            "Interesting! Agar koi tech-related sawal hai toh main bilkul madad kar sakta hoon! 🚀",
            f"'{user_message}' - Ye ek creative question hai! Tech ke field mein bohot scope hai. Specific topics mein mujhe help lene ke liye pooch! 💻"
        ]
        return random.choice(default_responses)
    
    def _format_with_personality(self, response, personality):
        """Format response according to personality"""
        style = self.personality_styles.get(personality, self.personality_styles['friendly'])
        
        if personality == 'professional':
            # Remove emojis for professional tone
            response = re.sub(r'[😊🤖💪🤔📚💡🚀👋]', '', response)
        elif personality == 'formal':
            # Remove casual language and emojis
            response = re.sub(r'[😊🤖💪🤔📚💡🚀👋✨]', '', response)
            response = response.replace('Acha,', 'Well,').replace('tum', 'you')
        elif personality == 'creative':
            # Add more emojis and creative language
            response = style['prefix'] + response
        
        return response.strip()
