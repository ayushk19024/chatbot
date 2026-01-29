#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test improved chatbot responses"""

from chatbot_engine import ChatbotEngine
import sys
import io

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_chatbot():
    bot = ChatbotEngine()
    
    print("\n" + "="*70)
    print("IMPROVED CHATBOT WITH SMART RESPONSES")
    print("="*70 + "\n")
    
    # Test questions
    test_questions = [
        ("Python kaise sikhun?", "friendly"),
        ("Machine Learning kya hai?", "friendly"),
        ("Web development kaise seekhun?", "professional"),
        ("JavaScript explain karo", "creative"),
        ("Career guidance do", "friendly"),
        ("Hello!", "friendly"),
    ]
    
    for question, personality in test_questions:
        print(f"Q: {question}")
        print(f"Mode: {personality}")
        print("-" * 70)
        response = bot.get_response(question, personality)
        print(response)
        print("\n")

if __name__ == "__main__":
    test_chatbot()
