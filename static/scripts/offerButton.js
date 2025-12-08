// Скрипт, показывающий и скрывающий кнопку оформить заказ на странице с заказами

$(document).ready(function () {
    $('.modal').on('shown.bs.modal', function () {
        // Находим и скрываем блок с классом placeResult
        $('.placeResult').css('display', 'none');
    }).on('hidden.bs.modal', function () {
        // Показываем блок с классом placeResult
        $('.placeResult').css('display', 'flex');
    });
});

