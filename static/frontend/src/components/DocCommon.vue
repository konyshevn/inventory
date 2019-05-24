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
      doc: {},
      docs: [],
    }
  },

  methods: {
    fetchDocs: function (docType) {
      var vm = this;
      HTTP.get(docType + '/')
        .then(function (response) {
          var DocsReady = response.data
          vm.docs = DocsReady
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
      vm.fetchWidgetInitCatlg(response.data['table_unit'], {'device': 'device', 'person': 'person'})
      vm.doc = response.data;
    },

    async regWriteDocItem (docType, item) {
      var vm = this;
      item.active = true
      try {
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        item.active = false
        console.log(error)
      }
    },

    async regDelDocItem (docType, item) {
      var vm = this;
      var itemStatus = item.active
      item.active = false
      try {
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        item.active = itemStatus
        console.log(error)
      }
    },

    async saveDocItem (docType, item) {
      var vm = this;
      try {
        var response = await HTTP.put(docType + '/' + item.id + '/', item)
      } catch(error) {
        console.log(error)
      }
    },

    async delDocItem (docType, item) {
      var vm = this;
      try {
        var response = await HTTP.delete(docType + '/' + item.id + '/')
      } catch(error) {
        console.log(error)
      }
    },
     
     

  },

  mounted: function () {
  }
}
</script>