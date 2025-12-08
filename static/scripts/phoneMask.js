// Скрипт, создающий маску для номеров в формах
  let utilsScriptLoaded = false;

  async function loadUtilsScript(url) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = url;
      script.onload = () => {
        utilsScriptLoaded = true;
        resolve();
      };
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  $(document).ready(async function() {
    try {
      await loadUtilsScript("../../../static/scripts/utils.min.js");
    } catch (error) {
      console.error("Ошибка загрузки utilsScript:", error);
      return;
    }

    function initializePhoneMasks() {
      console.log('initializePhoneMasks called');
      
      $('.phone-mask:not([data-intl-tel-input-initialized])').each(function() {
        const phoneInput = this;

        if ($(phoneInput).data('iti')) {
          $(phoneInput).data('iti').destroy();
        }
        
        const iti = intlTelInput(phoneInput, {
          separateDialCode: true,
          initialCountry: "ru",
          autoPlaceholder: "aggressive",
          nationalMode: true,
        });

        $(phoneInput).data('iti', iti);
        $(this).attr('data-intl-tel-input-initialized', 'true');

        $(phoneInput).on('input', function() {
          let number = iti.getNumber(intlTelInputUtils.numberFormat.E164);
          if (number.startsWith('+7')) {
            number = number.replace('+7', '');
            number = number
              .replace(/\D/g, '')
              .replace(/^(\d{3})(\d{3})(\d{2})(\d{2}).*/, '($1) $2-$3-$4');
            $(this).val(number);
          }
        });
      });
    }

    initializePhoneMasks();

    $('#modal').on('shown.bs.modal', function() {
      initializePhoneMasks();
    });

    // $(document).off('focus', '.phone-mask'); // Удаляем лишний обработчик
  });

document.addEventListener('DOMContentLoaded', function () {
  initializePhoneMasks();
});

function initializePhoneMasks() {
      console.log('initializePhoneMasks called');
      
      $('.phone-mask:not([data-intl-tel-input-initialized])').each(function() {
        const phoneInput = this;

        if ($(phoneInput).data('iti')) {
          $(phoneInput).data('iti').destroy();
        }
        
        const iti = intlTelInput(phoneInput, {
          separateDialCode: true,
          initialCountry: "ru",
          autoPlaceholder: "aggressive",
          nationalMode: true,
        });

        $(phoneInput).data('iti', iti);
        $(this).attr('data-intl-tel-input-initialized', 'true');

        $(phoneInput).on('input', function() {
          let number = iti.getNumber(intlTelInputUtils.numberFormat.E164);
          if (number.startsWith('+7')) {
            number = number.replace('+7', '');
            number = number
              .replace(/\D/g, '')
              .replace(/^(\d{3})(\d{3})(\d{2})(\d{2}).*/, '($1) $2-$3-$4');
            $(this).val(number);
          }
        });
      });
    }

document.addEventListener('htmx:afterSwap', function (event) {
  // Проверяем, что это именно модалка подгрузилась
  const target = event.detail.target;

  // Если обновлённый элемент содержит модалку (или phone-mask внутри)
  if (target && target.querySelector && target.querySelector('.phone-mask')) {
    console.log('HTMX modal content loaded — reinitializing phone masks');
    
    // Даём 100ms, чтобы DOM стабилизировался
    setTimeout(() => {
      initializePhoneMasks();
    }, 100);
  }
});

document.body.addEventListener('htmx:afterOnLoad', function (event) {
  try {
    const response = JSON.parse(event.detail.xhr.responseText);

    if (response.success) {
      console.log("Успешная отправка, закрываю модалку...");
      closeModal('order');

      if (response.reloadPage) {
        // setTimeout(() => location.reload(), 500);
      }
    }
  } catch (err) {
    // ответ не JSON — пропускаем
  }
});

function closeModal (typeA) {
  var modal = document.getElementById("modal")
  modal.style.display = 'none';
  modal.classList.remove('show');
  
  document.querySelectorAll(".modal-backdrop").forEach(function(backdrop) {
    backdrop.style.display = 'none';
  });
}

