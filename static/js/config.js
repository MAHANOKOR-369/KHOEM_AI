/**
 * ឯកសារ៖ config.js
 * មុខងារ៖ រក្សាទុកការកំណត់ (Settings), API Keys, និងទិន្នន័យថេរ (Constants)
 */

const APP_CONFIG = {
    appName: "Mahanokor 369 | AI Digital Insurance",
    version: "9.0.1",
    apiBaseUrl: "https://api.mahanokor369.com/v1", // តំណភ្ជាប់ទៅ Backend
    environment: "production", // 'development' ឬ 'production'
    
    // លេខកូដសម្ងាត់សម្រាប់ដោះសោរប្រព័ន្ធ (អាចប្រើបានច្រើន)
    masterKeys: ["369", "905", "906.106.905", "906106905"],
    
    // ការកំណត់សុវត្ថិភាព
    sessionTimeoutMinutes: 30,
    maxLoginAttempts: 3
};

console.log(`[Config] ផ្ទុកការកំណត់រួចរាល់៖ ${APP_CONFIG.appName} v${APP_CONFIG.version}`);
