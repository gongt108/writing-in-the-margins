console.log('hi');
window.addEventListener('load', () => {
	const loader = document.querySelector('.loader');
	console.log(loader);
	loader.classList.add('loader-hidden');
	loader.addEventListener('transitionend', () => {
		document.body.removeChild('loader');
	});
});
