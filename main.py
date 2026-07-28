import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

# បង្កើត Folder ទិន្នន័យបើមិនទាន់មាន
os.makedirs('data', exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'mahanokor_369_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/mahanokor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 💡 ប្រើប្រាស់ async_mode='threading' ដើម្បីភាពទន់ភ្លន់ និងស្ថិរភាពខ្ពស់លើ Termux
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# បង្កើត Variable សម្រាប់ការពារការបង្កើត Thread ជាន់គ្នា
telemetry_thread_started = False

# --- DATA MODELS ---
class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now) # កែសម្រួល៖ ប្រើ datetime.now
    action = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# --- WEB CORE ROUTES ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/config')
def config_page():
    return render_template('config.html')

@app.route('/tv')
def matrix_tv_view():
    return render_template('ty_ai369.html')

# --- API CORE SYSTEMS ---
@app.route('/api/v1/matrix/security/lock', methods=['POST'])
def api_matrix_lock():
    try:
        log_entry = SystemLog(action="EMERGENCY_LOCK", status='ACTIVATED')
        db.session.add(log_entry)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "🔒 SECURITY NOTICE: MAHANOKOR 369 Core layers have been EMERGENCY LOCKED!"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/v1/matrix/status', methods=['GET'])
def api_matrix_status():
    return jsonify({
        "success": True,
        "matrix_status": {
            "cooling_temp": 12.1,
            "defense_layers": 45,
            "node_state": "ONLINE",
            "server_time": datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
        }
    })

# --- SOCKET.IO REAL-TIME CHANNELS ---
def run_telemetry_loop():
    """ បោះទិន្នន័យ Hardware Telemetry ទៅកាន់ UI រៀងរាល់ ២វិនាទី """
    while True:
        socketio.sleep(2)
        # បោះតម្លៃគំរូថេរដែលមានសុវត្ថិភាព ជៀសវាងការប្រើ psutil នាំឱ្យខុស Lib លើទូរស័ព្ទ
        socketio.emit('hardware_telemetry', {'cpu': 28, 'ram': 46})

@socketio.on('connect')
def on_client_connect():
    global telemetry_thread_started
    # កែសម្រួល៖ បង្កើត Thread តែម្តងគត់ ការពារការដកដង្ហើមជាន់គ្នា និងគាំង CPU លើ Termux
    if not telemetry_thread_started:
        socketio.start_background_task(run_telemetry_loop)
        telemetry_thread_started = True
        
    emit('system_alert', {
        'message': '⚙️ [SYSTEM AUTH]: ពិនិត្យឃើញប្រព័ន្ធដំណើរការ! ប្រព័ន្ធសុវត្ថិភាព AI 369 និម្មិតរលូន ៤៥ ស្រទាប់ ដំណើរការធម្មតា!', 
        'color': '#00ff66'
    })

@socketio.on('execute_command')
def on_execute_command(data):
    cmd_action = data.get('action', 'UNKNOWN_ACTION')
    try:
        log_entry = SystemLog(action=cmd_action, status='SUCCESS')
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        print(f"Database error: {e}")
        
    emit('command_response', {
        'action': cmd_action, 
        'message': f'ការអនុវត្ត {cmd_action} បានសម្រេចជោគជ័យ', 
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }, broadcast=True)

# --- START APPLICATION ---
if __name__ == '__main__':
    # រត់លើ Port 3690 តាមការកំណត់
    socketio.run(app, host='0.0.0.0', port=3690, debug=True)
