from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os
import json
import random
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import pipeline

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

try:
    from ai_solver import AdvancedProblemSolver
    print("✅ AdvancedProblemSolver imported successfully!")
except ImportError as e:
    print(f"❌ Import error for AdvancedProblemSolver: {e}")
    AdvancedProblemSolver = None

class EnhancedChatBot:
    def __init__(self):
        self.load_training_data()
        self.setup_ai_models()
        self.problem_solver = AdvancedProblemSolver() if AdvancedProblemSolver else None
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
            print("❌ training_data.json not found. Using fallback data.")
            self.training_data = {"intents": []}
            self.patterns = ["hello", "hi", "how are you"]
            self.responses = [["Hello!", "Hi there!", "Hey!"]]
        except Exception as e:
            print(f"❌ Error loading training data: {e}")
            self.training_data = {"intents": []}
            self.patterns = ["hello", "hi", "how are you"]
            self.responses = [["Hello!", "Hi there!", "Hey!"]]
    
    def setup_ai_models(self):
        try:
            # Setup sentiment analysis
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            print("✅ Sentiment analyzer initialized successfully!")
        except Exception as e:
            print(f"❌ Error setting up sentiment analyzer: {e}")
            self.sentiment_analyzer = None
        
        # Setup text generation
        try:
            self.generator = pipeline("text-generation", model="microsoft/DialoGPT-small")
            print("✅ Text generator initialized successfully!")
        except Exception as e:
            print(f"❌ Error setting up text generator: {e}")
            self.generator = None
    
    def train_tfidf(self):
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.patterns)
            print("✅ TF-IDF model trained successfully!")
        except Exception as e:
            print(f"❌ Error training TF-IDF: {e}")
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
        except Exception as e:
            print(f"❌ Error in rule-based response: {e}")
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
            except Exception as e:
                print(f"❌ Error generating AI response: {e}")
        return None
    
    def solve_problem(self, user_input):
        """Enhanced problem solving for mathematical and logical queries"""
        if self.problem_solver:
            try:
                return self.problem_solver.solve_general_problem(user_input)
            except Exception as e:
                print(f"❌ Error in problem solver: {e}")
        
        # Fallback problem solving
        return {
            'answer': 'Problem solver not available',
            'explanation': 'The advanced problem solver is currently unavailable. Please try a simpler query.',
            'type': 'fallback'
        }
    
    def analyze_sentiment(self, text):
        if self.sentiment_analyzer:
            try:
                result = self.sentiment_analyzer(text)[0]
                return result['label'], result['score']
            except Exception as e:
                print(f"❌ Error in sentiment analysis: {e}")
        return "NEUTRAL", 0.5
    
    def process_message(self, user_input):
        # Get sentiment
        sentiment, confidence = self.analyze_sentiment(user_input)
        
        # Check if it's a problem to solve
        problem_keywords = ['solve', 'calculate', 'what is', 'how to', 'why does', 'explain']
        is_problem = any(keyword in user_input.lower() for keyword in problem_keywords)
        
        if is_problem and self.problem_solver:
            try:
                problem_solution = self.solve_problem(user_input)
                return {
                    "response": f"🤔 {problem_solution['answer']}\n💡 {problem_solution['explanation']}",
                    "type": f"problem_solution_{problem_solution['type']}",
                    "sentiment": sentiment,
                    "confidence": round(confidence, 2),
                    "solution_details": problem_solution
                }
            except Exception as e:
                print(f"❌ Error processing problem: {e}")
        
        # Try rule-based first
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
                "Let me think about that... Actually, could you ask me something else?",
                "I'm constantly learning! Could you provide more context?"
            ])
            response_type = "fallback"
        
        return {
            "response": response,
            "type": response_type,
            "sentiment": sentiment,
            "confidence": round(confidence, 2)
        }

# Initialize enhanced chatbot
try:
    chatbot = EnhancedChatBot()
    print("✅ EnhancedChatBot initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing EnhancedChatBot: {e}")
    
    # Fallback chatbot
    class FallbackChatBot:
        def process_message(self, user_input):
            return {
                "response": "Chatbot is experiencing technical difficulties. Please try again later.",
                "type": "error",
                "sentiment": "NEUTRAL", 
                "confidence": 0.0
            }
    
    chatbot = FallbackChatBot()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        bot_response = chatbot.process_message(user_message)
        
        return jsonify({
            "user_message": user_message,
            "bot_response": bot_response['response'],
            "response_type": bot_response['type'],
            "sentiment": bot_response['sentiment'],
            "confidence": round(bot_response['confidence'], 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "solution_details": bot_response.get('solution_details', {})
        })
    
    except Exception as e:
        print(f"❌ Error in /chat endpoint: {e}")
        return jsonify({
            "error": "Internal server error",
            "user_message": user_message if 'user_message' in locals() else "Unknown",
            "bot_response": "Sorry, I encountered an error processing your message.",
            "response_type": "error",
            "sentiment": "NEUTRAL",
            "confidence": 0.0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 500

@app.route('/solve', methods=['POST'])
def solve_problem():
    """Dedicated endpoint for problem solving"""
    try:
        data = request.get_json()
        problem = data.get('problem', '').strip()
        
        if not problem:
            return jsonify({"error": "Empty problem"}), 400
        
        solution = chatbot.solve_problem(problem)
        
        return jsonify({
            "problem": problem,
            "solution": solution,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    except Exception as e:
        print(f"❌ Error in /solve endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy", 
        "service": "Enhanced AI Chatbot API",
        "capabilities": [
            "Natural language conversation",
            "Mathematical problem solving",
            "Physics and science explanations",
            "Programming assistance",
            "Logical reasoning",
            "Unit conversions",
            "Time and date calculations"
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify the chatbot is working"""
    try:
        test_response = chatbot.process_message("Hello")
        return jsonify({
            "status": "working",
            "test_response": test_response
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced AI Chatbot Server...")
    print("📡 Server will be available at: http://localhost:5001")
    print("🔗 Make sure your frontend is configured to connect to port 5001")
    print("💡 Check the console for initialization status...")
    app.run(debug=True, host='0.0.0.0', port=5001)