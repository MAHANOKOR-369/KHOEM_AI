mkdir -p static/js
cat << 'JS' > static/js/auth_engine.js
/**
 * ឯកសារ៖ static/js/auth_engine.js
 * មុខងារ៖ ផ្ទៀងផ្ទាត់សោសម្ងាត់ (Master Key) និងគ្រប់គ្រងសិទ្ធិចូលប្រើប្រាស់
 * គម្រោង៖ KHOEM_AI / Mahanokor 369
 */

const AuthEngine = {
    isAuthenticated: false,
    attempts: 0,

    // ទាញយក Config ឬប្រើ Default fallback បើគ្មាន APP_CONFIG
    getConfig: function() {
        return window.APP_CONFIG || {
            masterKeys: ["369", "123456", "KHOEM2026"],
            maxLoginAttempts: 5
        };
    },

    /**
     * ផ្ទៀងផ្ទាត់ Master Key ជាមួយបញ្ចូល
     * @param {string} inputKey 
     * @returns {boolean}
     */
    verifyKey: function(inputKey) {
        const config = this.getConfig();
        const cleanKey = (inputKey || "").trim();

        if (config.masterKeys.includes(cleanKey)) {
            this.isAuthenticated = true;
            this.attempts = 0;
            this.unlockSystem();
            return true;
        } else {
            this.attempts++;
            this.handleFailedAttempt();
            return false;
        }
    },

    /**
     * ដោះសោប្រព័ន្ធ និងបើកដំណើរការ UI
     */
    unlockSystem: function() {
        const lockscreen = document.getElementById("lockscreen");
        const lockErrorMsg = document.getElementById("lockerrormsg");

        if (lockscreen) lockscreen.style.display = "none";
        if (lockErrorMsg) lockErrorMsg.style.display = "none";

        console.log("[Auth] 🔓 ដោះសោប្រព័ន្ធជោគជ័យ! សូមស្វាគមន៍មកកាន់ Mahanokor 369។");

        // ចាប់ផ្តើម DashboardUI (ប្រសិនបើមាន) ដោយសុវត្ថិភាព
        if (typeof DashboardUI !== "undefined") {
            if (typeof DashboardUI.initCharts === "function") DashboardUI.initCharts();
            if (typeof DashboardUI.renderTable === "function") DashboardUI.renderTable();
        }
    },

    /**
     * ចាក់សោប្រព័ន្ធឡើងវិញ
     */
    lockSystem: function() {
        this.isAuthenticated = false;
        const lockscreen = document.getElementById("lockscreen");
        const masterKeyInput = document.getElementById("masterkey");

        if (lockscreen) lockscreen.style.display = "flex";
        if (masterKeyInput) masterKeyInput.value = "";

        console.log("[Auth] 🔒 ប្រព័ន្ធត្រូវបានចាក់សោសុវត្ថិភាព។");
    },

    /**
     * គ្រប់គ្រងករណីបញ្ចូលកូដខុស
     */
    handleFailedAttempt: function() {
        const config = this.getConfig();
        const remaining = config.maxLoginAttempts - this.attempts;
        const errorMsg = document.getElementById("lockerrormsg");

        if (errorMsg) {
            errorMsg.style.display = "block";
            errorMsg.innerHTML = `⚠️ ពិធីការបរាជ័យ៖ កូដខុស! (សាកល្បងបាន ${remaining > 0 ? remaining : 0} ដងទៀត)`;
        }

        if (this.attempts >= config.maxLoginAttempts) {
            console.warn("!! ព្រមានកម្រិតធ្ងន់: រកឃើញការប៉ុនប៉ងជ្រៀតចូល !!");
            if (errorMsg) {
                errorMsg.innerHTML = "🚫 ប្រព័ន្ធត្រូវបានចាក់សោបណ្តោះអាសន្ន ដោយសារបញ្ចូលកូដខុសច្រើនដង!";
            }
        }
    }
};
JS
