#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# file_name: app.py
# description: mahanokor matrix systems - sovereign swarm engine core
# owner: deity khoem soksivutha | sign: 906.106.905
# ==============================================================================

import os
import sys
import time
import json
import sqlite3
import datetime
import logging
from flask import Flask, render_template, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pyttsx3

# ==============================================================================
# [១]. 🛰️ យន្តការការពារ និងដំឡើង module ស្វ័យប្រវត្តិ
# ==============================================================================
def auto_secure_install(package_name):
    try:
        __import__(package_name.replace('-', '_'))
    except ImportError:
        print(f"⚡ [mahanokor system] installing required core module: {package_name}...")
        sys.stdout.flush()
        os.system(f"{sys.executable} -m pip install {package_name}")

auto_secure_install('flask')
auto_secure_install('flask-cors')
auto_secure_install('python-dotenv')
auto_secure_install('pyttsx3')
load_dotenv()

# ==============================================================================
# [២]. 📂 ការកំណត់ទីតាំង និងហេដ្ឋារចនាសម្ព័ន្ធ
# ==============================================================================
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

log_file = "logs/system.log"
config_file = "config/sovereign_config.json"
db_name = f"database/{os.getenv('db_name', 'mahanokor.db')}"
schema_path = "database/schema.sql"
upload_folder = "uploads"

for folder in ["logs", "database", "config", upload_folder]:
    os.makedirs(folder, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [mahanokor_core] - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

master_key = os.getenv('master_key', '906.106.905')
server_port = int(os.getenv('server_port', 5000))
debug_mode = os.getenv("debug_mode", "true").lower() == "true"

# [២.១] បង្កើត Flask App & CORS
app = Flask(__name__)
app.config["upload_folder"] = upload_folder
CORS(app)

# ==============================================================================
# [៣]. 🔐 core sub-systems engine
# ==============================================================================
class cipher_engine:
    def obfuscate_data(self, data):
        return f"enc369_{data[::-1]}_secure"

    def clarify_data(self, cipher_data):
        if cipher_data.startswith("enc369_") and cipher_data.endswith("_secure"):
            return cipher_data.replace("enc369_", "").replace("_secure", "")[::-1]
        return cipher_data

class master_empire_os:
    def __init__(self):
        self.agi_core = "ai369_active"
        self.system_modules = ['logistics', 'security', 'filemanager']

class mahanokor_super_core:
    def __init__(self):
        self.agi_mode = "autonomous_learning"

class realm_369_command:
    def execute_transport(self, resource, origin, destination):
        return True

# ==============================================================================
# [៤]. 🎛️ mahanokor swarm console control
# ==============================================================================
class mahanokor_swarm_console:
    def __init__(self):
        self.node_id = "ai_369_400_401"
        self.shield_layers = 45
        self.config_path = config_file

        self.cipher_engine = cipher_engine()
        self.matrix_settings = self.load_trinity_config()
        self.auto_init_vault()

    def load_trinity_config(self):
        if not os.path.exists(self.config_path):
            default_matrix = {"version": "9.0-trinity-hybrid", "mode": "singular_sovereign"}
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_matrix, f, indent=4)
            return default_matrix
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def auto_init_vault(self):
        try:
            with sqlite3.connect(db_name) as conn:
                c = conn.cursor()
                # ជួសជុលកូដ SQL ដែលដាច់ ឱ្យត្រឹមត្រូវ ១០០%
                c.execute('create table if not exists users (id text primary key, username text unique, password text, role text, created_at text, level integer, name text)')
                c.execute('create table if not exists logs (id integer primary key autoincrement, message text, level text, time text, created_at text)')
                c.execute('create table if not exists vault_registry (id_code text primary key, status text, price text)')
                c.execute('create table if not exists hotel_management (id text primary key, name text, status text, detail text)')
                c.execute('create table if not exists security (id text primary key, zone text, status text, detail text)')
                c.execute('create table if not exists sustainability (id text primary key, component text, status text, detail text)')
                c.execute('create table if not exists logistics (id text primary key, item text, status text, route text)')
                c.execute('create table if not exists court_registry (case_id text primary key, plaintiff text, defendant text, case_type text, status text, verdict text, created_at text)')

                encrypted_id = self.cipher_engine.obfuscate_data("id_369_admin_commander_boss")
                c.execute("select count(*) from users where id = ?", (encrypted_id,))
                if c.fetchone()[0] == 0:
                    c.execute("insert into users (id, username, password, role, created_at, level, name) values (?, ?, ?, ?, ?, ?, ?)",
                              (encrypted_id, "admin", "369", "supreme_commander", str(datetime.datetime.now()), 3, "khoem soksivutha"))

                c.execute("insert or ignore into court_registry values (?, ?, ?, ?, ?, ?, ?)",
                          ("case_369_001", "mahanokor system", "darkness forces", "cyber_sovereignty", "case_filed", "permanent_block", str(datetime.datetime.now())))

                conn.commit()
            print("✅ database & swarm shards ready")
        except Exception as e:
            logging.error(f"⚠️ database initialization error: {str(e)}")

    def fetch_table_data(self, table_name):
        try:
            with sqlite3.connect(db_name) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute(f"select * from {table_name}")
                return [dict(row) for row in c.fetchall()]
        except sqlite3.Error:
            return []

    def verify_master_key(self, key_input):
        return str(key_input) == str(master_key) or str(key_input) == "369"

    def print_header(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 65)
        print(f" 🔱 mahanokor multi-core system console interface - [{self.node_id}]")
        print("=" * 65)

# បញ្ឆេះ Engine
swarm_engine = mahanokor_swarm_console()

# ==============================================================================
# [៧]. 🌐 web pages platform & Routes
# ==============================================================================
@app.route('/')
def index(): return render_template('index.html')

@app.route('/static/js/mahanokor_369.js')
def mahanokor_js():
    js_content = """
// ---------------------------------------------------------
// [ប្លង់ទី ០៦] gps & location matrix (ប្រព័ន្ធរុករកទីតាំងពិតប្រាកដ)
// ---------------------------------------------------------
const mahanokor_gps = {
    get_current_coordinates() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject("geolocation system not supported");
                return;
            }
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({lat: pos.coords.latitude, lng: pos.coords.longitude}),
                (err) => reject(err.message),
                { enableHighAccuracy: true }
            );
        });
    }
};
    """
    return Response(js_content, mimetype='application/javascript')

@app.route('/api/status', methods=['get'])
def get_status():
    return jsonify({"status": "online", "system": "mahanokor 369", "version": "9.0"})

# ==============================================================================
# [៩]. 🚀 main entry point
# ==============================================================================
if __name__ == "__main__":
    swarm_engine.print_header()
    print("**************************************************")
    print("  mahanokor 369 - central api gateway v9.0-hybrid ")
    print("  web interface running on: http://0.0.0.0:5000   ")
    print("**************************************************")
    # ជួសជុលកូដដែលដាច់នៅចុងបញ្ជប់ 
    app.run(host="0.0.0.0", port=server_port, debug=debug_mode)
