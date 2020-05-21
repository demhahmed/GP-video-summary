const { createProxyMiddleware } = require("http-proxy-middleware");
module.exports = function (app) {
  app.use(
    "/auth/google",
    createProxyMiddleware({
      target: "http://localhost:3001",
    })
  );

  app.use(
    "/auth/local",
    createProxyMiddleware({
      target: "http://localhost:3001",
    })
  );

  app.use(
    "/api/*",
    createProxyMiddleware({
      target: "http://localhost:3001",
    })
  );
  app.use(
    "/logos/*",
    createProxyMiddleware({
      target: "http://localhost:3001",
    })
  );
};
