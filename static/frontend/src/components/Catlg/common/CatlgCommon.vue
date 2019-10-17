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
	
	},
	
	mounted: function () {


	}
	
}
</script>