// ==============================================================================
// static/js/map.js
// KHOEM_AI 1.1 — 🗺️ ផែនទី + នាំផ្លូវពិត (Map + Real Navigation)
// ==============================================================================
// ប្រើ Leaflet.js (library ផែនទី ឥតគិតថ្លៃ) + OpenStreetMap tiles (ឥតគិតថ្លៃ)
// + OSRM demo server សម្រាប់គណនាផ្លូវ (ឥតគិតថ្លៃ គ្មានទាមទារ API key)
// ==============================================================================

const KhoemMap = {
  map: null,
  userMarker: null,
  destMarker: null,
  routeLine: null,

  // ------------------------------------------------------------------------
  // បង្កើតផែនទី ក្នុង container id ដែលបញ្ជាក់
  // ------------------------------------------------------------------------
  init(containerId, centerLat, centerLng) {
    this.map = L.map(containerId).setView([centerLat, centerLng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(this.map);

    // សញ្ញាទីតាំងបច្ចុប្បន្ន (ពណ៌ខៀវ)
    this.userMarker = L.marker([centerLat, centerLng])
      .addTo(this.map)
      .bindPopup("ទីតាំងរបស់អ្នក")
      .openPopup();
  },

  // ------------------------------------------------------------------------
  // ធ្វើបច្ចុប្បន្នភាពទីតាំងអ្នកប្រើ (ពេលធ្វើដំណើរ)
  // ------------------------------------------------------------------------
  updateUserLocation(lat, lng) {
    if (!this.map) return;
    if (this.userMarker) {
      this.userMarker.setLatLng([lat, lng]);
    }
    this.map.panTo([lat, lng]);
  },

  // ------------------------------------------------------------------------
  // ស្វែងរកទីតាំង destination ដោយឈ្មោះ (Geocoding តាមរយៈ Nominatim ឥតគិតថ្លៃ)
  // ------------------------------------------------------------------------
  async geocodeSearch(placeName) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(placeName)}&limit=1`;
    const res = await fetch(url, {
      headers: { "Accept-Language": "km,en" }
    });
    const results = await res.json();
    if (results.length === 0) {
      throw "រកមិនឃើញទីតាំង: " + placeName;
    }
    return {
      lat: parseFloat(results[0].lat),
      lng: parseFloat(results[0].lon),
      displayName: results[0].display_name
    };
  },

  // ------------------------------------------------------------------------
  // គណនាផ្លូវពី origin ទៅ destination (តាមរយៈ OSRM demo server ឥតគិតថ្លៃ)
  // ------------------------------------------------------------------------
  async getRoute(originLat, originLng, destLat, destLng) {
    const url = `https://router.project-osrm.org/route/v1/driving/${originLng},${originLat};${destLng},${destLat}?overview=full&geometries=geojson&steps=true`;
    const res = await fetch(url);
    const data = await res.json();

    if (data.code !== "Ok" || !data.routes || data.routes.length === 0) {
      throw "មិនអាចគណនាផ្លូវបានទេ";
    }

    const route = data.routes[0];
    return {
      distanceKm: (route.distance / 1000).toFixed(1),
      durationMin: Math.round(route.duration / 60),
      coordinates: route.geometry.coordinates.map(c => [c[1], c[0]]), // [lng,lat] -> [lat,lng]
      steps: route.legs[0].steps.map(step => ({
        instruction: this.translateManeuver(step.maneuver),
        distanceM: Math.round(step.distance)
      }))
    };
  },

  // ------------------------------------------------------------------------
  // បង្ហាញផ្លូវលើផែនទី (បន្ទាត់ពណ៌ខៀវ) + destination marker
  // ------------------------------------------------------------------------
  drawRoute(routeCoordinates, destLat, destLng) {
    if (this.routeLine) {
      this.map.removeLayer(this.routeLine);
    }
    if (this.destMarker) {
      this.map.removeLayer(this.destMarker);
    }

    this.routeLine = L.polyline(routeCoordinates, { color: '#4dabf7', weight: 5 }).addTo(this.map);
    this.destMarker = L.marker([destLat, destLng]).addTo(this.map).bindPopup("គោលដៅ");

    this.map.fitBounds(this.routeLine.getBounds(), { padding: [40, 40] });
  },

  // ------------------------------------------------------------------------
  // បម្លែងទិសដៅ OSRM (ភាសាអង់គ្លេស) ទៅជាភាសាខ្មែរសាមញ្ញ
  // ------------------------------------------------------------------------
  translateManeuver(maneuver) {
    const type = maneuver.type;
    const modifier = maneuver.modifier || "";

    if (type === "depart") return "ចាប់ផ្តើមធ្វើដំណើរ";
    if (type === "arrive") return "អ្នកបានមកដល់គោលដៅ";
    if (type === "turn") {
      if (modifier.includes("left")) return "បត់ឆ្វេង";
      if (modifier.includes("right")) return "បត់ស្តាំ";
      if (modifier === "straight") return "ទៅត្រង់";
      return "បត់";
    }
    if (type === "continue") return "បន្តទៅត្រង់";
    if (type === "roundabout") return "ចូល vόng-round";
    return "បន្តទៅមុខ";
  }
};

// ==============================================================================
// របៀបប្រើ (ឧទាហរណ៍ពេញលេញ)
// ==============================================================================
/*
// ១. ចាប់ផ្តើមផែនទី
await KhoemGPS.getCurrentLocation();
KhoemMap.init("map-container", KhoemGPS.currentPosition.lat, KhoemGPS.currentPosition.lng);

// ២. ស្វែងរកគោលដៅ + គណនាផ្លូវ
const dest = await KhoemMap.geocodeSearch("ផ្សារធំថ្មី ភ្នំពេញ");
const route = await KhoemMap.getRoute(
  KhoemGPS.currentPosition.lat, KhoemGPS.currentPosition.lng,
  dest.lat, dest.lng
);

// ៣. បង្ហាញលើផែនទី
KhoemMap.drawRoute(route.coordinates, dest.lat, dest.lng);

// ៤. និយាយជំហានដំបូង
KhoemVoice.speak(`ចម្ងាយ ${route.distanceKm} គីឡូម៉ែត្រ ប្រហែល ${route.durationMin} នាទី`);
route.steps.forEach(step => console.log(step.instruction, step.distanceM + "m"));
*/
