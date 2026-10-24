/**
 * Gaveta lateral de definições e consentimento de cookies.
 */
'use strict';

// ═══════════════════════════════════════════════════
// GAVETA LATERAL E COOKIES
// ═══════════════════════════════════════════════════
function openDrawer(){
  if (typeof updateThemeCheckmarks === 'function') updateThemeCheckmarks();
  document.getElementById('settings-drawer').classList.add('open');
  document.getElementById('drawer-overlay').classList.add('open');
}
function closeDrawer(){
  document.getElementById('settings-drawer').classList.remove('open');
  document.getElementById('drawer-overlay').classList.remove('open');
}

function acceptCookies(type){
  localStorage.setItem('sigaleve_cookie_consent', type);
  document.getElementById('cookie-banner').style.display = 'none';
}
