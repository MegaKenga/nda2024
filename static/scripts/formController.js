// // Скрипт для работы с модальными окнами
//
// const options = document.getElementById('options');
// const toggleOptions = document.getElementById('toggleOptions')
// const closeButton1 = document.getElementById('close1')
// const closeButton2 = document.getElementById('close2')
// $('html').removeClass('modal-open');
// document.getElementById('toggleOptions').onclick = function () {
//     options.style.display = 'flex';
//     toggleOptions.style.display = 'none'
//     $('body').removeClass('modal-open');
//     $('#emailModal, #callModal').on('hidden.bs.modal', function () {
//         $(this).find('form')[0].reset(); // Сбрасываем форму
//         if ($('.modal:visible').length === 0) {
//             document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
//         }
//     });
// };
//
// document.getElementById('close').onclick = function () {
//     options.style.display = 'none';
//     toggleOptions.style.display = 'flex'
//
//     $('body').removeClass('modal-open');
//     $('#emailModal, #callModal').on('hidden.bs.modal', function () {
//         $(this).find('form')[0].reset(); // Сбрасываем форму
//         if ($('.modal:visible').length === 0) {
//             document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
//         }
//     });
// };

// document.getElementById('close1').onclick = function () {
//     options.style.display = 'none';
//     toggleOptions.style.display = 'flex'
//     $('body').removeClass('modal-open');
//     $('#emailModal, #callModal').on('hidden.bs.modal', function () {
//         $(this).find('form')[0].reset(); // Сбрасываем форму
//         if ($('.modal:visible').length === 0) {
//             document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
//         }
//     });
//
// };

// document.getElementById('close2').onclick = function () {
//     options.style.display = 'none';
//     toggleOptions.style.display = 'flex'
//     $('body').removeClass('modal-open');
//     $('#emailModal, #callModal').on('hidden.bs.modal', function () {
//         $(this).find('form')[0].reset(); // Сбрасываем форму
//         if ($('.modal:visible').length === 0) {
//             document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
//         }
//     });
//
// };

document.addEventListener('DOMContentLoaded', function () {
  // Объявляем все переменные в начале
  const toggleOptions1 = document.getElementById('toggleOptions')
  const options1 = document.getElementById('options')
  const closeButton1 = document.getElementById('close')
  const options = document.getElementById('options')
  const formButtonEmail = document.querySelector('.formButtonEmail')
  const formButtonPhone = document.querySelector('.formButtonCall')
  const formButtonOrder = document.querySelector('#cart .orderButton')
  const emailModal = document.querySelector('#emailModal')
  const phoneModal = document.querySelector('#callModal')
  const orderModal = document.querySelector('.product ~ #modal')
  const closeButtons = document.querySelectorAll('.modal:not(#toast-warning) .btn-close');
  let fckClose = document.querySelector('#toast .btn-close')
  let fckClose2 = document.querySelector('#toast-warning .btn-close')
  //console.log(closeButtons)
  let modalBackdrop, needForm, modalContent, warnForm
  let isModalOpen = false
  fckClose.addEventListener('click', function () {
    closeModal('form')
  })
  fckClose2.addEventListener('click', function () {
    closeModal('warn')
  })

  // Создаем backdrop если его нет
  if (!document.querySelector('.modal-backdrop')) {
    modalBackdrop = document.createElement('div')
    modalBackdrop.className = 'modal-backdrop'
    modalBackdrop.style.display = 'none'
    modalBackdrop.style.backgroundColor = '#0000009e'
    document.body.appendChild(modalBackdrop)
  } else {
    modalBackdrop = document.querySelector('.modal-backdrop')
  }
  function addAsteriskToRequiredLabels() {
    // Находим все обязательные поля
    const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');

    requiredFields.forEach(field => {
      // Находим label, связанный с полем
      const label = findLabelForField(field);

      if (label && !label.innerHTML.includes('*')) {
        label.innerHTML += '*';
      }
    });
  }

// Функция для поиска label, связанного с полем
  function findLabelForField(field) {
    // Поиск по атрибуту for
    if (field.id) {
      const label = document.querySelector(`label[for="${field.id}"]`);
      if (label) return label;
    }

    // Поиск по вложенности (если поле внутри label)
    return field.closest('label');
  }
  addAsteriskToRequiredLabels();
  function applyModalStyles () {
    if (window.innerWidth <= 768) {
      needForm.style.width = '95%'
      needForm.style.margin = '20px auto'
      needForm.style.padding = '15px'
    } else {
      needForm.style.width = '100%'
      needForm.style.margin = '40px auto'
      needForm.style.padding = '30px'
    }
  }

  function closeModal (typeA) {

    document.getElementById("toast").classList.remove('show','modal')
    document.getElementById("toast-warning").classList.remove('show','modal')
    if(typeA === 'form') {
      if (needForm) {
        needForm.style.display = 'none'
        needForm.classList.remove('show')
        needForm.querySelector('form').reset();
        needForm.querySelectorAll('input,textarea,select').forEach( (elem) => {
          elem.style.border ="0px";
        })
      }
      modalBackdrop.style.display = 'none'
      document.body.style.overflow = ''
      isModalOpen = false
      document.querySelector('.container1 .toast-container').style.display = 'none';
    }
    //console.log(typeA)
  }

  function openModal (type) {
    emailModal.style.display = 'none'
    phoneModal.style.display = 'none'
    if(orderModal) orderModal.style.display = 'none'
    if (type === 'email') {
      emailModal.style.display = 'block'
      emailModal.classList.add('show')
      needForm = emailModal
    } else if (type === 'phone') {
      phoneModal.style.display = 'block'
      phoneModal.classList.add('show')
      needForm = phoneModal
    } else if (type === 'order') {
      orderModal.style.display = 'block'
      orderModal.classList.add('show')
      needForm = orderModal
    }
    modalBackdrop.style.display = 'block'
    document.body.style.overflow = 'hidden'
    isModalOpen = true
    applyModalStyles()
    document.addEventListener('click', function modalCloseHandler(e) {
      // Проверяем, что клик был вне .modal-dialog и его дочерних элементов
      if (!e.target.closest('.modal-dialog') && !e.target.closest('.formButtonEmail') && !e.target.closest('.formButtonCall') && !e.target.closest('.orderButton')) {
        if (!e.target.closest('#toast-warning')) {
          warnForm = 'form'
        } else {
          warnForm = 'warn'
        }
        closeModal(warnForm);
        // Удаляем обработчик после закрытия модального окна
        document.removeEventListener('click', modalCloseHandler);
      }
    });
  }

  // Обработчики событий
  toggleOptions1.addEventListener('click', function () {
    if (options1.style.display === 'none' || options1.style.display === '') {
      options1.style.display = 'flex'
      toggleOptions1.style.display = 'none'
    } else {
      options1.style.display = 'none'
      toggleOptions1.style.display = 'flex'
    }
  })

  closeButton1.addEventListener('click', function () {
    options1.style.display = 'none'
    toggleOptions1.style.display = 'flex'
  })

  formButtonEmail.addEventListener('click', function (e) {
    openModal('email')
  })

  formButtonPhone.addEventListener('click', function () {
    openModal('phone')
  })

  if(formButtonOrder) {
    formButtonOrder.addEventListener('click', function () {
      openModal('order')
    })
  }

  closeButtons.forEach(closeButton => {
    closeButton.addEventListener('click', function (e) {
      e.stopPropagation()
      if (!this.closest('#toast-warning')) {
        warnForm = 'form'
      } else {
        warnForm = 'warn'
      }
      closeModal(warnForm)
    })
  })
})
