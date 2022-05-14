const staticSnowcore = "Snowcore-v0.1"
const offline_url = "/offline.html";
const prepend = "/";
const assets = [
	offline_url,
	"https://fonts.googleapis.com/css?family=Work+Sans:200,400&display=swap",
]

self.addEventListener("install", installEvent => {
	console.log(installEvent);
	installEvent.waitUntil(
		caches.open(staticSnowcore).then(cache => {
			return cache.addAll(assets);
		})
	);
	console.log(caches);
});

self.addEventListener("activate", (event) => {
	event.waitUntil((async () => {
		if ("navigationPreload" in self.registration) {
			await self.registration.navigationPreload.enable();
		}
	})());
	self.clients.claim();
});


self.addEventListener('fetch', (event) => {
	if (event.request.mode === "navigate") {
		event.respondWith((async () => {
			try {
				const preloadResponse = await event.preloadResponse;
				if (preloadResponse) {
					return preloadResponse;
				}
				const networkResponse = await fetch(event.request);
				return networkResponse;
			} catch (error) {
				console.error(error);
				const cache = await caches.open(staticSnowcore);
				const cachedResponse = await cache.match(offline_url);
				return cachedResponse;
			}
		})());
	}
});