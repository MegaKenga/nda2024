window.changeQuantity = function (event, btn, delta) {
  if (event) event.preventDefault();
  var form = btn.closest('form');
  if (!form) return;
  var input = form.querySelector('input[name="quantity"]');
  if (!input) return;
  var uiMin = 0;
  var min = parseInt(input.getAttribute('min'), 10) || 1;
  var max = parseInt(input.getAttribute('max'), 10) || 99999;
  var parsed = parseInt(input.value, 10);
  var val = Number.isFinite(parsed) ? parsed : 0;
  val = val + delta;
  val = Math.max(uiMin, Math.min(max, val));
  input.value = val;
};

/* ========== Виджет куки ========== */
(function initCookieConsent() {
  try {
    var COOKIE_CONSENT_KEY = 'nda_cookie_consent';
    var accepted = false;
    try { accepted = localStorage.getItem(COOKIE_CONSENT_KEY) === 'accepted'; } catch (e) { }

    if (accepted) return;

    setTimeout(function () {
      var bar = document.getElementById('cookie-bar');
      if (!bar) return;
      try { if (localStorage.getItem(COOKIE_CONSENT_KEY) === 'accepted') return; } catch (e) { }
      bar.removeAttribute('hidden');
      bar.setAttribute('aria-hidden', 'false');

      var btn = bar.querySelector('[data-cookie-accept]');
      if (btn && !btn.dataset.cookieBound) {
        btn.dataset.cookieBound = '1';
        btn.addEventListener('click', function () {
          try { localStorage.setItem(COOKIE_CONSENT_KEY, 'accepted'); } catch (e) { }
          bar.setAttribute('hidden', '');
          bar.setAttribute('aria-hidden', 'true');
        });
      }
    }, 4000);
  } catch (e) { }
})();

