/**
 * ឯកសារ៖ auth_engine.js
 * មុខងារ៖ ផ្ទៀងផ្ទាត់សោសម្ងាត់ (Master Key) និងគ្រប់គ្រងសិទ្ធិចូលប្រើប្រាស់
 */

const AuthEngine = {
    isAuthenticated: false,
    attempts: 0,

    verifyKey: function(inputKey) {
        if (APP_CONFIG.masterKeys.includes(inputKey)) {
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

    unlockSystem: function() {
        document.getElementById("lockscreen").style.display = "none";
        document.getElementById("lockerrormsg").style.display = "none";
        console.log("[Auth] 🔓 ដោះសោរប្រព័ន្ធជោគជ័យ! សូមស្វាគមន៍មកកាន់ Mahanokor 369។");
        
        // ចាប់ផ្តើមមុខងារផ្សេងៗបន្ទាប់ពី Login ចូល
        DashboardUI.initCharts();
        DashboardUI.renderTable();
    },
    lockSystem: function() {
        this.isAuthenticated = false;
        document.getElementById("lockscreen").style.display = "flex";
        document.getElementById("masterkey").value = "";
        console.log("[Auth] 🔒 ប្រព័ន្ធត្រូវបានចាក់សោរសុវត្ថិភាព។");
    },

    handleFailedAttempt: function() {
        const errorMsg = document.getElementById("lockerrormsg");
        errorMsg.style.display = "block";
        errorMsg.innerHTML = `⚠️ ពិធីការបរាជ័យ៖ កូដខុស! (សាកល្បងបាន ${APP_CONFIG.maxLoginAttempts - this.attempts} ដងទៀត)`;
        
        if (this.attempts >= APP_CONFIG.maxLoginAttempts) {
            console.warn("!! ព្រមានកម្រិតធ្ងន់: រកឃើញការប៉ុនប៉ងជ្រៀតចូល !!");
            // អាចបន្ថែមមុខងារបិទប្រព័ន្ធ (Freeze System) នៅទីនេះ
        }
    }
};
