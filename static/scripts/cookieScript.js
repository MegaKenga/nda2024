// Скрипт, отображающий согласие о куки и переспрашивающий раз в год

document.addEventListener('DOMContentLoaded', function () {

  if (document.cookie.indexOf('cookie_consent=true') === -1) {
    document.getElementById('cookie-consent').style.display = 'flex'; 

    document.getElementById('cookie-consent-button').addEventListener('click', function () {
      document.cookie = 'cookie_consent=true; max-age=' + (365 * 24 * 60 * 60) + '; path=/';
      document.getElementById('cookie-consent').style.display = 'none'; 
    });
  }
});