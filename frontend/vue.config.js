// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true,
//   lintOnSave:false
// })
module.exports = {
  devServer: {
      proxy: {
          '/api': {
              target: `http://127.0.0.1:8000/api`,
              changeOrigin: true,
              pathRewrite: {
                  '^/api': ''
              }
          }
      }
  },
  lintOnSave: false,
};