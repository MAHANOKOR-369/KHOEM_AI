// ==============================================================================
// static/js/camera.js
// KHOEM_AI 2.0 — 👁️ មើល (Camera/Photo Analysis)
// ==============================================================================

const KhoemCamera = {
  stream: null,
  videoElement: null,

  // ------------------------------------------------------------------------
  // បើកកាមេរ៉ា (back camera ជាមុនសិន សម្រាប់មើលវត្ថុ/ផ្លូវ)
  // ------------------------------------------------------------------------
  async startCamera(videoElement) {
    this.videoElement = videoElement;
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" } // "environment" = back camera
      });
      videoElement.srcObject = this.stream;
      await videoElement.play();
      return true;
    } catch (err) {
      throw "មិនអាចបើកកាមេរ៉ា: " + err.message;
    }
  },

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
  },

  // ------------------------------------------------------------------------
  // ថតរូបភាព ពី video stream → បម្លែងទៅជា base64
  // ------------------------------------------------------------------------
  capturePhoto() {
    if (!this.videoElement) {
      throw "កាមេរ៉ាមិនទាន់បើកទេ";
    }

    const canvas = document.createElement("canvas");
    canvas.width = this.videoElement.videoWidth;
    canvas.height = this.videoElement.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(this.videoElement, 0, 0);

    // ត្រឡប់ជា base64 (ដកចេញ "data:image/jpeg;base64," ព្រោះ backend ត្រូវការតែ base64 ដុលៗ)
    const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
    const base64 = dataUrl.split(",")[1];
    return base64;
  },

  // ------------------------------------------------------------------------
  // ផ្ញើរូបភាពទៅ backend ដើម្បីវិភាគ
  // ------------------------------------------------------------------------
  async analyzeImage(base64Image, question) {
    const response = await fetch("/api/vision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        image: base64Image,
        question: question || "សូមពិពណ៌នារូបភាពនេះជាភាសាខ្មែរ",
        mime_type: "image/jpeg"
      })
    });
    return await response.json();
  },

  // ------------------------------------------------------------------------
  // ជម្រើសផ្សេង — ជ្រើសរើសរូបភាពពី file picker (មិនប្រើកាមេរ៉ាផ្ទាល់)
  // ------------------------------------------------------------------------
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
};

// ==============================================================================
// របៀបប្រើ (ឧទាហរណ៍)
// ==============================================================================
/*
// វិធីទី១ — ប្រើកាមេរ៉ាផ្ទាល់
const videoEl = document.getElementById("camera-preview");
await KhoemCamera.startCamera(videoEl);
const photo = KhoemCamera.capturePhoto();
const result = await KhoemCamera.analyzeImage(photo, "តើមានអ្វីនៅក្នុងរូបនេះ?");
console.log(result.answer);
KhoemCamera.stopCamera();

// វិធីទី២ — ជ្រើសរើស file ពី gallery (ស្រួលជាងលើ mobile browser ខ្លះ)
document.getElementById("file-input").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  const base64 = await KhoemCamera.fileToBase64(file);
  const result = await KhoemCamera.analyzeImage(base64, "នេះជាអ្វី?");
  console.log(result.answer);
});
*/
