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
import DocItem from './components/DocItem.vue'
import DocList from './components/DocList.vue'
import CatlgDeviceList from './components/CatlgDeviceList.vue'
import {store} from './components/store';

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
    path: '/doc/:docType',
    name: 'doc.list',
    props: (route) => ({
      docType: String(route.params.docType),
    }),
    component: DocList 
  },
  { 
    path: '/doc/:docType/:id',
    name: 'doc.item',
    props: (route) => ({
      id: Number(route.params.id),
      docType: String(route.params.docType),
    }),
    component: DocItem
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
  store,
  render: h => h(App),
}).$mount('#app')
