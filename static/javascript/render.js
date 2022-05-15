"use strict";

const demo = false;

if ("serviceWorker" in navigator) {
	window.addEventListener("load", () => {
		navigator.serviceWorker
			.register("sw.js")
			.then(res => console.log("service worker registered"))
			.catch(err => console.log("service worker not registered", err))
	})
}

let weather = null;

let weatherCache = [new Date(0, 0, 0, 0, 0, 0, 0), []];

const weatherInterval = 6;

const getWeather = async (resortId) => {
	const urls = [
		{
			"id": 333031,
			"url": "https://api.weatherunlocked.com/api/resortforecast/333031?app_id=a3fd6c9a&app_key=027a1023047a432b9ed2e4a7db484a07&hourly_interval=" + weatherInterval
		},
		{
			"id": 333005,
			"url": "https://api.weatherunlocked.com/api/resortforecast/333005?app_id=4c84c18d&app_key=5f4b7efa21bbda9d00d158c7c11ac815&hourly_interval=" + weatherInterval
		},
		{
			"id": 333014,
			"url": "https://api.weatherunlocked.com/api/resortforecast/333014?app_id=62707ed6&app_key=10981bcbfd38f7a0b53bb253990c0cbf&hourly_interval=" + weatherInterval
		},
	];
	let url = null;
	urls.forEach(resort => {
		if (resort["id"] == resortId) {
			url = resort["url"];
			return;
		}
	});
	if (url == null) {
		return null;
	}
	let cached = null;
	if ((new Date(new Date().getTime() - 60000)) < weatherCache[0]) {
		weatherCache[1].forEach(weatherCached => {
			if (weatherCached["id"] == resortId) {
				cached = weatherCached["weather"];
				return cached;
			}
		});
	}
	if (cached != null) {
		return cached;
	}
	const request = await fetch(url, {
		method: "GET",
		mode: "cors",
		headers: {
			"Accept": "application/json"
		},
	}).then(response => response.json()).catch(e => {
		return null;
	});
	let updated = false;
	weatherCache[1].forEach(weatherCached => {
		if (weatherCached["id"] == resortId) {
			weatherCache["weather"] = request;
			updated = true;
			return request;
		}
	});
	if (!updated) {
		weatherCache[0] = new Date();
		weatherCache[1].push({ "id": resortId, "weather": request });
	}
	return request;
}

const historicalWeather = async () => {
	if (weather == null)
		weather = await fetch("/historical_weather.json").then(response => response.json());
	return weather;
};

