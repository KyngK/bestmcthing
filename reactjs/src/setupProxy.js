const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/' + process.env.SECRET_URL,
    createProxyMiddleware({
      target: 'http://127.0.0.1:8080',
      changeOrigin: true,
      headers: {
        "Connection": "keep-alive"
    },
    })
  );
};