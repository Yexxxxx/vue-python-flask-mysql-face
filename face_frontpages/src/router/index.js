import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import index from '../views/index.vue'
import TEST from '../views/TEST.vue'
import Table_client_data from '../views/Table_client_data.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/Home',
    name: 'Home',
    component: Home,
    children:[
      {
        path: '/',
        name: '/index',
        component: index,
      },
      {
        path: '/Table_client_data',
        name: 'Table_client_data',
        component: Table_client_data,
      },
    ]
  },
  {
    path: '/Login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/TEST',
    name: 'TEST',
    component: TEST,
  },
]

const router = new VueRouter({
  routes
})

export default router
