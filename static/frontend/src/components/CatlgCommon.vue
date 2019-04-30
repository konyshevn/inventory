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
			console.log(catlgType)
			if (id in vm.catlgs[catlgType]){
				return vm.catlgs[catlgType][id]['label']
			}
		},

		async fetchCatlg (catlgType, query, fields){
			var vm = this;
			try {
				if ((query == undefined) | (fields == undefined)) {
					var response = await HTTP.get(catlgType + '/')
				} else {
					console.log(typeof(fields))
					
					var response = await HTTP.get(`${catlgType}/?query=${query}&fields=${fields.join(',')}`)
				}
				var catlgItemFetch = response.data
				for (var key in catlgItemFetch[0]){
            if (key in vm.catlgs) {
              var catlgToLoad = _.uniq(_.map(catlgItemFetch, _.property(key)))
              catlgToLoad = catlgToLoad.filter(function (el) {
                return el != null;
              });
              console.log(catlgToLoad)
              await vm.fetchCatlgItem(key, catlgToLoad)
            }
          }

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
					var catlgItemFetch = response.data
					Vue.set(vm.catlgs[catlgType], catlgItemFetch.id, catlgItemFetch)
					if ( !('label' in catlgItemFetch)) {
							vm.setCatlgLabel(catlgType, catlgItemFetch.id)
					}

				} else {
					var response = await HTTP.get(catlgType + '/?ids='+ id.join(','))
					var catlgItemFetch = response.data   

					catlgItemFetch.forEach(function(item, i, arr){
						Vue.set(vm.catlgs[catlgType], item.id, item)       
						if ( !('label' in item)) {
							vm.setCatlgLabel(catlgType, item.id)
						}    
					})
				}
				console.log('fetching ' + catlgType + ' ' + id)
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
					console.log(vm.type)
					/*
					if (!(vm.type == "CatlgList")){
						console.log('loading devicetype & nomenclature')
						await vm.fetchCatlgItem('devicetype', catlgItem['device_type'])
						await vm.fetchCatlgItem('nomenclature', catlgItem['name'])
					}
					*/
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