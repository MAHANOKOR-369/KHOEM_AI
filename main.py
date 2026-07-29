# ឈ្មោះឯកសារ: main.py

from flask import Flask, render_template
import os

app = Flask(__name__)

# ១. ទំព័រដើម (ផ្ទាំងបង្ហាញសេវាកម្ម / Dashboard)
@app.route('/')
def home():
    # វានឹងទៅទាញឯកសារ dashboard.html ពីក្នុងថត templates មកបង្ហាញ
    return render_template('dashboard.html')

# ២. ទំព័រប្រវត្តិរូប និងវិញ្ញាបនបត្រ (Portfolio & Skills)
@app.route('/portfolio')
def portfolio():
    # វានឹងទៅទាញឯកសារ portfolio.html ពីក្នុងថត templates មកបង្ហាញ
    return render_template('portfolio.html')

if __name__ == '__main__':
    # ធានាថាថត templates ត្រូវមានស្រាប់
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # ដំណើរការ Server នៅលើ Port 5000
    print("🚀 KHOEM_AI System is starting...")
    print("🌐 សូមចូលទៅកាន់: http://127.0.0.1:5000 ដើម្បីមើលលទ្ធផល")
    app.run(debug=True, host='0.0.0.0', port=5000)

