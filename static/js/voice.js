// ==============================================================================
// static/js/voice.js
// KHOEM_AI 1.0 — 🎤 ស្តាប់ (Listen) + 🔊 និយាយ (Voice)
// ==============================================================================
// ប្រើ Web Speech API ដែលមានស្រាប់ក្នុង browser (Chrome/Edge)
// មិនត្រូវការ library ខាងក្រៅ ឬ server ណាមួយសម្រាប់ voice ទេ
// ==============================================================================

const KhoemVoice = {
  recognition: null,
  isListening: false,

  // ------------------------------------------------------------------------
  // 🎤 ស្តាប់ — បម្លែងសំឡេងទៅជាអក្សរ (Speech-to-Text)
  // ------------------------------------------------------------------------
  initRecognition(onResult, onError) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      onError("browser នេះមិនគាំទ្រ voice recognition ទេ។ សូមប្រើ Chrome");
      return false;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.lang = "km-KH"; // ភាសាខ្មែរ (fallback ទៅ en-US បើមិនគាំទ្រ)
    this.recognition.continuous = false;
    this.recognition.interimResults = false;

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
      this.isListening = false;
    };

    this.recognition.onerror = (event) => {
      onError("បញ្ហាស្តាប់សំឡេង: " + event.error);
      this.isListening = false;
    };

    this.recognition.onend = () => {
      this.isListening = false;
    };

    return true;
  },

  startListening() {
    if (this.recognition && !this.isListening) {
      this.isListening = true;
      this.recognition.start();
    }
  },

  stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  },

  // ------------------------------------------------------------------------
  // 🔊 និយាយ — បម្លែងអក្សរទៅជាសំឡេង (Text-to-Speech)
  // ------------------------------------------------------------------------
  speak(text, lang = "km-KH") {
    if (!window.speechSynthesis) {
      console.error("browser មិនគាំទ្រ text-to-speech ទេ");
      return;
    }

    // បញ្ឈប់សំឡេងចាស់ (បើកំពុងនិយាយ) មុននិយាយថ្មី
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 1.0;   // ល្បឿននិយាយ (0.5 - 2.0)
    utterance.pitch = 1.0;  // សំឡេងខ្ពស់ទាប

    window.speechSynthesis.speak(utterance);
  },

  stopSpeaking() {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }
};

// ==============================================================================
// របៀបប្រើ (ឧទាហរណ៍)
// ==============================================================================
/*
// ចាប់ផ្តើម recognition
KhoemVoice.initRecognition(
  (transcript) => {
    console.log("អ្នកនិយាយថា:", transcript);
    // ផ្ញើ transcript ទៅ /api/chat
  },
  (error) => {
    console.error(error);
  }
);

// ចាប់ស្តាប់ពេលចុចប៊ូតុងមីក្រូហ្វូន
document.getElementById("mic-btn").addEventListener("click", () => {
  KhoemVoice.startListening();
});

// ឲ្យ Claude និយាយចម្លើយ
KhoemVoice.speak("សួស្តី! តើខ្ញុំអាចជួយអ្វីបាន?");
*/
