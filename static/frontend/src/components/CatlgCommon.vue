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
				'department': {},
				'stock': {},
				'person': {},
				'device': {},
				'deviceType': {},
				'nomenclature': {},
			} 
		}
	},
	methods: {
		displayCatlgItem(catlgType, id){
			var vm = this
			if (id in vm.catlgs[catlgType]){
				return vm.catlgs[catlgType][id]['label']
			}
		},

		async fetchDependentCatlg(items){
			var vm = this
			for (var key in items[0]){
        if (key in vm.catlgs) {
          var catlgToLoad = _.uniq(_.map(items, _.property(key)))
          catlgToLoad = catlgToLoad.filter(function (el) {
        	  return el != null;
      	  });
          //console.log(catlgToLoad)
          await vm.fetchCatlgItem(key, catlgToLoad)
        }
      }

		},

		async fetchWidgetInitCatlg(tableUnit, fieldsMap){
			var vm = this
			for (var fieldTableUnit in fieldsMap) {
				var catlgType  = fieldsMap[fieldTableUnit]
				var catlgToLoad = _.uniq(_.map(tableUnit, _.property(fieldTableUnit)))
				catlgToLoad = catlgToLoad.filter(function (el) {
        	  return el != null;
      	  });
				 vm.fetchCatlgItem(catlgType, catlgToLoad)
			}
		},

		async fetchCatlg (catlgType, query, fields){
			var vm = this;
			try {
				if ((query == undefined) | (fields == undefined)) {
					var response = await HTTP.get(catlgType + '/')
				} else {
					var response = await HTTP.get(`${catlgType}/?query=${query}&fields=${fields.join(',')}`)
				}
				var catlgItemFetch = response.data

				await vm.fetchDependentCatlg(catlgItemFetch)			
				catlgItemFetch.forEach(function(item, i, arr){
					Vue.set(vm.catlgs[catlgType], item.id, item)       
					if ( !('label' in item)) {
						vm.setCatlgLabel(catlgType, item.id)
					}    
				})
			} catch(error) {
				console.log(error)
			}
		},

		async fetchCatlgItem (catlgType, id) {
			var vm = this
			try {
				if (!Array.isArray(id)){
					var response = await HTTP.get(catlgType + '/'+ id + '/')
					var catlgItemFetch = [response.data]
				} else {
					var response = await HTTP.get(catlgType + '/?ids='+ id.join(','))
					var catlgItemFetch = response.data   
				}
					
				await vm.fetchDependentCatlg(catlgItemFetch)
				var time = performance.now();
				catlgItemFetch.forEach(function(item, i, arr){
					Vue.set(vm.catlgs[catlgType], item.id, item)       
					if ( !('label' in item)) {
						vm.setCatlgLabel(catlgType, item.id)
					}
				})
				time = performance.now() - time;
				console.log('Время выполнения = ', time);    
			} catch(error) {
				console.log(error)
			}

		},


		async setCatlgLabel (catlgName, id) {
			var vm = this;
			var label = "unknown";
			if (isNaN(id)){
				var catlgItem = id; //не число, значит передан объект
			} else {
				var catlgItem = vm.catlgs[catlgName][id]; //число, значит передано id
			}
			switch(catlgName){
				case 'device':
					var deviceType = vm.catlgs['deviceType'][catlgItem.deviceType]['label'];
					var nomenclature = vm.catlgs['nomenclature'][catlgItem.nomenclature]['label'];
					var serial_num = catlgItem['serial_num'] 
					label = deviceType + ' ' + nomenclature + ' (' + serial_num + ')';
					break;

				case 'person':
					label = catlgItem['surname'] + ' ' + catlgItem['name'];
					break;
			}
			Vue.set(vm.catlgs[catlgName][id], 'label', label)
		},

	},
	mounted: function () {


	}
	
}
</script>