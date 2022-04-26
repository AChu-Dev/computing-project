"use strict";

const addClasses = (element, classList) => {
	classList.forEach(className => {
		element.classList.add(className);
	});
}

const createResort = (id, name, image, isFavourite) => {
	const container = document.createElement("div");
	addClasses(container,["w-full","md:w-1/3","xl:w-1/4","p-6","flex","flex-col"]);
	const heroImage = document.createElement("img");
	heroImage.src = image || "images/skiing.jpg";
	addClasses(heroImage, ["hover:grow","hover:shadow-lg", "cursor-pointer"]);
	const containerFlex = document.createElement("div");
	addClasses(containerFlex, ["pt-3","flex","items-center","justify-between"]);
	const resortName = document.createElement("p");
	resortName.innerText = name;
	const favourite = document.createElement("svg");
	favourite.innerHTML = "<svg class=\"h-6 w-6 fill-current text-gray-500 hover:text-black\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z\" /></svg>";
	containerFlex.appendChild(resortName);
	containerFlex.appendChild(favourite);
	container.appendChild(heroImage);
	container.appendChild(containerFlex);
	return container;
}

const showResorts = async (resorts) => {
	const section = document.createElement("section");
	section.innerHTML = "Loading...";
	addClasses(section, ["bg-white","py-8"]);
	document.getElementById("main").appendChild(section);
	const container = document.createElement("div");
	addClasses(container, ["container","mx-auto","flex","items-center","flex-wrap","pt-4","pb-12"]);
	resorts.forEach(resort => {
		let test = createResort(resort["id"], resort["name"], resort["image"], resort["isFavourite"]);
		container.appendChild(test);
	});
	section.innerHTML = "";
	section.appendChild(container);
}

window.addEventListener('DOMContentLoaded', () => {
	if (typeof pageId === "undefined") {
		console.error("Invalid page ID");
	} else {
		switch (pageId) {
			case 0:
				showResorts([{"id":0,"name":"name","image":null,"isFavourite":true}, {"id":0,"name":"name","image":null,"isFavourite":true}, {"id":0,"name":"name","image":null,"isFavourite":true}, {"id":0,"name":"name","image":null,"isFavourite":true},{"id":0,"name":"name","image":null,"isFavourite":true}, {"id":0,"name":"name","image":null,"isFavourite":true}, {"id":0,"name":"name","image":null,"isFavourite":true}, {"id":0,"name":"name","image":null,"isFavourite":true}]);
				break;	
			default:
				break;
		}
	}
});