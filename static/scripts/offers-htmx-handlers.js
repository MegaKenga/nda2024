// HTMX код для работы с корзиной, всплывающим окном со статусом отправки запроса с форм


document.addEventListener('htmx:afterOnLoad', function(event) {
    if (event?.detail?.requestConfig?.elt?.id !== "remove-offer-button") {
        return
    }
    const counter = document.querySelector("#offers-in-cart-counter")
    const currentCount = parseInt(counter.textContent, 10);

    if (!isNaN(currentCount) && currentCount > 0) {
        counter.textContent = String(currentCount - 1);
    }
});

// htmx handlers
function htmxHandlers() {
     //console.log("i am called")
    htmx.on("showMessage", (e) => {
      const toastElement = document.getElementById("toast")
      const toastBody = document.getElementById("toast-body")

      // Устанавливаем текст сообщения
      toastBody.innerHTML = '<h2>Уважаемые коллеги!</h2><p>Мы благодарны вам, что вы обратились в ООО «НДА Деловая медицинская компания». В ближайшее время мы обязательно с вами свяжемся.</p>';

      // Показываем тост
      toastElement.style.opacity = "1";

      // Скрываем тост через 3 секунды
      setTimeout(() => {
        toastElement.style.opacity = "0";

        // Удаляем элемент после анимации исчезновения
        setTimeout(() => {
          toastElement.remove();
        }, 300); // Должно совпадать с длительностью перехода
      }, 3000);

      //const toast = new bootstrap.Toast(toastElement, { delay: 3000 })
      //toastBody.innerText = e.detail.value
      //toast.show()
    })

    htmx.on("showError", (e) => {
      const toastElement = document.getElementById("toast-warning")
      const toastBody = document.getElementById("toast-warning-body")

      // Устанавливаем текст ошибки
      toastBody.textContent = e.detail.value;

      // Показываем сообщение
      toastElement.style.opacity = "1";

      // Скрываем через 3 секунды
      toastElement.style.display = "block";

      // Скрываем тост через 3 секунды
      setTimeout(() => {
        toastElement.style.opacity = "0";

        // Полностью скрываем после анимации
        setTimeout(() => {
          toastElement.style.display = "none";

          // Если элемент нужно удалить (не рекомендуется если он используется повторно)
          // toastElement.remove();
        }, 300);
      }, 3000);

      //const toast = new bootstrap.Toast(toastElement, { delay: 3000 })
      //toastBody.innerText = e.detail.value
      //toast.show()
    })

    if (typeof bootstrap === 'undefined') {
        console.warn('Bootstrap JS не подключен, модальные окна работать не будут.');
        return;
    }

    const modal = new bootstrap.Modal(document.getElementById("modal"))

    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      console.log(e.detail.target);

      if (e.detail.target.id == "dialog") {
        modal.show()
      }
    })

    htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #cart_modal_form => hide the modal
    if (e.detail.target.id == "cart_modal_form" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
      const counter = document.querySelector("#offers-in-cart-counter")
      counter.textContent = String(0);
    }
    })

    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("htmxHandlers");
    htmxHandlers()
});