document.addEventListener('DOMContentLoaded', function () {

  /* ========== Секция: Очистка корзины при переходе на другую страницу ========== */
  (function initCartPageClearing() {
    var CART_PAGE_KEY = 'nda_cart_page_url';
    var CART_IDS_KEY = 'nda_cart_offer_ids';
    var currentPath = window.location.pathname;

    var storedPath = null;
    var storedIds = '';
    try {
      storedPath = sessionStorage.getItem(CART_PAGE_KEY);
      storedIds = sessionStorage.getItem(CART_IDS_KEY) || '';
    } catch (e) { }

    var currentPanel = document.getElementById('orderTotalPanel');
    var serverIds = currentPanel ? (currentPanel.getAttribute('data-offer-ids') || '') : '';

    if (storedPath && storedPath !== currentPath) {
      var allIdsSet = {};
      storedIds.split(',').concat(serverIds.split(',')).forEach(function (id) {
        id = id.trim();
        if (id) allIdsSet[id] = true;
      });
      var allIds = Object.keys(allIdsSet);
      if (currentPanel) currentPanel.setAttribute('hidden', '');
      try {
        sessionStorage.setItem(CART_PAGE_KEY, currentPath);
        sessionStorage.setItem(CART_IDS_KEY, '');
      } catch (e) { }
      if (allIds.length) {
        var csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || '';
        function deleteSequential(ids, index) {
          if (index >= ids.length) {
            document.documentElement.classList.remove('_cart-clearing');
            return;
          }
          fetch('/cart/remove/' + ids[index] + '/', {
            method: 'DELETE',
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrf }
          })
            .catch(function () { })
            .then(function () { deleteSequential(ids, index + 1); });
        }
        deleteSequential(allIds, 0);
      } else {
        document.documentElement.classList.remove('_cart-clearing');
      }
    } else {
      document.documentElement.classList.remove('_cart-clearing');
      try {
        sessionStorage.setItem(CART_PAGE_KEY, currentPath);
        sessionStorage.setItem(CART_IDS_KEY, '');
      } catch (e) { }
    }
  })();

  /* ========== Секция: Floating labels для form-floating ========== */
  (function initFloatingLabelsPlaceholders() {
    var roots = document.querySelectorAll(
      '#modal_form_container, ' +
      '#physical_modal_form_container, ' +
      '#call-form-container, ' +
      '#call_form, ' +
      '#mail_form'
    );
    if (!roots.length) return;
    roots.forEach(function (root) {
      var fields = root.querySelectorAll('.form-floating input.form-control, .form-floating textarea.form-control');
      fields.forEach(function (el) {
        if (!el.hasAttribute('placeholder')) el.setAttribute('placeholder', ' ');
      });
    });
  })();

  function bindFloatingLabelStateInRoot(root) {
    if (!root || !root.querySelectorAll) return;
    var wraps = root.querySelectorAll('.form-floating');
    wraps.forEach(function (wrap) {
      if (wrap.dataset.ndaFloatingBound === '1') return;
      wrap.dataset.ndaFloatingBound = '1';
      var field = wrap.querySelector('input, textarea, select');
      if (!field) return;

      function update() {
        var filled = !!String(field.value || '').trim();
        wrap.classList.toggle('form-floating_is-filled', filled);
      }

      field.addEventListener('input', update);
      field.addEventListener('change', update);
      field.addEventListener('blur', update);
      update();
    });
  }

  var labelStateRoots = document.querySelectorAll(
    '#modal_form_container, ' +
    '#physical_modal_form_container, ' +
    '#call-form-container, ' +
    '#call_form, ' +
    '#mail_form'
  );
  labelStateRoots.forEach(function (r) { bindFloatingLabelStateInRoot(r); });

  /* ========== Маска телефона (intl-tel-input) ========== */
  window.ndaIntlTelInputs = window.ndaIntlTelInputs || new Map();

  function buildInputmaskFromExample(example) {
    if (!example) return '';
    return String(example).replace(/\d/g, '9');
  }

  function applyPhoneMaskForInput(input, iti, attempt) {
    attempt = attempt || 0;
    if (!input) return;
    var InputmaskCtor = window.Inputmask || window.inputmask;
    if (!InputmaskCtor) {
      if (attempt < 10) setTimeout(function () { applyPhoneMaskForInput(input, iti, attempt + 1); }, 200);
      return;
    }
    var hasUtils = !!window.intlTelInputUtils;

    try {
      var countryData = iti && iti.getSelectedCountryData ? iti.getSelectedCountryData() : null;
      var iso2 = countryData && countryData.iso2 ? countryData.iso2 : 'ru';
      var dialCode = countryData && countryData.dialCode ? String(countryData.dialCode).replace(/\D/g, '') : '';

      if (dialCode) {
        var digits = String(input.value || '').replace(/\D/g, '');
        if (digits && digits.indexOf(dialCode) === 0 && digits.length >= dialCode.length) {
          input.value = digits.slice(dialCode.length);
        }
      }

      var maskByCountry = {
        ru: '(999) 999-99-99',
        kz: '(999) 999-99-99',
        by: '(999) 999-99-99',
        kg: '(999) 999-99-99',
        am: '(999) 999-99-99'
      };

      var mask = maskByCountry[iso2] || '';

      if (!mask) {
        var ex = '';
        if (hasUtils) {
          try {
            ex = window.intlTelInputUtils.getExampleNumber(
              iso2,
              true,
              window.intlTelInputUtils.numberType.MOBILE
            );
          } catch (e) { }
        }

        if (ex) {
          var exStr = String(ex).trim();
          if (dialCode) {
            exStr = exStr.replace(new RegExp('^\\+?' + dialCode), '').trim();
          }
          mask = buildInputmaskFromExample(exStr);
        }
      }

      if (!mask) mask = '(999) 999-99-99';

      try { if (input.inputmask) input.inputmask.remove(); } catch (e) { }

      InputmaskCtor({
        mask: mask,
        showMaskOnHover: false,
        showMaskOnFocus: true,
        clearIncomplete: true,
        definitions: { '9': { validator: '[0-9]', cardinality: 1 } }
      }).mask(input);
    } catch (e) { }
  }

  function initIntlTelInputsInRoot(root, attempt) {
    attempt = attempt || 0;
    var itiCtor = window.intlTelInput;
    if (!itiCtor) {
      if (attempt < 10) setTimeout(function () { initIntlTelInputsInRoot(root, attempt + 1); }, 300);
      return;
    }

    if (!root || !root.querySelectorAll) return;
    var inputs = root.querySelectorAll(
      '#modal_form_container .phone-mask, ' +
      '#physical_modal_form_container .phone-mask, ' +
      '#call-form-container .phone-mask, ' +
      '#call_form .phone-mask, ' +
      '#mail_form .phone-mask, ' +
      '#modal_form_container input[id^="validationPhoneNumber"], ' +
      '#physical_modal_form_container input[id^="validationPhoneNumber"], ' +
      '#call_form input[id^="validationPhoneNumber"], ' +
      '#mail_form input[id^="validationPhoneNumber"]'
    );
    inputs.forEach(function (input) {
      if (!input || input.dataset.ndaItiInit === '1') return;

      try {
        var isCallOrMail = !!(input.closest('#call_form') || input.closest('#call-form-container') || input.closest('#mail_form'));
        if (!input.hasAttribute('placeholder')) input.setAttribute('placeholder', ' ');

        var iti = itiCtor(input, {
          initialCountry: 'ru',
          nationalMode: true,
          separateDialCode: true,
          preferredCountries: ['ru', 'kz', 'am', 'by', 'kg'],
          autoPlaceholder: 'polite',
          placeholderNumberType: 'MOBILE',
          utilsScript: 'https://cdn.jsdelivr.net/npm/intl-tel-input@18.2.1/build/js/utils.js'
        });
        window.ndaIntlTelInputs.set(input, iti);
        input.dataset.ndaItiInit = '1';

        var shouldApplyPhoneMask = !!(
          input.closest('#modal_form_container') ||
          input.closest('#physical_modal_form_container') ||
          input.closest('#call_form') ||
          input.closest('#call-form-container') ||
          input.closest('#mail_form')
        );
        if (shouldApplyPhoneMask) {
          setTimeout(function () { applyPhoneMaskForInput(input, iti, 0); }, 0);
        }

        input.addEventListener('countrychange', function () {
          if (shouldApplyPhoneMask) setTimeout(function () { applyPhoneMaskForInput(input, iti, 0); }, 50);
        });
      } catch (e) { }
    });

    bindFloatingLabelStateInRoot(root);
  }

  function normalizeIntlPhoneInForm(form) {
    if (!form) return;
    form.querySelectorAll('.phone-mask').forEach(function (input) {
      var iti = window.ndaIntlTelInputs.get(input);
      if (!iti) return;
      try {
        var num = iti.getNumber && iti.getNumber();
        if (num) {
          input.value = num;
          return;
        }
        var countryData = iti.getSelectedCountryData && iti.getSelectedCountryData();
        var dial = countryData && countryData.dialCode ? String(countryData.dialCode).replace(/\D/g, '') : '';
        var digits = String(input.value || '').replace(/\D/g, '');
        if (!dial || !digits.length) return;
        if (digits.indexOf(dial) === 0 && digits.length > dial.length) {
          digits = digits.slice(dial.length);
        }
        input.value = '+' + dial + digits;
      } catch (e) { }
    });
  }

  function bootPhoneInputs() {
    initIntlTelInputsInRoot(document, 0);
  }

  if (window.ndaDeferred) {
    window.ndaDeferred.on('phone', bootPhoneInputs);
    document.addEventListener('nda:heavy-ready', function () {
      if (!window.ndaDeferred.needs.phone && document.querySelector('.phone-mask')) {
        window.ndaLoadHeavyAssets().then(bootPhoneInputs);
      }
    });
  } else {
    bootPhoneInputs();
  }

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

  /* ========== Секция: Прокрутка вверх ========== */
  var scrollTopBtn = document.getElementById('scroll-top');

  if (scrollTopBtn) {
    var scrollTopShowAfter = 400;

    function updateScrollTopVisibility() {
      var visible = window.scrollY > scrollTopShowAfter;
      scrollTopBtn.classList.toggle('scroll-top_is-visible', visible);
      if (visible) {
        scrollTopBtn.removeAttribute('hidden');
      } else {
        scrollTopBtn.setAttribute('hidden', '');
      }
    }

    window.addEventListener('scroll', updateScrollTopVisibility, { passive: true });
    updateScrollTopVisibility();

    scrollTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
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
      if (!btnMinus.getAttribute('onclick') && !btnPlus.getAttribute('onclick')) {
        btnMinus.addEventListener('click', function () {
          var val = parseInt(input.value, 10) || 0;
          if (val > 0) input.value = val - 1;
        });
        btnPlus.addEventListener('click', function () {
          var val = parseInt(input.value, 10) || 0;
          input.value = val + 1;
        });
      }
    }
    if (btnAdd) {
      btnAdd.addEventListener('click', function () {
        var row = control.closest('ol.ru-table__ru-blue, ol.ru-table__ru-gray');
        var qty = parseInt(control.querySelector('.ru-table__qty-input').value, 10) || 0;
        if (row && qty > 0) {
          row.setAttribute('data-order-added', 'true');
          if (window.updateOrderTotalCount) window.updateOrderTotalCount();
        }
      });
    }
  });

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

  if (orderTotalPanel && orderTotalCount) {
    if (orderTotalPanel.hasAttribute('hidden')) {
      updateOrderTotalCount();
    }
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
    var uploadBtnDefaultBgColor = uploadBtn.style.backgroundColor;
    fileInput.addEventListener('change', function () {
      if (this.files && this.files.length) {
        uploadBtn.style.backgroundColor = '#0BDA51';
      } else {
        uploadBtn.style.backgroundColor = uploadBtnDefaultBgColor;
      }
    });
  }

  /* ========== Секция: Попап «Оформить заказ» ========== */
  var orderPopup = document.getElementById('orderPopup');
  var orderPopupCaption = document.querySelector('.product-order__total-caption');
  var orderPopupCloseBtns = document.querySelectorAll('[data-order-popup-close]');
  var orderPopupTabs = document.querySelectorAll('.order-popup__tab');
  var orderPopupSummaryList = document.getElementById('orderPopupSummaryList');
  var orderPopupSummaryEmpty = document.getElementById('orderPopupSummaryEmpty');

  var _scrollLockDepth = 0;

  function lockBodyScroll() {
    if (_scrollLockDepth === 0) {
      var scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
      if (scrollbarWidth > 0) document.body.style.paddingRight = scrollbarWidth + 'px';
      document.body.style.overflow = 'hidden';
    }
    _scrollLockDepth++;
  }

  function unlockBodyScroll() {
    _scrollLockDepth = Math.max(0, _scrollLockDepth - 1);
    if (_scrollLockDepth === 0) {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    }
  }

  function forceUnlockBodyScroll() {
    _scrollLockDepth = 0;
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
  }

  window.ndaScroll = {
    lock: lockBodyScroll,
    unlock: unlockBodyScroll,
    forceUnlock: forceUnlockBodyScroll
  };

  function openOrderPopup() {
    if (!orderPopup) return;
    orderPopup.removeAttribute('hidden');
    orderPopup.setAttribute('aria-hidden', 'false');
    lockBodyScroll();
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
    var closed = false;
    function finish() {
      if (closed) return;
      closed = true;
      orderPopup.setAttribute('hidden', '');
      orderPopup.setAttribute('aria-hidden', 'true');
      unlockBodyScroll();
      document.body.classList.remove('body_order-popup-open');
    }
    orderPopup.classList.remove('order-popup_is-open');
    orderPopup.addEventListener('transitionend', function onCloseEnd(e) {
      if (e.target !== orderPopup || e.propertyName !== 'opacity') return;
      orderPopup.removeEventListener('transitionend', onCloseEnd);
      finish();
    });
    setTimeout(finish, 400);
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
      li.setAttribute('data-offer-code', code);
      li.innerHTML =
        '<span class="order-popup__summary-row-name">' + (code || '—') + '</span>' +
        '<span class="order-popup__summary-row-qty">' + qty + '</span>' +
        '<button type="button" class="order-popup__summary-row-remove" data-order-summary-remove aria-label="Удалить">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">' +
        '<path d="M9 3h6l1 2h4v2H4V5h4l1-2zm1 7h2v9h-2v-9zm4 0h2v9h-2v-9zM7 10h2v9H7v-9z" fill="currentColor"/>' +
        '</svg>' +
        '</button>';
      orderPopupSummaryList.appendChild(li);
    });
  }

  if (orderPopupSummaryList) {
    orderPopupSummaryList.addEventListener('click', function (e) {
      var btn = e.target && e.target.closest ? e.target.closest('[data-order-summary-remove]') : null;
      if (!btn) return;
      var li = btn.closest('.order-popup__summary-row');
      if (!li) return;
      if (!window.confirm('Вы уверены?')) return;
      var code = li.getAttribute('data-offer-code') || '';
      var candidates = document.querySelectorAll('.ru-table-wrap_order .ru-table__ru-blue[data-order-added], .ru-table-wrap_order .ru-table__ru-gray[data-order-added]');
      for (var i = 0; i < candidates.length; i++) {
        var r = candidates[i];
        var cEl = r.querySelector('.ru-table__td.ru-table__td_num');
        var c = cEl ? cEl.textContent.trim() : '';
        if (c && c === code) {
          r.removeAttribute('data-order-added');
          var q = r.querySelector('.ru-table__qty-input');
          if (q) q.value = '0';
          if (window.updateOrderTotalCount) window.updateOrderTotalCount();
          break;
        }
      }
      fillOrderPopupSummary();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var anyOpen = false;
    var orderP = document.getElementById('orderPopup');
    if (orderP && orderP.classList.contains('order-popup_is-open')) {
      closeOrderPopupDynamic();
      anyOpen = true;
    }
    var cb = document.getElementById('callbackPopup');
    if (cb && cb.classList.contains('callback-popup_is-open')) {
      if (typeof window.ndaCloseCallbackPopup === 'function') window.ndaCloseCallbackPopup();
      anyOpen = true;
    }
    var mail = document.getElementById('mailPopup');
    if (mail && mail.classList.contains('callback-popup_is-open')) {
      if (typeof window.ndaCloseMailPopup === 'function') window.ndaCloseMailPopup();
      anyOpen = true;
    }
    var succ = document.getElementById('successPopup');
    if (succ && succ.classList.contains('success-popup_is-open')) {
      if (typeof window.ndaCloseSuccessPopup === 'function') window.ndaCloseSuccessPopup();
      anyOpen = true;
    }
    if (!anyOpen) forceUnlockBodyScroll();
  });

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
        var physicalFormEl = document.getElementById('physical_modal_form');
        var legalFormEl = document.getElementById('cart_modal_form');
        orderPopupTabs.forEach(function (t) {
          t.classList.remove('order-popup__tab_active');
          t.setAttribute('aria-selected', 'false');
        });
        this.classList.add('order-popup__tab_active');
        this.setAttribute('aria-selected', 'true');
        if (physicalFormEl && legalFormEl) {
          if (target === 'legal') {
            physicalFormEl.setAttribute('hidden', '');
            legalFormEl.removeAttribute('hidden');
          } else {
            legalFormEl.setAttribute('hidden', '');
            physicalFormEl.removeAttribute('hidden');
          }
        }
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

  function isOrderForm(form) {
    return !!form && (form.id === 'cart_modal_form' || form.id === 'physical_modal_form');
  }

  function clearOrderFormErrors(form) {
    form.querySelectorAll('.order-popup__input_error').forEach(function (el) {
      el.classList.remove('order-popup__input_error');
    });
    form.querySelectorAll('.js-form-error').forEach(function (el) { el.remove(); });
  }

  function appendErrorNearField(fieldEl, message) {
    if (!fieldEl || !message) return;
    var container = fieldEl.closest('.form-floating, .mb-3, .order-popup__checkbox-wrap_cookie') || fieldEl.parentElement;
    if (!container) return;
    var error = document.createElement('div');
    error.className = 'text-danger js-form-error';
    error.textContent = message;
    container.appendChild(error);
  }

  function markOrderFieldError(form, fieldName, message) {
    if (fieldName === '__all__') {
      appendErrorNearField(form.querySelector('.modal-footer') || form, message || 'Ошибка формы.');
      return;
    }
    if (fieldName === 'captcha') {
      var captchaWrap = form.querySelector('.smart-captcha');
      if (captchaWrap) captchaWrap.classList.add('order-popup__input_error');
      appendErrorNearField(captchaWrap, message);
      return;
    }
    if (fieldName === 'privacy') {
      var privacyWrap = form.querySelector('.order-popup__checkbox-wrap_cookie');
      if (privacyWrap) privacyWrap.classList.add('order-popup__input_error');
      appendErrorNearField(privacyWrap, message);
      return;
    }
    var field = form.querySelector('[name="' + fieldName + '"]');
    if (field) {
      field.classList.add('order-popup__input_error');
      appendErrorNearField(field, message);
    }
  }

  function validateOrderFormClient(form) {
    var valid = true;
    clearOrderFormErrors(form);
    var requiredFields = form.querySelectorAll('input[required], textarea[required], select[required]');
    requiredFields.forEach(function (field) {
      var isCheckbox = field.type === 'checkbox';
      var empty = isCheckbox ? !field.checked : !String(field.value || '').trim();
      if (!empty) return;
      valid = false;
      if (isCheckbox) markOrderFieldError(form, 'privacy', 'Обязательное поле.');
      else field.classList.add('order-popup__input_error');
    });
    return valid;
  }

  function getOrderCaptchaToken(form) {
    var tokenEl = form.querySelector('input[name="smart-token"]');
    if (tokenEl && String(tokenEl.value || '').trim()) {
      return String(tokenEl.value || '').trim();
    }
    var captchaWrap = form.querySelector('.smart-captcha');
    if (captchaWrap) {
      var nestedToken = captchaWrap.querySelector('input[name="smart-token"]');
      if (nestedToken && String(nestedToken.value || '').trim()) {
        return String(nestedToken.value || '').trim();
      }
      var nearbyToken = captchaWrap.parentElement && captchaWrap.parentElement.querySelector('input[name="smart-token"]');
      if (nearbyToken && String(nearbyToken.value || '').trim()) {
        return String(nearbyToken.value || '').trim();
      }
    }
    return '';
  }

  document.addEventListener('input', function (e) {
    var form = e.target && e.target.form;
    if (!isOrderForm(form)) return;
    e.target.classList.remove('order-popup__input_error');
    if (e.target.name === 'smart-token') {
      var c = form.querySelector('.smart-captcha');
      if (c) c.classList.remove('order-popup__input_error');
    }
  });

  document.addEventListener('change', function (e) {
    var form = e.target && e.target.form;
    if (!isOrderForm(form)) return;
    if (e.target.type === 'checkbox') {
      var wrap = e.target.closest('.order-popup__checkbox-wrap_cookie');
      if (wrap) wrap.classList.remove('order-popup__input_error');
    }
  });

  setInterval(function () {
    var forms = document.querySelectorAll('#cart_modal_form, #physical_modal_form');
    forms.forEach(function (form) {
      var token = getOrderCaptchaToken(form);
      if (!token) return;
      var captchaWrap = form.querySelector('.smart-captcha');
      if (captchaWrap) captchaWrap.classList.remove('order-popup__input_error');
      form.querySelectorAll('.js-form-error').forEach(function (err) {
        if (err.textContent && err.textContent.indexOf('капч') !== -1) err.remove();
      });
    });
  }, 500);

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!isOrderForm(form)) return;
    e.preventDefault();
    if (form.dataset.submitting === '1') return;
    normalizeIntlPhoneInForm(form);
    if (!validateOrderFormClient(form)) return;

    form.dataset.submitting = '1';
    var submitBtn = form.querySelector('button[type="submit"]');
    var orderSubmitLabel = submitBtn ? submitBtn.querySelector('.js-order-submit-label') : null;
    var orderSubmitDefaultText = orderSubmitLabel
      ? orderSubmitLabel.textContent.trim()
      : (submitBtn ? submitBtn.textContent.trim() : '');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.setAttribute('aria-busy', 'true');
    }
    if (orderSubmitLabel) orderSubmitLabel.textContent = 'Отправляем...';
    else if (submitBtn) submitBtn.textContent = 'Отправляем...';

    var formData = new FormData(form);
    var maxAttempts = 10;
    var attempt = 0;

    function sendWithCaptchaRetry() {
      attempt++;
      var smartToken = getOrderCaptchaToken(form);
      if (smartToken) formData.set('smart-token', smartToken);

      if (!smartToken && attempt < maxAttempts) {
        setTimeout(sendWithCaptchaRetry, 150);
        return;
      }

      fetch(form.getAttribute('action'), {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken()
        }
      })
        .then(function (r) {
          return r.json().then(function (data) {
            return { ok: r.ok, data: data };
          });
        })
        .then(function (res) {
          clearOrderFormErrors(form);
          if (res.ok && res.data && res.data.success) {
            closeOrderPopupDynamic();

            var panelEl = document.getElementById('orderTotalPanel');
            var countEl = document.getElementById('orderTotalCount');
            if (panelEl && countEl) {
              countEl.textContent = '0';
              panelEl.setAttribute('hidden', '');
            }

            var orderRows = document.querySelectorAll(
              '.ru-table-wrap_order .ru-table__ru-blue[data-order-added], ' +
              '.ru-table-wrap_order .ru-table__ru-gray[data-order-added]'
            );
            orderRows.forEach(function (row) { row.removeAttribute('data-order-added'); });
            document.querySelectorAll('.ru-table-wrap_order .ru-table__qty-input').forEach(function (input) {
              input.value = '0';
            });
            if (window.updateOrderTotalCount) window.updateOrderTotalCount();

            var successPopup = document.getElementById('successPopup');
            if (successPopup) {
              successPopup.style.removeProperty('display');
              successPopup.removeAttribute('hidden');
              successPopup.setAttribute('aria-hidden', 'false');
              lockBodyScroll();
              requestAnimationFrame(function () {
                successPopup.classList.add('success-popup_is-open');
              });
            }
            return;
          }
          var errors = (res.data && res.data.errors) ? res.data.errors : {};
          Object.keys(errors).forEach(function (name) {
            markOrderFieldError(form, name, errors[name]);
          });
        })
        .catch(function () {
          markOrderFieldError(form, '__all__', 'Ошибка отправки формы. Попробуйте позже.');
        })
        .finally(function () {
          form.dataset.submitting = '0';
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.removeAttribute('aria-busy');
          }
          if (orderSubmitLabel) orderSubmitLabel.textContent = orderSubmitDefaultText;
          else if (submitBtn) submitBtn.textContent = orderSubmitDefaultText;
        });
    }

    sendWithCaptchaRetry();
  });

  var successPopup = document.getElementById('successPopup');
  var successPopupCloseBtns = document.querySelectorAll('[data-success-popup-close]');
  if (successPopup && successPopupCloseBtns.length) {
    function closeSuccessPopup() {
      var done = false;
      function finish() {
        if (done) return;
        done = true;
        successPopup.setAttribute('hidden', '');
        successPopup.setAttribute('aria-hidden', 'true');
        unlockBodyScroll();
      }
      successPopup.classList.remove('success-popup_is-open');
      successPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== successPopup || e.propertyName !== 'opacity') return;
        successPopup.removeEventListener('transitionend', onEnd);
        finish();
      }, { once: true });
      setTimeout(finish, 400);
    }
    window.ndaCloseSuccessPopup = closeSuccessPopup;
    successPopupCloseBtns.forEach(function (btn) {
      btn.addEventListener('click', closeSuccessPopup);
    });
    var successBackdropEl = successPopup.querySelector('.success-popup__backdrop');
    if (successBackdropEl) {
      successBackdropEl.addEventListener('click', closeSuccessPopup);
    }
  }

  var errorPopup = document.getElementById('errorPopup');
  var errorPopupCloseBtns = document.querySelectorAll('[data-error-popup-close]');
  if (errorPopup && errorPopupCloseBtns.length) {
    var errorPopupDefaultText = (function () {
      var t = document.getElementById('errorPopupTitle');
      return t ? t.textContent : '';
    })();
    function closeErrorPopup() {
      errorPopup.classList.remove('error-popup_is-open');
      errorPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== errorPopup || e.propertyName !== 'opacity') return;
        errorPopup.removeEventListener('transitionend', onEnd);
        errorPopup.setAttribute('hidden', '');
        errorPopup.setAttribute('aria-hidden', 'true');
        var tReset = document.getElementById('errorPopupTitle');
        if (tReset && errorPopupDefaultText) tReset.textContent = errorPopupDefaultText;
      }, { once: true });
    }
    errorPopupCloseBtns.forEach(function (btn) {
      btn.addEventListener('click', closeErrorPopup);
    });
    var errorBackdropEl = errorPopup.querySelector('.error-popup__backdrop');
    if (errorBackdropEl) {
      errorBackdropEl.addEventListener('click', closeErrorPopup);
    }
  }

  function ndaSyncInputFileLabel(fileInput) {
    if (!fileInput || fileInput.type !== 'file') return;
    var label = fileInput.closest('.input-file');
    if (!label) return;
    var span = label.querySelector('span');
    var def = label.getAttribute('data-input-file-default') || 'Прикрепить файл';
    if (fileInput.files && fileInput.files.length) {
      label.classList.add('input-file_has-file');
      if (span) span.textContent = fileInput.files[0].name;
    } else {
      label.classList.remove('input-file_has-file');
      if (span) span.textContent = def;
    }
  }

  document.addEventListener('change', function (e) {
    var t = e.target;
    if (!t || t.type !== 'file' || t.name !== 'company_details') return;
    ndaSyncInputFileLabel(t);
  });

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.id !== 'mail_form') return;

    e.preventDefault();
    if (form.dataset.submitting === '1') return;

    var cb = form.querySelector('input[name="mail_privacy"]') || document.getElementById('mailPopupPrivacy');
    var privacyWrap = cb ? cb.closest('.order-popup__checkbox-wrap_cookie') : form.querySelector('.order-popup__checkbox-wrap_cookie');
    if (!cb || !cb.checked) {
      if (privacyWrap) {
        privacyWrap.classList.add('order-popup__input_error');
        if (!privacyWrap.querySelector('.js-form-error')) {
          var errEl = document.createElement('div');
          errEl.className = 'text-danger js-form-error';
          errEl.textContent = 'Обязательное поле.';
          privacyWrap.appendChild(errEl);
        }
      }
      return;
    }
    if (privacyWrap) {
      privacyWrap.classList.remove('order-popup__input_error');
      var prevErr = privacyWrap.querySelector('.js-form-error');
      if (prevErr) prevErr.remove();
    }

    var emailInput = form.querySelector('[name="email"]');
    var nameInput = form.querySelector('[name="name"]');
    var phoneInput = form.querySelector('[name="phone_number"]');
    var captchaBox = form.querySelector('.smart-captcha');
    var submitBtn = form.querySelector('button[type="submit"]');
    var submitLabel = submitBtn ? submitBtn.querySelector('.js-mail-submit-label') : null;
    var mailSubmitDefaultText = submitLabel ? submitLabel.textContent.trim() : 'Отправить';

    function markMailFieldError(el, hasError) {
      if (!el) return;
      if (hasError) el.classList.add('order-popup__input_error');
      else el.classList.remove('order-popup__input_error');
    }

    var emailEmpty = !emailInput || !String(emailInput.value || '').trim();
    markMailFieldError(emailInput, emailEmpty);

    var hasCaptchaToken = !!getOrderCaptchaToken(form);
    if (captchaBox) {
      if (hasCaptchaToken) captchaBox.classList.remove('order-popup__input_error');
      else captchaBox.classList.add('order-popup__input_error');
    }

    if (emailEmpty || !hasCaptchaToken) return;

    form.dataset.submitting = '1';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.setAttribute('aria-busy', 'true');
    }
    if (submitLabel) submitLabel.textContent = 'Отправляем...';

    var maxAttempts = 10;
    var attempt = 0;

    function sendMailWithCaptchaRetry() {
      attempt++;
      normalizeIntlPhoneInForm(form);
      var formData = new FormData(form);
      var smartToken = getOrderCaptchaToken(form);
      if (smartToken) formData.set('smart-token', smartToken);

      if (!smartToken && attempt < maxAttempts) {
        setTimeout(sendMailWithCaptchaRetry, 150);
        return;
      }

      fetch(form.getAttribute('action'), {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken()
        }
      })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data || {} };
          }).catch(function () {
            return { ok: response.ok, data: {} };
          });
        })
        .then(function (payload) {
          var data = payload.data || {};
          var success = payload.ok && data.success === true;

          markMailFieldError(emailInput, false);
          markMailFieldError(nameInput, false);
          markMailFieldError(phoneInput, false);
          if (captchaBox) captchaBox.classList.remove('order-popup__input_error');

          if (success) {
            form.reset();
            var fileIn = form.querySelector('input[type="file"][name="company_details"]');
            if (fileIn) ndaSyncInputFileLabel(fileIn);
            if (window.ndaCloseMailPopup) window.ndaCloseMailPopup();
            var sp = document.getElementById('successPopup');
            if (sp) {
              sp.style.removeProperty('display');
              sp.removeAttribute('hidden');
              sp.setAttribute('aria-hidden', 'false');
              lockBodyScroll();
              requestAnimationFrame(function () {
                sp.classList.add('success-popup_is-open');
              });
            }
            return;
          }

          var errors = data.errors || {};
          if (errors.email) markMailFieldError(emailInput, true);
          if (errors.name) markMailFieldError(nameInput, true);
          if (errors.phone_number) markMailFieldError(phoneInput, true);
          if (errors.captcha && captchaBox) captchaBox.classList.add('order-popup__input_error');

          var ep = document.getElementById('errorPopup');
          if (ep) {
            var titleEl = document.getElementById('errorPopupTitle');
            if (titleEl && errors.__all__) titleEl.textContent = String(errors.__all__);
            else if (titleEl) {
              titleEl.textContent = 'Ошибка при отправке! Пожалуйста, попробуйте повторить запрос через пару минут.';
            }
            ep.style.removeProperty('display');
            ep.removeAttribute('hidden');
            ep.setAttribute('aria-hidden', 'false');
            requestAnimationFrame(function () {
              ep.classList.add('error-popup_is-open');
            });
          }
        })
        .catch(function () {
          var ep = document.getElementById('errorPopup');
          if (ep) {
            var t = document.getElementById('errorPopupTitle');
            if (t) t.textContent = 'Ошибка при отправке! Пожалуйста, попробуйте повторить запрос через пару минут.';
            ep.style.removeProperty('display');
            ep.removeAttribute('hidden');
            ep.setAttribute('aria-hidden', 'false');
            requestAnimationFrame(function () {
              ep.classList.add('error-popup_is-open');
            });
          }
        })
        .finally(function () {
          form.dataset.submitting = '0';
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.removeAttribute('aria-busy');
          }
          if (submitLabel) submitLabel.textContent = mailSubmitDefaultText;
        });
    }

    sendMailWithCaptchaRetry();
  });

  function openOrderPopupDynamic() {
    var popup = document.getElementById('orderPopup');
    if (!popup) return;
    popup.removeAttribute('hidden');
    popup.setAttribute('aria-hidden', 'false');
    lockBodyScroll();
    document.body.classList.add('body_order-popup-open');
    requestAnimationFrame(function () {
      popup.classList.add('order-popup_is-open');
    });
  }

  function closeOrderPopupDynamic() {
    var popup = document.getElementById('orderPopup');
    if (!popup) return;
    var closed = false;
    function finish() {
      if (closed) return;
      closed = true;
      popup.setAttribute('hidden', '');
      popup.setAttribute('aria-hidden', 'true');
      unlockBodyScroll();
      document.body.classList.remove('body_order-popup-open');
    }
    popup.classList.remove('order-popup_is-open');
    popup.addEventListener('transitionend', function onEnd(e) {
      if (e.target !== popup || e.propertyName !== 'opacity') return;
      popup.removeEventListener('transitionend', onEnd);
      finish();
    }, { once: true });
    setTimeout(finish, 400);
  }

  function switchOrderPopupTab(target) {
    var popup = document.getElementById('orderPopup');
    if (!popup) return;
    var tabs = popup.querySelectorAll('.order-popup__tab');
    var panels = popup.querySelectorAll('.order-popup__form-panel');
    var physicalFormEl = document.getElementById('physical_modal_form');
    var legalFormEl = document.getElementById('cart_modal_form');
    var orderPopupTitlePhysical = popup.querySelector('[data-order-summary-title-physical]');
    var orderPopupTitleLegal = popup.querySelector('[data-order-summary-title-legal]');
    var orderPopupLegalIntro = document.getElementById('orderPopupLegalIntro');

    tabs.forEach(function (t) {
      var tTarget = t.getAttribute('data-order-tab');
      var isActive = tTarget === target;
      t.classList.toggle('order-popup__tab_active', isActive);
      t.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    if (physicalFormEl && legalFormEl) {
      if (target === 'legal') {
        physicalFormEl.setAttribute('hidden', '');
        legalFormEl.removeAttribute('hidden');
      } else {
        legalFormEl.setAttribute('hidden', '');
        physicalFormEl.removeAttribute('hidden');
      }
    }

    panels.forEach(function (panel) {
      if (panel.getAttribute('data-order-panel') === target) {
        panel.removeAttribute('hidden');
      } else {
        panel.setAttribute('hidden', '');
      }
    });

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
  }

  function syncCartIdsToSession() {
    var panel = document.getElementById('orderTotalPanel');
    var ids = panel ? (panel.getAttribute('data-offer-ids') || '') : '';
    try { sessionStorage.setItem('nda_cart_offer_ids', ids); } catch (e) { }
  }

  function getCsrfToken() {
    var hxHeaders = document.body && document.body.getAttribute('hx-headers');
    if (hxHeaders) {
      try { return JSON.parse(hxHeaders)['X-CSRFToken'] || ''; } catch (e) { }
    }
    var inp = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return inp ? inp.value : '';
  }

  document.addEventListener('submit', function (e) {
    var form = e.target && e.target.closest ? e.target.closest('.ru-table__qty-control') : null;
    if (!form) return;
    e.preventDefault();
    var url = form.getAttribute('action');
    if (!url) return;
    var formData = new FormData(form);
    fetch(url, {
      method: 'POST',
      body: formData,
      headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCsrfToken() }
    })
      .then(function (r) { return r.text(); })
      .then(function (html) {
        var panel = document.getElementById('orderTotalPanel');
        if (!panel) return;
        var tmp = document.createElement('div');
        tmp.innerHTML = html.trim();
        var newPanel = tmp.firstElementChild;
        if (newPanel) {
          panel.parentNode.replaceChild(newPanel, panel);
          syncCartIdsToSession();
        }
      })
      .catch(function (err) { console.error('cart_add error:', err); });
  });

  function initCaptchaInElement(container, attempt) {
    if (!window.smartCaptcha) {
      if ((attempt || 0) < 10) {
        setTimeout(function () { initCaptchaInElement(container, (attempt || 0) + 1); }, 500);
      }
      return;
    }
    var divs = container.querySelectorAll('.smart-captcha');
    divs.forEach(function (div) {
      if (div.querySelector('iframe')) return;
      var sitekey = div.getAttribute('data-sitekey');
      if (sitekey) {
        window.smartCaptcha.render(div, { sitekey: sitekey });
      }
    });
  }

  function loadAndOpenOrderPopup(url) {
    var existing = document.getElementById('orderPopup');
    if (existing) {
      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(function (r) { return r.text(); })
        .then(function (html) {
          var tmp = document.createElement('div');
          tmp.innerHTML = html;
          var newTable = tmp.querySelector('#offers-table');
          var curTable = existing.querySelector('#offers-table');
          if (newTable && curTable) curTable.parentNode.replaceChild(newTable, curTable);
          openOrderPopupDynamic();
          initIntlTelInputsInRoot(existing, 0);
        })
        .catch(function () { openOrderPopupDynamic(); });
      return;
    }
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) { return r.text(); })
      .then(function (html) {
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        while (tmp.firstChild) {
          document.body.appendChild(tmp.firstChild);
        }
        var popup = document.getElementById('orderPopup');
        if (popup) initCaptchaInElement(popup);
        if (popup) initIntlTelInputsInRoot(popup, 0);
        openOrderPopupDynamic();
      })
      .catch(function (err) { console.error('cart_modal load error:', err); });
  }

  document.addEventListener('click', function (e) {
    var orderBtn = e.target && e.target.closest ? e.target.closest('.product-order__total-caption') : null;
    if (orderBtn) {
      var url = orderBtn.getAttribute('hx-get') || orderBtn.getAttribute('action');
      if (url) {
        e.preventDefault();
        loadAndOpenOrderPopup(url);
      }
      return;
    }

    var closeBtn = e.target && e.target.closest ? e.target.closest('[data-order-popup-close]') : null;
    if (closeBtn) {
      closeOrderPopupDynamic();
      return;
    }

    var tabBtn = e.target && e.target.closest ? e.target.closest('.order-popup__tab') : null;
    if (tabBtn) {
      var tabTarget = tabBtn.getAttribute('data-order-tab');
      if (tabTarget) switchOrderPopupTab(tabTarget);
      return;
    }

    var removeBtn = e.target && e.target.closest ? e.target.closest('.offers-table__remove-btn') : null;
    if (removeBtn) {
      if (!window.confirm('Вы уверены?')) return;
      var delUrl = removeBtn.getAttribute('hx-delete');
      if (!delUrl) return;
      fetch(delUrl, {
        method: 'DELETE',
        headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': getCsrfToken() }
      })
        .then(function (r) { return r.text(); })
        .then(function (html) {
          var table = document.getElementById('offers-table');
          if (table) {
            table.innerHTML = html;
            var remainingIds = Array.from(table.querySelectorAll('[hx-delete]')).map(function (btn) {
              var m = btn.getAttribute('hx-delete').match(/\/cart\/remove\/(\d+)\//);
              return m ? m[1] : null;
            }).filter(Boolean).join(',');
            var panel = document.getElementById('orderTotalPanel');
            if (panel) {
              panel.setAttribute('data-offer-ids', remainingIds);
              if (!remainingIds) panel.setAttribute('hidden', '');
            }
            try { sessionStorage.setItem('nda_cart_offer_ids', remainingIds); } catch (e) { }
          }
        })
        .catch(function (err) { console.error('cart_remove error:', err); });
    }
  });

  var callbackPopup = document.getElementById('callbackPopup');
  var callbackPopupCloseBtns = document.querySelectorAll('[data-callback-popup-close]');
  var callbackPopupOpenBtns = document.querySelectorAll('[data-callback-popup-open]');
  if (callbackPopup) {
    function openCallbackPopup() {
      callbackPopup.style.removeProperty('display');
      callbackPopup.removeAttribute('hidden');
      callbackPopup.setAttribute('aria-hidden', 'false');
      initIntlTelInputsInRoot(callbackPopup, 0);
      lockBodyScroll();
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          callbackPopup.classList.add('callback-popup_is-open');
        });
      });
    }
    function closeCallbackPopup() {
      unlockBodyScroll();
      callbackPopup.classList.remove('callback-popup_is-open');
      var finished = false;
      function onFinish() {
        if (finished) return;
        finished = true;
        callbackPopup.setAttribute('hidden', '');
        callbackPopup.setAttribute('aria-hidden', 'true');
      }
      callbackPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== callbackPopup || e.propertyName !== 'opacity') return;
        callbackPopup.removeEventListener('transitionend', onEnd);
        onFinish();
      }, { once: true });
      setTimeout(onFinish, 400);
      var callFormEl = document.getElementById('call_form');
      if (callFormEl) callFormEl.reset();
    }
    window.ndaCloseCallbackPopup = closeCallbackPopup;
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
    var callbackPopupFormEl = document.getElementById('callbackPopupForm');
    if (callbackPopupFormEl) {
      callbackPopupFormEl.addEventListener('submit', function (e) {
        e.preventDefault();
        var fio = callbackPopupFormEl.querySelector('[name="callback_fio"]');
        var phone = callbackPopupFormEl.querySelector('[name="callback_phone"]');
        var captcha = callbackPopupFormEl.querySelector('[name="callback_captcha"]');
        var privacy = callbackPopupFormEl.querySelector('[name="callback_privacy"]');
        var privacyWrapLegacy = callbackPopupFormEl.querySelector('.order-popup__checkbox-wrap_cookie, .callback-form__checkbox-wrap_cookie');
        callbackPopupFormEl.querySelectorAll('.order-popup__input, .order-popup__textarea, .callback-form__input, .callback-form__textarea').forEach(function (el) {
          el.classList.remove('order-popup__input_error', 'callback-form__input_error');
        });
        if (privacyWrapLegacy) privacyWrapLegacy.classList.remove('order-popup__input_error', 'callback-form__input_error');
        var valid = true;
        if (!fio || !fio.value.trim()) { valid = false; if (fio) fio.classList.add('order-popup__input_error', 'callback-form__input_error'); }
        if (!phone || !phone.value.trim()) { valid = false; if (phone) phone.classList.add('order-popup__input_error', 'callback-form__input_error'); }
        if (captcha && !captcha.checked) { valid = false; }
        if (privacy && !privacy.checked && privacyWrapLegacy) { valid = false; privacyWrapLegacy.classList.add('order-popup__input_error', 'callback-form__input_error'); }
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

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.id !== 'call_form') return;
    e.preventDefault();
    e.stopImmediatePropagation();

    var nameInput = form.querySelector('[name="name"]');
    var phoneInput = form.querySelector('[name="phone_number"], input[type="tel"]');
    var requiredFields = form.querySelectorAll('[required]');
    var privacyCb = form.querySelector('input[name="callback_privacy"]');
    var privacyWrap = privacyCb ? privacyCb.closest('.order-popup__checkbox-wrap_cookie') : null;
    var captchaBox = form.querySelector('.smart-captcha');
    var tokenInput = form.querySelector('input[name="smart-token"]');
    var validCall = true;

    function markError(el, hasError) {
      if (!el) return;
      if (hasError) el.classList.add('order-popup__input_error');
      else el.classList.remove('order-popup__input_error');
    }

    if (privacyWrap) {
      privacyWrap.classList.remove('order-popup__input_error');
      privacyWrap.querySelectorAll('.js-form-error').forEach(function (el) { el.remove(); });
    }

    requiredFields.forEach(function (field) {
      if (field.type === 'checkbox') return;
      var empty = !field.value || !String(field.value).trim();
      markError(field, empty);
      if (empty) validCall = false;
    });

    if (!privacyCb || !privacyCb.checked) {
      if (privacyWrap) {
        privacyWrap.classList.add('order-popup__input_error');
        if (!privacyWrap.querySelector('.js-form-error')) {
          var privacyErr = document.createElement('div');
          privacyErr.className = 'text-danger js-form-error';
          privacyErr.textContent = 'Обязательное поле.';
          privacyWrap.appendChild(privacyErr);
        }
      }
      validCall = false;
    }

    var phoneEmpty = !phoneInput || !phoneInput.value || !phoneInput.value.trim();
    markError(phoneInput, phoneEmpty);
    if (phoneEmpty) validCall = false;

    var nameEmpty = !nameInput || !nameInput.value || !nameInput.value.trim();
    markError(nameInput, nameEmpty);
    if (nameEmpty) validCall = false;

    var hasCaptchaToken = !!(tokenInput && tokenInput.value && tokenInput.value.trim());
    if (captchaBox) {
      if (hasCaptchaToken) captchaBox.classList.remove('order-popup__input_error');
      else captchaBox.classList.add('order-popup__input_error');
    }
    if (!hasCaptchaToken) validCall = false;

    if (!validCall) return;

    var callSubmitBtn = form.querySelector('button[type="submit"]');
    var callSubmitLabel = callSubmitBtn ? callSubmitBtn.querySelector('.js-call-submit-label') : null;
    var callSubmitDefaultText = callSubmitLabel
      ? callSubmitLabel.textContent.trim()
      : (callSubmitBtn ? callSubmitBtn.textContent.trim() : 'Отправить');
    if (callSubmitBtn) {
      callSubmitBtn.disabled = true;
      callSubmitBtn.setAttribute('aria-busy', 'true');
    }
    if (callSubmitLabel) callSubmitLabel.textContent = 'Отправляем...';
    else if (callSubmitBtn) callSubmitBtn.textContent = 'Отправляем...';

    normalizeIntlPhoneInForm(form);
    fetch(form.getAttribute('action') || form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken()
      }
    }).then(function (response) {
      return response.json().then(function (data) {
        return { ok: response.ok, data: data || {} };
      }).catch(function () {
        return { ok: response.ok, data: {} };
      });
    }).then(function (payload) {
      var data = payload.data || {};
      var success = payload.ok && data.success === true;

      markError(nameInput, false);
      markError(phoneInput, false);
      if (captchaBox) captchaBox.classList.remove('order-popup__input_error');

      if (success) {
        if (window.ndaCloseCallbackPopup) window.ndaCloseCallbackPopup();
        var successPopupCall = document.getElementById('successPopup');
        if (successPopupCall) {
          successPopupCall.removeAttribute('hidden');
          successPopupCall.setAttribute('aria-hidden', 'false');
          requestAnimationFrame(function () {
            successPopupCall.classList.add('success-popup_is-open');
          });
        }
        return;
      }

      var errors = data.errors || {};
      if (errors.name) markError(nameInput, true);
      if (errors.phone_number) markError(phoneInput, true);
      if (errors.captcha && captchaBox) captchaBox.classList.add('order-popup__input_error');

      if (errorPopup) {
        errorPopup.removeAttribute('hidden');
        errorPopup.setAttribute('aria-hidden', 'false');
        requestAnimationFrame(function () {
          errorPopup.classList.add('error-popup_is-open');
        });
      }
    }).catch(function () {
      if (errorPopup) {
        errorPopup.removeAttribute('hidden');
        errorPopup.setAttribute('aria-hidden', 'false');
        requestAnimationFrame(function () {
          errorPopup.classList.add('error-popup_is-open');
        });
      }
    }).finally(function () {
      if (callSubmitBtn) {
        callSubmitBtn.disabled = false;
        callSubmitBtn.removeAttribute('aria-busy');
      }
      if (callSubmitLabel) callSubmitLabel.textContent = callSubmitDefaultText;
      else if (callSubmitBtn) callSubmitBtn.textContent = callSubmitDefaultText;
    });
  }, true);

  var mailPopup = document.getElementById('mailPopup');
  var mailPopupCloseBtns = document.querySelectorAll('[data-mail-popup-close]');
  var mailPopupOpenBtns = document.querySelectorAll('[data-mail-popup-open]');
  if (mailPopup) {
    function openMailPopup() {
      mailPopup.style.removeProperty('display');
      mailPopup.removeAttribute('hidden');
      mailPopup.setAttribute('aria-hidden', 'false');
      initIntlTelInputsInRoot(mailPopup, 0);
      lockBodyScroll();
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          mailPopup.classList.add('callback-popup_is-open');
        });
      });
    }
    function closeMailPopup() {
      unlockBodyScroll();
      mailPopup.classList.remove('callback-popup_is-open');
      var finished = false;
      function onFinish() {
        if (finished) return;
        finished = true;
        mailPopup.setAttribute('hidden', '');
        mailPopup.setAttribute('aria-hidden', 'true');
      }
      mailPopup.addEventListener('transitionend', function onEnd(e) {
        if (e.target !== mailPopup || e.propertyName !== 'opacity') return;
        mailPopup.removeEventListener('transitionend', onEnd);
        onFinish();
      }, { once: true });
      setTimeout(onFinish, 400);
    }
    window.ndaCloseMailPopup = closeMailPopup;
    if (mailPopupCloseBtns.length) {
      mailPopupCloseBtns.forEach(function (btn) {
        btn.addEventListener('click', closeMailPopup);
      });
    }
    if (mailPopupOpenBtns.length) {
      mailPopupOpenBtns.forEach(function (btn) {
        btn.addEventListener('click', function () { openMailPopup(); });
      });
    }
    var mailModal = mailPopup.querySelector('.callback-popup__modal');
    if (mailModal) {
      mailPopup.addEventListener('click', function (e) {
        if (!mailModal.contains(e.target)) closeMailPopup();
      });
    }
  }

  /* ========== Секция: Swiper (после отложенной загрузки) ========== */
  function ensureProductGalleryArrowStyles() {
    if (document.getElementById('nda-product-gallery-arrow-fix')) {
      return;
    }
    var style = document.createElement('style');
    style.id = 'nda-product-gallery-arrow-fix';
    style.textContent = [
      '.product-gallery-main .product-gallery__arrow.swiper-button-prev,',
      '.product-gallery-main .product-gallery__arrow.swiper-button-next {',
      '  --swiper-navigation-size: 80px;',
      '  display: flex !important;',
      '  align-items: center !important;',
      '  justify-content: center !important;',
      '  width: 50px !important;',
      '  height: 80px !important;',
      '  min-width: 50px !important;',
      '  min-height: 80px !important;',
      '  margin-top: 0 !important;',
      '  padding: 0 !important;',
      '  overflow: visible !important;',
      '  transform: translateY(-50%) !important;',
      '  color: #000 !important;',
      '}',
      '.product-gallery-main .product-gallery__arrow svg {',
      '  display: block !important;',
      '  width: 13px !important;',
      '  height: 21px !important;',
      '  flex-shrink: 0 !important;',
      '  overflow: visible !important;',
      '  pointer-events: none;',
      '}',
      '.product-gallery-main .product-gallery__arrow svg path {',
      '  stroke: #000 !important;',
      '}',
      '.product-gallery-main .product-gallery__arrow::after {',
      '  content: none !important;',
      '  display: none !important;',
      '}',
      '@media (max-width: 1440px) {',
      '  .product-gallery-main .product-gallery__arrow.swiper-button-prev,',
      '  .product-gallery-main .product-gallery__arrow.swiper-button-next {',
      '    width: 40px !important;',
      '    height: 60px !important;',
      '    min-width: 40px !important;',
      '    min-height: 60px !important;',
      '    --swiper-navigation-size: 60px;',
      '  }',
      '  .product-gallery-main .product-gallery__arrow svg {',
      '    width: 11px !important;',
      '    height: 18px !important;',
      '  }',
      '}',
      '@media (max-width: 1020px) {',
      '  .product-gallery-main .product-gallery__arrow.swiper-button-prev,',
      '  .product-gallery-main .product-gallery__arrow.swiper-button-next {',
      '    width: 30px !important;',
      '    height: 48px !important;',
      '    min-width: 30px !important;',
      '    min-height: 48px !important;',
      '    --swiper-navigation-size: 48px;',
      '  }',
      '  .product-gallery-main .product-gallery__arrow svg {',
      '    width: 10px !important;',
      '    height: 17px !important;',
      '  }',
      '}'
    ].join('\n');
    document.head.appendChild(style);
  }

  function initNdaSwipers() {
  if (typeof Swiper === 'undefined') {
    return;
  }

  ensureProductGalleryArrowStyles();

  var productGalleryEl = document.querySelector('[data-product-gallery]');
  if (productGalleryEl) {
    var thumbsEl = productGalleryEl.querySelector('.product-gallery-thumbs');
    var mainEl = productGalleryEl.querySelector('.product-gallery-main');
    var thumbsSwiper = null;
    var thumbsProgressTrack = null;
    var thumbsProgressBar = null;

    function thumbsNeedScroll(swiper) {
      if (!swiper || !swiper.el) {
        return false;
      }
      if (swiper.isLocked) {
        return false;
      }
      if (swiper.snapGrid && swiper.snapGrid.length > 1) {
        return true;
      }
      var slidesPerView = swiper.params.slidesPerView;
      if (typeof slidesPerView !== 'number') {
        slidesPerView = parseFloat(slidesPerView) || 1;
      }
      return swiper.slides.length > slidesPerView;
    }

    function updateThumbsProgressVisibility() {
      if (!thumbsProgressTrack || !thumbsSwiper) {
        return;
      }
      var needsScroll = thumbsNeedScroll(thumbsSwiper);
      thumbsProgressTrack.classList.toggle('is-hidden', !needsScroll);
      thumbsProgressTrack.hidden = !needsScroll;
      if (!needsScroll && thumbsProgressBar) {
        thumbsProgressBar.style.transform = 'scaleX(0)';
      }
    }

    function updateThumbsProgress() {
      if (!thumbsProgressBar || !thumbsProgressTrack || thumbsProgressTrack.hidden) {
        return;
      }
      var p = typeof thumbsSwiper.progress === 'number' ? thumbsSwiper.progress : 0;
      p = Math.max(0, Math.min(1, p));
      thumbsProgressBar.style.transform = 'scaleX(' + p + ')';
    }

    function cleanupSwiperEl(el) {
      if (!el) return;
      if (!el.swiper && !el.classList.contains('swiper-initialized')) {
        return;
      }
      if (el.swiper) {
        el.swiper.destroy(true, true);
      }
      el.classList.remove('swiper-initialized');
      el.querySelectorAll('.swiper-slide-duplicate').forEach(function (slide) {
        slide.remove();
      });
    }

    cleanupSwiperEl(thumbsEl);
    cleanupSwiperEl(mainEl);

    if (thumbsEl && !thumbsEl.classList.contains('swiper-initialized')) {
      var thumbsParent = thumbsEl.parentElement;
      thumbsProgressTrack = thumbsParent
        ? thumbsParent.querySelector('.product-gallery-thumbs-progress-track')
        : null;
      if (!thumbsProgressTrack) {
        thumbsProgressTrack = document.createElement('div');
        thumbsProgressTrack.className = 'product-gallery-thumbs-progress-track is-hidden';
        thumbsProgressTrack.hidden = true;
        thumbsProgressBar = document.createElement('div');
        thumbsProgressBar.className = 'product-gallery-thumbs-progress-bar';
        thumbsProgressTrack.appendChild(thumbsProgressBar);
        if (thumbsParent) {
          thumbsParent.appendChild(thumbsProgressTrack);
        } else {
          thumbsEl.appendChild(thumbsProgressTrack);
        }
      } else {
        thumbsProgressBar = thumbsProgressTrack.querySelector('.product-gallery-thumbs-progress-bar');
        thumbsProgressTrack.classList.add('is-hidden');
        thumbsProgressTrack.hidden = true;
      }

      thumbsSwiper = new Swiper(thumbsEl, {
        spaceBetween: 10,
        slidesPerView: 4,
        slideToClickedSlide: true,
        breakpoints: {
          0: { slidesPerView: 3 },
          640: { slidesPerView: 4 },
          1021: { slidesPerView: 3 },
          1441: { slidesPerView: 4 }
        },
        freeMode: false,
        watchSlidesProgress: true,
        watchOverflow: true,
        observer: true,
        observeParents: true,
        loop: false,
        on: {
          init: function () {
            requestAnimationFrame(function () {
              updateThumbsProgressVisibility();
              updateThumbsProgress();
            });
          },
          resize: function () {
            updateThumbsProgressVisibility();
            updateThumbsProgress();
          },
          update: function () {
            updateThumbsProgressVisibility();
          },
          breakpoint: function () {
            updateThumbsProgressVisibility();
            updateThumbsProgress();
          },
          imagesReady: function () {
            updateThumbsProgressVisibility();
            updateThumbsProgress();
          },
          slideChange: function () {
            updateThumbsProgress();
          }
        }
      });

      thumbsSwiper.on('progress', function () {
        updateThumbsProgress();
      });
      requestAnimationFrame(function () {
        updateThumbsProgressVisibility();
        updateThumbsProgress();
      });
    }

    if (mainEl && !mainEl.classList.contains('swiper-initialized')) {
      var mainSlidesCount = mainEl.querySelectorAll('.swiper-slide:not(.swiper-slide-duplicate)').length;
      if (!mainSlidesCount) {
        mainSlidesCount = mainEl.querySelectorAll('.swiper-slide').length;
      }
      var prevArrow = mainEl.querySelector('.swiper-button-prev');
      var nextArrow = mainEl.querySelector('.swiper-button-next');

      function keepGalleryArrowsVisible() {
        [prevArrow, nextArrow].forEach(function (btn) {
          if (!btn) return;
          btn.classList.remove('swiper-button-lock');
          btn.style.removeProperty('display');
        });
      }

      var mainSwiperConfig = {
        slidesPerView: 1,
        spaceBetween: 0,
        loop: false,
        rewind: mainSlidesCount > 1,
        speed: 300,
        observer: true,
        observeParents: true,
        navigation: {
          prevEl: prevArrow,
          nextEl: nextArrow,
          lockClass: 'product-gallery__arrow_locked',
          disabledClass: 'product-gallery__arrow_disabled'
        },
        on: {
          init: keepGalleryArrowsVisible,
          resize: keepGalleryArrowsVisible,
          update: keepGalleryArrowsVisible,
          slideChange: keepGalleryArrowsVisible
        }
      };

      if (thumbsSwiper) {
        mainSwiperConfig.thumbs = {
          swiper: thumbsSwiper,
          slideThumbActiveClass: 'swiper-slide-thumb-active',
          multipleActiveThumbs: false,
          autoScrollOffset: 1
        };
      }

      new Swiper(mainEl, mainSwiperConfig);
    }
  }

  /* ========== Секция: Hero-слайдер ========== */
  var heroSwiperEl = document.querySelector('.hero-swiper');
  if (heroSwiperEl && !heroSwiperEl.classList.contains('swiper-initialized')) {
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
  function centerAboutGalleryPagination(swiper) {
    if (!swiper || !swiper.pagination || !swiper.pagination.el) {
      return;
    }
    var pag = swiper.pagination.el;
    pag.style.setProperty('display', 'flex', 'important');
    pag.style.setProperty('justify-content', 'center', 'important');
    pag.style.setProperty('align-items', 'center', 'important');
    pag.style.setProperty('width', '100%', 'important');
    pag.style.setProperty('left', '0', 'important');
    pag.style.setProperty('right', '0', 'important');
    pag.style.setProperty('transform', 'none', 'important');
    (swiper.pagination.bullets || []).forEach(function (bullet) {
      bullet.style.setProperty('position', 'static', 'important');
      bullet.style.setProperty('left', 'auto', 'important');
      bullet.style.setProperty('transform', 'none', 'important');
      bullet.style.setProperty('margin', '0', 'important');
    });
  }

  var aboutGallery = document.querySelector('.about__gallery');
  if (aboutGallery && !aboutGallery.classList.contains('swiper-initialized')) {
    new Swiper('.about__gallery', {
      slidesPerView: 1,
      spaceBetween: 0,
      loop: true,
      pagination: {
        el: aboutGallery.querySelector('.about__pagination'),
        clickable: true
      },
      autoplay: {
        delay: 5000,
        disableOnInteraction: false
      },
      on: {
        init: function () { centerAboutGalleryPagination(this); },
        paginationUpdate: function () { centerAboutGalleryPagination(this); },
        resize: function () { centerAboutGalleryPagination(this); }
      }
    });
  }
  }

  if (window.ndaDeferred && window.ndaDeferred.needs.swiper) {
    window.ndaDeferred.on('swiper', initNdaSwipers);
  } else if (typeof Swiper !== 'undefined') {
    initNdaSwipers();
  }

  /* ========== Секция: Карта сайта — сворачивание веток ========== */
  (function initSitemapTree() {
    var tree = document.querySelector('.sitemap-tree');
    if (!tree) return;

    var lines = Array.from(tree.querySelectorAll('.sitemap-tree__line'));
    if (!lines.length) return;

    var depths = lines.map(function (line) {
      return parseInt(line.getAttribute('data-depth') || '0', 10);
    });

    function getAncestorIndices(index) {
      var ancestors = [];
      var targetDepth = depths[index] - 1;
      for (var i = index - 1; i >= 0 && targetDepth >= 0; i--) {
        if (depths[i] === targetDepth) {
          ancestors.push(i);
          targetDepth--;
        }
      }
      return ancestors;
    }

    function areAncestorsExpanded(index) {
      return getAncestorIndices(index).every(function (ancestorIndex) {
        return !lines[ancestorIndex].classList.contains('is-collapsed');
      });
    }

    function updateVisibility() {
      lines.forEach(function (line, index) {
        if (index === 0) {
          line.hidden = false;
          return;
        }
        line.hidden = !areAncestorsExpanded(index);
      });
    }

    tree.querySelectorAll('.sitemap-tree__prefix_toggle').forEach(function (button) {
      button.addEventListener('click', function () {
        var line = button.closest('.sitemap-tree__line');
        if (!line) return;

        var collapsed = line.classList.toggle('is-collapsed');
        button.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
        button.setAttribute('aria-label', collapsed ? 'Развернуть раздел' : 'Свернуть раздел');
        updateVisibility();
      });
    });
  })();

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
});