const loading = (clear, append = false) => {
	let main = document.getElementById("main");
	addClasses(main, ["mb-6", "flex-auto"]);
	if (!append) {
		main.innerHTML = "";
	}
	if (!clear) {
		const loader = document.createElement("div");
		loader.id = "loaderMessage";
		addClasses(loader, ["container", "mx-auto", "text-center", "pb-12", "pt-6", "cursor-wait", "select-none"]);
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
	heroImage.src = image || "/images/skiing.jpg";
	addClasses(heroImage, ["hover:grow", "hover:shadow-lg", "h-64"]);
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["pt-3", "flex", "items-center", "justify-between"]);
	const resortName = document.createElement("p");
	resortName.innerText = name;
	const favourite = document.createElement("svg");
	if (isFavourite) {
		favourite.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	} else {
		favourite.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black\" width=\"24\" height=\"24\" xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" clip-rule=\"evenodd\"><path d=\"M12 21.593c-5.63-5.539-11-10.297-11-14.402 0-3.791 3.068-5.191 5.281-5.191 1.312 0 4.151.501 5.719 4.457 1.59-3.968 4.464-4.447 5.726-4.447 2.54 0 5.274 1.621 5.274 5.181 0 4.069-5.136 8.625-11 14.402m5.726-20.583c-2.203 0-4.446 1.042-5.726 3.238-1.285-2.206-3.522-3.248-5.719-3.248-3.183 0-6.281 2.187-6.281 6.191 0 4.661 5.571 9.429 12 15.809 6.43-6.38 12-11.148 12-15.809 0-4.011-3.095-6.181-6.274-6.181\"/></svg>";
	}
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

const showResort = async (resortId) => {
	loading(false);
	const resort = await getResortByID(resortId);
	if (resort == null) {
		pageId = 0;
		newPage(pageId);
		return;
	}
	pageId = resortId;
	let weather = await getWeather(resortId);
	if (weather != null) {
		let weatherForecast = [];
		for (let i = 0; i < Math.min(weather["forecast"].length, 6); i++) {
			weatherForecast.push(weather["forecast"][i]["date"] + " " + weather["forecast"][i]["time"] + ": " + weather["forecast"][i]["base"]["wx_desc"]);
		}
		weather = [weather["forecast"][0]["base"]["wx_desc"], weather["forecast"][0]["base"]["wx_icon"], weatherForecast];
	} else {
		weather = ["Unknown", null, []];
	}
	let image = resort["image"];
	let name = resort["name"];
	let weatherImage = weather[1];
	let resortDescription = resort["description"];
	let totalFavourites = 0;
	let isFavourite = resort["isFavourite"];
	const heroImage = document.createElement("div");
	heroImage.style.backgroundImage = "url(" + (image || "/images/skiing.jpg") + ")";
	addClasses(heroImage, ["w-full", "mx-auto", "h-96", "bg-cover", "bg-center", "bg-no-repeat", "relative", "mb-12", "select-none"]);
	if (weather[0] == "Unknown") {
		heroImage.classList.remove("h-96");
		heroImage.style.height = "33rem";
	} else {
		const weatherIcon = document.createElement("div");
		addClasses(weatherIcon, ["w-24", "h-24", "rounded-full", "bg-white", "bg-no-repeat", "bg-contain", "bg-center", "mx-auto", "absolute", "inset-x-0", "select-none", "cursor-pointer"]);
		weatherIcon.style.bottom = "-48px";
		weatherIcon.style.backgroundImage = "url(\"" + "/icons/" + weatherImage + "\")";
		weatherIcon.title = "Current weather of resort: " + weather[0];
		weatherIcon.addEventListener("click", () => {
			alert("Weather forecast for the next " + (weather[2].length * weatherInterval) + " hours:\n" + weather[2].join("\n"));
		});
		heroImage.append(weatherIcon);
	}
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["flex", "items-center", "px-8", "mb-8", "justify-center", "select-none"]);
	const resortName = document.createElement("h2");
	resortName.innerText = name;
	addClasses(resortName, ["container", "px-8", "text-center", "text-4xl", "pb-2", "mx-auto", "select-none"]);
	const favourite = document.createElement("svg");
	if (isFavourite) {
		favourite.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black ml-4\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	} else {
		favourite.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black ml-4\" width=\"24\" height=\"24\" xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" clip-rule=\"evenodd\"><path d=\"M12 21.593c-5.63-5.539-11-10.297-11-14.402 0-3.791 3.068-5.191 5.281-5.191 1.312 0 4.151.501 5.719 4.457 1.59-3.968 4.464-4.447 5.726-4.447 2.54 0 5.274 1.621 5.274 5.181 0 4.069-5.136 8.625-11 14.402m5.726-20.583c-2.203 0-4.446 1.042-5.726 3.238-1.285-2.206-3.522-3.248-5.719-3.248-3.183 0-6.281 2.187-6.281 6.191 0 4.661 5.571 9.429 12 15.809 6.43-6.38 12-11.148 12-15.809 0-4.011-3.095-6.181-6.274-6.181\"/></svg>";
	}
	let descriptions = resortDescription.split("\n");
	let mapLink = document.createElement("a");
	addClasses(mapLink, ["px-8", "pb-6", "underline", "text-center", "text-blue-600", "hover:text-blue-800", "visited:text-purple-600", "container", "mx-auto", "w-full", "flex", "justify-center", "cursor-pointer", "select-none"]);
	mapLink.innerText = "Piste map";
	mapLink.href = "http://maps.google.com/maps?z=14&t=p&q=loc:" + resort["latitude"] + "+" + resort["longitude"];
	mapLink.target = "_blank";
	if (pageId != resortId) {
		return;
	}
	loading(true);
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
		addClasses(descriptionParagraph, ["px-8", "text-justify", "pb-6", "container", "mx-auto", "select-none"]);
		if (top) {
			addClasses(descriptionParagraph, ["mt-8"]);
		}
		main.appendChild(descriptionParagraph);
		top = false;
	});
	let historicWeather = document.createElement("img");
	historicWeather.src = "/historic_weather_2021.png";
	addClasses(historicWeather, ["mx-auto", "select-none"]);
	main.appendChild(historicWeather);
	main.appendChild(mapLink);
	document.title = name + " | Snowcore";
};

