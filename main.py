import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

# បង្កើត Mock Class ការពារកុំឱ្យគាំង ប្រសិនបើមិនទាន់មានឯកសារ core មេ
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
app.config['SECRET_KEY'] = 'khoem_ai_369_sovereign'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core/database/system_ids.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
mahanokor_engine = MahanokorCore()
telemetry_thread_started = False

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    action = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# --- WEB PAGES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/config')
def config_page():
    return render_template('config.html')

@app.route('/tv')
def matrix_tv_view():
    return render_template('dashboard.html') # អាចដូរទៅលីងទូរទស្សន៍ផ្សេងបាន

# --- APIS ---
@app.route('/api/v1/matrix/security/lock', methods=['POST'])
def api_matrix_lock():
    try:
        mahanokor_engine.trigger_security_lock()
        log_entry = SystemLog(action="EMERGENCY_LOCK", status="ACTIVATED")
        db.session.add(log_entry)
        db.session.commit()
        return jsonify({"success": True, "message": f"🔒 SECURITY NOTICE: {mahanokor_engine.system_name} Core layers have been EMERGENCY LOCKED!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/v1/matrix/status', methods=['GET'])
def api_matrix_status():
    core_status = mahanokor_engine.get_matrix_status()
    return jsonify({
        "success": True,
        "matrix_status": {
            "cooling_temp": core_status["cooling_temp"],
            "defense_layers": mahanokor_engine.defense_layers,
            "node_state": core_status["status"].upper(),
            "server_time": datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
        }
    })

# --- SOCKET IO REAL-TIME ---
def run_telemetry_loop():
    while True:
        socketio.sleep(2)
        status_now = mahanokor_engine.get_matrix_status()
        socketio.emit('hardware_telemetry', {
            'cpu': 28,
            'ram': 46,
            'temp': status_now['cooling_temp']
        })

@socketio.on('connect')
def on_client_connect():
    global telemetry_thread_started
    if not telemetry_thread_started:
        socketio.start_background_task(run_telemetry_loop)
        telemetry_thread_started = True
    emit('system_alert', {'message': f'🔌 @ [SYSTEM AUTH]: និរន្តរភាពប្រព័ន្ធ {mahanokor_engine.system_name} ដំណើរការហើយ!', 'color': '#00ffc8'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
