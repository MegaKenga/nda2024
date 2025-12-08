// Скрипт, перезагружающий страницу при нажатии не на открытую форму

document.addEventListener('htmx:afterRequest', function(evt) {
    if (evt.detail.successful) {
        try {
            const triggerData = JSON.parse(evt.detail.xhr.getResponseHeader('HX-Trigger'));
            /*if (triggerData && triggerData.reloadPage === true) {
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            }*/
        } catch (e) {
            console.error("Ошибка при разборе HX-Trigger:", e);
        }
    }
});