import Vue from 'vue'
import VueRouter from 'vue-router'

import VueSelect from 'vue-cool-select'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import App from './App.vue'
import HelloWorld from './components/HelloWorld.vue'
import DocIncomeList from './components/DocIncomeList.vue'
import DocIncomeItem from './components/DocIncomeItem.vue'
import CatlgDeviceList from './components/CatlgDeviceList.vue'

Vue.use(VueRouter)
Vue.config.productionTip = false
Vue.use(VueSelect, {
  theme: 'bootstrap' // or 'material-design'
})
Vue.use(BootstrapVue)

const routes = [
  { 
    path: '/',
    name: 'home', 
    component: HelloWorld 
  },
  { 
    path: '/docincome',
    name: 'docincome.list', 
    component: DocIncomeList 
  },
  { 
    path: '/docincome/:id',
    name: 'docincome.item',
    props: (route) => ({ id: Number(route.params.id) }),
    component: DocIncomeItem
  },
  { 
    path: '/catlg/device',
    name: 'catlg.device.list', 
    component: CatlgDeviceList 
  },

]

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes // короткая форма для routes: routes
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
