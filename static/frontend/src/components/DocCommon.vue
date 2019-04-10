<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
var _ = require('lodash');

export default {
  name: 'DocCommon',
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
      }
    }
  },

  methods: {
    fetchDocs: function (docType) {
      var vm = this;
      HTTP.get(docType + '/')
        .then(function (response) {
          // установить данные в vm
          var DocsReady = response.data.map(function (doc) {
            return doc
          })
          Vue.set(vm.docs, docType, DocsReady);
        });
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