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
      catlgs: {
        'department': [],
        'stock': [],
        'person': [],
        'device': [],
        'devicetype': [],
        'nomenclature': [],
      } 
    }
  },
  methods: {
    fetchCatlg: function(catlgType){
      var vm = this;
      HTTP.get(catlgType + '/')
        .then(function (response) {
          if ( !('label' in response.data[0])) {
            var catlgReady = response.data.map(function(item){
              item.label = vm.getCatlgLabel(catlgType, item)
              return item
            })
            catlgReady = _.orderBy(catlgReady, ['label'], ['asc'])
          } else {
            var catlgReady = response.data
            catlgReady = _.orderBy(catlgReady, ['label'], ['asc'])
          }
          Vue.set(vm.catlgs, catlgType, catlgReady);
        }) 
    },

    getCatlgItem: function (catlgType, id) {
      var vm = this;
      if (id === null) {
        return "";
      }
      var catlgItem = _.find(vm.catlgs[catlgType], function(item){ return item['id'] == id });
      return catlgItem
    },

    getCatlgLabel: function(catlgName, id){
      var vm = this;
      var label = "unknown";
      if (isNaN(id)){
        var catlgItem = id; //не число, значит передан объект
      } else {
        var catlgItem = vm.getCatlgItem(catlgName, id); //число, значит передано id 
      }
      switch(catlgName){
        case 'device':
          var devicetype = vm.getCatlgItem('devicetype', catlgItem['device_type'])['label'];
          var nomenclature = vm.getCatlgItem('nomenclature', catlgItem['name'])['label'];
          var serial_num = catlgItem['serial_num'] 
          label = devicetype + ' ' + nomenclature + ' (' + serial_num + ')';
          break;

        case 'person':
          label = catlgItem['surname'] + ' ' + catlgItem['name'];
          break;
      }
      return label;
    },

  },
  mounted: function () {
    this.fetchCatlg('department');
    this.fetchCatlg('stock');
    this.fetchCatlg('person');
    this.fetchCatlg('devicetype');
    this.fetchCatlg('nomenclature');
    this.fetchCatlg('device');
    //this.addCatlgLabel();
  }
  
}
</script>