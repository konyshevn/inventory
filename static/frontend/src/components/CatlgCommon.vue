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
      return myarr 
    },

    async fetchCatlgItem (catlgType, id) {
      var vm = this
      try {
        var response = await HTTP.get(catlgType + '/'+ id + '/')
        var catlgItemFetch = response.data
        
        /*       
        if ( !('label' in catlgItemFetch)) {
          catlgItemFetch.label = vm.getCatlgLabel(catlgType, catlgItemFetch)
        }    
       */
        var catlg_new = _.unionBy([catlgItemFetch], vm.catlgs[catlgType], 'id')
        vm.catlgs[catlgType] = catlg_new
      } catch(error) {
        console.log(error)
      }

    },

    getCatlgItem: function (catlgType, id) {
      var vm = this;
      //vm.fetchCatlgItem(catlgType, id)
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
    /*
    this.catlgs['device'].push({
      'comment':"",
      'device_type': 128,
      'id': 1190,
      'inv_num': "",
      'name': 7777,
      'serial_num': "CNU1170534"
    })
    */
    //this.fetchCatlg('department');
    //this.fetchCatlg('stock');
    console.log(this.fetchCatlg('person'));
    //this.fetchCatlg('devicetype');
    //this.fetchCatlg('nomenclature');
    //this.fetchCatlg('device');

    //this.fetchCatlgItem('device', 1190);
    //var myitem = this.fetchCatlgItem('device')
    //console.log(myitem);
    //this.addCatlgLabel();
  }
  
}
</script>