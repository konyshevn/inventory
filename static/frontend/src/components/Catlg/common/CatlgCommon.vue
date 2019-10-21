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
	methods: {
		...mapActions([
	  'DELcatlg',
	  'PUTcatlg',
	]),
	
		async delCatlgs (catlgType, ids) {
	  	var vm = this;
	  	try {
				var confirm = await vm.confirmMsg('Вы действительно хотите удалить выделенные элементы?')
				if (confirm) {
		  		ids.forEach(function(item, i, arr){
					vm.DELcatlg([catlgType, item])
		  	})
				}
	  	} catch(error) {
				console.log(error)
				EventBus.$emit('openStatusMsg', [`Ошибка удаления: ${vm.getErrorMsg(error)}`])
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