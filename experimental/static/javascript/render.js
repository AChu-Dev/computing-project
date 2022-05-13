"use strict";

const prepend = "/static/";

if ("serviceWorker" in navigator) {
	window.addEventListener("load", function () {
		navigator.serviceWorker
			.register(prepend + "javascript/sw.js")
			.then(res => console.log("service worker registered"))
			.catch(err => console.log("service worker not registered", err))
	})
}

let weather = null;

const historicalWeather = async () => {
	if (weather == null)
		weather = await fetch(prepend + "historical_weather.json").then(response => response.json());
	return weather;
};

const loading = (clear) => {
	let main = document.getElementById("main");
	addClasses(main, ["mb-6"]);
	main.innerHTML = "";
	if (!clear) {
		const loader = document.createElement("div");
		addClasses(loader, ["container", "mx-auto", "text-center", "pb-12", "pt-6"]);
		loader.innerText = "Loading...";
		main.appendChild(loader);
	}
};

const addClasses = (element, classList) => {
	classList.forEach(className => {
		element.classList.add(className);
	});
};

const createResort = (id, name, image, isFavourite) => {
	const container = document.createElement("div");
	addClasses(container, ["w-full", "md:w-1/3", "xl:w-1/4", "p-6", "flex", "flex-col", "cursor-pointer"]);
	const heroImage = document.createElement("img");
	heroImage.src = image || prepend + "images/skiing.jpg";
	addClasses(heroImage, ["hover:grow", "hover:shadow-lg", "h-64"]);
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["pt-3", "flex", "items-center", "justify-between"]);
	const resortName = document.createElement("p");
	resortName.innerText = name;
	const favourite = document.createElement("svg");
	favourite.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	heroImage.addEventListener("click", () => {
		showResort(id);
	});
	resortName.addEventListener("click", () => {
		showResort(id);
	});
	containerFlex.appendChild(resortName);
	containerFlex.appendChild(favourite);
	container.appendChild(heroImage);
	container.appendChild(containerFlex);
	return container;
};

const showResorts = async (resorts) => {
	const section = document.createElement("section");
	section.innerHTML = "Loading...";
	addClasses(section, ["bg-white", "pb-8"]);
	const container = document.createElement("div");
	addClasses(container, ["container", "mx-auto", "flex", "items-center", "flex-wrap", "pt-4", "pb-12"]);
	resorts.forEach(resort => {
		let test = createResort(resort["id"], resort["name"], resort["image"], resort["isFavourite"]);
		container.appendChild(test);
	});
	section.innerHTML = "";
	section.appendChild(container);
	loading(true);
	document.getElementById("main").appendChild(section);
};

const showResort = async (resort) => {
	// 'resort_id','name','address','longitude','latitude', 'weather', 'wx_icon', 'description', 'favourites'
	loading(false);
	let image = null;
	let name = "Example";
	let weatherImage = "Blizzard.gif";
	let resortDescription = "example";
	let totalFavourites = 0;
	const heroImage = document.createElement("div");
	heroImage.style.backgroundImage = "url(" + (image || prepend + "images/skiing.jpg") + ")";
	addClasses(heroImage, ["container", "w-full", "mx-auto", "h-96", "bg-cover", "bg-center", "bg-no-repeat", "relative", "mb-12", "rounded-t-2xl", "mt-6"]);
	const weatherIcon = document.createElement("div");
	addClasses(weatherIcon, ["w-24", "h-24", "rounded-full", "bg-white", "bg-no-repeat", "bg-contain", "bg-center", "mx-auto", "absolute", "inset-x-0"]);
	weatherIcon.style.bottom = "-48px";
	weatherIcon.style.backgroundImage = "url(\"" + prepend + "icons/" + weatherImage + "\")";
	weatherIcon.title = "Current weather of resort";
	heroImage.append(weatherIcon);
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["flex", "items-center", "px-8", "mb-8", "justify-center"]);
	const resortName = document.createElement("h2");
	resortName.innerText = name;
	addClasses(resortName, ["container", "px-8", "text-center", "text-4xl", "pb-2", "mx-auto"]);
	const favourite = document.createElement("svg");
	favourite.innerHTML = "<svg class=\"ml-2 h-6 w-6 fill-current text-gray-500 hover:text-black\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	let descriptions = resortDescription.split("\n");
	loading(true);
	let mapLink = document.createElement("a");
	addClasses(mapLink, ["px-8", "pb-6", "underline", "text-center", "text-blue-600", "hover:text-blue-800", "visited:text-purple-600", "container", "mx-auto", "w-full", "flex", "justify-center", "cursor-pointer"]);
	mapLink.innerText = "Piste map";
	let main = document.getElementById("main");
	main.appendChild(heroImage);
	main.appendChild(resortName);
	main.appendChild(containerFlex);
	let favouriteParagraph = document.createElement("p");
	favouriteParagraph.innerHTML = "Favourited by: <span id=\"resortFavouriteCount\">" + totalFavourites + "</span> users";
	addClasses(favouriteParagraph, ["text-center"]);
	containerFlex.appendChild(favouriteParagraph);
	containerFlex.appendChild(favourite);
	main.appendChild(containerFlex);
	let top = true;
	descriptions.forEach(paragraph => {
		let descriptionParagraph = document.createElement("p");
		descriptionParagraph.innerText = paragraph;
		addClasses(descriptionParagraph, ["px-8", "text-justify", "pb-6", "container", "mx-auto"]);
		if (top) {
			addClasses(descriptionParagraph, ["mt-8"]);
		}
		main.appendChild(descriptionParagraph);
		top = false;
	});
	let historicWeather = document.createElement("img");
	historicWeather.src = prepend + "historic_weather_2021.png";
	addClasses(historicWeather, ["mx-auto"]);
	main.appendChild(historicWeather);
	main.appendChild(mapLink);
	document.title = name + " | Snowcore";
};

const newPage = (pageId) => {
	loading(false);
	switch (pageId) {
		case 0:
			document.title = "Snowcore";
			showResorts([{ "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }, { "id": 0, "name": "name", "image": null, "isFavourite": true }]);
			break;
		default:
			break;
	}
};

window.addEventListener('DOMContentLoaded', () => {
	if (typeof pageId === "undefined") {
		console.error("Invalid page ID");
	} else {
		newPage(pageId);
	}
	document.getElementById("headerMain").addEventListener("click", () => {
		pageId = 0;
		newPage(pageId);
	})
});