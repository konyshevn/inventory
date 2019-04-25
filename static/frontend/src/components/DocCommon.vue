<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
import CatlgCommon from './CatlgCommon.vue';
var _ = require('lodash');

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

    getDocItem: function (docType, id) {
      var vm = this;
      HTTP.get(docType + '/' + id + '/')
        .then(function (response) {
          Vue.set(vm.doc, docType, response.data);
        })
    },
     

  },

  mounted: function () {
  }
}
</script>