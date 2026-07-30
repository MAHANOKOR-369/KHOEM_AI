#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# app.py — KHOEM_AI 1.0 backend
# Chat (Claude API) + GPS Directions endpoint
# Voice (ស្តាប់/និយាយ) ដំណើរការក្នុង browser ផ្ទាល់ (static/js/voice.js)
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
# Claude API
# ------------------------------------------------------------------------------
def call_claude(messages, system_prompt=""):
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
        text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
        return True, "\n".join(text_blocks)
    except requests.exceptions.RequestException as e:
        logging.error(f"Claude API error: {e}")
        return False, f"មានបញ្ហាក្នុងការភ្ជាប់ទៅ Claude API: {str(e)}"

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
    return jsonify({"status": "online", "system": "khoem_ai", "version": "1.0"})

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    🧠 គិត និងវិភាគ — ចំណុចកណ្តាលនៃការសន្ទនាទាំងអស់
    ទទួលទាំងអត្ថបទវាយធម្មតា និងអត្ថបទដែលបានមកពី voice recognition
    """
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    system_prompt = data.get(
        "system_prompt",
        "អ្នកជាជំនួយការឆ្លាតវៃឈ្មោះ KHOEM_AI ។ ឆ្លើយខ្លីៗច្បាស់លាស់ជាភាសាខ្មែរ "
        "ព្រោះចម្លើយរបស់អ្នកនឹងត្រូវបានអានឮជាសំឡេងផងដែរ។"
    )

    if not session_id or not user_message:
        return jsonify({"error": "session_id និង message ត្រូវការទាំងពីរ"}), 400

    save_message(session_id, "user", user_message)
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
    return jsonify({"session_id": session_id, "messages": get_history(session_id, limit=100)})

@app.route('/api/directions', methods=['POST'])
def directions():
    """
    🗺️ នាំផ្លូវ — ត្រូវការភ្ជាប់ routing API ពិត (Google Directions API,
    OpenRouteService, ឬ Mapbox) ដើម្បីគណនាផ្លូវជាក់ស្តែង។

    ឥឡូវនេះជា STUB (គំរូ) ត្រឡប់សារធម្មតា — ជំហានបន្ទាប់ (KHOEM_AI 1.1)
    ត្រូវភ្ជាប់ជាមួយ routing API ពិត។
    """
    data = request.get_json(silent=True) or {}
    origin = data.get("origin")
    destination = data.get("destination")

    if not origin or not destination:
        return jsonify({"error": "ត្រូវការទាំង origin និង destination"}), 400

    # TODO (KHOEM_AI 1.1): ភ្ជាប់ជាមួយ OpenRouteService ឬ Google Directions API
    # ដើម្បីទទួលបានជំហាននាំផ្លូវពិត (turn-by-turn instructions)
    return jsonify({
        "instruction": f"កំពុងស្វែងរកផ្លូវទៅ {destination}។ (មុខងារនេះកំពុងអភិវឌ្ឍន៍)",
        "origin": origin,
        "destination": destination
    })

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("SERVER_PORT", 5000))
    debug = os.getenv("DEBUG_MODE", "true").lower() == "true"
    print("=" * 50)
    print("  KHOEM_AI 1.0 — Chat + Voice + GPS")
    print(f"  running on: http://0.0.0.0:{port}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=debug)
