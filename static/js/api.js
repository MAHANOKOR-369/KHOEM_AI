/**
 * ឯកសារ៖ api.js
 * មុខងារ៖ គ្រប់គ្រងការស្នើសុំទិន្នន័យពីម៉ាស៊ីនមេ (Fetch Data)
 */

const APIEngine = {
    // មុខងារទាញយកទិន្នន័យ (GET)
    fetchData: async function(endpoint) {
        try {
            console.log(`[API] កំពុងទាញយកទិន្នន័យពី: ${endpoint}...`);
            // សម្រាប់ពេលនេះ យើងប្រើទិន្នន័យសិប្បនិម្មិត (Mock Data) សិន
            return { status: "success", data: "ទិន្នន័យទទួលបានជោគជ័យ" };
            
            /* កូដពិតប្រាកដនៅពេលមាន Backend:
            const response = await fetch(`${APP_CONFIG.apiBaseUrl}${endpoint}`);
            return await response.json();
            */
        } catch (error) {
            console.error(`[API Error] បរាជ័យក្នុងការទាញយកទិន្នន័យ:`, error);
            return null;
        }
    },

    // មុខងារបញ្ជូនទិន្នន័យ (POST) - ឧ. បញ្ជូនសំណុំរឿងទាមទារសំណង
    sendData: async function(endpoint, payload) {
        console.log(`[API] កំពុងបញ្ជូនទិន្នន័យទៅកាន់ ${endpoint}...`, payload);
        return { status: "success", message: "ទិន្នន័យបានបញ្ជូនដោយជោគជ័យ" };
    }
};