const signIn = (register, usernameString = "") => {
	const signInContainer = document.createElement("form");
	addClasses(signInContainer, ["container", "w-full", "mx-auto"]);
	const names = [document.createElement("input"), document.createElement("input")];
	const email = document.createElement("input");
	const username = document.createElement("input");
	username.value = usernameString;
	const passwords = [document.createElement("input"), document.createElement("input")];
	addClasses(names[0], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(names[1], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(email, ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(username, ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(passwords[0], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(passwords[1], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	names[0].setAttribute("required", "required");
	names[1].setAttribute("required", "required");
	email.setAttribute("required", "required");
	username.setAttribute("required", "required");
	passwords[0].setAttribute("required", "required");
	passwords[1].setAttribute("required", "required");
	email.type = "email";
	passwords[0].type = "password";
	passwords[1].type = "password";
	const tips = [document.createElement("p"), document.createElement("p"), document.createElement("p"), document.createElement("p"), document.createElement("p"), document.createElement("p")];
	tips[0].innerText = "First name:";
	addClasses(tips[0], ["block", "text-center", "select-none"]);
	tips[1].innerText = "Surname:";
	addClasses(tips[1], ["block", "text-center", "select-none"]);
	tips[2].innerText = "Email:";
	addClasses(tips[2], ["block", "text-center", "select-none"]);
	tips[3].innerText = "Username:";
	addClasses(tips[3], ["block", "text-center", "select-none"]);
	tips[4].innerText = "Password:";
	addClasses(tips[4], ["block", "text-center", "select-none"]);
	tips[5].innerText = "Repeat password:";
	addClasses(tips[5], ["block", "text-center", "select-none"]);
	const submit = document.createElement("input");
	addClasses(submit, ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "mx-auto", "select-none"]);
	submit.type = "submit";
	submit.value = { true: "Register", false: "Sign in" }[register];
	if (register) {
		document.title = "Sign up | Snowcore";
		addClasses(tips[0], ["pt-12"]);
		signInContainer.appendChild(tips[0]);
		signInContainer.appendChild(names[0]);
		signInContainer.appendChild(tips[1]);
		signInContainer.appendChild(names[1]);
		signInContainer.appendChild(tips[2]);
		signInContainer.appendChild(email);
		signInContainer.appendChild(tips[3]);
		signInContainer.appendChild(username);
		signInContainer.appendChild(tips[4]);
		signInContainer.appendChild(passwords[0]);
		signInContainer.appendChild(tips[5]);
		signInContainer.appendChild(passwords[1]);
		signInContainer.appendChild(submit);
	} else {
		document.title = "Sign in | Snowcore";
		addClasses(tips[3], ["pt-12"]);
		signInContainer.appendChild(tips[3]);
		signInContainer.appendChild(username);
		signInContainer.appendChild(tips[4]);
		signInContainer.appendChild(passwords[0]);
		signInContainer.appendChild(submit);
		const register = document.createElement("input");
		addClasses(register, ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "mx-auto", "select-none"]);
		register.type = "button";
		register.value = "Register?";
		register.addEventListener("click", () => {
			signIn(true, username.value);
		});
		signInContainer.appendChild(register);
	}
	signInContainer.addEventListener("submit", async (e) => {
		e.preventDefault();
		let requestBody = { "username": username.value, password1: passwords[0].value, password2: passwords[1].value, firstName: names[0].value, lastName: names[1].value, email: email.value };
		if (!register) {
			delete requestBody["password1"];
			delete requestBody["password2"];
			delete requestBody["firstName"];
			delete requestBody["lastName"];
			delete requestBody["email"];
			requestBody["password"] = passwords[0].value;
		}
		loading(false);
		const request = await fetch("/rest_api/sign" + { true: "up", false: "in" }[register], {
			method: "POST",
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
			body: JSON.stringify({ "username": username.value, password1: passwords[0].value, password2: passwords[1].value, firstName: names[0].value, lastName: names[1].value, email: email.value })
		}).catch(e => {
			signIn(register, requestBody["username"]);
			if (register) {
				alert("Failed to register your account.");
			} else {
				alert("Failed to sign in to your account.");
			}
		});
		const content = await request.json();
		console.log(content);
	});
	loading(true);
	document.getElementById("main").appendChild(signInContainer);
};

const getResortByID = async (id) => {
	const resorts = await getResorts();
	if (resorts[1] != 0) {
		return null;
	}
	for (let i = 0; i < resorts[0].length; i++) {
		const resort = resorts[0][i];
		if (resort["id"] == id) {
			return resort;
		}
	}
	return null;
};

const getResorts = async () => {
	let resorts = null;
	if (!demo) {
		const request = await fetch("/rest_api/resort/", {
			method: "GET",
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
			body: null
		}).then(async r => {
			resorts = await r.json();
		}).catch(e => {
			resorts = 0;
		});
		if (typeof resorts == "number") {
			return [null, 1];
		}
		if (Array.isArray(resorts) && resorts.length == 0) {
			return [null, 2];
		}
	} else {
		resorts = [{ id: 333031, name: "Saint Martin De Belleville", longitude: 6.504810, latitude: 45.379800, description: "The Alpine area of Saint-Martin-de-Belleville is known for its charming namesake village, with traditional stone-and-wood farmhouses, plus a handful of Savoyard restaurants and ski rental shops.", image: "/images/Saint-Martin-de-Belleville-ski-resort-French-Alps-1920.jpg" }, { id: 333005, name: "Courchevel", longitude: 6.637370, latitude: 45.434330, description: "Courchevel is a French Alps ski resort. It is a part of Les Trois Vallées, the largest linked ski areas in the world. Courchevel also refers to the towns of Courchevel 1300, Courchevel 1550, Courchevel 1650, and Courchevel 1850, which are named for their altitudes in metres.", image: "/images/courchevel.jpg" }, { id: 333014, name: "Meribel", longitude: 6.566170, latitude: 45.396549, description: "Méribel is a ski resort in the French Alps. Méribel refers to three neighbouring villages in the Les Allues commune of the Savoie department of France, near the town of Moûtiers, called Méribel Centre, Méribel-Mottaret and Méribel Village.", image: "/images/Meribel.png" }]
	}
	for (let i = 0; i < resorts.length; i++) {
		resorts[i]["image"] = resorts[i]["image"] || "/images/skiing.jpg";
		resorts[i]["isFavourite"] = false; // Call API
	}
	return [resorts, 0];
};

const createNewResort = async (update, name, description, longitude, latitude, image) => {
	let error = false;
	const request = await fetch("/rest_api/resort/", {
		method: { false: "POST", true: "PUT" }[update],
		headers: {
			"Accept": "application/json",
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ "name": name, "description": description, "longitude": longitude, "latitude": latitude, "image": image})
	}).catch(e => {
		console.error(e);
		error = true;
	});
	if (error) {
		return null;
	}
	return await request.json();
};

const createNewResortPage = () => {
	// name, address, lon, lat, description
	document.title = "Create new resort | Snowcore";
	const createResortContainer = document.createElement("form");
	addClasses(createResortContainer, ["container", "w-full", "mx-auto"]);
	const name = document.createElement("input");
	const lonLat = [document.createElement("input"), document.createElement("input")];
	lonLat[0].type = "number";
	lonLat[0].max = "90.0000000";
	lonLat[0].min = "-90.0000000";
	lonLat[1].type = "number";
	lonLat[1].max = "180.0000000";
	lonLat[1].min = "-180.0000000";
	const description = document.createElement("textarea");
	description.style.resize = "none";
	addClasses(name, ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(lonLat[0], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(lonLat[1], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(description, ["rounded-md", "border-black", "border", "block", "mx-auto", "h-36", "px-2", "w-64"]);
	name.setAttribute("required", "required");
	lonLat[0].setAttribute("required", "required");
	lonLat[1].setAttribute("required", "required");
	description.setAttribute("required", "required");
	const tips = [document.createElement("p"), document.createElement("p"), document.createElement("p"), document.createElement("p")];
	tips[0].innerText = "Resort name:";
	addClasses(tips[0], ["block", "text-center", "select-none"]);
	tips[1].innerText = "Longitude:";
	addClasses(tips[1], ["block", "text-center", "select-none"]);
	tips[2].innerText = "Latitude:";
	addClasses(tips[2], ["block", "text-center", "select-none"]);
	tips[3].innerText = "Description:";
	addClasses(tips[3], ["block", "text-center", "select-none"]);
	const submit = document.createElement("input");
	addClasses(submit, ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "mx-auto", "select-none"]);
	submit.type = "submit";
	submit.value = "Create resort";
	addClasses(tips[0], ["pt-12"]);
	createResortContainer.appendChild(tips[0]);
	createResortContainer.appendChild(name);
	createResortContainer.appendChild(tips[1]);
	createResortContainer.appendChild(lonLat[0]);
	createResortContainer.appendChild(tips[2]);
	createResortContainer.appendChild(lonLat[1]);
	createResortContainer.appendChild(tips[3]);
	createResortContainer.appendChild(description);
	createResortContainer.appendChild(submit);
	submit.addEventListener("click", async (e) => {
		e.preventDefault();
		if (name.value.length == 0 || lonLat[0].value.length == 0 || lonLat[1].value.length == 0 || description.value.length == 0) {
			alert("Please make sure you do not leave any field blank!");
			return;
		}
		loading(false, true);
		const response = await createNewResort(false, name.value, description.value, lonLat[0].value, lonLat[1].value, null);
		if (response != null && "pk" in response) {
			loading(false);
			pageId = 0;
			newPage(pageId);
			return;
		}
		document.getElementById("loaderMessage").outerHTML = "";
		alert("Failed to create resort!");
	});
	loading(true);
	let main = document.getElementById("main");
	main.appendChild(createResortContainer);
};

const newPage = async (pageId) => {
	loading(false);
	switch (pageId) {
		case 0:
			document.title = "Snowcore";
			let error = 0;
			let resorts = await getResorts();
			error = resorts[1];
			resorts = resorts[0];
			if (Array.isArray(resorts) && resorts.length == 0) {
				error = 2;
			}
			if (error > 0) {
				const loader = document.getElementById("loaderMessage");
				loader.classList.remove("cursor-wait");
				loader.classList.remove("pb-12");
				loader.classList.remove("pt-6");
				addClasses(loader, ["pt-12", "pb-10", "px-8"]);
				if (error == 1) {
					loader.innerText = "An error occurred when attempting to load up the resorts.";
				} else if (error == 2) {
					loader.innerText = "There are currently no resorts available to Snowcore users.";
				}
				break;
			}
			for (let i = 0; i < resorts.length; i++) {
				resorts[i]["image"] = resorts[i]["image"] || "/images/skiing.jpg";
				resorts[i]["isFavourite"] = false; // Call API
			}
			showResorts(resorts);
			break;
		case 1:
			signIn(false);
			break;
		case 2:
			signIn(true);
			break;
		default:
			const loader = document.getElementById("loaderMessage");
			loader.classList.remove("cursor-wait");
			loader.classList.remove("pb-12");
			loader.classList.remove("pt-6");
			addClasses(loader, ["pt-12", "pb-10"]);
			loader.innerText = "An unknown error occurred.";
			break;
	}
};

window.addEventListener('DOMContentLoaded', () => {
	if (typeof pageId === "undefined") {
		console.error("Invalid page ID");
	} else {
		newPage(pageId);
	}
	let userState = 0;
	document.getElementById("headerMain").addEventListener("click", () => {
		if (window.scrollY > 30) {
			window.scroll({
				top: 0,
				left: 0,
				behavior: "smooth"
			});
		} else {
			pageId = 0;
			newPage(pageId);
		}
	});
	document.getElementById("user").addEventListener("click", () => {
		pageId = (userState + 1);
		newPage(pageId);
	});
});