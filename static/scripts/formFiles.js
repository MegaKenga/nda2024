// Имя прикреплённого файла в форме

$('#modal').on('shown.bs.modal', function () {
    function handleFiles(inputId, containerClass) {
        var input = document.getElementById(inputId);
        var filenameContainer = document.querySelector(containerClass);
    
        input.addEventListener("change", function () {
            var fileName = "";
            if (this.files && this.files.length > 0) {
                fileName = this.files[0].name;
            }
            filenameContainer.textContent = fileName || "Нет выбранного файла";
        });
    }


    function legalFunction() {
        handleFiles("contact_form_company_details_input", ".filename");
    }
    
    function physicalFunction() {
        handleFiles("p_contact_form_company_details_input", ".filename1");
    }


    const tabs = document.querySelectorAll('#myTab .nav-link');
    legalFunction()
    // Подписываемся на событие shown.bs.tab
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', (e) => {
            const targetTab = e.target.getAttribute('data-bs-target'); // Получаем цель текущей вкладки
            
            switch(targetTab) {
                case '#legal':
                    legalFunction(); // Вызываем функцию для юридической вкладки
                    break;
                case '#physical':
                    physicalFunction(); // Вызываем функцию для физической вкладки
                    break;
                
                    
            }
        });
    });
    

});