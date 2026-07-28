// ==========================================================
// 🔱 MAHANOKOR-369 TY_AI369 STREAMING & ROUTING CORE ENGINE
// ==========================================================
console.log("[MAHANOKOR-369] Initializing production streaming & routing engine...");

let videoPlayer;
let hlsInstance = null;

// បង្រួម DOMContentLoaded ចូលគ្នាដើម្បីកុំឲ្យជាន់គ្នាលើ Termux
document.addEventListener("DOMContentLoaded", () => {
    videoPlayer = document.getElementById("live-video-player");
    
    // ១. ចាប់ផ្ដើមលេងឆានែលទី១ (Football Stadium) ពេលបើកដំបូង
    if (videoPlayer) {
        loadStreamSource("https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8");
    }

    // ២. ចាប់ផ្ដើមដំណើរការប្រព័ន្ធផែនទីដែនដីភូមិសាស្ត្រវៃឆ្លាត
    if (document.getElementById('map')) {
        // កំណត់ចំណុចកណ្តាលនៅទីតាំងកោះពេជ្រ ភ្នំពេញ ដូចក្នុងវីដេអូរបស់បង
        var map = L.map('map').setView([11.5564, 104.9282], 15);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; MAHANOKOR 369'
        }).addTo(map);

        var currentRouteLayer = null;
        var currentMarker = null;
        var startPoint = [104.9282, 11.5564]; // កូអរដោនេ [Lng, Lat] ទីស្នាក់ការកណ្តាល

        map.on('click', function(e) {
            var destLng = e.latlng.lng;
            var destLat = e.latlng.lat;

            if (currentRouteLayer) { map.removeLayer(currentRouteLayer); }
            if (currentMarker) { map.removeLayer(currentMarker); }

            // ហៅទិន្នន័យផ្លូវថ្នល់ពិតប្រាកដពី Routing API ដើម្បីគូសខ្សែ
            var url = `https://router.project-osrm.org/route/v1/driving/${startPoint[0]},${startPoint[1]};${destLng},${destLat}?overview=full&geometries=geojson`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.routes && data.routes.length > 0) {
                        var route = data.routes[0];
                        var distanceKm = (route.distance / 1000).toFixed(2);
                        var routeCoords = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
                        
                        // គូរបន្ទាត់ដាច់ៗ (Cyan Dotted Line) រត់តាមដងផ្លូវពិតប្រាកដ
                        currentRouteLayer = L.polyline(routeCoords, {
                            color: '#00e5ff',
                            weight: 6,
                            dashArray: '10, 15',
                            opacity: 0.9
                        }).addTo(map);

                        currentMarker = L.marker([destLat, destLng]).addTo(map)
                            .bindPopup(`<b>📍 គោលដៅ MAHANOKOR 369</b><br>ចម្ងាយផ្លូវ៖ ${distanceKm} គ.ម`)
                            .openPopup();

                        map.fitBounds(currentRouteLayer.getBounds());
                    }
                })
                .catch(error => console.log("Routing Matrix Error: ", error));
        });
    }
});

// មុខងារទាញយកប្រភពវីដេអូ HLS Live Stream
function loadStreamSource(streamUrl) {
    const logContainer = document.getElementById("log-box"); // កែទៅជា log-box ឲ្យត្រូវជាមួយ HTML
    if (!logContainer) return;
    const timestamp = new Date().toLocaleTimeString();

    if (Hls.isSupported()) {
        if (hlsInstance) {
            hlsInstance.destroy();
        }
        hlsInstance = new Hls();
        hlsInstance.loadSource(streamUrl);
        hlsInstance.attachMedia(videoPlayer);
        hlsInstance.on(Hls.Events.MANIFEST_PARSED, function() {
            videoPlayer.play().catch(e => console.log("Auto-play prevented:", e));
        });
        logContainer.innerHTML += `<br>[${timestamp}] HLS_STREAM: Connected to live source successfully.`;
    } else if (videoPlayer && videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
        videoPlayer.src = streamUrl;
        videoPlayer.addEventListener('loadedmetadata', function() {
            videoPlayer.play();
        });
        logContainer.innerHTML += `<br>[${timestamp}] NATIVE_STREAM: Apple HLS player initialized.`;
    } else {
        logContainer.innerHTML += `<br><span style="color:red">[ERROR]: Browser does not support HLS streaming.</span>`;
    }
    logContainer.scrollTop = logContainer.scrollHeight;
}

// មុខងារជ្រើសរើស Item ឆានែលនៅលើ UI
function selectChannelItem(index, titleText, streamUrl, descText) {
    const items = document.querySelectorAll(".channel-item");
    if(items.length > 0) {
        items.forEach((item, idx) => {
            if(idx === index) {
                item.classList.add("active");
            } else {
                item.classList.remove("active");
            }
        });
    }

    const titleEl = document.getElementById("active-channel-title");
    const descEl = document.getElementById("active-channel-desc");
    
    if(titleEl) titleEl.innerText = titleText;
    if(descEl) descEl.innerText = descText;
    
    loadStreamSource(streamUrl);
}

// មុខងារប្តូរឆានែលតាមប៊ូតុងបញ្ជា
function switchChannel(type) {
    if(type === 'football') {
        selectChannelItem(0, 'CH-03: LIVE FOOTBALL STADIUM HD', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'Broadcasting live international & local football match streams.');
    } else if(type === 'local') {
        selectChannelItem(1, 'CH-01: CAMBODIA NATIONAL TV', 'https://cph-p2p-ms.akamaized.net/hls/live/2000341/test/master.m3u8', 'Local Cambodian network broadcasts, news, and entertainment.');
    } else if(type === 'global') {
        selectChannelItem(2, 'CH-04: INTERNATIONAL NEWS HD', 'https://devimages-cdn.apple.com/samplecode/files/example_hls/playlist.m3u8', 'International breaking news, global markets, and diplomacy.');
    }
}

// មុខងារ Picture-in-Picture (មើលវីដេអូអណ្តែតលើអេក្រង់)
function togglePictureInPicture() {
    const logContainer = document.getElementById("log-box");
    if (!videoPlayer) return;
    
    if (document.pictureInPictureElement) {
        document.exitPictureInPicture();
    } else if (document.pictureInPictureEnabled) {
        videoPlayer.requestPictureInPicture().catch(error => {
            if(logContainer) logContainer.innerHTML += `<br><span style="color:orange">[WARN]: PiP mode not supported on this device.</span>`;
        });
    }
}

// មុខងារចាក់សោសុវត្ថិភាពបន្ទាន់ (Emergency Lock Protocol)
function triggerEmergencyLock() {
    const logContainer = document.getElementById("log-box");
    
    fetch('/api/v1/matrix/security/lock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        const statusNode = document.getElementById("node-status");
        if(statusNode) {
            statusNode.innerText = "STATUS: LOCKED";
            statusNode.style.color = "#ef4444";
        }
        
        if(logContainer) {
            logContainer.innerHTML += `<br><span style="color:#ef4444">[CRITICAL]: Emergency lock triggered! Streaming paused.</span>`;
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        if(videoPlayer) videoPlayer.pause();
        alert("MAHANOKOR-369: Matrix Security Lock Activated!");
    })
    .catch(error => {
        console.error("Lock error:", error);
    });
}
