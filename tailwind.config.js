module.exports = {
	// add daisyUI plugin
	plugins: [require("daisyui")],
	content: ["./templates/**/*.{html,js,ts}", "wishlist/templates/**/*.{html,js,ts}"],

	// daisyUI config (optional)
	daisyui: {
		themes: ['light', 'dark']
	}
};
