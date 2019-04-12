import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'

import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
Vue.use(Vuetify, {
  iconfont: 'md'
})

require("selectize/dist/css/selectize.bootstrap3.css");


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
