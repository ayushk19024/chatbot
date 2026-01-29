#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple test script for chatbot responses"""

from chatbot_engine import ChatbotEngine
import sys
import io

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_chatbot():
    bot = ChatbotEngine()
    
    # Test questions
    test_questions = [
        ("Namaste!", "friendly"),
        ("Python kaise sikhoon?", "friendly"),
        ("Machine Learning kya hai?", "friendly"),
        ("Web development mein kya sikhmum?", "professional"),
        ("JavaScript explain karo", "creative"),
    ]
    
    print("\n" + "="*60)
    print("CHATBOT TEST RESPONSES")
    print("="*60 + "\n")
    
    for question, personality in test_questions:
        print(f"Q: {question}")
        print(f"Personality: {personality}")
        response = bot.get_response(question, personality)
        print(f"A: {response}")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    test_chatbot()
