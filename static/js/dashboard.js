/**
 * ឯកសារ៖ dashboard.js
 * មុខងារ៖ ធ្វើបច្ចុប្បន្នភាពទិន្នន័យលើអេក្រង់ ដូចជាតារាង ក្រាហ្វ និង CCTVs
 */

const DashboardUI = {
    initCharts: function() {
        console.log("[Dashboard] កំពុងរៀបចំក្រាហ្វចំណូល...");
        // កូដគូរ Chart.js របស់ប្អូនអាចយកមកដាក់ក្នុងនេះបាន
    },

    updateCCTV: function(location, statusText) {
        document.getElementById("cctvid").innerHTML = `cam-${Math.floor(Math.random() * 10)} [${location}]`;
        document.getElementById("cctvstatus").innerHTML = statusText;
        console.log(`[UI] បានប្តូរ CCTV ទៅតំបន់: ${location}`);
    },

    logToTerminal: function(message, color = "#06b6d4") {
        const terminal = document.getElementById("logoutput");
        if (terminal) {
            const time = new Date().toLocaleTimeString();
            terminal.innerHTML += `<div><span class="text-slate-500">[${time}]</span> <span style="color: ${color}">${message}</span></div>`;
            terminal.scrollTop = terminal.scrollHeight; // ឲ្យវារំកិលចុះក្រោមរហូត
        }
    }
};
