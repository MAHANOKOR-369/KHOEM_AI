import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

# បង្កើត Core បម្រុងការពារកុំឱ្យគាំងប្រព័ន្ធ
class MahanokorCore:
    def __init__(self):
        self.system_name = "MAHANOKOR-369"
        self.defense_layers = 45
        self.matrix_locked = False
    def get_matrix_status(self):
        import random
        return {
            "status": "online" if not self.matrix_locked else "emergency_locked",
            "cooling_temp": round(random.uniform(11.8, 13.5), 1)
        }
    def trigger_security_lock(self):
        self.matrix_locked = True
        self.defense_layers = 0
        return True

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'mahanokor_369_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core/database/system_ids.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
mahanokor_engine = MahanokorCore()
telemetry_started = False

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    action = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# --- WEB PAGES LINKS ---
@app.route('/')
def index():
    return render_template('dashboard.html')  # ឱ្យចូលទៅកាន់ទំព័រ Dashboard ផ្ទាល់តែម្តង

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/config')
def config_page():
    return render_template('config.html')

# --- APIS ---
@app.route('/api/v1/matrix/security/lock', methods=['POST'])
def api_matrix_lock():
    try:
        mahanokor_engine.trigger_security_lock()
        log = SystemLog(action="EMERGENCY_LOCK", status="ACTIVATED")
        db.session.add(log)
        db.session.commit()
        return jsonify({"success": True, "message": "🔒 SECURITY NOTICE: MAHANOKOR-369 Core layers EMERGENCY LOCKED!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- REAL-TIME TELEMETRY LOOP ---
def telemetry_loop():
    while True:
        socketio.sleep(2)
        status = mahanokor_engine.get_matrix_status()
        socketio.emit('hardware_telemetry', {
            'cpu': 36,
            'ram': 69,
            'temp': status['cooling_temp']
        })

@socketio.on('connect')
def on_connect():
    global telemetry_started
    if not telemetry_started:
        socketio.start_background_task(telemetry_loop)
        telemetry_started = True
    emit('system_alert', {'message': '🔌 System Synchronized.', 'color': '#00ffc8'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
