"use strict";

const prepend = "/";

if ("serviceWorker" in navigator) {
	window.addEventListener("load", () => {
		navigator.serviceWorker
			.register("sw.js")
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
	addClasses(main, ["mb-6", "flex-auto"]);
	main.innerHTML = "";
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
	addClasses(heroImage, ["container", "w-full", "mx-auto", "h-96", "bg-cover", "bg-center", "bg-no-repeat", "relative", "mb-12", "rounded-t-2xl", "mt-6", "select-none"]);
	const weatherIcon = document.createElement("div");
	addClasses(weatherIcon, ["w-24", "h-24", "rounded-full", "bg-white", "bg-no-repeat", "bg-contain", "bg-center", "mx-auto", "absolute", "inset-x-0", "select-none"]);
	weatherIcon.style.bottom = "-48px";
	weatherIcon.style.backgroundImage = "url(\"" + prepend + "icons/" + weatherImage + "\")";
	weatherIcon.title = "Current weather of resort";
	heroImage.append(weatherIcon);
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["flex", "items-center", "px-8", "mb-8", "justify-center", "select-none"]);
	const resortName = document.createElement("h2");
	resortName.innerText = name;
	addClasses(resortName, ["container", "px-8", "text-center", "text-4xl", "pb-2", "mx-auto", "select-none"]);
	const favourite = document.createElement("svg");
	favourite.innerHTML = "<svg class=\"ml-2 h-6 w-6 fill-current text-gray-500 hover:text-black\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	let descriptions = resortDescription.split("\n");
	loading(true);
	let mapLink = document.createElement("a");
	addClasses(mapLink, ["px-8", "pb-6", "underline", "text-center", "text-blue-600", "hover:text-blue-800", "visited:text-purple-600", "container", "mx-auto", "w-full", "flex", "justify-center", "cursor-pointer", "select-none"]);
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
		addClasses(descriptionParagraph, ["px-8", "text-justify", "pb-6", "container", "mx-auto", "select-none"]);
		if (top) {
			addClasses(descriptionParagraph, ["mt-8"]);
		}
		main.appendChild(descriptionParagraph);
		top = false;
	});
	let historicWeather = document.createElement("img");
	historicWeather.src = prepend + "historic_weather_2021.png";
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
	addClasses(names[0], ["rounded-md", "border-black", "border", "block", "mx-auto"]);
	addClasses(names[1], ["rounded-md", "border-black", "border", "block", "mx-auto"]);
	addClasses(email, ["rounded-md", "border-black", "border", "block", "mx-auto"]);
	addClasses(username, ["rounded-md", "border-black", "border", "block", "mx-auto"]);
	addClasses(passwords[0], ["rounded-md", "border-black", "border", "block", "mx-auto"]);
	addClasses(passwords[1], ["rounded-md", "border-black", "border", "block", "mx-auto"]);
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
	submit.value = {true:"Register",false:"Sign in"}[register];
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
		let requestBody = {"username": username.value, password1: passwords[0].value, password2: passwords[1].value, firstName: names[0].value, lastName: names[1].value, email: email.value};
		if (!register) {
			delete requestBody["password1"];
			delete requestBody["password2"];
			delete requestBody["firstName"];
			delete requestBody["lastName"];
			delete requestBody["email"];
			requestBody["password"] = passwords[0].value;
		}
		loading(false);
		const request = await fetch("/rest_api/sign" + {true:"up",false:"in"}[register], {
			method: 'POST',
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json"
			},
			body: JSON.stringify({"username": username.value, password1: passwords[0].value, password2: passwords[1].value, firstName: names[0].value, lastName: names[1].value, email: email.value})
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

const newPage = async (pageId) => {
	loading(false);
	switch (pageId) {
		case 0:
			document.title = "Snowcore";
			let error = 0;
			let resorts = null;
			const request = await fetch("/rest_api/resort/list", {
				method: 'POST',
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
				body: null
			}).then(async r => {
				resorts = await r.json();
			}).catch(e => {
				error = 1;
			});
			if (Array.isArray(resorts) && resorts.length == 0) {
				error = 2;
			}
			if (error > 0) {
				const loader = document.getElementById("loaderMessage");
				loader.classList.remove("cursor-wait");
				loader.classList.remove("pb-12");
				loader.classList.remove("pt-6");
				addClasses(loader, ["pt-12", "pb-10"]);
				if (error == 1) {
					loader.innerText = "An error occurred when attempting to load up the resorts.";
				} else if (error == 2) {
					loader.innerText = "There are currently no resorts available to Snowcore users.";
				}
				break;
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
	addClasses(document.getElementById("main"), ["flex-auto"]);
	if (typeof pageId === "undefined") {
		console.error("Invalid page ID");
	} else {
		newPage(pageId);
	}
	let userState = 0;
	document.getElementById("headerMain").addEventListener("click", () => {
		pageId = 0;
		newPage(pageId);
	});
	document.getElementById("user").addEventListener("click", () => {
		pageId = (userState + 1);
		newPage(pageId);
	});
});