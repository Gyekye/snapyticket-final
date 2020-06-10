// Note that anytime you make a change in any of the pages or static files you must update the version of either the staticCacheName or dynamicCacheName before you will see your changes (i.e 'site-static' must become 'site-static-v1' and vice versa)

// Site-static caches the assets array
const staticCacheName = 'site-static';
// Site-dynamic caches the other individual pages
const dynamicCacheName = 'site-dynamic';
// This array stores common pages and static files(other static files can be added)
const assets = [
    '/',
    '/index.html',
    'auth/login.html',
    'auth/signup.html',
    'static/js/app.js',
    'static/js/main.js',
    'static/js/materialize.min.js',
    'static/js/jquery-3.4.1.min.js',
    'static/css/style.css',
    'static/css/materialize.min.css',
    'static/imgs/icons/evesbay.ico',
    'static/imgs/icons/tickets.png',
    'static/imgs/icons/shoppingBag.png',
    'static/imgs/icons/trash.png',
    'static/imgs/icons/user.png',
    'static/imgs/icons/settings.svg',
    'static/fonts/icon.css',
    'static/fonts/default.css',
];

// Cache size limit function
const limitCacheSize = (name, size) => {
    caches.open(name).then(cache => {
        cache.keys().then(keys => {
            if (keys.length > size) {
                cache.delete(keys[0]).then(limitCacheSize(name, size));
            }
        })
    })
};

// Install Service Worker
self.addEventListener('install', evt => {
    //caches elements in the assets array
    evt.waitUntil(
        caches.open(staticCacheName).then(cache => {
            console.log('caching shell assets');
            cache.addAll(assets);
        })
    );
});

// Activate Event
self.addEventListener('activate', evt => {
    //Deletes the old cache version
    evt.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(keys
                .filter(key => key !== staticCacheName && key !== dynamicCacheName)
                .map(key => caches.delete(key))
            )
        })
    );
});

// fetch event
self.addEventListener('fetch', evt => {
    //Limits the cache size of the other cached pages
    evt.respondWith(
        caches.match(evt.request).then(cachesRes => {
            return cachesRes || fetch(evt.request).then(fetchRes => {
                return caches.open(dynamicCacheName).then(cache => {
                    cache.put(evt.request.url, fetchRes.clone());
                    limitCacheSize(dynamicCacheName, 20);
                    return fetchRes;
                })
            });
        }).catch(() => {
            // Redirects to fallback page if requested page is not cached
            if (evt.request.url.indexOf('.html') > -1) {
                return caches.match('/templates/fallback.html')
            }
        })
    )
});