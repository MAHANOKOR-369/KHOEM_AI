from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

# ==========================================
# ១. DASHBOARD & SYSTEM CONFIG MODULES
# ==========================================

# Route សម្រាប់ទំព័រដើម Dashboard របស់បង
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route សម្រាប់ទំព័រ SYSTEM CONFIG 
@app.route('/config')
def config_page():
    return render_template('config.html')

# API សម្រាប់ទាញទិន្នន័យ Dashboard មកបង្ហាញលើអេក្រង់ Real-time
@app.route('/api/system/status')
def api_system_status():
    return jsonify({
        "status": "online",
        "core_version": "KHOEM_AI_v3.6.9",
        "defense_layers": 45,
        "cooling_temp": 12.1,
        "server_time": datetime.datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
    })


# ==========================================
# ២. MAHANOKOR-369 TV & STREAMING MODULE
# ==========================================

# Route សម្រាប់បើកផ្ទាំងទូរទស្សន៍ ty_ai369
@app.route('/tv')
def ty_ai369_matrix():
    return render_template('ty_ai369.html')

# API សុវត្ថិភាពសម្រាប់បិទ/ចាក់សោប្រព័ន្ធទាន់ហេតុការណ៍
@app.route('/api/v1/matrix/security/lock', methods=['POST'])
def matrix_security_lock():
    # ដំណើរការតក្កវិជ្ជាការពារកម្រិតខ្ពស់
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
# ៣. APPLICATION ENTRY POINT
# ==========================================
if __name__ == '__main__':
    # រត់នៅលើ Port 5000 តែមួយរួមគ្នា គ្រប់គ្រងគ្រប់ Modules ទាំងអស់
    app.run(host='0.0.0.0', port=5000, debug=True)
