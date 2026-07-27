from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

# Route សម្រាប់ទំព័រដើម Dashboard របស់បង
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route សម្រាប់ទំព័រ SYSTEM CONFIG 
@app.route('/config')
def config_page():
    return render_template('config.html')

# API សម្រាប់ទាញទិន្នន័យមកបង្ហាញលើអេក្រង់ Real-time
@app.route('/api/system/status')
def system_status():
    return jsonify({
        "status": "online",
        "core_version": "KHOEM_AI_v3.6.9",
        "defense_layers": 45,
        "cooling_temp": 12.1,
        "server_time": datetime.datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
    })

if __name__ == '__main__':
    # រត់នៅលើ Port 5000 ដូចកម្មវិធីពិតរបស់បង
    app.run(host='0.0.0.0', port=5000, debug=True)
