const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/ba24d209-064f-41a9-bffc-f5050a574e16',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8080',
      changeOrigin: true,
      headers: {
        "Connection": "keep-alive"
    },
    })
  );
};