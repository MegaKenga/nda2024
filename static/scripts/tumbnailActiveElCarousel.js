// Выделение активного элемента в миниатюрах карусели внутри товара

document.addEventListener('DOMContentLoaded', function() {
    const carouselElement = document.getElementById('carouselExampleIndicators');

    carouselElement.addEventListener('slid.bs.carousel', function(e) {
        const activeSlideIndex = e.to;
        const thumbnailList = document.querySelector('.tumbnails-list'); // Получаем контейнер миниатюр
        const currentActive = thumbnailList.querySelector('.thumbnailContainer.active'); // Получаем текущий активный элемент
        const nextActive = thumbnailList.querySelector(`.thumbnailContainer[data-bs-slide-to="${activeSlideIndex}"]`); // Получаем следующий активный элемент

        if (currentActive) {
            currentActive.classList.remove('active');
        }

        if (nextActive) {
            nextActive.classList.add('active');
        }
    });
});
