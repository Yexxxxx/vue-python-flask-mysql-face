import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import './plugins/element.js'
import VueParticles from 'vue-particles'
import VueEllipseProgress from 'vue-ellipse-progress';
import VueSocketIO from 'vue-socket.io';
import SocketIO from "socket.io-client"









// axios.defaults.baseURL = 'http://127.0.0.1:5000/';
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
Vue.use(VueParticles)
// Vue.use(VueAxios,axios)
Vue.config.productionTip = false
Vue.use(VueResource)
Vue.use(VueRouter)
Vue.use(VueEllipseProgress);

// Vue.use(VueSocketIO, SocketIO('127.0.0.1:5000'));
Vue.use(new VueSocketIO({
  debug: true,
  connection:SocketIO('127.0.0.1:5000') ,
  autoConnect:false,
  vuex: {       // 不需要用到vuex这个可以不加
    store,
    actionPrefix: 'SOCKET_',
    mutationPrefix: 'SOCKET_'
  }

}))

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
