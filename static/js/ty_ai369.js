// MAHANOKOR-369 TY_AI369 STREAMING ENGINE
console.log("[MAHANOKOR-369] Initializing production streaming engine...");

let videoPlayer;
let hlsInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    videoPlayer = document.getElementById("live-video-player");
    // ចាប់ផ្ដើមលេងឆានែលទី១ (Football Stadium) ពេលបើកដំបូង
    loadStreamSource("https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8");
});

function loadStreamSource(streamUrl) {
    const logContainer = document.getElementById("terminal-logs");
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
    } else if (videoPlayer.canPlayType('application/vnd.apple.mpegurl')) {
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

function selectChannelItem(index, titleText, streamUrl, descText) {
    const items = document.querySelectorAll(".channel-item");
    items.forEach((item, idx) => {
        if(idx === index) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });

    document.getElementById("active-channel-title").innerText = titleText;
    document.getElementById("active-channel-desc").innerText = descText;
    loadStreamSource(streamUrl);
}

function switchChannel(type) {
    if(type === 'football') {
        selectChannelItem(0, 'CH-03: LIVE FOOTBALL STADIUM HD', 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'Broadcasting live international & local football match streams.');
    } else if(type === 'local') {
        selectChannelItem(1, 'CH-01: CAMBODIA NATIONAL TV', 'https://cph-p2p-ms.akamaized.net/hls/live/2000341/test/master.m3u8', 'Local Cambodian network broadcasts, news, and entertainment.');
    } else if(type === 'global') {
        selectChannelItem(3, 'CH-04: INTERNATIONAL NEWS HD', 'https://devimages-cdn.apple.com/samplecode/files/example_hls/playlist.m3u8', 'International breaking news, global markets, and diplomacy.');
    }
}

// មុខងារ Picture-in-Picture (សម្រាប់មើលវីដេអូអណ្តែតលើទូរសព្ទ/កុំព្យូទ័រ)
function togglePictureInPicture() {
    const logContainer = document.getElementById("terminal-logs");
    const timestamp = new Date().toLocaleTimeString();
    
    if (document.pictureInPictureElement) {
        document.exitPictureInPicture();
    } else if (document.pictureInPictureEnabled && videoPlayer) {
        videoPlayer.requestPictureInPicture().catch(error => {
            logContainer.innerHTML += `<br><span style="color:orange">[WARN]: PiP mode not supported on this device/browser.</span>`;
        });
    }
}

function triggerEmergencyLock() {
    const logContainer = document.getElementById("terminal-logs");
    const timestamp = new Date().toLocaleTimeString();
    
    fetch('/api/v1/matrix/security/lock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            document.getElementById("node-status").innerText = "STATUS: LOCKED";
            document.getElementById("node-status").style.color = "var(--neon-magenta)";
            document.getElementById("node-status").style.borderColor = "var(--neon-magenta)";
            
            logContainer.innerHTML += `<br><span style="color:var(--neon-magenta)">[CRITICAL]: Emergency lock triggered! Streaming paused.</span>`;
            logContainer.scrollTop = logContainer.scrollHeight;
            videoPlayer.pause();
            alert("MAHANOKOR-369: Matrix Security Lock Activated!");
        }
    })
    .catch(error => {
        console.error("Lock error:", error);
    });
}
