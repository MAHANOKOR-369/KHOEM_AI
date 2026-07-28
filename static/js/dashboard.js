// ឈ្មោះឯកសារ: static/js/dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("KHOEM_AI Dashboard Loaded Successfully.");

    // ចាប់យកប៊ូតុងទាំងអស់នៅលើទំព័រ
    const buttons = document.querySelectorAll('button');

    buttons.forEach(button => {
        // ដកមុខងារ onclick ចាស់ចេញសិន ដើម្បីកុំឱ្យជាន់គ្នា
        button.removeAttribute('onclick');
        
        button.addEventListener('click', function(e) {
            const serviceName = e.target.parentElement.querySelector('h3').innerText;
            
            // លោតផ្ទាំងបញ្ជាក់ទៅកាន់អតិថិជន
            alert(`សូមអរគុណដែលចាប់អារម្មណ៍លើ: ${serviceName}\n\nសូមផ្ញើសារមកកាន់ Telegram: @ដាក់ឈ្មោះតេឡេក្រាមបងទីនេះ ដើម្បីពិភាក្សាលម្អិត និងបង់ប្រាក់។`);
            
            // បើកតេឡេក្រាមបងតែម្តង (បងអាចដូរលីងទៅតេឡេក្រាមបងផ្ទាល់)
            // window.open('https://t.me/ដាក់ឈ្មោះតេឡេក្រាមបងទីនេះ', '_blank');
        });
    });
});
