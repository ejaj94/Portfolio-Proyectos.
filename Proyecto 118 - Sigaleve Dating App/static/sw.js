// Service Worker Sigaleve — PWA shell cache + network-first para API
// Estratégia: network-first em tudo (dados de dating são dinâmicos/sensíveis),
// com fallback offline do shell (CSS/ícones) e uma página offline amigável.
const CACHE = 'sigaleve-v1';
const SHELL = [
  '/static/img/favicon-32x32.png',
  '/static/img/logo-icon-192.png',
  '/static/img/logo-icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  // Nunca cachear: API, socket.io, uploads de usuário
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/socket.io/') || url.pathname.startsWith('/uploads/')) return;
  // POST/PUT/DELETE: deixa passar direto
  if (e.request.method !== 'GET') return;

  // GET estático/imagem: stale-while-revalidate (resposta rápida + atualiza em fundo)
  if (url.pathname.startsWith('/static/')) {
    e.respondWith(
      caches.match(e.request).then((cached) => {
        const fetchAndCache = fetch(e.request).then((res) => {
          if (res.ok) caches.open(CACHE).then((c) => c.put(e.request, res.clone()));
          return res;
        }).catch(() => cached);
        return cached || fetchAndCache;
      })
    );
    return;
  }

  // Páginas do app (HTML): network-first com fallback offline
  e.respondWith(
    fetch(e.request).catch(() =>
      caches.match(e.request).then((cached) => cached || new Response(
        '<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sigaleve — Offline</title><style>body{background:#0d0e15;color:#fff;font-family:-apple-system,system-ui,sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}div{padding:24px}h1{font-size:22px}p{color:#94a3b8;font-size:14px}button{background:linear-gradient(135deg,#9333ea,#ec4899);color:#fff;border:none;padding:12px 28px;border-radius:14px;font-weight:700;font-size:14px;margin-top:12px}</style></head><body><div><h1>👻 Estás offline</h1><p>O Sigaleve precisa de ligação à internet para te mostrar novos perfis e mensagens.</p><button onclick="location.reload()">Tentar novamente</button></div></body></html>',
        { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
      ))
    )
  );
});

// ── PUSH NOTIFICATIONS ──────────────────────────────────────────────────────
self.addEventListener('push', (e) => {
  let data = {};
  try { data = e.data ? e.data.json() : {}; } catch (err) { data = {}; }
  const title = data.title || 'Sigaleve';
  const body = data.body || 'Tens novidades!';
  const url = data.url || '/app';
  e.waitUntil(
    self.registration.showNotification(title, {
      body,
      icon: '/static/img/logo-icon-192.png',
      badge: '/static/img/favicon-32x32.png',
      tag: 'sigaleve-' + (data.ts || Date.now()),
      data: { url },
      vibrate: [100, 50, 100]
    })
  );
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || '/app';
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((list) => {
      for (const c of list) {
        if ('focus' in c) { c.focus(); return; }
      }
      return clients.openWindow(url);
    })
  );
});
