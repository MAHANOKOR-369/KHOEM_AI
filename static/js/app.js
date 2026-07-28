/**
 * ឯកសារ៖ app.js
 * មុខងារ៖ ជាឯកសារមេសម្រាប់ Boot ប្រព័ន្ធទាំងមូលឡើងនៅពេលវេបសាយបើក
 */

document.addEventListener("DOMContentLoaded", () => {
    console.log("🚀 កំពុងចាប់ផ្តើមប្រព័ន្ធ Mahanokor 369...");

    // ១. ភ្ជាប់ Event Listener ទៅប៊ូតុង Login
    const unlockBtn = document.querySelector("button[onclick=\"customtrigger('unlock_system')\"]");
    if (unlockBtn) {
        unlockBtn.onclick = function(e) {
            e.preventDefault();
            const key = document.getElementById("masterkey").value;
            AuthEngine.verifyKey(key);
        };
    }

    // ២. បើកមុខងារតាមដានពេលវេលា (Clock)
    setInterval(() => {
        const clockEl = document.getElementById("clock");
        if (clockEl) {
            clockEl.innerText = "CELESTIAL TIME: " + new Date().toLocaleString();
        }
    }, 1000);

    // ៣. បង្ហាញសារស្វាគមន៍ក្នុង Terminal (បើមិនទាន់ Login ក៏ឃើញដែរ)
    DashboardUI.logToTerminal("ប្រព័ន្ធត្រៀមរួចរាល់។ សូមវាយកូដសម្ងាត់មេដើម្បីដំណើរការ ម៉ាស៊ីន AI ធានារ៉ាប់រង។", "#64748b");
});
