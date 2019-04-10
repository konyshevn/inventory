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
          var catlgReady = response.data.map(function(item){
            item.label = vm.getCatlgLabel(catlgType, item)
            return item
          })
          Vue.set(vm.catlgs, catlgType, response.data);
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
        var item = id; //не число, значит передан объект
      } else {
        var item = vm.getCatlgItem(catlgName, id); //число, значит передано id 
      }
      switch(catlgName){
        case 'device':
          var devicetype = vm.getCatlgItem('devicetype', item['device_type'])['name'];
          var nomenclature = vm.getCatlgItem('nomenclature', item['name'])['name'];
          label = devicetype + ' ' + nomenclature;
          break;

        case 'person':
          label = item['surname'] + ' ' + item['name'];
          break;

        case 'department':
          label = item['name'];
          break;

        case 'stock':
          label = item['name'];
          break;
      }
      return label;
    },

    addCatlgLabel: function (){
      var vm = this;
      console.log(vm.catlgs['device']);
      for (var catlg in vm.catlgs){
        //console.log(catlg);
        //console.log(vm.catlgs[catlg]);
        /*
        var labeledCatlg = vm.catlgs[catlg].map(function (catlgItem) {
            catlgItem.label = vm.getCatlgLabel(catlg, catlgItem['id'])
            console.log(catlgItem)
            return catlgItem
          })
        */
        //console.log(labeledCatlg);
        //vm.catlgs[catlg] = labeledCatlg;
      }
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