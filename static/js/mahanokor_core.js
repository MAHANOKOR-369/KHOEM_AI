/**
 * ឯកសារ៖ mahanokor_core.js
 * មុខងារ៖ ខួរក្បាល AI ស្នូលសម្រាប់គ្រប់គ្រងប្រព័ន្ធធានារ៉ាប់រងឌីជីថល ៣៦៩
 */

const MahanokorInsuranceCore = {
    // កំណត់ទិន្នន័យក្លែងបន្លំ (Mock Database) សម្រាប់ធ្វើតេស្ត
    insuranceRegistry: {
        "vehicle_001": { type: "Vehicle", owner: "ID-905", status: "Active", riskLevel: "Low", autoClaim: true },
        "machinery_999": { type: "Machinery", owner: "Corp-A", status: "Active", riskLevel: "Medium", autoClaim: true },
        "infra_bridge_01": { type: "Infrastructure", location: "PP", status: "Monitoring", riskLevel: "High", autoClaim: false },
        "human_369": { type: "Human", healthScore: 98, heartRate: "Normal", status: "Active", autoClaim: true },
        "animal_k9": { type: "Animal", species: "Dog", tracking: "Online", status: "Active", autoClaim: true }
    },

    // មុខងារត្រួតពិនិត្យសុពលភាពនៃការធានារ៉ាប់រង
    validateCoverage: function(targetId) {
        console.log(`[AI Core] ⚙️ កំពុងស្កេនទិន្នន័យធានារ៉ាប់រងសម្រាប់គោលដៅ ID: ${targetId}...`);
        
        const data = this.insuranceRegistry[targetId];
        
        if (data) {
            console.log(`[AI Core] ✅ រកឃើញទិន្នន័យ! ប្រភេទ៖ ${data.type}`);
            this.processSmartContract(data);
            return data;
        } else {
            console.error(`[AI Core] ❌ ស្វែងរកមិនឃើញទិន្នន័យធានារ៉ាប់រងសម្រាប់ ID: ${targetId} នេះទេ!`);
            return null;
        }
    },

    // មុខងារវិភាគហានិភ័យ និងអនុម័តសំណងស្វ័យប្រវត្តិ (Smart Contract)
    processSmartContract: function(data) {
        if (data.autoClaim && data.status === "Active") {
            console.log(`[Smart Contract] ⚡ ការទូទាត់សំណង និងការធានាត្រូវបានអនុម័តដោយស្វ័យប្រវត្តិសម្រាប់ ${data.type}។ (Risk Level: ${data.riskLevel || 'N/A'})`);
        } else {
            console.warn(`[Alert] ⚠️ ${data.type} ទាមទារការត្រួតពិនិត្យបន្ថែមពីភ្នាក់ងារ AI សន្តិសុខ! (ហានិភ័យកម្រិតខ្ពស់ ឬអសកម្ម)`);
        }
    },
    
    // មុខងារស្កេនបរិស្ថានជុំវិញ (Sensor Pulse)
    environmentalScan: function() {
        console.log("[Sensor] 🌐 កំពុងធ្វើបច្ចុប្បន្នភាពស្ថានភាពហេដ្ឋារចនាសម្ព័ន្ធ និងគ្រឿងចក្រនៅក្នុងប្រព័ន្ធរួម...");
        // Logic បន្ថែមអាចសរសេរនៅទីនេះ...
    }
};

// --- ការភ្ជាប់ទៅកាន់ UI របស់ប្អូន ---
// នៅពេលដែលចុចប៊ូតុងនៅក្នុង HTML, វានឹងហៅមុខងារទាំងនេះ

window.triggerInsuranceCheck = function(id) {
    MahanokorInsuranceCore.validateCoverage(id);
};

// ដំណើរការដំបូងពេលឯកសារនេះត្រូវបាន Load ចូល
document.addEventListener("DOMContentLoaded", () => {
    console.log("🔱 Mahanokor Core System [Insurance Matrix] is ONLINE.");
    MahanokorInsuranceCore.environmentalScan();
});

function addNewTarget() {
    const id = document.getElementById("targetId").value;
    const type = document.getElementById("targetType").value;
    
    // បន្ថែមទិន្នន័យចូលទៅក្នុង AI Core
    MahanokorInsuranceCore.insuranceRegistry[id] = {
        type: type,
        status: "Active",
        riskLevel: "Low", // កំណត់កម្រិតហានិភ័យទាបជាបឋម
        autoClaim: true
    };
    
    // បង្ហាញ Log ក្នុង Terminal
    DashboardUI.logToTerminal(`បានចុះឈ្មោះគោលដៅធានារ៉ាប់រងថ្មីជោគជ័យ៖ [${id}] - ប្រភេទ៖ ${type}`, "var(--green)");
    
    // ធ្វើបច្ចុប្បន្នភាពតារាង
    DashboardUI.renderTable();
    
    // លុបអក្សរក្នុងប្រអប់វិញ
    document.getElementById("targetId").value = "";
}
