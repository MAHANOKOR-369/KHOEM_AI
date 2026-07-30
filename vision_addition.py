#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# vision_addition.py — KHOEM_AI 2.0: 👁️ មើល (Camera/Photo Analysis)
# ==============================================================================
#
# Groq មាន vision model ដែលអាចមើលរូបភាព + ឆ្លើយសំណួរអំពីវា
# ត្រូវការបញ្ចូល base64 image ចូល message content
#
# របៀបប្រើ: copy function និង route ខាងក្រោមទៅដាក់ក្នុង app.py
# ==============================================================================

import base64

# ត្រូវប្រើ model ដែលគាំទ្រ vision — ពិនិត្យ console.groq.com/docs/models
# សម្រាប់ model ចុងក្រោយបំផុតដែលអាចប្រើបាន
GROQ_VISION_MODEL = "llama-3.2-90b-vision-preview"


def call_groq_vision(image_base64, question, mime_type="image/jpeg"):
    """
    ផ្ញើរូបភាព (base64) + សំណួរ ទៅ Groq vision model
    ត្រឡប់ជា (success: bool, answer_text: str)
    """
    if not GROQ_API_KEY:
        return False, "សូមកំណត់ GROQ_API_KEY ជាមុនសិន"

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
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_base64}"
                        }
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
        answer = data["choices"][0]["message"]["content"]
        return True, answer
    except requests.exceptions.RequestException as e:
        logging.error(f"Groq Vision API error: {e}")
        error_detail = ""
        try:
            error_detail = response.json().get("error", {}).get("message", "")
        except Exception:
            pass
        return False, f"មានបញ្ហាវិភាគរូបភាព: {str(e)} {error_detail}"


# ==============================================================================
# Route ថ្មី — ដាក់ក្នុង app.py (ក្រោម route /api/chat ដែលមានស្រាប់)
# ==============================================================================
"""
@app.route('/api/vision', methods=['POST'])
def vision():
    '''
    👁️ មើល — ទទួលរូបភាព (base64) + សំណួរ → ត្រឡប់ការវិភាគ
    Request body (JSON):
    {
        "image": "base64_string_without_prefix",
        "question": "នេះជាអ្វី?",
        "mime_type": "image/jpeg"  (ស្រេចចិត្ត)
    }
    '''
    data = request.get_json(silent=True) or {}
    image_b64 = data.get("image", "")
    question = data.get("question", "សូមពិពណ៌នារូបភាពនេះជាភាសាខ្មែរ")
    mime_type = data.get("mime_type", "image/jpeg")

    if not image_b64:
        return jsonify({"error": "ត្រូវការ image (base64)"}), 400

    success, answer = call_groq_vision(image_b64, question, mime_type)

    if success:
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": answer}), 502
"""
