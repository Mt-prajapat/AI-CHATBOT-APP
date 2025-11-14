import math
import re
import sympy as sp
from sympy import symbols, solve, diff, integrate, limit, oo
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import random
from transformers import pipeline

class SmartChatBot:
    def __init__(self):
        self.load_training_data()
        self.setup_ai_models()
        self.setup_mathematical_functions()
        self.vectorizer = TfidfVectorizer()
        self.train_tfidf()
    
    def load_training_data(self):
        try:
            with open('training_data.json', 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
            
            self.patterns = []
            self.responses = []
            
            for intent in self.training_data['intents']:
                for pattern in intent['patterns']:
                    self.patterns.append(pattern)
                    self.responses.append(intent['responses'])
        except FileNotFoundError:
            print("Warning: training_data.json not found. Using default responses.")
            self.patterns = ["hello", "hi", "how are you"]
            self.responses = [["Hello!", "Hi there!", "Hey!"]]
    
    def setup_ai_models(self):
        try:
            # Setup sentiment analysis
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            
            # Setup text generation
            try:
                self.generator = pipeline("text-generation", model="microsoft/DialoGPT-small")
            except:
                print("DialoGPT model not available, using fallback responses")
                self.generator = None
        except Exception as e:
            print(f"Error setting up AI models: {e}")
            self.sentiment_analyzer = None
            self.generator = None
    
    def setup_mathematical_functions(self):
        self.math_patterns = {
            'arithmetic': r'(\d+\.?\d*)\s*([+\-*/^])\s*(\d+\.?\d*)',
            'equation': r'solve\s+(.+)',
            'derivative': r'derivative\s+of\s+(.+)',
            'integral': r'integral\s+of\s+(.+)',
            'limit': r'limit\s+of\s+(.+)',
            'divide_by_zero': r'(\d+)\s*/\s*0',
            'zero_by_zero': r'0\s*/\s*0'
        }
    
    def train_tfidf(self):
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.patterns)
        except:
            # Fallback if no training data
            self.tfidf_matrix = None
    
    def get_rule_based_response(self, user_input):
        if self.tfidf_matrix is None:
            return None
            
        try:
            user_input_vec = self.vectorizer.transform([user_input])
            similarities = cosine_similarity(user_input_vec, self.tfidf_matrix)
            best_match_idx = np.argmax(similarities)
            
            if similarities[0, best_match_idx] > 0.3:
                return random.choice(self.responses[best_match_idx])
        except:
            pass
        return None
    
    def get_ai_response(self, user_input):
        if self.generator:
            try:
                response = self.generator(
                    user_input, 
                    max_length=100, 
                    num_return_sequences=1,
                    pad_token_id=50256
                )
                return response[0]['generated_text']
            except:
                pass
        return None
    
    def solve_math_problem(self, problem):
        problem_lower = problem.lower()
        
        # Check for divide by zero cases first
        if re.search(r'0\s*/\s*0', problem_lower):
            return "0/0 is an indeterminate form. 🚫\nIn mathematics, 0 divided by 0 is undefined and considered an indeterminate form.\nThis means it could potentially equal any number, depending on the context."
        
        if re.search(r'(\d+)\s*/\s*0', problem_lower):
            match = re.search(r'(\d+)\s*/\s*0', problem_lower)
            if match:
                number = match.group(1)
                return f"{number}/0 is undefined! ❌\nDivision by zero is undefined in mathematics.\nAs the denominator approaches zero, the value approaches infinity."
        
        # Try basic arithmetic
        try:
            # Remove spaces and evaluate safely
            clean_expr = problem.replace(' ', '').replace('^', '**')
            
            # Basic arithmetic operations
            if re.match(r'^[\d+\-*/().\s]+$', clean_expr):
                result = eval(clean_expr)
                return f"Calculation: {problem} = {result}"
        except:
            pass
        
        # Try to handle other math problems
        if any(word in problem_lower for word in ['calculate', 'solve', 'what is']):
            numbers = re.findall(r'\d+', problem)
            if len(numbers) >= 2:
                if '+' in problem:
                    result = int(numbers[0]) + int(numbers[1])
                    return f"Addition: {numbers[0]} + {numbers[1]} = {result}"
                elif '-' in problem:
                    result = int(numbers[0]) - int(numbers[1])
                    return f"Subtraction: {numbers[0]} - {numbers[1]} = {result}"
                elif '*' in problem:
                    result = int(numbers[0]) * int(numbers[1])
                    return f"Multiplication: {numbers[0]} × {numbers[1]} = {result}"
                elif '/' in problem:
                    if numbers[1] != '0':
                        result = int(numbers[0]) / int(numbers[1])
                        return f"Division: {numbers[0]} ÷ {numbers[1]} = {result}"
        
        return None
    
    def analyze_sentiment(self, text):
        if self.sentiment_analyzer:
            try:
                result = self.sentiment_analyzer(text)[0]
                return result['label'], result['score']
            except:
                pass
        return "NEUTRAL", 0.5
    
    def process_message(self, user_input):
        # Get sentiment
        sentiment, confidence = self.analyze_sentiment(user_input)
        
        # Check if it's a math problem first
        math_solution = self.solve_math_problem(user_input)
        if math_solution:
            return {
                "response": math_solution,
                "type": "problem_solution_mathematics",
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "solution_details": {"type": "mathematics"}
            }
        
        # Try rule-based response
        response = self.get_rule_based_response(user_input)
        response_type = "rule_based"
        
        # Fallback to AI model
        if not response and self.generator:
            response = self.get_ai_response(user_input)
            response_type = "ai_generated"
        
        # Final fallback
        if not response:
            response = random.choice([
                "I'm still learning. Can you rephrase that?",
                "That's interesting! Tell me more.",
                "I'm not sure I understand. Could you explain differently?",
                "Let me think about that... Actually, could you ask me something else?"
            ])
            response_type = "fallback"
        
        return {
            "response": response,
            "type": response_type,
            "sentiment": sentiment,
            "confidence": round(confidence, 2)
        }