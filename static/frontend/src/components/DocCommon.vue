<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
import CatlgCommon from './CatlgCommon.vue';
var _ = require('lodash');
import {EventBus} from './event-bus.js'
import moment from 'moment';

export default {
  name: 'DocCommon',
  mixins: [CatlgCommon],
  props: {
    //msg: String
  },
  data () {
    return {
      doc: {
        'docincome': {},
        'docwriteoff': {},
        'docmove': {},
        'docinventory': {},
      },
      docs: {
        'docincome': [],
        'docwriteoff': [],
        'docmove': [],
        'docinventory': [],
      },
    }
  },

  methods: {
    fetchDocs: function (docType) {
      var vm = this;
      HTTP.get(docType + '/')
        .then(function (response) {
          var DocsReady = response.data
          Vue.set(vm.docs, docType, DocsReady);
          for (var key in DocsReady[0]){
            if (key in vm.catlgs) {
              var catlgToLoad = _.uniq(_.map(DocsReady, _.property(key)))
              catlgToLoad = catlgToLoad.filter(function (el) {
                return el != null;
              });

              vm.fetchCatlgItem(key, catlgToLoad)
            }
          }
        })
    },

    async getDocItem (docType, id) {
      var vm = this;
      var response = await HTTP.get(docType + '/' + id + '/')
//      response.data.doc_date = moment(String(response.data.doc_date)).format('MM.DD.YYYY hh:mm:ss')
      vm.fetchWidgetInitCatlg(response.data['table_unit'], {'device': 'device', 'person': 'person'})
      Vue.set(vm.doc, docType, response.data);
          //EventBus.$emit('widgetInitCatlg', vm.catlgs)
        
    },
     

  },

  mounted: function () {
  }
}
</script>