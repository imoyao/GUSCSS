import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import ElementUI from 'element-ui'

import 'normalize.css'
import 'element-ui/lib/theme-chalk/index.css'
import './registerServiceWorker'
import './global.scss'
import './assets/fonts/font.css'

import commons from './commons.js'

Vue.prototype.common = commons
Vue.config.productionTip = false

// Vue.use(ElementUI)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
