import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'

//import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
//Vue.use(Vuetify, {
//  iconfont: 'md'
//})

//require("selectize/dist/css/selectize.bootstrap3.css");
//require("vue-bootstrap-typeahead/dist/VueBootstrapTypeahead.css");

import VueSelect from 'vue-cool-select'
 
Vue.use(VueSelect, {
  theme: 'bootstrap' // or 'material-design'
})


import Autocomplete from 'v-autocomplete'

// You need a specific loader for CSS files like https://github.com/webpack/css-loader
import 'v-autocomplete/dist/v-autocomplete.css'

Vue.use(Autocomplete)


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
