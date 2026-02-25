import re
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import google.genai as genai

class ChatbotEngine:
    """Advanced chatbot engine with NLP-like features"""
    
    def __init__(self):
        load_dotenv()
        self.knowledge_base = self._load_knowledge_base()
        self.personality_styles = {
            'friendly': {'prefix': '😊 ', 'tone': 'casual'},
            'professional': {'prefix': '', 'tone': 'formal'},
            'creative': {'prefix': '✨ ', 'tone': 'creative'},
            'formal': {'prefix': '', 'tone': 'respectful'}
        }
        
        # Configure Google Gemini API
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
    
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
        """Generate response based on user message"""
        # Try AI response first if API is available
        if self.client:
            try:
                prompt = f"You are a helpful AI assistant. Respond in Hindi language. Be {personality} in tone. User message: {user_message}"
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash-exp',
                    contents=prompt
                )
                ai_response = response.text.strip()
                return self._format_with_personality(ai_response, personality)
            except Exception as e:
                print(f"API Error: {e}")
                # Fall back to knowledge base
        
        # Fallback to knowledge base
        user_message_lower = user_message.lower()
        
        # Check for greetings
        if self._matches_keywords(user_message_lower, self.knowledge_base['greetings']['keywords']):
            response = self._get_random_response(self.knowledge_base['greetings']['responses'])
            return self._format_with_personality(response, personality)
        
        # Check for programming topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['programming']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['programming'], personality)
            if response:
                return response
        
        # Check for AI/ML topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['ai_ml']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['ai_ml'], personality)
            if response:
                return response
        
        # Check for web development topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['web_development']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['web_development'], personality)
            if response:
                return response
        
        # Check for career topics
        if self._matches_keywords(user_message_lower, self.knowledge_base['career']['keywords']):
            response = self._get_specific_response(user_message_lower, self.knowledge_base['career'], personality)
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
    
    def _get_specific_response(self, user_message, knowledge_section, personality):
        """Get specific response based on detailed keywords"""
        for key, content in knowledge_section.items():
            if key == 'keywords':
                continue
            if any(keyword in user_message for keyword in [key] + content.get('keywords', [])):
                responses = content if isinstance(content, list) else content.get('responses', [])
                if responses:
                    response = self._get_random_response(responses)
                    return self._format_with_personality(response, personality)
        return None
    
    def _generate_default_response(self, user_message, personality):
        """Generate default response for unknown topics"""
        default_responses = [
            f"Acha, tum pucha: '{user_message}' - Ye bahut interesting sawal hai! 🤔 Kya tum aur details de sakte ho?",
            f"Ye topic ke baare mein main poora jankari rakhta hoon! 📚 Agar aap Python, JavaScript, Machine Learning ya Web Development ke baare mein poochte ho toh main aur help kar sakta hoon.",
            f"Mujhe lagta hai ye ek bahut accha sawal hai! 💡 Kya aap kisi specific topic ke baare mein seekhna chahte ho?",
            "Interesting! Agar koi tech-related sawal hai toh main bilkul madad kar sakta hoon! 🚀"
        ]
        import random
        response = random.choice(default_responses)
        return self._format_with_personality(response, personality)
    
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
