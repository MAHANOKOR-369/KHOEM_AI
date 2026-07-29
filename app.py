#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# file_name: app.py
# description: KHOEM_AI backend — Flask + Claude API chat server
# ==============================================================================

import os
import sqlite3
import logging
import datetime
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # ផ្ទុកអថេរពី .env file (API key, config)

# ------------------------------------------------------------------------------
# [1] ការកំណត់មូលដ្ឋាន (Configuration)
# ------------------------------------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

# ⚠️ សំខាន់៖ កុំដាក់ API key ជាអក្សរផ្ទាល់ក្នុងកូដ! ដាក់ក្នុងឯកសារ .env វិញ:
#   ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-6"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

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
# [2] Database — រក្សាទុកប្រវត្តិសន្ទនា
# ------------------------------------------------------------------------------
def init_db():
    """បង្កើតតារាង conversations បើមិនទាន់មាន"""
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
    logging.info("✅ database ready")

def save_message(session_id, role, content):
    """រក្សាទុកសារមួយចូល database"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO conversations (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content, str(datetime.datetime.now()))
        )
        conn.commit()

def get_history(session_id, limit=20):
    """ទាញយកប្រវត្តិសន្ទនាចុងក្រោយសម្រាប់ session មួយ"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            "SELECT role, content FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit)
        )
        rows = [dict(r) for r in c.fetchall()]
        return list(reversed(rows))  # ត្រឡប់តាមលំដាប់ត្រឹមត្រូវ (ចាស់ → ថ្មី)

init_db()

# ------------------------------------------------------------------------------
# [3] Claude API — ភ្ជាប់ទៅ AI
# ------------------------------------------------------------------------------
def call_claude(messages, system_prompt=""):
    """
    ហៅ Claude API ដោយផ្ញើប្រវត្តិសន្ទនា + system prompt
    ត្រឡប់ជា tuple (success: bool, text_or_error: str)
    """
    if not ANTHROPIC_API_KEY:
        return False, "សូមកំណត់ ANTHROPIC_API_KEY ក្នុងឯកសារ .env សិន"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }
    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": messages
    }

    try:
        response = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        text_blocks = [block["text"] for block in data.get("content", []) if block.get("type") == "text"]
        return True, "\n".join(text_blocks)
    except requests.exceptions.RequestException as e:
        logging.error(f"⚠️ Claude API error: {e}")
        return False, f"មានបញ្ហាក្នុងការភ្ជាប់ទៅ Claude API: {str(e)}"

# ------------------------------------------------------------------------------
# [4] Routes — Web pages
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------------------------------------------------------------------
# [5] Routes — API endpoints
# ------------------------------------------------------------------------------
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "system": "khoem_ai_backend",
        "version": "1.0"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint សំខាន់៖ ទទួលសារពីអ្នកប្រើ ហៅ Claude API ហើយត្រឡប់ចម្លើយ

    Request body (JSON):
    {
        "session_id": "user_123",
        "message": "សួស្តី Claude",
        "system_prompt": "អ្នកជាជំនួយការ..."  (ស្រេចចិត្ត)
    }
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    system_prompt = data.get("system_prompt", "អ្នកជាជំនួយការឆ្លាតវៃ ឆ្លើយជាភាសាខ្មែរ។")

    if not session_id or not user_message:
        return jsonify({"error": "session_id និង message ត្រូវការទាំងពីរ"}), 400

    # រក្សាទុកសារអ្នកប្រើ
    save_message(session_id, "user", user_message)

    # ទាញយកប្រវត្តិសន្ទនា ដើម្បីផ្ញើទាំងអស់ទៅ Claude (Claude គ្មានការចងចាំ)
    history = get_history(session_id)
    claude_messages = [{"role": h["role"], "content": h["content"]} for h in history]

    success, reply = call_claude(claude_messages, system_prompt)

    if success:
        save_message(session_id, "assistant", reply)
        return jsonify({"reply": reply, "session_id": session_id})
    else:
        return jsonify({"error": reply}), 502

@app.route('/api/history/<session_id>', methods=['GET'])
def history(session_id):
    """ទាញយកប្រវត្តិសន្ទនាទាំងអស់សម្រាប់ session មួយ"""
    return jsonify({"session_id": session_id, "messages": get_history(session_id, limit=100)})

# ------------------------------------------------------------------------------
# [6] Main entry point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("SERVER_PORT", 5000))
    debug = os.getenv("DEBUG_MODE", "true").lower() == "true"

    print("=" * 60)
    print("  KHOEM_AI backend — Flask + Claude API")
    print(f"  running on: http://0.0.0.0:{port}")
    print("=" * 60)

    app.run(host="0.0.0.0", port=port, debug=debug)
