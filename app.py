#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# app.py — KHOEM_AI 2.0 backend
# Chat + GPS Directions + Vision (Photo Analysis)
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
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_VISION_MODEL = "llama-3.2-90b-vision-preview"
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
# Groq — Chat
# ------------------------------------------------------------------------------
def call_groq(messages, system_prompt=""):
    if not GROQ_API_KEY:
        return False, "sorm kamnot GROQ_API_KEY knong ekasar .env sen"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

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
        return True, data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Groq API error: {e}")
        return False, f"panha phcheab tow Groq API: {str(e)}"

# ------------------------------------------------------------------------------
# Groq — Vision (Photo Analysis)
# ------------------------------------------------------------------------------
def call_groq_vision(image_base64, question, mime_type="image/jpeg"):
    if not GROQ_API_KEY:
        return False, "sorm kamnot GROQ_API_KEY moun sen"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": GROQ_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}
                    }
                ]
            }
        ],
        "max_tokens": 1024
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return True, data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Groq Vision API error: {e}")
        return False, f"panha vipheak roub pheap: {str(e)}"

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
    return jsonify({"status": "online", "system": "khoem_ai", "version": "2.0-groq"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    user_message = data.get("message", "").strip()
    system_prompt = data.get(
        "system_prompt",
        "anak ja chomnuoyka chlatvei chhmuoh KHOEM_AI. chhlaey khley khley chbas chbas ja pheasa khmer."
    )

    if not session_id or not user_message:
        return jsonify({"error": "session_id ning message trauvkar teang pi"}), 400

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

@app.route('/api/directions', methods=['POST'])
def directions():
    data = request.get_json(silent=True) or {}
    origin = data.get("origin")
    destination = data.get("destination")

    if not origin or not destination:
        return jsonify({"error": "trauvkar teang origin ning destination"}), 400

    return jsonify({
        "instruction": f"komporng svengrok plov tow {destination}. (feature kompong aphivotdn)",
        "origin": origin,
        "destination": destination
    })

@app.route('/api/vision', methods=['POST'])
def vision():
    """
    👁️ mueil — totuol roub pheap (base64) + samnuor -> trolop kar vipheak
    """
    data = request.get_json(silent=True) or {}
    image_b64 = data.get("image", "")
    question = data.get("question", "sorm piponnea roub pheap nis ja pheasa khmer")
    mime_type = data.get("mime_type", "image/jpeg")

    if not image_b64:
        return jsonify({"error": "trauvkar image (base64)"}), 400

    success, answer = call_groq_vision(image_b64, question, mime_type)

    if success:
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": answer}), 502

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("SERVER_PORT", 5000))
    debug = os.getenv("DEBUG_MODE", "true").lower() == "true"
    print("=" * 50)
    print("  KHOEM_AI 2.0 - Chat + Voice + GPS + Vision")
    print(f"  running on: http://0.0.0.0:{port}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=debug)
