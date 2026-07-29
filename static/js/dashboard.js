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

const DashboardUI = {
    // ... (ទុកកូដចាស់ៗដដែល) ...

    // មុខងារថ្មី៖ គូរតារាងទិន្នន័យ
    renderTable: function() {
        const tbody = document.getElementById("dataTableBody");
        if (!tbody) return;
        
        tbody.innerHTML = ""; // សម្អាតទិន្នន័យចាស់
        const data = MahanokorInsuranceCore.insuranceRegistry; // ទាញពីខួរក្បាលស្នូល
        
        for (let key in data) {
            let riskColor = data[key].riskLevel === "High" ? "var(--red)" : 
                           (data[key].riskLevel === "Medium" ? "var(--gold)" : "var(--green)");
            
            tbody.innerHTML += `
                <tr>
                    <td>${key}</td>
                    <td>${data[key].type}</td>
                    <td style="color: ${riskColor}; font-weight: bold;">${data[key].riskLevel || 'N/A'}</td>
                    <td><span style="background: rgba(16, 185, 129, 0.2); padding: 2px 5px; border-radius: 3px; color: var(--green);">${data[key].status}</span></td>
                </tr>
            `;
        }
    },

    logToTerminal: function(message, color = "#06b6d4") {
        const terminal = document.getElementById("logoutput");
        if (terminal) {
            const time = new Date().toLocaleTimeString();
            terminal.innerHTML += `<div><span class="text-slate-500">[${time}]</span> <span style="color: ${color}">${message}</span></div>`;
            terminal.scrollTop = terminal.scrollHeight;
        }
    }
};
