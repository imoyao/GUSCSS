var ImageminPlugin = require('imagemin-webpack-plugin').default
// 生产模式使用cdn
function getProdExternals () {
  return {
    vue: 'Vue',
    'vue-router': 'VueRouter',
  }
}
module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
  // 输出文件目录
  outputDir: 'docs',
  pwa: {
    themeColor: '#ffffff',
    msTileColor: '#ffffff',
    workboxOptions: {
      skipWaiting: true,
      clientsClaim: true,
    },
    iconPaths: {
      favicon32: 'img/icons/fuji-mountain-32x32.png',
      favicon16: 'img/icons/fuji-mountain-16x16.png',
      appleTouchIcon: 'img/icons/apple-touch-icon-152x152.png',
      maskIcon: 'img/icons/safari-pinned-tab.svg',
      msTileImage: 'img/icons/msapplication-icon-144x144.png',
    },
  },
  lintOnSave: process.env.NODE_ENV !== 'production',
  devServer: {
    overlay: {
      warnings: true,
      errors: true,
    },
  },
  configureWebpack: {
    // https://www.dongwm.com/post/optimize-vue-admin/
    // see also: https://www.cnblogs.com/xbzhu/p/11815197.html
    // see also: https://blog.csdn.net/qq_35844177/article/details/78599064
    externals: process.env.NODE_ENV === 'production'
      ? getProdExternals() : {},
    plugins: [
      new ImageminPlugin({
        disable: true, // Disable for windows
        // disable: process.env.NODE_ENV !== 'production', // Disable during development
        pngquant: {
          quality: '80',
        },
      }),
    ],
  },
  chainWebpack: config => {
    config.resolve.symlinks(true)
    config.plugin('preload').tap(options => {
      options[0] = {
        rel: 'preload',
        as (entry) {
          if (/\.css$/.test(entry)) return 'style'
          if (/\.(woff||ttf)$/.test(entry)) return 'font'
          if (/\.png$/.test(entry)) return 'image'
          return 'script'
        },
        include: 'allAssets',
        fileBlacklist: [ /\.map$/, /hot-update\.js$/ ],
      }
      return options
    })
    return config
  },
}
