#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Direct API test without Flask"""

from chatbot_engine import ChatbotEngine
import json
import sys
import io

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

bot = ChatbotEngine()

# Test different questions
questions = [
    ("Python kaise sikhun?", "friendly"),
    ("JavaScript kya hai?", "professional"),
    ("Machine Learning explain karo", "friendly"),
]

print("\n" + "="*70)
print("DIRECT CHATBOT API TEST")
print("="*70 + "\n")

for q, personality in questions:
    response = bot.get_response(q, personality)
    print(f"Q: {q}")
    print(f"Personality: {personality}")
    print(f"Response: {response}")
    print("\n" + "-"*70 + "\n")

print("✅ All tests completed successfully!")
print("\nNow you can run: python app.py")
print("Then visit: http://127.0.0.1:5000 in your browser")
