import { defineConfig } from "tsup";

export default defineConfig((options) => ({
  entry: ["src/index.ts"],
  format: ["esm", "cjs"],
  dts: false, // Temporarily disabled until protoc is installed
  splitting: false,
  sourcemap: true,
  clean: !options.watch, // Don't clean in watch mode to prevent race conditions
  skipNodeModulesBundle: true
}));
