console.log('hi');
const loader = document.querySelector('.loader');

window.addEventListener('load', () => {
	loader.classList.add('loader-hidden');
	loader.addEventListener('transitionend', () => {
		document.body.removeChild(loader);
	});
});

window.addEventListener('click', function (event) {
	console.log(event.target.classList.contains('start-load'));
	// Check if the clicked element is a link
	if (event.target.classList.contains('start-load')) {
		// Do something when a link is clicked
		loader.classList.remove('loader-hidden');
		document.body.appendChild(loader);
	}
});
