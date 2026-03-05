document.addEventListener('DOMContentLoaded', function () {

  /* ========== Секция: Мобильное меню ========== */
  var mobileMenu = document.getElementById('mobile-menu');
  var menuOpenBtn = document.querySelector('[data-menu-open]');
  var menuCloseBtns = document.querySelectorAll('[data-menu-close]');

  if (mobileMenu && menuOpenBtn) {
    function openMenu() {
      mobileMenu.classList.add('mobile-menu_is-open');
      document.body.classList.add('body_mobile-menu-open');
      mobileMenu.setAttribute('aria-hidden', 'false');
      menuOpenBtn.setAttribute('aria-expanded', 'true');
      menuOpenBtn.setAttribute('aria-label', 'Закрыть меню');
      document.body.style.overflow = 'hidden';
    }
    function closeMenu() {
      mobileMenu.classList.remove('mobile-menu_is-open');
      document.body.classList.remove('body_mobile-menu-open');
      mobileMenu.setAttribute('aria-hidden', 'true');
      menuOpenBtn.setAttribute('aria-expanded', 'false');
      menuOpenBtn.setAttribute('aria-label', 'Открыть меню');
      document.body.style.overflow = '';
    }
    menuOpenBtn.addEventListener('click', function () {
      if (mobileMenu.classList.contains('mobile-menu_is-open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });
    menuCloseBtns.forEach(function (btn) {
      btn.addEventListener('click', closeMenu);
    });
  }

  /* ========== Секция: Дропдаун «Каталог» в мобильном меню ========== */
  var dropdownBlock = document.querySelector('[data-dropdown]');
  var dropdownToggle = document.querySelector('[data-dropdown-toggle]');
  if (dropdownBlock && dropdownToggle) {
    dropdownToggle.addEventListener('click', function () {
      var isOpen = dropdownBlock.classList.toggle('mobile-menu__dropdown_is-open');
      dropdownToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  /* ========== Секция: Hero-contact ========== */
  var heroContact = document.getElementById('hero-contact');
  var contactTrigger = document.querySelector('[data-contact-trigger]');

  if (heroContact && contactTrigger) {
    contactTrigger.addEventListener('click', function () {
      heroContact.classList.toggle('hero-contact_is-open');
      var open = heroContact.classList.contains('hero-contact_is-open');
      heroContact.setAttribute('aria-expanded', open);
      contactTrigger.setAttribute('aria-label', open ? 'Закрыть' : 'Способы связи');
    });
  }

  /* ========== Секция: Табы каталога ========== */
  var catalogTabs = document.querySelectorAll('.catalog__tab');
  var catalogPanels = document.querySelectorAll('.catalog__panel');

  if (catalogTabs.length && catalogPanels.length) {
    catalogTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var tabName = this.getAttribute('data-tab');
        catalogTabs.forEach(function (t) { t.classList.remove('catalog__tab_active'); });
        this.classList.add('catalog__tab_active');
        catalogPanels.forEach(function (panel) {
          panel.classList.remove('catalog__panel_active');
          if (panel.getAttribute('data-panel') === tabName) {
            panel.classList.add('catalog__panel_active');
          }
        });
      });
    });
  }

  /* ========== Секция: Вкладки страницы товара ========== */
  var productTabBtns = document.querySelectorAll('[data-product-tab]');
  var productPanels = document.querySelectorAll('[data-product-panel]');

  if (productTabBtns.length && productPanels.length) {
    productTabBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var tabId = this.getAttribute('data-product-tab');
        var isAccordion = this.closest('.product-tabs-accordion');
        var isAccordionView = window.matchMedia('(max-width: 640px)').matches;
        var isAlreadyActive = this.classList.contains('product-tabs__btn_active');

        if (isAccordion && isAccordionView && isAlreadyActive) {
          this.classList.remove('product-tabs__btn_active');
          this.setAttribute('aria-selected', 'false');
          var panelToHide = document.querySelector('[data-product-panel="' + tabId + '"]');
          if (panelToHide) {
            panelToHide.classList.remove('product-panel_active');
            panelToHide.setAttribute('hidden', '');
          }
          return;
        }

        productTabBtns.forEach(function (b) {
          b.classList.remove('product-tabs__btn_active');
          b.setAttribute('aria-selected', 'false');
        });
        this.classList.add('product-tabs__btn_active');
        this.setAttribute('aria-selected', 'true');
        productPanels.forEach(function (panel) {
          if (panel.getAttribute('data-product-panel') === tabId) {
            panel.classList.add('product-panel_active');
            panel.removeAttribute('hidden');
          } else {
            panel.classList.remove('product-panel_active');
            panel.setAttribute('hidden', '');
          }
        });

        var accordion = this.closest('.product-tabs-accordion');
        if (accordion) {
          if (tabId === 'order') {
            accordion.classList.add('product-tabs-accordion_order-active');
          } else {
            accordion.classList.remove('product-tabs-accordion_order-active');
          }
        }
      });
    });

    var initialActiveBtn = document.querySelector('.product-tabs-accordion .product-tabs__btn_active[data-product-tab]');
    if (initialActiveBtn) {
      var initialTabId = initialActiveBtn.getAttribute('data-product-tab');
      var accordion = initialActiveBtn.closest('.product-tabs-accordion');
      if (accordion && initialTabId === 'order') {
        accordion.classList.add('product-tabs-accordion_order-active');
      }
    }
  }

  /* ========== Секция: Количество +/- в таблице заказа ========== */
  var qtyControls = document.querySelectorAll('.ru-table-wrap_order .ru-table__qty-control');
  qtyControls.forEach(function (control) {
    var input = control.querySelector('.ru-table__qty-input');
    var btnMinus = control.querySelector('.ru-table__qty-btn_minus');
    var btnPlus = control.querySelector('.ru-table__qty-btn_plus');
    var btnAdd = control.querySelector('.ru-table__qty-add');
    if (input && btnMinus && btnPlus) {
      btnMinus.addEventListener('click', function () {
        var val = parseInt(input.value, 10) || 0;
        if (val > 0) input.value = val - 1;
      });
      btnPlus.addEventListener('click', function () {
        var val = parseInt(input.value, 10) || 0;
        input.value = val + 1;
      });
    }
    if (btnAdd) {
      btnAdd.addEventListener('click', function (e) {
        e.preventDefault();
        var row = control.closest('ol.ru-table__ru-blue, ol.ru-table__ru-gray');
        var qty = parseInt(control.querySelector('.ru-table__qty-input').value, 10) || 0;
        if (row && qty > 0) {
          row.setAttribute('data-order-added', 'true');
          if (window.updateOrderTotalCount) window.updateOrderTotalCount();
        }
      });
    }
  });

  /* Плашка «Всего изделий в заказе» — показывается только когда count > 0 */
  var orderTotalPanel = document.getElementById('orderTotalPanel');
  var orderTotalCount = document.getElementById('orderTotalCount');

  function updateOrderTotalCount() {
    if (!orderTotalCount || !orderTotalPanel) return;
    var addedRows = document.querySelectorAll('.ru-table-wrap_order .ru-table__ru-blue[data-order-added], .ru-table-wrap_order .ru-table__ru-gray[data-order-added]');
    var count = addedRows.length;
    orderTotalCount.textContent = String(count);
    if (count > 0) {
      orderTotalPanel.removeAttribute('hidden');
    } else {
      orderTotalPanel.setAttribute('hidden', '');
    }
  }

  window.updateOrderTotalCount = updateOrderTotalCount;

  if (orderTotalPanel) {
    orderTotalPanel.setAttribute('hidden', '');
  }
  if (orderTotalPanel && orderTotalCount) {
    updateOrderTotalCount();
  }

  var btnDeleteAll = document.querySelector('.product-order__action-btn_delete');
  if (btnDeleteAll && window.updateOrderTotalCount) {
    btnDeleteAll.addEventListener('click', function () {
      document.querySelectorAll('.ru-table-wrap_order .ru-table__ru-blue[data-order-added], .ru-table-wrap_order .ru-table__ru-gray[data-order-added]').forEach(function (row) {
        row.removeAttribute('data-order-added');
      });
      document.querySelectorAll('.ru-table-wrap_order .ru-table__qty-input').forEach(function (input) {
        input.value = '0';
      });
      updateOrderTotalCount();
    });
  }

  var fileInput = document.getElementById('product-order-file-input');
  var uploadBtn = document.querySelector('[data-upload-btn]');
  if (fileInput && uploadBtn) {
    var uploadBtnDefaultText = uploadBtn.textContent;
    fileInput.addEventListener('change', function () {
      uploadBtn.textContent = this.files && this.files.length ? this.files[0].name : uploadBtnDefaultText;
    });
  }

  /* ========== Секция: Попап «Оформить заказ» ========== */
  var orderPopup = document.getElementById('orderPopup');
  var orderPopupCaption = document.querySelector('.product-order__total-caption');
  var orderPopupCloseBtns = document.querySelectorAll('[data-order-popup-close]');
  var orderPopupTabs = document.querySelectorAll('.order-popup__tab');
  var orderPopupSummaryList = document.getElementById('orderPopupSummaryList');
  var orderPopupSummaryEmpty = document.getElementById('orderPopupSummaryEmpty');

  function openOrderPopup() {
    if (!orderPopup) return;
    orderPopup.removeAttribute('hidden');
    orderPopup.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    document.body.classList.add('body_order-popup-open');
    fillOrderPopupSummary();
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        orderPopup.classList.add('order-popup_is-open');
      });
    });
  }

  function closeOrderPopup() {
    if (!orderPopup) return;
    orderPopup.classList.remove('order-popup_is-open');
    orderPopup.addEventListener('transitionend', function onCloseEnd(e) {
      if (e.target !== orderPopup || e.propertyName !== 'opacity') return;
      orderPopup.removeEventListener('transitionend', onCloseEnd);
      orderPopup.setAttribute('hidden', '');
      orderPopup.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      document.body.classList.remove('body_order-popup-open');
    });
  }

  function fillOrderPopupSummary() {
    if (!orderPopupSummaryList || !orderPopupSummaryEmpty) return;
    var rows = document.querySelectorAll('.ru-table-wrap_order .ru-table__ru-blue[data-order-added], .ru-table-wrap_order .ru-table__ru-gray[data-order-added]');
    orderPopupSummaryList.innerHTML = '';
    if (rows.length === 0) {
      orderPopupSummaryList.appendChild(orderPopupSummaryEmpty);
      orderPopupSummaryEmpty.hidden = false;
      return;
    }
    orderPopupSummaryEmpty.hidden = true;
    rows.forEach(function (row) {
      var codeEl = row.querySelector('.ru-table__td.ru-table__td_num');
      var qtyInput = row.querySelector('.ru-table__qty-input');
      var code = codeEl ? codeEl.textContent.trim() : '';
      var qty = qtyInput ? (parseInt(qtyInput.value, 10) || 0) : 0;
      if (qty <= 0) return;
      var li = document.createElement('li');
      li.className = 'order-popup__summary-row';
      li.innerHTML = '<span class="order-popup__summary-row-name">' + (code || '—') + '</span><span class="order-popup__summary-row-qty">' + qty + '</span>';
      orderPopupSummaryList.appendChild(li);
    });
  }

  if (orderPopupCaption) {
    orderPopupCaption.addEventListener('click', function () {
      openOrderPopup();
    });
  }
  if (orderPopupCloseBtns.length) {
    orderPopupCloseBtns.forEach(function (btn) {
      btn.addEventListener('click', closeOrderPopup);
    });
  }
  var orderPopupPanels = orderPopup ? orderPopup.querySelectorAll('.order-popup__form-panel') : [];
  var orderPopupTitlePhysical = document.querySelector('[data-order-summary-title-physical]');
  var orderPopupTitleLegal = document.querySelector('[data-order-summary-title-legal]');
  var orderPopupLegalIntro = document.getElementById('orderPopupLegalIntro');

  if (orderPopupTabs.length) {
    orderPopupTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var target = this.getAttribute('data-order-tab');
        orderPopupTabs.forEach(function (t) {
          t.classList.remove('order-popup__tab_active');
          t.setAttribute('aria-selected', 'false');
        });
        this.classList.add('order-popup__tab_active');
        this.setAttribute('aria-selected', 'true');
        if (orderPopupPanels.length) {
          orderPopupPanels.forEach(function (panel) {
            if (panel.getAttribute('data-order-panel') === target) {
              panel.removeAttribute('hidden');
            } else {
              panel.setAttribute('hidden', '');
            }
          });
        }
        if (orderPopupTitlePhysical && orderPopupTitleLegal) {
          if (target === 'legal') {
            orderPopupTitlePhysical.setAttribute('hidden', '');
            orderPopupTitleLegal.removeAttribute('hidden');
          } else {
            orderPopupTitlePhysical.removeAttribute('hidden');
            orderPopupTitleLegal.setAttribute('hidden', '');
          }
        }
        if (orderPopupLegalIntro) {
          if (target === 'legal') {
            orderPopupLegalIntro.removeAttribute('hidden');
          } else {
            orderPopupLegalIntro.setAttribute('hidden', '');
          }
        }
      });
    });
  }

  var orderPopupForm = document.getElementById('orderPopupForm');
  if (orderPopupForm) {
    var orderPopupInputs = orderPopupForm.querySelectorAll('.order-popup__input, .order-popup__textarea');
    var orderPopupPrivacyWraps = orderPopupForm.querySelectorAll('.order-popup__checkbox-wrap_cookie');
    var orderPopupPrivacyCheckbox = document.getElementById('orderPopupPrivacy');
    var orderPopupPrivacyCheckboxLegal = document.getElementById('orderPopupPrivacyLegal');
    var orderPopupCaptcha = document.getElementById('orderPopupCaptcha');
    var orderPopupCaptchaLegal = document.getElementById('orderPopupCaptchaLegal');

    function removeError(el) {
      if (!el) return;
      el.classList.remove('order-popup__input_error');
      orderPopupPrivacyWraps.forEach(function (wrap) {
        wrap.classList.remove('order-popup__input_error');
      });
    }
    orderPopupInputs.forEach(function (input) {
      input.addEventListener('input', function () { removeError(this); });
      input.addEventListener('change', function () { removeError(this); });
    });
    if (orderPopupPrivacyCheckbox) {
      orderPopupPrivacyCheckbox.addEventListener('change', function () {
        var w = this.closest('.order-popup__checkbox-wrap_cookie');
        if (w) w.classList.remove('order-popup__input_error');
      });
    }
    if (orderPopupPrivacyCheckboxLegal) {
      orderPopupPrivacyCheckboxLegal.addEventListener('change', function () {
        var w = this.closest('.order-popup__checkbox-wrap_cookie');
        if (w) w.classList.remove('order-popup__input_error');
      });
    }

    orderPopupForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;
      var activePanel = orderPopupForm.querySelector('.order-popup__form-panel:not([hidden])');
      var isLegal = activePanel && activePanel.getAttribute('data-order-panel') === 'legal';

      function setError(el, hasError) {
        if (!el) return;
        if (hasError) {
          el.classList.add('order-popup__input_error');
        } else {
          el.classList.remove('order-popup__input_error');
        }
      }

      if (isLegal) {
        var fioL = orderPopupForm.querySelector('[name="fio_legal"]');
        var phoneL = orderPopupForm.querySelector('[name="phone_legal"]');
        var emailL = orderPopupForm.querySelector('[name="email_legal"]');
        var inn = orderPopupForm.querySelector('[name="inn"]');
        var companyName = orderPopupForm.querySelector('[name="company_name"]');
        var privacyWrapL = orderPopupForm.querySelector('.order-popup__form-panel_legal .order-popup__checkbox-wrap_cookie');
        var privacyL = orderPopupPrivacyCheckboxLegal;
        if (!fioL || !fioL.value.trim()) { setError(fioL, true); valid = false; } else { setError(fioL, false); }
        if (!phoneL || !phoneL.value.trim()) { setError(phoneL, true); valid = false; } else { setError(phoneL, false); }
        var emailLValid = emailL && emailL.value.trim() && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailL.value.trim());
        if (!emailLValid) { setError(emailL, true); valid = false; } else { setError(emailL, false); }
        if (!inn || !inn.value.trim()) { setError(inn, true); valid = false; } else { setError(inn, false); }
        if (!companyName || !companyName.value.trim()) { setError(companyName, true); valid = false; } else { setError(companyName, false); }
        if (privacyWrapL && privacyL && !privacyL.checked) {
          privacyWrapL.classList.add('order-popup__input_error');
          valid = false;
        } else if (privacyWrapL) {
          privacyWrapL.classList.remove('order-popup__input_error');
        }
        if (orderPopupCaptchaLegal && !orderPopupCaptchaLegal.checked) {
          valid = false;
          var errPop = document.getElementById('errorPopup');
          if (errPop) {
            errPop.removeAttribute('hidden');
            errPop.setAttribute('aria-hidden', 'false');
            requestAnimationFrame(function () { errPop.classList.add('error-popup_is-open'); });
          }
        }
      } else {
        var fio = orderPopupForm.querySelector('[name="fio"]');
        var phone = orderPopupForm.querySelector('[name="phone"]');
        var email = orderPopupForm.querySelector('[name="email"]');
        var orderPopupPrivacyWrap = orderPopupForm.querySelector('.order-popup__form-panel_physical .order-popup__checkbox-wrap_cookie');
        if (!fio || !fio.value.trim()) { setError(fio, true); valid = false; } else { setError(fio, false); }
        if (!phone || !phone.value.trim()) { setError(phone, true); valid = false; } else { setError(phone, false); }
        var emailValid = email && email.value.trim() && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
        if (!emailValid) { setError(email, true); valid = false; } else { setError(email, false); }
        if (orderPopupPrivacyWrap && orderPopupPrivacyCheckbox && !orderPopupPrivacyCheckbox.checked) {
          orderPopupPrivacyWrap.classList.add('order-popup__input_error');
          valid = false;
        } else if (orderPopupPrivacyWrap) {
          orderPopupPrivacyWrap.classList.remove('order-popup__input_error');
        }
        if (orderPopupCaptcha && !orderPopupCaptcha.checked) {
          valid = false;
          var errPop = document.getElementById('errorPopup');
          if (errPop) {
            errPop.removeAttribute('hidden');
            errPop.setAttribute('aria-hidden', 'false');
            requestAnimationFrame(function () { errPop.classList.add('error-popup_is-open'); });
          }
        }
      }

      if (valid) {
        closeOrderPopup();
        var successPopup = document.getElementById('successPopup');
        if (successPopup) {
          successPopup.removeAttribute('hidden');
          successPopup.setAttribute('aria-hidden', 'false');
          requestAnimationFrame(function () {
            successPopup.classList.add('success-popup_is-open');
          });
        }
      }
    });
  }

  /* Окно об успехе отправки */
  var successPopup = document.getElementById('successPopup');
  var successPopupCloseBtns = document.querySelectorAll('[data-success-popup-close]');
  if (successPopup && successPopupCloseBtns.length) {
    function closeSuccessPopup() {
      successPopup.classList.remove('success-popup_is-open');
      successPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== successPopup || e.propertyName !== 'opacity') return;
        successPopup.removeEventListener('transitionend', onEnd);
        successPopup.setAttribute('hidden', '');
        successPopup.setAttribute('aria-hidden', 'true');
      }, { once: true });
    }
    successPopupCloseBtns.forEach(function (btn) {
      btn.addEventListener('click', closeSuccessPopup);
    });
  }

  /* Попап ошибки */
  var errorPopup = document.getElementById('errorPopup');
  var errorPopupCloseBtns = document.querySelectorAll('[data-error-popup-close]');
  if (errorPopup && errorPopupCloseBtns.length) {
    function closeErrorPopup() {
      errorPopup.classList.remove('error-popup_is-open');
      errorPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== errorPopup || e.propertyName !== 'opacity') return;
        errorPopup.removeEventListener('transitionend', onEnd);
        errorPopup.setAttribute('hidden', '');
        errorPopup.setAttribute('aria-hidden', 'true');
      }, { once: true });
    }
    errorPopupCloseBtns.forEach(function (btn) {
      btn.addEventListener('click', closeErrorPopup);
    });
  }

  /* Попап «Запросить звонок» (ogyokhhw) */
  var callbackPopup = document.getElementById('callbackPopup');
  var callbackPopupCloseBtns = document.querySelectorAll('[data-callback-popup-close]');
  var callbackPopupOpenBtns = document.querySelectorAll('[data-callback-popup-open]');
  if (callbackPopup) {
    function openCallbackPopup() {
      callbackPopup.removeAttribute('hidden');
      callbackPopup.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          callbackPopup.classList.add('callback-popup_is-open');
        });
      });
    }
    function closeCallbackPopup() {
      document.body.style.overflow = '';
      callbackPopup.classList.remove('callback-popup_is-open');
      callbackPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== callbackPopup || e.propertyName !== 'opacity') return;
        callbackPopup.removeEventListener('transitionend', onEnd);
        callbackPopup.setAttribute('hidden', '');
        callbackPopup.setAttribute('aria-hidden', 'true');
      }, { once: true });
    }
    if (callbackPopupCloseBtns.length) {
      callbackPopupCloseBtns.forEach(function (btn) {
        btn.addEventListener('click', closeCallbackPopup);
      });
    }
    if (callbackPopupOpenBtns.length) {
      callbackPopupOpenBtns.forEach(function (btn) {
        btn.addEventListener('click', function () { openCallbackPopup(); });
      });
    }
    var callbackModal = callbackPopup.querySelector('.callback-popup__modal');
    if (callbackModal) {
      callbackPopup.addEventListener('click', function (e) {
        if (!callbackModal.contains(e.target)) closeCallbackPopup();
      });
    }
    var callbackForm = document.getElementById('call_form') || document.getElementById('callbackPopupForm');
    if (callbackForm) {
      if (callbackForm.id === 'call_form') {
        var callFormPhone = callbackForm.querySelector('input[name="phone_number"], input[type="tel"]');
        if (callFormPhone) {
          callFormPhone.addEventListener('input', function () {
            var v = this.value.replace(/\D/g, '');
            if (v.length > 0) {
              if (v[0] === '8') v = '7' + v.slice(1);
              else if (v[0] !== '7') v = '7' + v;
            }
            v = v.slice(0, 11);
            if (v.length <= 1) this.value = v ? '+7' : '';
            else this.value = '+7 (' + v.slice(1, 4) + ') ' + v.slice(4, 7) + '-' + v.slice(7, 9) + '-' + v.slice(9);
          });
          callFormPhone.addEventListener('focus', function () {
            if (this.value.replace(/\D/g, '').length === 0) this.value = '+7 ';
          });
        }
      }
      callbackForm.addEventListener('submit', function (e) {
        if (this.id === 'call_form') return;
        e.preventDefault();
        var fio = callbackForm.querySelector('[name="callback_fio"]');
        var phone = callbackForm.querySelector('[name="callback_phone"]');
        var captcha = callbackForm.querySelector('[name="callback_captcha"]');
        var privacy = callbackForm.querySelector('[name="callback_privacy"]');
        var privacyWrap = callbackForm.querySelector('.order-popup__checkbox-wrap_cookie, .callback-form__checkbox-wrap_cookie');
        callbackForm.querySelectorAll('.order-popup__input, .order-popup__textarea, .callback-form__input, .callback-form__textarea').forEach(function (el) {
          el.classList.remove('order-popup__input_error', 'callback-form__input_error');
        });
        if (privacyWrap) privacyWrap.classList.remove('order-popup__input_error', 'callback-form__input_error');
        var valid = true;
        if (!fio || !fio.value.trim()) { valid = false; if (fio) fio.classList.add('order-popup__input_error', 'callback-form__input_error'); }
        if (!phone || !phone.value.trim()) { valid = false; if (phone) phone.classList.add('order-popup__input_error', 'callback-form__input_error'); }
        if (captcha && !captcha.checked) { valid = false; }
        if (privacy && !privacy.checked && privacyWrap) { valid = false; privacyWrap.classList.add('order-popup__input_error', 'callback-form__input_error'); }
        if (valid) {
          closeCallbackPopup();
          var successPopup = document.getElementById('successPopup');
          if (successPopup) {
            successPopup.removeAttribute('hidden');
            successPopup.setAttribute('aria-hidden', 'false');
            requestAnimationFrame(function () {
              successPopup.classList.add('success-popup_is-open');
            });
          }
        }
      });
    }
  }

  /* ========== Секция: Галерея товара (Swiper) ========== */
  var productGalleryEl = document.querySelector('[data-product-gallery]');
  if (productGalleryEl && typeof Swiper !== 'undefined') {
    var thumbsSwiper = new Swiper('.product-gallery-thumbs', {
      spaceBetween: 10,
      slidesPerView: 4,
      breakpoints: {
        0: { slidesPerView: 3 },
        640: { slidesPerView: 4 },
        1021: { slidesPerView: 3 },
        1441: { slidesPerView: 4 }
      },
      freeMode: false,
      watchSlidesProgress: true,
      observer: true,
      observeParents: true,
      loop: false
    });
    var mainSlidesCount = productGalleryEl.querySelectorAll('.product-gallery-main .swiper-slide').length;
    new Swiper('.product-gallery-main', {
      spaceBetween: 0,
      loop: true,
      loopedSlides: mainSlidesCount,
      thumbs: { swiper: thumbsSwiper },
      navigation: {
        prevEl: '.product-gallery-main .swiper-button-prev',
        nextEl: '.product-gallery-main .swiper-button-next'
      },
      observer: true,
      observeParents: true
    });
  }

  /* ========== Секция: Hero-слайдер ========== */
  var heroSwiperEl = document.querySelector('.hero-swiper');
  if (heroSwiperEl && typeof Swiper !== 'undefined') {
    new Swiper('.hero-swiper', {
      slidesPerView: 1,
      spaceBetween: 0,
      loop: true,
      speed: 600,
      autoplay: {
        delay: 6000,
        disableOnInteraction: false
      }
    });
  }

  /* ========== Секция: Слайдер «О компании» ========== */
  var aboutGallery = document.querySelector('.about__gallery');
  if (aboutGallery) {
    new Swiper('.about__gallery', {
      slidesPerView: 1,
      spaceBetween: 0,
      loop: true,
      pagination: {
        el: '.about__pagination',
        clickable: true
      },
      autoplay: {
        delay: 5000,
        disableOnInteraction: false
      }
    });
  }

  /* ========== Секция: Пагинация поиска — переключение по кнопкам prev/next ========== */
  var searchPaginations = document.querySelectorAll('.search-pagination');
  searchPaginations.forEach(function (nav) {
    var prevBtn = nav.querySelector('.search-pagination__btn_prev');
    var nextBtn = nav.querySelector('.search-pagination__btn_next');
    var numLinks = nav.querySelectorAll('.search-pagination__numbers a.search-pagination__num');
    var endLink = nav.querySelector('.search-pagination__link[href*="page="]:last-of-type');
    if (!prevBtn || !nextBtn || !numLinks.length) return;

    function getPageFromHref(href) {
      if (!href) return null;
      var match = href.match(/[?&]page=(\d+)/);
      return match ? parseInt(match[1], 10) : null;
    }

    function getActivePage() {
      var active = nav.querySelector('.search-pagination__num_active');
      return active ? getPageFromHref(active.getAttribute('href')) : 1;
    }

    function getMaxPage() {
      if (endLink) {
        var p = getPageFromHref(endLink.getAttribute('href'));
        if (p) return p;
      }
      var max = 1;
      numLinks.forEach(function (a) {
        var n = getPageFromHref(a.getAttribute('href'));
        if (n !== null && n > max) max = n;
      });
      return max;
    }

    function findLinkByPage(pageNum) {
      for (var i = 0; i < numLinks.length; i++) {
        if (getPageFromHref(numLinks[i].getAttribute('href')) === pageNum) return numLinks[i];
      }
      return null;
    }

    prevBtn.addEventListener('click', function () {
      var current = getActivePage();
      var target = current > 1 ? current - 1 : 1;
      var targetLink = findLinkByPage(target);
      if (targetLink) targetLink.click();
      else window.location.href = '?page=' + target;
    });

    nextBtn.addEventListener('click', function () {
      var current = getActivePage();
      var maxPage = getMaxPage();
      var target = current < maxPage ? current + 1 : maxPage;
      var targetLink = findLinkByPage(target);
      if (targetLink) targetLink.click();
      else window.location.href = '?page=' + target;
    });
  });

  /* ========== Виджет куки ========== */
  var cookieBar = document.getElementById('cookie-bar');
  var cookieAcceptBtn = document.querySelector('[data-cookie-accept]');
  var COOKIE_CONSENT_KEY = 'nda_cookie_consent';

  if (cookieBar) {
    if (localStorage.getItem(COOKIE_CONSENT_KEY) === 'accepted') {
      cookieBar.classList.add('cookie-bar_hidden');
    }
    if (cookieAcceptBtn) {
      cookieAcceptBtn.addEventListener('click', function () {
        try {
          localStorage.setItem(COOKIE_CONSENT_KEY, 'accepted');
        } catch (e) {}
        cookieBar.classList.add('cookie-bar_hidden');
      });
    }
  }
});
