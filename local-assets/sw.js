/* rousseau-agent docs — service worker
 * Cache-first for fonts + fingerprinted CSS/JS (long-lived, hashed);
 * network-first for HTML (freshness matters);
 * offline fallback to /offline/ when the network is unreachable.
 */
const VERSION = 'ra-docs-v1';
const HTML_CACHE = `${VERSION}-html`;
const ASSET_CACHE = `${VERSION}-assets`;

const OFFLINE_URL = '/offline/index.html';
const PRECACHE_URLS = [
  '/',
  '/quickstart/',
  '/offline/index.html',
  '/manifest.json',
  '/fonts/fonts.css',
  '/fonts/inter-latin.woff2',
  '/fonts/newsreader-latin.woff2',
  '/fonts/jetbrains-mono-latin.woff2',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(ASSET_CACHE)
      .then((c) => c.addAll(PRECACHE_URLS).catch(() => null))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter((k) => !k.startsWith(VERSION))
          .map((k) => caches.delete(k)),
      );
      await self.clients.claim();
    })(),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // Cache-first for long-lived fingerprinted assets and fonts.
  if (
    url.pathname.startsWith('/_csp/') ||
    url.pathname.startsWith('/fonts/') ||
    url.pathname.endsWith('.woff2') ||
    url.pathname.endsWith('.svg') ||
    url.pathname.endsWith('.png') ||
    url.pathname.endsWith('.ico')
  ) {
    event.respondWith(
      caches.match(request).then(
        (hit) =>
          hit ||
          fetch(request).then((resp) => {
            const clone = resp.clone();
            caches.open(ASSET_CACHE).then((c) => c.put(request, clone));
            return resp;
          }),
      ),
    );
    return;
  }

  // Network-first for HTML with offline fallback.
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((resp) => {
          const clone = resp.clone();
          caches.open(HTML_CACHE).then((c) => c.put(request, clone));
          return resp;
        })
        .catch(() =>
          caches
            .match(request)
            .then((hit) => hit || caches.match(OFFLINE_URL)),
        ),
    );
    return;
  }

  // Default: stale-while-revalidate.
  event.respondWith(
    caches.match(request).then((hit) => {
      const refresh = fetch(request)
        .then((resp) => {
          const clone = resp.clone();
          caches.open(ASSET_CACHE).then((c) => c.put(request, clone));
          return resp;
        })
        .catch(() => hit);
      return hit || refresh;
    }),
  );
});
