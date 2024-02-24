// Add a click event listener to a parent element
document.addEventListener('click', function (event) {
	// select datepicker modal
	const parentElement = document.querySelector('div.datepicker-picker');
	// select all children elements
	const darkTextWhite = parentElement.querySelectorAll('*');

	// Iterate over each span tag and update its class
	darkTextWhite.forEach(function (element) {
		// console.log(spanTag);
		if (element.classList.contains('dark:text-white')) {
			// Remove the text-white class and add the text-gray-900 class
			element.classList.remove('dark:text-white');
			element.classList.add('text-gray-900');
		}
	});

	// remove flex class with dynamically generated grid
	monthsGrid = parentElement.querySelector('div.months');
	monthsGrid.classList.remove('flex');
	yearsGrid = parentElement.querySelector('div.years');
	yearsGrid.classList.remove('flex');
});
