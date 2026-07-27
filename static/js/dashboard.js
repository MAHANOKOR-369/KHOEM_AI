// MAHANOKOR 369 CORE LOGIC & INTERACTION

document.addEventListener('DOMContentLoaded', function() {
    console.log("🔱 MAHANOKOR 369 | Core System Initialized.");
    
    // 1. មុខងារ Update ម៉ោង Celestial Time ឱ្យដើរ Real-time
    setInterval(function() {
        const timeDisplay = document.getElementById('time-display');
        if (timeDisplay) {
            const now = new Date();
            timeDisplay.textContent = now.toLocaleString('en-US', { 
                day: 'numeric', 
                month: 'numeric', 
                year: 'numeric', 
                hour: 'numeric', 
                minute: 'numeric', 
                second: 'numeric', 
                hour12: true 
            });
        }
    }, 1000);

    // 2. មុខងារប៊ូតុង LOCK MATRIX
    const lockBtn = document.querySelector('.btn-action');
    if (lockBtn) {
        lockBtn.addEventListener('click', function() {
            alert("🚨 PROTOCOL EMPIRE: Matrix has been locked securely!");
            appendTerminalLog("🔒 [System]: Defense Matrix fully locked by Admin.");
        });
    }

    // មុខងារជំនួយសម្រាប់បន្ថែម Log ចូលអេក្រង់ Terminal
    function appendTerminalLog(message) {
        const terminal = document.querySelector('.terminal-screen');
        if (terminal) {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            terminal.innerHTML += `<br>[${timeStr}] ${message}`;
            terminal.scrollTop = terminal.scrollHeight; // អូសចុះក្រោមស្វ័យប្រវត្តិ
        }
    }
});
