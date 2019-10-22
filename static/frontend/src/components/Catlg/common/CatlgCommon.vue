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
		  	ids.forEach(async function(item, i, arr){
				  let response = await vm.DELcatlg([catlgType, item])
          if (!(response.status == 200 || response.status == 201 || response.status == 204)) {
            errors.push(`Ошибка удаления "${vm.GETcatlgItemLabel(catlgType, item)}": ${response.data}`)
          }
		    })
        if (errors.length >= 1){
          EventBus.$emit('openStatusMsg', errors)
        }
			}
	},
	

		async saveCatlgItem (catlgType, item){
			var vm = this
      var isNewCatlg = item.id
      try {
        //if (!vm.widgetsIsValid) { 
        //  throw new Error('Заполните все необходимые реквизиты документа.')
        //}
        var response = await vm.PUTcatlg([catlgType, item])
        if (!(isNewCatlg) && (response.status == 200 || response.status == 201)) {
          vm.$router.push({ name: 'catlg.item', params: {catlgType: catlgType, id: response.data.id} })
        }
      } catch(error) {
        console.log(error)
        EventBus.$emit('openStatusMsg', [`Ошибка сохранения: ${vm.getErrorMsg(error)}`])
      }
		}

	},
	
	mounted: function () {


	}
	
}
</script>