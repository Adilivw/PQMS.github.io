module.exports = {
  publicPath: process.env.NODE_ENV === 'production' 
    ? '/Adilivw.github.io/'
    : '/',
  outputDir: 'dist',
  assetsDir: 'static',
  productionSourceMap: false,
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  }
} 