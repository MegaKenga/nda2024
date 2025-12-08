// Карусель на главная в блоке работаем для вас


$(document).ready(function(){
    $('.sliderInfo .slider ').slick({
      autoplay: true,          
      autoplaySpeed: 5000,      
      infinite: true,          
      slidesToShow: 1,          
      slidesToScroll: 1,        
      arrows: false,          
      dots: true,              
      dotsClass: 'slick-dots', 
      appendDots: '.slick-dots' 
    });
  window.addEventListener('load', function() {
    // Находим все элементы с классом lazyloading
    const lazyElements = document.querySelectorAll('.lazyloading');

    // Перебираем найденные элементы
    lazyElements.forEach(function(element) {
      // Заменяем класс lazyloading на lazyloaded
      element.classList.remove('lazyloading');
      element.classList.add('lazyloaded');

      // Можно добавить дополнительную обработку
      if (element.tagName === 'IMG' && element.dataset.src) {
        element.src = element.dataset.src;
      }
    });

    console.log(`Обработано ${lazyElements.length} элементов с lazy loading`);
  });
});

