const staticSnowcore = "Snowcore-v0.1"
const prepend = "/";
const assets = [
	prepend + "index.html",
	prepend + "css/style.css",
	prepend + "javascript/render.js",
	prepend + "icons/",
	prepend + "icons/Blizzard.gif",
	prepend + "icons/FreezingDrizzle.gif",
	prepend + "icons/HeavySleet.gif",
	prepend + "icons/IsoRainSwrsDay.gif",
	prepend + "icons/mist.gif",
	prepend + "icons/ModSleetSwrsNight.gif",
	prepend + "icons/OccLightSnow.gif",
	prepend + "icons/PartlyCloudyDay.gif",
	prepend + "icons/Clear.gif",
	prepend + "icons/FreezingFog.gif",
	prepend + "icons/HeavySleetSwrsDay.gif",
	prepend + "icons/IsoRainSwrsNight.gif",
	prepend + "icons/ModRain.gif",
	prepend + "icons/ModSnow.gif",
	prepend + "icons/Overcast.gif",
	prepend + "icons/PartlyCloudyNight.gif",
	prepend + "icons/CloudRainThunder.gif",
	prepend + "icons/FreezingRain.gif",
	prepend + "icons/HeavySleetSwrsNight.gif",
	prepend + "icons/IsoSleetSwrsDay.gif",
	prepend + "icons/ModRainSwrsDay.gif",
	prepend + "icons/ModSnowSwrsDay.gif",
	prepend + "icons/PartCloudRainThunderDay.gif",
	prepend + "icons/Sunny.gif",
	prepend + "icons/CloudSleetSnowThunder.gif",
	prepend + "icons/HeavyRain.gif",
	prepend + "icons/HeavySnow.gif",
	prepend + "icons/IsoSleetSwrsNight.gif",
	prepend + "icons/ModRainSwrsNight.gif",
	prepend + "icons/ModSnowSwrsNight.gif",
	prepend + "icons/PartCloudRainThunderNight.gif",
	prepend + "icons/Cloudy.gif",
	prepend + "icons/HeavyRainSwrsDay.gif",
	prepend + "icons/HeavySnowSwrsDay.gif",
	prepend + "icons/IsoSnowSwrsDay.gif",
	prepend + "icons/ModSleet.gif",
	prepend + "icons/OccLightRain.gif",
	prepend + "icons/PartCloudSleetSnowThunderDay.gif",
	prepend + "icons/Fog.gif",
	prepend + "icons/HeavyRainSwrsNight.gif",
	prepend + "icons/HeavySnowSwrsNight.gif",
	prepend + "icons/IsoSnowSwrsNight.gif",
	prepend + "icons/ModSleetSwrsDay.gif",
	prepend + "icons/OccLightSleet.gif",
	prepend + "icons/PartCloudSleetSnowThunderNight.gif",
	prepend + "icons/Blizzard.gif",
	prepend + "images/skiing.jpg",
	prepend + "images/snowcore.png",
	"https://fonts.googleapis.com/css?family=Work+Sans:200,400&display=swap",
	"https://fonts.gstatic.com/s/worksans/v17/QGYsz_wNahGAdqQ43Rh_c6Dpp_k.woff2",
	"https://fonts.gstatic.com/s/worksans/v17/QGYsz_wNahGAdqQ43Rh_cqDpp_k.woff2",
	"https://fonts.gstatic.com/s/worksans/v17/QGYsz_wNahGAdqQ43Rh_fKDp.woff2",
	// "https://cdn.tailwindcss.com/",
]

self.addEventListener("install", installEvent => {
	installEvent.waitUntil(
		caches.open(staticSnowcore).then(cache => {
			cache.addAll(assets)
		})
	)
});

addEventListener("fetch", function (e) {
	e.respondWith((async function () {
		const cachedResponse = await caches.match(e.request);
		if (cachedResponse) {
			return cachedResponse;
		}

		const networkResponse = await fetch(e.request);

		const hosts = [
			'https://fonts.googleapis.com',
			'https://maxcdn.bootstrapcdn.com',
			'https://cdnjs.cloudflare.com',
		];

		if (hosts.some((host) => e.request.url.startsWith(host))) {
			// This clone() happens before `return networkResponse` 
			const clonedResponse = networkResponse.clone();

			e.waitUntil((async function () {
				const cache = await caches.open(CACHE_NAME);
				// This will be called after `return networkResponse`
				// so make sure you already have the clone!
				await cache.put(e.request, clonedResponse);
			})());
		}

		return networkResponse;
	})());
});  