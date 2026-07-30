#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# app.py — KHOEM_AI backend (Groq API version — ឥតគិតថ្លៃ)
# ==============================================================================

import os
import sqlite3
import logging
import datetime
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------
# Groq API configuration — ចុះឈ្មោះឥតគិតថ្លៃនៅ console.groq.com
# ------------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"  # model ឥតគិតថ្លៃដ៏ខ្លាំងបំផុតរបស់ Groq
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

DB_PATH = os.path.join(base_dir, "database", "khoem_ai.db")
os.makedirs(os.path.join(base_dir, "database"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [khoem_ai] - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(base_dir, "logs", "system.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

def save_message(session_id, role, content):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO conversations (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content, str(datetime.datetime.now()))
        )
        conn.commit()

def get_history(session_id, limit=20):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            "SELECT role, content FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit)
        )
        rows = [dict(r) for r in c.fetchall()]
        return list(reversed(rows))

init_db()

# ------------------------------------------------------------------------------
# Groq API — ប្រើទម្រង់ស្រដៀង OpenAI (chat completions)
# ------------------------------------------------------------------------------
def call_groq(messages, system_prompt=""):
    """
    ហៅ Groq API (ឥតគិតថ្លៃ) ជំនួស Claude API
    Groq ប្រើទម្រង់ស្រដៀង OpenAI: messages array ជាមួយ role "system"/"user"/"assistant"
    """
    if not GROQ_API_KEY:
        return False, "សូមកំណត់ GROQ_API_KEY ក្នុងឯកសារ .env សិន"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    # Groq ដាក់ system prompt ជា message ដំបូងក្នុង array (មិនដាច់ដោយឡែកដូច Claude)
    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    payload = {
        "model": GROQ_MODEL,
        "messages": full_messages,
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        reply_text = data["choices"][0]["message"]["content"]
        return True, reply_text
    except requests.exceptions.RequestException as e:
        logging.error(f"Groq API error: {e}")
        # បង្ហាញ error message លម្អិតជាងដើម្បីជួយ debug (ឧ. key ខុស, rate limit)
        error_detail = ""
        try:
            error_detail = response.json().get("error", {}).get("message", "")
        except Exception:
            pass
        return False, f"មានបញ្ហាក្នុងការភ្ជាប់ទៅ Groq API: {str(e)} {error_detail}"

# ------------------------------------------------------------------------------
# Routes — Pages
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------------------------------------------------------------
# Routes — API
# ------------------------------------------------------------------------------
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"status": "online", "system": "khoem_ai", "version": "1.0-groq"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    system_prompt = data.get(
        "system_prompt",
        "អ្នកជាជំនួយការឆ្លាតវៃឈ្មោះ KHOEM_AI ។ ឆ្លើយខ្លីៗច្បាស់លាស់ជាភាសាខ្មែរ។"
    )

    if not session_id or not user_message:
        return jsonify({"error": "session_id និង message ត្រូវការទាំងពីរ"}), 400

    save_message(session_id, "user", user_message)
    history = get_history(session_id)
    groq_messages = [{"role": h["role"], "content": h["content"]} for h in history]

    success, reply = call_groq(groq_messages, system_prompt)

    if success:
        save_message(session_id, "assistant", reply)
        return jsonify({"reply": reply, "session_id": session_id})
    else:
        return jsonify({"error": reply}), 502

@app.route('/api/history/<session_id>', methods=['GET'])
def history(session_id):
    return jsonify({"session_id": session_id, "messages": get_history(session_id, limit=100)})

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("SERVER_PORT", 5000))
    debug = os.getenv("DEBUG_MODE", "true").lower() == "true"
    print("=" * 50)
    print("  KHOEM_AI backend — Groq API (ឥតគិតថ្លៃ)")
    print(f"  running on: http://0.0.0.0:{port}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=debug)
