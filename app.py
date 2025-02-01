from flask import Flask, request, jsonify, render_template
import openai
import json
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import time
import logging
from openai.error import RateLimitError, OpenAIError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client.faq_assistant
logs_collection = db.logs

# Load knowledge base
with open("knowledge_base/faq.json", "r") as f:
    knowledge_base = json.load(f)["faqs"]

# Token Bucket for Rate Limiting
class TokenBucket:
    def __init__(self, tokens, refill_rate, refill_period):
        self.max_tokens = tokens
        self.tokens = tokens
        self.refill_rate = refill_rate
        self.refill_period = refill_period
        self.last_refill_time = time.time()

    def consume(self, tokens_to_consume):
        now = time.time()
        elapsed_time = now - self.last_refill_time
        self.tokens = min(self.max_tokens, self.tokens + (self.refill_rate * elapsed_time))
        self.last_refill_time = now

        if self.tokens >= tokens_to_consume:
            self.tokens -= tokens_to_consume
            return True
        else:
            return False

# Adjust Rate Limiting Configuration (Increased Capacity & Refill Speed)
rate_limiter = TokenBucket(tokens=20, refill_rate=5, refill_period=1)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Function to fetch answer from FAQ file
def get_answer_from_faq(question):
    for faq in knowledge_base:
        if faq["question"].lower() == question.lower():
            return faq["answer"]
    return "Sorry, I couldn't find an answer to your question."

# API endpoint to handle queries
@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # Rate limiting check
    if not rate_limiter.consume(1):
        logger.warning("Rate limit exceeded! Tokens remaining: %.2f", rate_limiter.tokens)
        return jsonify({"error": "Too many requests. Please wait before trying again."}), 429
    
    if api_key:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful FAQ assistant."},
                    {"role": "user", "content": user_query},
                ],
            )
            
            logger.info("User Query: %s", user_query)
            logger.info("OpenAI API Response: %s", response)

            answer = response["choices"][0]["message"]["content"]
        except RateLimitError:
            logger.error("OpenAI Rate Limit Exceeded!")
            answer = "OpenAI rate limit exceeded. Please try again later."
        except OpenAIError as e:
            logger.error("OpenAI API Error: %s", str(e))
            answer = "An error occurred while processing your request."
        except Exception as e:
            logger.error("Unexpected Error: %s", str(e))
            answer = "An unexpected error occurred."
    else:
        answer = get_answer_from_faq(user_query)

    return jsonify({"response": answer})

# Admin route to update knowledge base
@app.route("/admin/update_kb", methods=["POST"])
def update_kb():
    try:
        new_kb = request.json.get("knowledge_base")
        with open("knowledge_base/faq.json", "w") as f:
            json.dump(new_kb, f)
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error("Error updating knowledge base: %s", str(e))
        return jsonify({"error": "Failed to update knowledge base"}), 500

# Admin route to view logs
@app.route("/admin/logs", methods=["GET"])
def view_logs():
    try:
        logs = list(logs_collection.find({}, {"_id": 0}))
        return jsonify(logs)
    except Exception as e:
        logger.error("Error retrieving logs: %s", str(e))
        return jsonify({"error": "Failed to retrieve logs"}), 500

if __name__ == "__main__":
    app.run(debug=True)
