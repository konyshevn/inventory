<template>
  <div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import {HTTP} from '../http-common'
var _ = require('lodash');

export default {
  name: 'CatlgCommon',
  props: {
    //msg: String
  },
  data () {
    return {
    }
  },
  methods: {
    fetchCatlg: function(catlgType){
      var vm = this;
      HTTP.get(catlgType + '/')
        .then(function (response) {
          vm.catlgs[catlgType] = response.data;
        }) 
    },

    getCatlgItem: function (id, catlgType) {
      var vm = this;
      if (id === null) {
        return "";
      }
      var catlgItem = _.find(vm.catlgs[catlgType], function(item){ return item['id'] == id });
      return catlgItem
    },

    getCatlgLabel: function(id, catlgName){
      var vm = this;
      var label = "unknown";
      var item = vm.getCatlgItem(id, catlgName);
      switch(catlgName){
        case 'device':
          var devicetype = vm.getCatlgItem(item['device_type'], 'devicetype')['name'];
          var nomenclature = vm.getCatlgItem(item['name'], 'nomenclature')['name'];
          label = devicetype + ' ' + nomenclature;
          break;

        case 'person':
          label = item['surname'] + ' ' + item['name'];
          break;
          
        case 'department':
          label = item['name'];
          break;
      }
      return label;
    },
     
  },
  mounted: function () {
  }
}
</script>