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
      });
    });
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
        var val = parseInt(input.value, 10) || 1;
        if (val > 1) input.value = val - 1;
      });
      btnPlus.addEventListener('click', function () {
        var val = parseInt(input.value, 10) || 0;
        input.value = val + 1;
      });
    }
    if (btnAdd) {
      btnAdd.addEventListener('click', function () {
        /* TODO: добавление в заказ */
      });
    }
  });

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
      freeMode: true,
      watchSlidesProgress: true,
      observer: true,
      observeParents: true
    });
    new Swiper('.product-gallery-main', {
      spaceBetween: 0,
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
});
