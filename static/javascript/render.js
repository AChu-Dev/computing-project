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

let user = { id: null, admin: false, token: null};

let weather = null;

let weatherCache = [new Date(0, 0, 0, 0, 0, 0, 0), []];

const weatherInterval = 6;

const alert = async (title = "", message, type = "", button = "Close") => {
	document.body.style.overflowY = "hidden";
	setTimeout(() => {
		document.getElementsByClassName("swal-overlay")[0].scrollTo(0, 0);
	}, 1);
	await swal({title: title, text: message, icon: type, button: button});
	document.body.style.overflowY = "unset";
};

const getWeather = async (resortId) => {
	const urls = [
		{
			"id": 1,
			"url": "https://api.weatherunlocked.com/api/resortforecast/333031?app_id=a3fd6c9a&app_key=027a1023047a432b9ed2e4a7db484a07&hourly_interval=" + weatherInterval
		},
		{
			"id": 2,
			"url": "https://api.weatherunlocked.com/api/resortforecast/333005?app_id=4c84c18d&app_key=5f4b7efa21bbda9d00d158c7c11ac815&hourly_interval=" + weatherInterval
		},
		{
			"id": 3,
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
				const currentDate = ("0" + new Date().getDate()).slice(-2) + "/" + ("0" + (new Date().getMonth() + 1)).slice(-2) + "/" + new Date().getFullYear();
				const currentTime = new Date(0,0,0,new Date().getHours(),new Date().getMinutes(),0,0);
				while (weatherCached["weather"]["forecast"][0]["date"] == currentDate) {
					const weatherTime = new Date(0,0,0,weatherCached["weather"]["forecast"][0]["time"].split(":")[0],weatherCached["weather"]["forecast"][0]["time"].split(":")[1],0,0);
					if (currentTime > weatherTime) {
						weatherCached["weather"]["forecast"].shift();
					} else {
						break;
					}
				}
				if (weatherCached["weather"]["forecast"].length < 10) {
					return;
				}
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

const userSignedIn = () => {
	const userIcon = document.getElementById("user");
	if (user["id"] !== null) {
		userIcon.title = "Menu";
	} else {
		userIcon.title = "Sign in";
	}
}

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

const setFavourite = (element) => {
	if (!element.hasAttribute("state")) {
		element.setAttribute("state", "0");
	}
	let state = (element.getAttribute("state") != "0");
	if (state) {
		element.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	} else {
		element.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black\" width=\"24\" height=\"24\" xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" clip-rule=\"evenodd\"><path d=\"M12 21.593c-5.63-5.539-11-10.297-11-14.402 0-3.791 3.068-5.191 5.281-5.191 1.312 0 4.151.501 5.719 4.457 1.59-3.968 4.464-4.447 5.726-4.447 2.54 0 5.274 1.621 5.274 5.181 0 4.069-5.136 8.625-11 14.402m5.726-20.583c-2.203 0-4.446 1.042-5.726 3.238-1.285-2.206-3.522-3.248-5.719-3.248-3.183 0-6.281 2.187-6.281 6.191 0 4.661 5.571 9.429 12 15.809 6.43-6.38 12-11.148 12-15.809 0-4.011-3.095-6.181-6.274-6.181\"/></svg>";
	}
	state = !state;
	element.setAttribute("state", (state ? "1" : "0"));
	return state;
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
	addClasses(resortName, ["text-ellipsis", "overflow-hidden"]);
	resortName.style.lineHeight = "2ch";
	resortName.style.maxHeight = "2ch";
	let favourite = null;
	if (user["id"] != null) {
		favourite = document.createElement("svg");
		setFavourite(favourite);
		if (isFavourite != 0) {
			setFavourite(favourite);
		}
		favourite.addEventListener("click", async () => {
			const newFavourite = !setFavourite(favourite);
			const favouriteId = await favouriteResort(newFavourite, id, isFavourite);
			if (newFavourite) {
				isFavourite = favouriteId;
			}
		});
	}
	heroImage.addEventListener("click", () => {
		showResort(id);
	});
	resortName.addEventListener("click", () => {
		showResort(id);
	});
	containerFlex.appendChild(resortName);
	if (user["id"] != null) {
		containerFlex.appendChild(favourite);
	}
	container.appendChild(heroImage);
	container.appendChild(containerFlex);
	container.title = "View " + name;
	return container;
};

const showResorts = async (resorts) => {
	const section = document.createElement("section");
	section.innerHTML = "Loading...";
	addClasses(section, ["bg-white", "pb-8"]);
	const container = document.createElement("div");
	addClasses(container, ["container", "mx-auto", "flex", "items-center", "flex-wrap", "pt-4", "pb-12"]);
	resorts.forEach(resort => {
		let resortRender = createResort(resort["pk"], resort["name"], resort["image"], resort["isFavourite"]);
		container.appendChild(resortRender);
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
			alert("Weather forecast for the next " + (weather[2].length * weatherInterval) + " hours:", weather[2].join("\n"));
		});
		heroImage.append(weatherIcon);
	}
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["flex", "items-center", "px-8", "mb-8", "justify-center", "select-none"]);
	const resortName = document.createElement("h2");
	resortName.innerText = name;
	addClasses(resortName, ["container", "px-8", "text-center", "text-4xl", "pb-2", "ml-2", "mx-auto", "select-none"]);
	let favourite = null;
	if (user["id"] != null) {
		let isFavourite = 0;
		const favourites = await getFavourites();
		favourites.forEach(favouriteData => {
			if (favouriteData[0] == resort["pk"]) {
				isFavourite = favouriteData[1];
			}
		});
		favourite = document.createElement("svg");
		addClasses(favourite, ["pl-2"])
		setFavourite(favourite);
		if (isFavourite != 0) {
			setFavourite(favourite);
		}
		favourite.addEventListener("click", async () => {
			const newFavourite = !setFavourite(favourite);
			const favouriteId = await favouriteResort(newFavourite, resort["pk"], isFavourite);
			const counter = document.getElementById("resortFavouriteCount");
			if (newFavourite) {
				isFavourite = favouriteId;
				counter.innerText = (parseInt(counter.innerText) + 1);
			} else {
				counter.innerText = (parseInt(counter.innerText) - 1);
			}
		});
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
	if (user["id"] != null) {
		containerFlex.appendChild(favourite);
	}
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

const signIn = (register, emailString = "") => {
	const signInContainer = document.createElement("form");
	addClasses(signInContainer, ["container", "w-full", "mx-auto"]);
	const username = document.createElement("input");
	const email = document.createElement("input");
	email.value = emailString;
	const passwords = [document.createElement("input"), document.createElement("input")];
	addClasses(username, ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(email, ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(passwords[0], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	addClasses(passwords[1], ["rounded-md", "border-black", "border", "block", "mx-auto", "px-2", "w-64"]);
	username.setAttribute("required", "required");
	email.setAttribute("required", "required");
	passwords[0].setAttribute("required", "required");
	passwords[1].setAttribute("required", "required");
	email.type = "email";
	passwords[0].type = "password";
	passwords[1].type = "password";
	const tips = [document.createElement("p"), document.createElement("p"), document.createElement("p"), document.createElement("p")];
	tips[0].innerText = "Email:";
	addClasses(tips[0], ["block", "text-center", "select-none", "pt-12"]);
	tips[1].innerText = "Username:";
	addClasses(tips[1], ["block", "text-center", "select-none"]);
	tips[2].innerText = "Password:";
	addClasses(tips[2], ["block", "text-center", "select-none"]);
	tips[3].innerText = "Repeat password:";
	addClasses(tips[3], ["block", "text-center", "select-none"]);
	const submit = document.createElement("input");
	addClasses(submit, ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "mx-auto", "w-64", "select-none"]);
	submit.type = "submit";
	submit.value = { true: "Register", false: "Sign in" }[register];
	if (register) {
		document.title = "Sign up | Snowcore";
		signInContainer.appendChild(tips[0]);
		signInContainer.appendChild(email);
		signInContainer.appendChild(tips[1]);
		signInContainer.appendChild(username);
		signInContainer.appendChild(tips[2]);
		signInContainer.appendChild(passwords[0]);
		signInContainer.appendChild(tips[3]);
		signInContainer.appendChild(passwords[1]);
		signInContainer.appendChild(submit);
	} else {
		document.title = "Sign in | Snowcore";
		addClasses(tips[1], ["pt-12"]);
		signInContainer.appendChild(tips[1]);
		signInContainer.appendChild(username);
		signInContainer.appendChild(tips[2]);
		signInContainer.appendChild(passwords[0]);
		signInContainer.appendChild(submit);
		const register = document.createElement("input");
		addClasses(register, ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "mx-auto", "w-64", "select-none"]);
		register.type = "button";
		register.value = "Register?";
		register.addEventListener("click", () => {
			signIn(true, email.value);
		});
		signInContainer.appendChild(register);
	}
	signInContainer.addEventListener("submit", async (e) => {
		e.preventDefault();
		let requestBody = { password: passwords[0].value, username: username.value};
		if (register) {
			if (!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))) {
				alert("Wait a second", "That email address is invalid!", "warning");
				return;
			}
			requestBody["email"] = email.value;
			if (passwords[0].value != passwords[1].value || passwords[0].value.length == 0) {
				alert("Wait a second", "Please make sure both passwords match and are not blank.", "warning");
				return;
			}
		}
		loading(false);
		const request = await fetch("/rest_api/" + {true: "register", false: "api-token-auth"}[register] + "/", {
			method: "POST",
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
			body: JSON.stringify(requestBody)
		}).catch(e => {
			signIn(register, requestBody["username"]);
			if (register) {
				alert("", "Failed to register your account.", "error");
			} else {
				alert("", "Failed to sign in to your account.", "error");
			}
		});
		const content = await request.json();
		if ("user" in content) {
			let error = false;
			if (register) {
				alert("Success", "Your account has successfully been created.", "success", "Continue");
			}
			const request2 = await fetch("/rest_api/duser/list/", {
				method: "GET",
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
			}).catch(e => {
				console.error(e);
				error = true;
			});
			if (error) {
				return null;
			}
			const usersList = await request2.json();
			const request3 = await fetch("/rest_api/superuser/" + usersList.length + "/", {
				method: "GET",
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
			}).catch(e => {
				console.error(e);
				error = true;
			});
			if (error) {
				return null;
			}
			const userDetails = await request3.json();
			user["id"] = userDetails["id"];
			user["admin"] = userDetails["is_superuser"];
			pageId = 0;
			newPage(0);
			return;
		} else if ("username" in content) {
			alert("Error", content["username"].join("\n"), "error");
		} else if (register){
			alert("Error", "Failed to create user!", "error");
		} else {
			alert("Error", "Failed to sign in, please check your credentials!", "error");
		}
		loading(true);
		signIn(register);
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
		if (resort["pk"] == id) {
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
		resorts = [{ pk: 1, name: "Saint Martin De Belleville", longitude: 6.504810, latitude: 45.379800, description: "The Alpine area of Saint-Martin-de-Belleville is known for its charming namesake village, with traditional stone-and-wood farmhouses, plus a handful of Savoyard restaurants and ski rental shops.", image: "/images/Saint-Martin-de-Belleville-ski-resort-French-Alps-1920.jpg" }, { pk: 2, name: "Courchevel", longitude: 6.637370, latitude: 45.434330, description: "Courchevel is a French Alps ski resort. It is a part of Les Trois Vallées, the largest linked ski areas in the world. Courchevel also refers to the towns of Courchevel 1300, Courchevel 1550, Courchevel 1650, and Courchevel 1850, which are named for their altitudes in metres.", image: "/images/courchevel.jpg" }, { pk: 3, name: "Méribel", longitude: 6.566170, latitude: 45.396549, description: "Méribel is a ski resort in the French Alps. Méribel refers to three neighbouring villages in the Les Allues commune of the Savoie department of France, near the town of Moûtiers, called Méribel Centre, Méribel-Mottaret and Méribel Village.", image: "/images/Meribel.png" }]
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
		body: JSON.stringify({ "name": name, "description": description, "longitude": longitude, "latitude": latitude, "image": image })
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
	addClasses(submit, ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "mx-auto", "w-64", "select-none"]);
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
			alert("","Please make sure you do not leave any field blank!", "warning");
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
		alert("Error", "Failed to create resort!", "error");
	});
	loading(true);
	let main = document.getElementById("main");
	main.appendChild(createResortContainer);
};

const getFavourites = async () => {
	let favourites = [];
	if (user["id"] === null) {
		return favourites;
	}
	let error = false;
	const request = await fetch("/rest_api/favourite/list/user/?pk=" + user["id"], {
		method: "GET",
		headers: {
			"Accept": "application/json",
			"Content-Type": "application/json"
		},
	}).catch(e => {
		console.error(e);
		error = true;
	});
	if (error) {
		return favourites;
	}
	const response = await request.json();
	response.forEach(favourite => {
		favourites.push([favourite["resort_id"], favourite["pk"]]);
	});
	return favourites;
}

const favouriteResort = async (favourite, resortId, favouriteId = "") => {
	if (user["id"] === null) {
		return;
	}
	if (favourite) {
		favouriteId = "";
	} else if (favouriteId != "") {
		favouriteId = favouriteId + "/";
	}
	let error = false;
	const requestBody = {"resort_id": resortId, "user_id": user["id"]};
	const request = await fetch("/rest_api/favourite/" + favouriteId, {
		method: {true: "POST", false: "DELETE"}[favourite],
		headers: {
			"Accept": "application/json",
			"Content-Type": "application/json"
		},
		body: JSON.stringify(requestBody),
	}).catch(e => {
		console.error(e);
		error = true;
	});
	if (!favourite) {
		return null;
	} else if (error) {
		return 0;
	}
	const response = await request.json();
	return response["pk"];
};

const listUsers = async () => {
	loading(false);
	let error = false;
	const request = await fetch("/rest_api/duser/list/", {
		method: "GET",
		headers: {
			"Accept": "application/json",
			"Content-Type": "application/json"
		},
	}).catch(e => {
		console.error(e);
		error = true;
	});
	if (error) {
		return null;
	}
	const users = await request.json();
	if (pageId != 5) {
		return;
	}
	loading(true);
	let main = document.getElementById("main");
	let total = document.createElement("p");
	total.innerText = "There are " + users.length + " registered users" + {true: ":", false: "."}[users.length > 0];
	addClasses(total, ["block", "text-center", "select-none", "pt-12", "mb-2", "font-bold"]);
	main.appendChild(total);
	users.forEach(userData => {
		let userDataPara = document.createElement("p");
		userDataPara.innerText = userData["username"];
		addClasses(userDataPara, ["block", "text-center", "pt-2"]);
		main.appendChild(userDataPara);
	});
	document.title = "List of users | Snowcore";
};

const userMenu = (admin) => {
	loading(false);
	const links = [document.createElement("button"), document.createElement("button"), document.createElement("button"), document.createElement("button"), document.createElement("button")];
	links[0].innerText = "Create resort";
	links[0].addEventListener("click", () => {
		pageId = 3;
		newPage(pageId);
	});
	links[1].innerText = "List of users";
	links[1].addEventListener("click", () => {
		pageId = 5;
		newPage(pageId);
	});
	links[2].innerText = "List of favourites";
	links[2].addEventListener("click", () => {
		pageId = 6;
		newPage(pageId);
	});
	links[3].innerText = "Resorts";
	links[3].addEventListener("click", () => {
		pageId = 0;
		newPage(pageId);
	});
	links[4].innerText = "Sign out";
	links[4].addEventListener("click", () => {
		loading(false);
		user["id"] = null;
		user["admin"] = false;
		pageId = 0;
		newPage(pageId);
	});
	if (!admin) {
		admin = 3;
	} else {
		admin = 0;
	}
	loading(true);
	let main = document.getElementById("main");
	for (let i = admin; i < 5; i++) {
		addClasses(links[i], ["rounded-md", "block", "my-4", "p-2", "cursor-pointer", "bg-sky-500", "hover:bg-sky-700", "px-5", "py-2", "text-sm", "leading-5", "rounded-full", "font-semibold", "text-white", "w-64", "mx-auto", "select-none"]);
		main.appendChild(links[i]);
	}
	document.title = "Menu | Snowcore";
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
			const favourites = await getFavourites();
			for (let i = 0; i < resorts.length; i++) {
				resorts[i]["image"] = resorts[i]["image"] || "/images/skiing.jpg";
				resorts[i]["isFavourite"] = 0;
				favourites.forEach(favourite => {
					if (resorts[i]["pk"] == favourite[0]) {
						resorts[i]["isFavourite"] = favourite[1];
					}
				});
			}
			showResorts(resorts);
			break;
		case 1:
			signIn(false);
			break;
		case 2:
			userMenu(user["admin"] || false);
			break;
		case 3:
			createNewResortPage(false);
			break;
		case 4:
			createNewResortPage(false);
			break;
		case 5:
			listUsers();
			break;
		case 6:
			alert("Unimplemented", "Sorry, but this feature isn't implemented yet", "error");
			pageId = 2;
			newPage(pageId);
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

window.addEventListener('DOMContentLoaded', async () => {
	if (typeof pageId === "undefined") {
		console.error("Invalid page ID");
	} else {
		newPage(pageId);
	}
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
		if (user["id"] === null) {
			pageId = 1;
		} else {
			pageId = 2;
		}
		newPage(pageId);
	});
	userSignedIn();
});