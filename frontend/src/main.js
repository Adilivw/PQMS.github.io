import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './styles/index.scss'
import * as echarts from 'echarts'
import particles from 'particles.js'

Vue.use(ElementUI)
Vue.prototype.$echarts = echarts
Vue.prototype.$particles = particles

Vue.config.productionTip = false
Vue.config.errorHandler = (err, vm, info) => {
  console.error(err)
  ElementUI.Message.error('系统错误，请稍后重试')
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app') 