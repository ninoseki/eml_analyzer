module.exports = {
  outputDir: "dist",
  assetsDir: "static",
  devServer: {
    proxy: {
      "/api/*": {
        target: "http://localhost:8000/",
      },
      "/docs": {
        target: "http://localhost:8000/",
      },
      "/openapi.json": {
        target: "http://localhost:8000/",
      },
    },
  },
};
