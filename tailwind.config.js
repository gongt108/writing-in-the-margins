/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./django_tailwind_boilerplate/**/*.{html,js}',
		'./templates/**/*.{html,js}',
		'./components/**/*.{html,js}',
	],
	theme: {
		extend: {
			backgroundImage: {
				'home-page':
					"url('https://i.pinimg.com/originals/33/83/23/338323a53f478978f8605f69d7f8ca9e.jpg')",
			},
		},
	},
	variants: {
		extend: {
			backgroundColor: ['even'],
		},
	},
	plugins: [],
};
