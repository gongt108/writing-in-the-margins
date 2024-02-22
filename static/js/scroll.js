// scroll.js
document.addEventListener('DOMContentLoaded', function () {
	const scrollToBottomBtn = document.getElementById('scroll-to-bottom-btn');

	scrollToBottomBtn.addEventListener('click', function () {
		window.scrollTo({
			top: document.body.scrollHeight,
			behavior: 'smooth',
		});
	});
});
