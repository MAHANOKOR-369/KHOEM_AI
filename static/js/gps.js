// ==============================================================================
// static/js/gps.js
// KHOEM_AI 1.0 — 🗺️ នាំផ្លូវ (Navigation)
// ==============================================================================
// ប្រើ Geolocation API របស់ browser សម្រាប់ទីតាំងបច្ចុប្បន្ន
// ការគណនាផ្លូវពិត (routing/directions) ត្រូវការ API ខាងក្រៅ ដូចជា
// Google Maps Directions API ឬ OpenRouteService (ឥតគិតថ្លៃ)
// ==============================================================================

const KhoemGPS = {
  currentPosition: null,
  watchId: null,

  // ------------------------------------------------------------------------
  // ទាញយកទីតាំងបច្ចុប្បន្នមួយដង
  // ------------------------------------------------------------------------
  getCurrentLocation() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject("browser នេះមិនគាំទ្រ GPS ទេ");
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy
          };
          resolve(this.currentPosition);
        },
        (error) => {
          reject("មិនអាចទាញយកទីតាំង: " + error.message);
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    });
  },

  // ------------------------------------------------------------------------
  // តាមដានទីតាំងជាបន្តបន្ទាប់ (សម្រាប់ live navigation)
  // ------------------------------------------------------------------------
  startWatching(onUpdate, onError) {
    if (!navigator.geolocation) {
      onError("browser នេះមិនគាំទ្រ GPS ទេ");
      return;
    }

    this.watchId = navigator.geolocation.watchPosition(
      (position) => {
        this.currentPosition = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
          heading: position.coords.heading // ទិសដៅកំពុងធ្វើដំណើរ
        };
        onUpdate(this.currentPosition);
      },
      (error) => onError("បញ្ហា GPS: " + error.message),
      { enableHighAccuracy: true }
    );
  },

  stopWatching() {
    if (this.watchId !== null) {
      navigator.geolocation.clearWatch(this.watchId);
      this.watchId = null;
    }
  },

  // ------------------------------------------------------------------------
  // ស្នើសុំផ្លូវទៅកន្លែងដែលចង់បាន (ត្រូវការ backend endpoint /api/directions)
  // backend នឹងហៅ routing API ពិត (Google/OpenRouteService) ជំនួសអ្នកប្រើ
  // ------------------------------------------------------------------------
  async getDirections(destinationText) {
    if (!this.currentPosition) {
      await this.getCurrentLocation();
    }

    const response = await fetch("/api/directions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin: this.currentPosition,
        destination: destinationText
      })
    });

    return await response.json();
  }
};

// ==============================================================================
// របៀបប្រើ (ឧទាហរណ៍)
// ==============================================================================
/*
// ទាញយកទីតាំងបច្ចុប្បន្ន
KhoemGPS.getCurrentLocation().then(pos => {
  console.log("ទីតាំងបច្ចុប្បន្ន:", pos.lat, pos.lng);
});

// នាំផ្លូវទៅមន្ទីរពេទ្យ
KhoemGPS.getDirections("មន្ទីរពេទ្យ ខេមរៈ-សូភាក់").then(directions => {
  KhoemVoice.speak(directions.instruction); // "បត់ស្តាំក្នុងចម្ងាយ ១០០ម៉ែត្រ"
});

// តាមដានពេលធ្វើដំណើរ
KhoemGPS.startWatching(
  (pos) => console.log("ទីតាំងថ្មី:", pos),
  (err) => console.error(err)
);
*/
