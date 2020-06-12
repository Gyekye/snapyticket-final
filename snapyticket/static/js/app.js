if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('http://127.0.0.1:8000/static/sw.js')
        .then((reg) => console.log('service worker registered', reg))
        .catch((err) => console.log('service worker not registered', err));
}