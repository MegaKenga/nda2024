/**
 * Тяжёлые CSS/JS и карты Яндекса — только после взаимодействия пользователя
 * (скролл, движение мыши, касание, клавиатура) или клика по форме/карте.
 */
(function () {
  'use strict';

  var activated = false;
  var loading = {};
  var loaded = { swiper: false, phone: false, captcha: false, maps: false };
  var callbacks = { swiper: [], phone: [], captcha: [], maps: [] };

  var URLS = {
    swiperCss: 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css',
    swiperJs: 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js',
    intlCss: 'https://cdn.jsdelivr.net/npm/intl-tel-input@18.2.1/build/css/intlTelInput.min.css',
    intlJs: 'https://cdn.jsdelivr.net/npm/intl-tel-input@18.2.1/build/js/intlTelInput.min.js',
    inputmaskJs: 'https://cdn.jsdelivr.net/npm/inputmask@5.0.8/dist/inputmask.min.js',
    captchaJs: 'https://smartcaptcha.cloud.yandex.ru/captcha.js'
  };

  function detectNeeds() {
    return {
      swiper: !!document.querySelector('.hero-swiper, .about__gallery, [data-product-gallery]'),
      captcha: !!document.querySelector('.smart-captcha'),
      phone: !!document.querySelector('.phone-mask, input[type="tel"]'),
      maps: !!document.querySelector('[data-yandex-map]')
    };
  }

  function loadCss(href) {
    return new Promise(function (resolve) {
      if (document.querySelector('link[data-nda-href="' + href + '"]')) {
        resolve();
        return;
      }
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = href;
      link.setAttribute('data-nda-href', href);
      link.onload = function () { resolve(); };
      link.onerror = function () { resolve(); };
      document.head.appendChild(link);
    });
  }

  function loadScript(src, defer) {
    return new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[data-nda-src="' + src + '"]');
      if (existing) {
        if (existing.getAttribute('data-nda-loaded') === '1') {
          resolve();
          return;
        }
        existing.addEventListener('load', function () { resolve(); });
        existing.addEventListener('error', reject);
        return;
      }
      var script = document.createElement('script');
      script.src = src;
      script.setAttribute('data-nda-src', src);
      if (defer) {
        script.defer = true;
      }
      script.onload = function () {
        script.setAttribute('data-nda-loaded', '1');
        resolve();
      };
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  function flush(bundle) {
    loaded[bundle] = true;
    (callbacks[bundle] || []).forEach(function (fn) {
      try {
        fn();
      } catch (e) { /* ignore */ }
    });
    callbacks[bundle] = [];
  }

  function on(bundle, fn) {
    if (loaded[bundle]) {
      fn();
      return;
    }
    if (!callbacks[bundle]) {
      callbacks[bundle] = [];
    }
    callbacks[bundle].push(fn);
  }

  function loadSwiper() {
    if (loaded.swiper) {
      return Promise.resolve();
    }
    if (loading.swiper) {
      return loading.swiper;
    }
    loading.swiper = loadCss(URLS.swiperCss)
      .then(function () { return loadScript(URLS.swiperJs); })
      .then(function () { flush('swiper'); })
      .catch(function () { flush('swiper'); });
    return loading.swiper;
  }

  function loadPhone() {
    if (loaded.phone) {
      return Promise.resolve();
    }
    if (loading.phone) {
      return loading.phone;
    }
    loading.phone = loadCss(URLS.intlCss)
      .then(function () { return loadScript(URLS.intlJs); })
      .then(function () { return loadScript(URLS.inputmaskJs); })
      .then(function () { flush('phone'); })
      .catch(function () { flush('phone'); });
    return loading.phone;
  }

  function loadCaptcha() {
    if (loaded.captcha) {
      return Promise.resolve();
    }
    if (loading.captcha) {
      return loading.captcha;
    }
    loading.captcha = loadScript(URLS.captchaJs, true)
      .then(function () { flush('captcha'); })
      .catch(function () { flush('captcha'); });
    return loading.captcha;
  }

  function mountMap(el) {
    if (!el || el.getAttribute('data-map-loaded') === '1') {
      return;
    }
    var src = el.getAttribute('data-map-src');
    if (!src) {
      return;
    }
    var iframe = document.createElement('iframe');
    iframe.src = src;
    iframe.width = '100%';
    iframe.height = '100%';
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('loading', 'lazy');
    iframe.setAttribute('title', el.getAttribute('data-map-title') || 'Карта');
    el.appendChild(iframe);
    el.setAttribute('data-map-loaded', '1');
  }

  function initMaps() {
    if (loaded.maps) {
      return Promise.resolve();
    }
    var nodes = document.querySelectorAll('[data-yandex-map]');
    if (!nodes.length) {
      loaded.maps = true;
      return Promise.resolve();
    }

    function loadVisibleMaps() {
      nodes.forEach(function (el) {
        mountMap(el);
      });
      loaded.maps = true;
      flush('maps');
    }

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            mountMap(entry.target);
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '200px 0px' });
      nodes.forEach(function (el) {
        if (el.getAttribute('data-map-loaded') !== '1') {
          observer.observe(el);
        }
      });
      loaded.maps = true;
      flush('maps');
      return Promise.resolve();
    }

    loadVisibleMaps();
    return Promise.resolve();
  }

  function activate() {
    if (activated) {
      return window.ndaLoadHeavyAssets._promise || Promise.resolve();
    }
    activated = true;

    var needs = detectNeeds();
    var tasks = [];

    if (needs.swiper) {
      tasks.push(loadSwiper());
    }
    if (needs.phone) {
      tasks.push(loadPhone());
    }
    if (needs.captcha) {
      tasks.push(loadCaptcha());
    }
    if (needs.maps) {
      tasks.push(initMaps());
    }

    window.ndaLoadHeavyAssets._promise = Promise.all(tasks).then(function () {
      document.dispatchEvent(new CustomEvent('nda:heavy-ready'));
    });

    return window.ndaLoadHeavyAssets._promise;
  }

  function activateForms() {
    var needs = detectNeeds();
    var tasks = [activate()];
    if (needs.phone) {
      tasks.push(loadPhone());
    }
    if (needs.captcha) {
      tasks.push(loadCaptcha());
    }
    return Promise.all(tasks);
  }

  window.ndaDeferred = {
    needs: detectNeeds(),
    on: on,
    activate: activate,
    loadSwiper: loadSwiper,
    loadPhone: loadPhone,
    loadCaptcha: loadCaptcha,
    loadMaps: function () {
      return activate().then(initMaps);
    }
  };

  window.ndaLoadHeavyAssets = activate;
  window.ndaLoadHeavyAssets._promise = null;

  var interactionEvents = ['scroll', 'mousemove', 'touchstart', 'keydown', 'pointerdown'];
  var interactionOpts = { passive: true, capture: true, once: true };

  function onFirstInteraction() {
    interactionEvents.forEach(function (eventName) {
      window.removeEventListener(eventName, onFirstInteraction, interactionOpts);
    });
    activate();
  }

  interactionEvents.forEach(function (eventName) {
    window.addEventListener(eventName, onFirstInteraction, interactionOpts);
  });

  document.addEventListener('click', function (event) {
    var target = event.target.closest(
      '[data-callback-popup-open], [data-mail-popup-open], [data-contact-trigger], ' +
      '.smart-captcha, [data-yandex-map], .phone-mask, input[type="tel"]'
    );
    if (target) {
      if (target.matches('[data-yandex-map]') || target.closest('[data-yandex-map]')) {
        activate().then(initMaps);
        return;
      }
      activateForms();
    }
  }, true);
})();
