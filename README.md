KHOEM_AI 1.0
AI Assistant សម្រាប់ជីវិតប្រចាំថ្ងៃ — Chat + Voice + GPS
បង្កើតដោយ KHOEM_AI (KHOEM SOKSIVUTHA)
📋 ទិដ្ឋភាពទូទៅ
KHOEM_AI គឺជា AI Assistant ដែលមិនត្រឹមតែជា chatbot ធម្មតាទេ ប៉ុន្តែជាជំនួយការឆ្លាតវៃសម្រាប់ជីវិតប្រចាំថ្ងៃ ដោយផ្តោតលើ ៥ មុខងារស្នូល៖
មុខងារ
ស្ថានភាព
បច្ចេកវិទ្យា
🧠 គិត និងវិភាគ (Chat)
✅ ដំណើរការ
Groq API (Llama 3.3 70B)
🎤 ស្តាប់ (Voice Input)
✅ ដំណើរការ
Web Speech API
🔊 និយាយ (Voice Output)
✅ ដំណើរការ
Web Speech Synthesis
🗺️ នាំផ្លូវ (GPS)
🚧 កំពុងអភិវឌ្ឍន៍
Geolocation API
👁️ មើល (Camera/Vision)
📅 គម្រោង 2.0
getUserMedia API
🏗️ ស្ថាបត្យកម្ម
Code
⚙️ ការដំឡើង
១. ដំឡើង Python packages
Bash
២. ទទួល Groq API Key (ឥតគិតថ្លៃ)
ចូល console.groq.com
Sign up (គ្មានទាមទារ credit card)
API Keys → Create API Key
Copy key (ចាប់ផ្តើម gsk_...)
៣. កំណត់ Environment Variables
បង្កើតឯកសារ .env:
Bash
៤. ដំណើរការ Server
Bash
បើក browser ចូល http://127.0.0.1:5000
🔌 API Endpoints
Method
Path
ការពិពណ៌នា
GET
/
ទំព័រ Chat UI
GET
/api/status
ពិនិត្យស្ថានភាព server
POST
/api/chat
ផ្ញើសារ → ទទួលចម្លើយ AI
GET
/api/history/<session_id>
ទាញយកប្រវត្តិសន្ទនា
POST
/api/directions
ស្នើសុំផ្លូវ (កំពុងអភិវឌ្ឍន៍)
ឧទាហរណ៍ការហៅ /api/chat
Bash
🎤 មុខងារ Voice
ចុចប៊ូតុង 🎤 → និយាយសំណួរជាភាសាខ្មែរ → ប្រព័ន្ធបម្លែងទៅជាអក្សរស្វ័យប្រវត្តិ
ចម្លើយពី AI ត្រូវបានអានឮដោយស្វ័យប្រវត្តិ (Text-to-Speech)
ត្រូវការ browser Chrome/Edge សម្រាប់ភាពត្រូវគ្នាល្អបំផុត
🗺️ មុខងារ GPS
ចុចប៊ូតុង 📍 → បង្ហាញទីតាំងបច្ចុប្បន្ន (latitude/longitude)
មុខងារនាំផ្លូវ (turn-by-turn directions) កំពុងអភិវឌ្ឍន៍ — ត្រូវការភ្ជាប់ជាមួយ routing API ពិត (ជំហានបន្ទាប់)
🔒 សុវត្ថិភាព
✅ .env មិនត្រូវ commit ចូល git — ការពារ API key លេចធ្លាយ
✅ Chat history រក្សាទុកតាម session_id ក្នុង SQLite local
⚠️ Development server នេះមិនសមរម្យសម្រាប់ production — ត្រូវប្រើ production WSGI server (Gunicorn) ពេលដាក់ដំណើរការជាក់ស្តែង
🛣️ ផែនការអភិវឌ្ឍន៍បន្ត
KHOEM_AI 1.1 — ភ្ជាប់ GPS ជាមួយ routing API ពិត (turn-by-turn navigation)
KHOEM_AI 2.0 — បន្ថែម Camera/Photo/Video Analysis (មើលផ្លូវ សញ្ញាចរាចរណ៍)
KHOEM_AI 3.0 — AI Guide ពេញលេញ (ស្គាល់បរិស្ថាន ណែនាំដំណើរដោយស្វ័យប្រវត្តិ)
📜 អាជ្ញាប័ណ្ណ
Personal project — សិក្សា និងអភិវឌ្ឍន៍ដោយ KHOEM_AI
