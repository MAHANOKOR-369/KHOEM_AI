import os
import requests
import shutil
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash

# ==========================================
# ១. SYSTEM INITIALIZATION & CONFIG
# ==========================================
# បង្កើត Folder ស្វ័យប្រវត្ត ការពារ OperationalError
os.makedirs('data', exist_ok=True)
os.makedirs('data/backups', exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'mahanokor_369_super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/mahanokor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 💡 កែសម្រួល៖ បន្ថែម async_mode='threading' ដើម្បីដោះស្រាយ Error គាំងនៅលើ Termux/Android
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ==========================================
# ២. DATABASE MODELS
# ==========================================
class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# បង្កើត Database និងគណនី Admin គំរូ
with app.app_context():
    db.create_all()
    if not AdminUser.query.filter_by(username='123').first():
        hashed_pw = generate_password_hash('123456', method='pbkdf2:sha256')
        db.session.add(AdminUser(username='123', password_hash=hashed_pw))
        db.session.commit()

# ==========================================
# ៣. CORE DASHBOARD & MATRIX ROUTES
# ==========================================
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # 💡 កែសម្រួល៖ ប្តូរឱ្យទៅបើកទំព័រ dashboard.html ដែលបងទើបតែកែសម្រួលនៅលើ GitHub
    return render_template('dashboard.html')

@app.route('/config')
def config_page():
    return render_template('config.html')

@app.route('/tv')
def ty_ai369_matrix():
    # រក្សាទុកទំព័រ ty_ai369.html សម្រាប់មុខងារចាក់ទូរទស្សន៍ Matrix TV ដាច់ដោយឡែក
    return render_template('ty_ai369.html')

# API សម្រាប់ទាញទិន្នន័យ Dashboard មកបង្ហាញលើអេក្រង់ Real-time
@app.route('/api/system/status')
def api_system_status():
    return jsonify({
        "status": "online",
        "core_version": "KHOEM_AI_v3.6.9",
        "defense_layers": 45,
        "cooling_temp": 12.1,
        "server_time": datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
    })

# API សុវត្ថិភាពសម្រាប់បិទ/ចាក់សោប្រព័ន្ធទាន់ហេតុការណ៍
@app.route('/api/v1/matrix/security/lock', methods=['POST'])
def matrix_security_lock():
    new_log = SystemLog(action="EMERGENCY_LOCK", status='ACTIVATED')
    db.session.add(new_log)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "MAHANOKOR-369: Matrix Security Lock Activated Successfully."
    })

# API សម្រាប់ទាញយកស្ថានភាពប្រព័ន្ធ Matrix Real-time
@app.route('/api/v1/matrix/status', methods=['GET'])
def api_matrix_status():
    return jsonify({
        "success": True,
        "matrix_status": {
            "cooling_temp": 12.4,
            "defense_layers": 45,
            "node_state": "ONLINE"
        }
    })

# ==========================================
# ៤. SOCKET.IO REAL-TIME TELEMETRY
# ==========================================
def telemetry_thread():
    while True:
        socketio.sleep(1)
        socketio.emit('hardware_telemetry', {'cpu': 45, 'ram': 60})

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(telemetry_thread)
    socketio.emit('system_alert', {'message': '⚙️ [system auth]: ពិនិត្យឃើញប្រព័ន្ធដំណើរការ! ប្រព័ន្ធសុវត្ថិភាព AI 369 និម្មិតរលូន ៤៥ ស្រទាប់ ដំណើរការធម្មតា!', 'color': '#00ff00'})

@socketio.on('execute_command')
def handle_command(data):
    action = data.get('action')
    new_log = SystemLog(action=action, status='EXECUTED')
    db.session.add(new_log)
    db.session.commit()
    emit('command_response', {'action': action, 'message': f'ការអនុវត្ត {action} បានសម្រេច', 'timestamp': datetime.utcnow().strftime("%H:%M:%S")}, broadcast=True)

# ==========================================
# ៥. APPLICATION ENTRY POINT
# ==========================================
if __name__ == '__main__':
    # 💡 កែសម្រួល៖ ប្តូរទៅ Port 3690 ឱ្យត្រូវទៅនឹងការកំណត់ប្រព័ន្ធសន្តិសុខ Termux របស់បង
    socketio.run(app, host='0.0.0.0', port=3690, debug=True)
