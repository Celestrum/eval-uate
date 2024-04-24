import { defineConfig } from "vite";
import solid from "vite-plugin-solid";

export default defineConfig({
	plugins: [solid()],
	build: {
		// places the output in the templates folder in the backend
		outDir: "../backend/templates"
	}
});
