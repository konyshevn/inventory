<template>
	<div></div>
</template>

<script>
/* eslint-disable no-console */
import Vue from 'vue'
import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';
import { mapMutations } from 'vuex';
import Common from '@/components/common/Common.vue';
import {EventBus} from '@/components/common/event-bus.js'

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

export default {
	name: 'CatlgCommon',
	mixins: [Common,],
	props: {
		//msg: String
	},
	data () {
		return {
		}
	},

  computed: {
    ...mapGetters([
      'GETcatlgItem',
      'GETcatlgItemLabel',
    ])
  },


	methods: {
		...mapActions([
	  'DELcatlg',
	  'PUTcatlg',
	]),
	
		async delCatlgs (catlgType, ids) {
	  	var vm = this;
      var errors = []
	  	var confirm = await vm.confirmMsg('Вы действительно хотите удалить выбранные элементы?')
			if (confirm) {
		  	await asyncForEach(ids, async function(item){
				  let response = await vm.DELcatlg([catlgType, item])
          if (!(response.status == 200 || response.status == 201 || response.status == 204)) {
            console.log('delCatlgs', response)
            errors.push(`Ошибка удаления "${vm.GETcatlgItemLabel(catlgType, item)}": ${response.data}`)
          }
		    })
      
        if (errors.length == 0){
          vm.$router.push({ name: 'catlg.list', params: {catlgType: catlgType} })
        } else {
          EventBus.$emit('openStatusMsg', errors)
        }
			}
	},
	

		async saveCatlgItem (catlgType, item){
			var vm = this
      var isNewCatlg = item.id
      var errors = []
        //if (!vm.widgetsIsValid) { 
        //  throw new Error('Заполните все необходимые реквизиты документа.')
        //}
      var response = await vm.PUTcatlg([catlgType, item])
      if (!(isNewCatlg) && (response.status == 200 || response.status == 201)) {
        vm.$router.push({ name: 'catlg.item', params: {catlgType: catlgType, id: response.data.id} })
        item.id = response.data.id
      } 
      if (!(response.status == 200 || response.status == 201)) {
        errors.push(`Ошибка сохранения "${vm.GETcatlgItemLabel(catlgType, item.id)}": ${response.data}`)
        EventBus.$emit('openStatusMsg', errors)
      }
		}

	},
	
	mounted: function () {


	}
	
}
</script>